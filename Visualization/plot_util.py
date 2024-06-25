import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pgeocode
import plotly.graph_objects as go
from decimal import Decimal
import seaborn as sns
import folium as fl
import io
from PIL import Image

def fit_dat_and_plot(x, y, deg, label="", label_plot=False, log=False):

    # fits an arbitrary degree polynomial and then plots it
    if deg == "linear":
        deg = 1
    if deg == "quadratic":
        deg = 2
    
    if log:
        y = np.log(y)

    coeff = np.polynomial.polynomial.Polynomial.fit(x, y, deg).convert().coef
    pred = np.zeros(y.shape)
    poly_str = '%.1E' % Decimal(coeff[0])
    for i in range(deg + 1):
        pred += coeff[i] * (x ** i)
        if i > 0:
            poly_str = '%.1E' % Decimal(coeff[i]) +"x^" +str(i) +" + "  + poly_str

    if log:
        pred = np.exp(pred)

    if label_plot:
        plt.plot(x, pred, label=str(deg) + " degree polynomial best fit -- " + label, linewidth=3) 
    else: 
        plt.plot(x, pred, linewidth=3) 

    return coeff

# Creates a scatter plot as you'd expect with autogenerated title
def scatter_plot(x, y, xlabel="", ylabel="", title=None, fit=None, label="", show=True, color="palegreen", log=False):

    dat = pd.DataFrame()
    dat['x'] = x
    dat['y'] = y
    dat = dat.dropna(axis=0)

    if fit is not None:
        dat = dat.sort_values("x")
        max_x = max(dat["x"])
        # dat["x"] /= max_x
        if type(fit) is int:
            fit = [fit]
        for deg in fit:
                fit_dat_and_plot(dat["x"].values, dat["y"].values, deg, label, label_plot=True, log=log)

    xticks = np.arange(0, 1, 0.25)
    xlabels = [np.round(max_x * x, 2) for x in xticks]
    plt.xticks(xticks, labels=xlabels)
    plt.scatter(dat['x'], dat['y'], color=color, alpha=0.1, label=label)

    if show:
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend()
        if title is None:
            plt.title(ylabel + " versus " + xlabel)
        else:
            plt.title(title)
        plt.show()

def quartile_binning(vals, key):

    q1, q2, q3 = np.quantile(vals, [0.25,0.5,0.75])

    q1_bin = (key, (0, q1), key + " in lower quartile", "blue")
    q2_bin = (key, (q1, q2), key + " in middle lower quartile", "orange")
    q3_bin = (key, (q2, q3), key + " in middle upper quartile", "green")
    q4_bin = (key, (q3, np.max(vals)), key + " in upper quartile", "red")

    return [q1_bin,q2_bin, q3_bin, q4_bin]

def complex_scatter(combined_df, x, y, xlabel, ylabel, fit=[1], title=None, bins=None, show=True, states=None):
    '''
    Inputs:
        Cenus_df : DataFrame object of all saved census data
        Solar_df : DataFrame object of all saved Proj Sunroof data
        x : The x axis for the plot (will be a col of either census or solar)
        y : Ditto but for the y axis
        bins: A list of tuples with (key:str, range:tuple, label:str, color:str)
            - key wil denote which col we are binning on, range will determine the range that we will mask the data for
            - label will be a label for plottin, color will be the color for the scatter plot
    '''


    keys = combined_df.keys()

    for (key, range, label, color) in bins:
        low, high = range
        if key in keys:
            mask1 = (low <= combined_df[key]) 
            df = combined_df[mask1] 
            mask2 = (df[key] < high)
            scatter_plot(x=x[mask1][mask2], y=y[mask1][mask2], fit=fit, show=False, label=label, color=color)
        else:
            print("Key error in Complex Scatter on key:", key, " -- not a valid key for census or solar, skipping")
        
    if show:
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend()
        if title is None:
            plt.title(ylabel + " versus " + xlabel)
        else:
            plt.title(title)
        plt.show()

