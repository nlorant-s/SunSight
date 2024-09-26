from plot_util import *
from data_load_util import *

combined_df = make_dataset(remove_outliers=True)
max_num_added = 1850000
projections = create_projections(combined_df, n=max_num_added, load=True)

panel_estimations_by_year = [("Net-Zero" , 479000 * 3), ("2030", 479000 * 1), ("2034", 479000 * 2)]
 
def plot_projections(projections, panel_estimations=None, net_zero_horizontal=False, interval=1, fontsize=20, fmts=["-X", "-H", "o-", "D-", "v-"]):

    plt.style.use("seaborn-whitegrid")

    if net_zero_horizontal:
        two_mill_continued = np.array(projections['Continued'])[479000 * 3]

    keys = projections.keys()
    x = np.arange((len(projections[keys[0]]) // interval) + 1) * interval

    for key,fmt in zip(keys,fmts):
        plt.plot(x, np.array(projections[key])[0::interval], fmt, label=key, linewidth=3)

    if panel_estimations is not None:
        for label, value in panel_estimations:
            plt.vlines(value, np.array(projections['Greedy Carbon Offset'])[-1]/18, np.array(projections['Greedy Carbon Offset'])[-1], colors='darkgray' , linestyles='dashed', linewidth=2, alpha=0.5)
            plt.text(value - len(projections['Greedy Carbon Offset'])/23, np.array(projections['Greedy Carbon Offset'])[-1]/80, label, alpha=0.7, fontsize=16)

    if net_zero_horizontal:
        plt.hlines(two_mill_continued, 0, len(projections['Greedy Carbon Offset']), colors='black' , linestyles='dashed', linewidth=2, alpha=0.5)
        plt.text(0, two_mill_continued*1.05, "Continued trend at\nNet-zero prediction", alpha=0.7, fontsize=16, color='black')
    
    

    plt.locator_params(axis='x', nbins=8) 
    plt.locator_params(axis='y', nbins=8) 
    plt.yticks(fontsize=fontsize/(1.5))
    plt.xticks(fontsize=fontsize/(1.5))

    plt.xlabel("Additional Panels Built", fontsize=fontsize, labelpad=20)
    plt.ylabel('Carbon Offset (metric tons)', fontsize=fontsize, labelpad=20)
    plt.legend(fontsize=fontsize/(1.5))
    plt.show()

plot_projections(projections, panel_estimations_by_year, net_zero_horizontal=True, interval=100000)