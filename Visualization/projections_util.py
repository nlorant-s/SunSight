from data_load_util import *


# Creates a projection of carbon offset if the current ratio of panel locations remain the same 
# allowing partial placement of panels in zips and not accounting in the filling of zip codes.
def create_continued_projection(combined_df, n=1000, metric='carbon_offset_metric_tons'):
    total_panels = np.sum(combined_df['existing_installs_count'])
    # print("total, current existing panels:", total_panels)
    panel_percentage = combined_df['existing_installs_count'] / total_panels
    ratiod_carbon_offset_per_panel = np.sum(panel_percentage * combined_df[metric])
    return np.arange(n+1) * ratiod_carbon_offset_per_panel

# Greedily adds 1-> n solar panels to zips which maximize the sort_by metric until no more can be added
# Returns the Carbon offset for each amount of panels added
def create_greedy_projection(combined_df, n=1000, sort_by='carbon_offset_metric_tons_per_panel', ascending=False, metric='carbon_offset_metric_tons_per_panel', record=True):
    sorted_combined_df = combined_df.sort_values(sort_by, ascending=ascending, inplace=False, ignore_index=True)
    projection = np.zeros(n+1)
    greedy_best_not_filled_index = 0
    existing_count = sorted_combined_df['existing_installs_count'][greedy_best_not_filled_index]
    i = 0

    if record:
        picked = [sorted_combined_df['region_name'][greedy_best_not_filled_index]]

    while (i < n):
        if existing_count >= sorted_combined_df['count_qualified'][greedy_best_not_filled_index]:
            greedy_best_not_filled_index += 1
            existing_count = sorted_combined_df['existing_installs_count'][greedy_best_not_filled_index]

        else:
            projection[i+1] = projection[i] + sorted_combined_df[metric][greedy_best_not_filled_index]
            existing_count += 1
            i += 1
            if record:
                picked.append(sorted_combined_df['region_name'][greedy_best_not_filled_index])
    
    return projection, picked

# Creates a projection which decides each placement alternating between different policies
def create_round_robin_projection(projection_list, picked_list):
    n = len(projection_list[0])
    number_of_projections = len(projection_list)
    projection = np.zeros(n)
    picked = [picked_list[0][0]]
    for i in range(1, n):
        chosen_projection = projection_list[i % number_of_projections]
        projection[i] = projection[i-1] + (chosen_projection[i] - chosen_projection[i-1])
        picked.append(picked_list[i % number_of_projections][i])
    return projection, picked

# Creates the projection of a policy which weighs multiple different factors (objectives)
# and greedily chooses zips based on the weighted total of proportions to national avg. 
def create_weighted_proj(combined_df, n=1000, objectives=['carbon_offset_metric_tons_per_panel'], weights=[1], metric='carbon_offset_metric_tons_per_panel'):

    new_df = combined_df
    new_df['weighted_combo_metric'] = combined_df[objectives[0]] * 0

    for weight, obj in zip(weights,objectives):
        new_df['weighted_combo_metric'] = new_df['weighted_combo_metric'] + (combined_df[obj] / np.mean(combined_df[obj])) * weight

    return create_greedy_projection(combined_df=new_df, n=n, sort_by='weighted_combo_metric', metric=metric)

# Creates a projection of the carbon offset if we place panels to normalize the panel utilization along the given "demographic"
# I.e. if we no correlation between the demographic and the panel utilization and only fous on that, how Carbon would we offset
# TODO
def create_pop_demo_normalizing_projection(combined_df, n=1000, demographic="black_prop", metric='carbon_offset_metric_tons_per_panel'):
    pass

# Creates a projection of carbon offset for adding solar panels to random zipcodes
# The zipcode is randomly chosen for each panel, up to n panels
def create_random_proj(combined_df, n=1000, metric='carbon_offset_metric_tons_per_panel'):
    projection = np.zeros(n+1)
    picks = np.random.randint(0, len(combined_df['region_name']) -1, (n))
    for i, pick in enumerate(picks):

        while math.isnan(combined_df[metric][pick]):
            pick = np.random.randint(0, len(combined_df[metric]))
        projection[i+1] = projection[i] + combined_df[metric][pick]

    return projection

