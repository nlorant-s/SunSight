from plot_util import *
from data_load_util import *

combined_df = make_dataset(remove_outliers=False)
max_num_added = 100000
projections = create_projections(combined_df, n=max_num_added, load=False)

def plot_projections(projections):
    keys = projections.keys()
    x = np.arange(len(projections[keys[0]]))
    
    for key in keys:
        plt.plot(x, np.array(projections[key]), label=key)
    
    plt.xlabel("number of panels added")
    plt.ylabel('Carbon Offset (metric tons)')
    # plt.yscale('log')
    plt.legend()
    plt.show()

plot_projections(projections)