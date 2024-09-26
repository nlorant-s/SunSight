from plot_util import *
from data_load_util import *

combined_df = make_dataset(remove_outliers=True)
max_num_added = 2500000
projections = create_projections(combined_df, n=max_num_added, load=True)

panel_estimations_by_year = [("2030 Net Zero Scenario" , 2000000), ("2030 SEIA prediction", 1000000), ("2034 SEIA prediction", 1500000)]
 
def plot_projections(projections, panel_estimations=None, net_zero_horizontal=False):
    keys = projections.keys()
    x = np.arange(len(projections[keys[0]]))
    
    for key in keys:
        plt.plot(x, np.array(projections[key]), label=key, linewidth=3)

    if panel_estimations is not None:
        for label, value in panel_estimations:
            plt.vlines(value, 0, np.array(projections['Greedy Carbon Offset'])[-1], colors='darkgray' , linestyles='dashed', linewidth=2)
            plt.text(value + len(projections['Greedy Carbon Offset'])/80, 5, label, alpha=0.7, fontsize=10)

    if net_zero_horizontal:
        plt.hlines(np.array(projections['Continued'])[2000000], 0, len(projections['Greedy Carbon Offset']), colors='darkblue' , linestyles='dashed', linewidth=2)
        plt.text(0, np.array(projections['Continued'])[2000000]*1.025, "Carbon offset in 2030 Net Zero case with continued trend", alpha=0.7, fontsize=10)
    
    plt.xlabel("number of panels added")
    plt.ylabel('Carbon Offset (metric tons)')
    plt.legend()
    plt.show()

plot_projections(projections, panel_estimations_by_year, True)