# Creates a US map plot of the dat, edf should be provided, but if it isn't then it will be created as necessary using the zipcodes provided
def geo_plot(dat, color_scale, title, edf=None, zipcodes=None):

    # This should basically never get called since we define edf below, but if you were to import this you'd have to make sure zipcodes are provided to create the edf
    if edf is None:
        if zipcodes is None:
            print("invalid Geo Plotting, you must include an EDF or zipcode list")
            return -1
        else:
            nomi = pgeocode.Nominatim('us')
            edf = pd.DataFrame()
            edf['Latitude'] = (nomi.query_postal_code(zipcodes).latitude)
            edf['Longitude'] = (nomi.query_postal_code(zipcodes).longitude)
            edf['zip_code'] = zipcodes

    # For scaling of the bar, we do 15 ticks over the range of the data
    dat_range = max(dat) - min(dat)
    edf['dat'] = dat
    clean_dat = edf.dropna(axis=0)

    fig = go.Figure(data=go.Scattergeo(
            lon = clean_dat['Longitude'],
            lat = clean_dat['Latitude'],
            mode = 'markers',
            marker = dict(
            color = clean_dat['dat'],
            colorscale = color_scale,
            reversescale = True,
            opacity = 0.6,
            size = 10,
            colorbar = dict(
                titleside = "right",
                outlinecolor = "rgba(68, 68, 68, 0)",
                ticks = "outside",
                showticksuffix = "last",
                dtick = dat_range/15
            )
            )))

    fig.update_layout(
            title = title,
            geo_scope='usa',
        )
    fig.show()

def energy_gen_bar_plot(energy_gen_df, states=['Texas', 'Massachusetts', "California", 'New York', "US Total"], keys=['Clean', 'Bioenergy', 'Coal','Gas','Fossil','Solar','Hydro','Nuclear'], sort_by="Coal",stack=True):

    if states is not None:
        # Removes all states besides those in the 'states' list
        energy_gen_df = energy_gen_df[energy_gen_df['State'].isin(states)]
        
    # Drop Total Generation so it doesn't plot
    df =  energy_gen_df[keys + ['State'] + ['State code']]

    df = df.sort_values(sort_by)

    if states is None:
        df = pd.concat([df[:10], df[-10:]])

    # sns.barplot(data=energy_gen_df,x= 'State')

    #set seaborn plotting aesthetics
    sns.set(style='white')

    #create stacked bar chart
    df.set_index('State code').plot(kind='bar', stacked=stack)

    plt.ylabel("Proportion of energy generation")
    plt.title("Energy Generation Proportions by state")
    plt.show()

def plot_state_map(stats_df, key):

    url = (
        "https://raw.githubusercontent.com/python-visualization/folium/main/examples/data"
    )
    state_geo = f"{url}/us-states.json"

    m = fl.Map([43, -100], zoom_start=4)

    fl.Choropleth(geo_data=state_geo, data=stats_df,
    columns=['State code', key],key_on='feature.id',fill_color='BuPu',fill_opacity=0.7,line_opacity=.1,legend_name=key).add_to(m)

    img_data = m._to_png(5)
    img = Image.open(io.BytesIO(img_data))
    img.save("Maps/" + key + '_by_state.png')
    img.show()

    # m.show_in_browser()


def plot_state_stats(stats_df, key, states=None, sort_by='mean'):

    if states is not None:
        # Removes all states besides those in the 'states' list
        stats_df = stats_df[stats_df['state_name'].isin(states)]

    stats_df = stats_df.sort_values(sort_by)

    if states is None:
        stats_df = pd.concat([stats_df[:5], stats_df[-5:]])

    stats_df.set_index('State code').plot(kind='bar', stacked=False)

    plt.ylabel(key)

    title_add = ""
    if key in ['solar_utilization', 'carbon_offset_metric_tons','existing_install_count']:
        title_add = " per capita"


    plt.title("States sorted by "+ sort_by +" of "+ key+ title_add +" -- (bottom and top 5)")
    plt.legend()
    plt.show()





