from pandas import DataFrame
import plotly.express as px

def plot_map_distribution(df: DataFrame, map_predicted:bool=True):

    year = list(df["year"])[0]
    if map_predicted:
        hue = "predicted incidence"
        title = f"Predicted Malaria Incidence in {year}"
    else:
        hue = "incidence"
        title = f"Malaria Incidence in {year}"

    # plot original data
    fig = px.choropleth(df, locations="code",color=hue, hover_name="country", 
                        color_continuous_scale=px.colors.sequential.Plasma) 
    fig.update_layout(
        title=dict(text=title, font=dict(size=30), automargin=True, yref='paper'),
        title_x=0.40, autosize=True,width=1000,height=600, margin=dict( l=10, r=50, b=1, t=1))
    return fig