# Creates multiple different projections and returns them
def create_projections(combined_df, n=1000, load=False, metric='carbon_offset_metric_tons_per_panel', save=True):

    ## TODO remove rrtest (just for a new version of round robin)
    if load and exists("Clean_Data/projections_"+metric+".csv") and exists("Clean_Data/projections_picked.csv"):
        return pd.read_csv("Clean_Data/projections_"+metric+".csv"), pd.read_csv("Clean_Data/projections_picked.csv")
    
    picked = pd.DataFrame()
    proj = pd.DataFrame()
    print("Creating Continued Projection")
    proj['Status-Quo'] = create_continued_projection(combined_df, n, metric)
    print("Creating Greedy Carbon Offset Projection")
    proj['Carbon-Efficient'], picked['Carbon-Efficient'] = create_greedy_projection(combined_df, n, sort_by='carbon_offset_metric_tons_per_panel', metric=metric)
    print("Creating Greedy Average Sun Projection")
    proj['Energy-Efficient'], picked['Energy-Efficient'] = create_greedy_projection(combined_df, n, sort_by='yearly_sunlight_kwh_kw_threshold_avg', metric=metric)
    print("Creating Greedy Black Proportion Projection")
    proj['Racial-Equity-Aware'], picked['Racial-Equity-Aware'] = create_greedy_projection(combined_df, n, sort_by='black_prop', metric=metric)
    print("Creating Greedy Low Median Income Projection")
    proj['Income-Equity-Aware'], picked['Income-Equity-Aware'] = create_greedy_projection(combined_df, n, sort_by='Median_income', ascending=True, metric=metric)

    print("Creating Round Robin Projection")
    proj['Round Robin'], picked['Round Robin'] = create_round_robin_projection(projection_list=
                                                                                                   [proj['Carbon-Efficient'], proj['Energy-Efficient'], proj['Racial-Equity-Aware'], proj['Income-Equity-Aware']],
                                                                                                   picked_list=
                                                                                                   [picked['Carbon-Efficient'], picked['Energy-Efficient'], picked['Racial-Equity-Aware'], picked['Income-Equity-Aware']])

    # print("Creating Weighted Greedy Projection")
    # proj['Weighted Greedy'], picked['Weighted Greedy'] = create_weighted_proj(combined_df, n, ['carbon_offset_metric_tons_per_panel', 'yearly_sunlight_kwh_kw_threshold_avg', 'black_prop'], [2,4,1], metric=metric)

    # uniform_samples = 10

    # print("Creating uniform random projection with", uniform_samples, "samples")

    # proj['Uniform Random (' + str(uniform_samples) + ' samples)' ] = np.zeros(n+1)
    # for i in range(uniform_samples):
    #     proj['Uniform Random (' + str(uniform_samples) + ' samples)' ] += create_random_proj(combined_df, n)/uniform_samples
    
    ## TODO remove rrtest (just for a new version of round robin)
    if save:
        proj.to_csv("Clean_Data/projections_"+metric+".csv",index=False)
        picked.to_csv("Clean_Data/projections_picked.csv", index=False)

    return proj, picked

# Searches over many different weight settings, with the first weight being set permenantly to 1 and the other two being set proportionally
# Returns a 2d array of projections (i.e. 3d array)
def create_many_weighted(combined_df, n=1000, objectives=['carbon_offset_metric_tons_per_panel'], weight_starts=[], weight_ends=[], number_of_samples=1, metric='carbon_offset_metric_tons_per_panel', save=None, load=None):

    if exists(load):
       return np.load(load)

    all_projections = np.zeros((number_of_samples,number_of_samples,n+1))

    for i, weight1 in enumerate(np.arange(weight_starts[0], weight_ends[0], (weight_ends[0] - weight_starts[0]) / number_of_samples)):
        for j, weight2 in enumerate(np.arange(weight_starts[1], weight_ends[1], (weight_ends[1] - weight_starts[1]) / number_of_samples)):

            print("weighted proj number:", (i*number_of_samples + j))
            
            all_projections[i][j],_ = create_weighted_proj(combined_df, n=n, objectives=objectives, weights=[1, weight1, weight2], metric=metric)
    

    if save is not None:
        np.save(save, all_projections)

    return all_projections