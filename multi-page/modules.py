from typing import Callable
from pathlib import Path

import pandas as pd
import numpy as np
import plotly.express as px
import time
from plots import plot_map_distribution

from shiny import Inputs, Outputs, Session, module, render, ui
from shiny.express import input as input_exp
from shiny.express import ui as ui_exp
from shinywidgets import output_widget, render_widget  
from utils import load_object

 	 	 	
@module.ui
def data_view_ui():
    return ui.nav_panel(
        "View Data",
        ui.layout_columns(
            ui.value_box(
                title="Row count",
                value=ui.output_text("row_count"),
                theme="primary",
            ),
            ui.value_box(
                title="Average Precipitation",
                value=ui.output_text("mean_precipitation"),
                theme="bg-green",
            ),
            ui.value_box(
                title="Average AvMeanSurAirTemp",
                value=ui.output_text("mean_AvMeanSurAirTemp"),
                theme="bg-purple",
            ),
            ui.value_box(
                title="Average AvMaxSurAirTemp",
                value=ui.output_text("mean_AvMaxSurAirTemp"),
                theme="bg-orange",
            ),
            ui.value_box(
                title="Average AvMinSurAirTemp",
                value=ui.output_text("mean_AvMinSurAirTemp"),
                theme="bg-yellow",
            ),
            gap="20px",
        ),
        ui.layout_columns(
            ui.card(ui.output_data_frame("data")),
            style="margin-top: 20px;",
        ),
    )


@module.server
def data_view_server(
    input: Inputs, output: Outputs, session: Session, df: Callable[[], pd.DataFrame]
):
    @render.text
    def row_count():
        return df().shape[0]

    @render.text
    def mean_precipitation():
        return round(df()["precipitation"].mean(), 2)

    @render.text
    def mean_AvMeanSurAirTemp():
        return round(df()["AvMeanSurAirTemp"].mean(), 2)

    @render.text
    def mean_AvMaxSurAirTemp():
        return round(df()["AvMaxSurAirTemp"].mean(), 2)

    @render.text
    def mean_AvMinSurAirTemp():
        return round(df()["AvMinSurAirTemp"].mean(), 2)

    @render.data_frame
    def data():
        return df()


@module.ui
def map_view_ui():
    return ui.nav_panel(
        "View Data Distribution",
        ui.layout_columns(
            ui.card(output_widget("map1"))
        ),
        ui.layout_columns(
            ui.card(output_widget("map2"))
        ),
    )



@module.server
def map_view_server(
    input: Inputs,
    output: Outputs,
    session: Session,
    df: Callable[[], pd.DataFrame],
):
    
    @render_widget
    def map1():
        return plot_map_distribution(df(), map_predicted=False)

    @render_widget
    def map2():
        return plot_map_distribution(df(), map_predicted=True)


@module.ui
def predict_ui():
    return ui.nav_panel(
        "Make Predictions",
        ui.layout_columns(
            ui.card(
                ui.input_numeric("longitude", "Inser a Longitude", 0),
                ui.input_numeric("latitude", "Insert a Latitude", 0),
            ),
            ui.card(
                ui.input_numeric("precipitation", "Insert a value for Precipitation", 0),
                ui.input_numeric("year", "Insert a value for Year", value = 2021),
            ),
            ui.card(
                ui.input_numeric("avmeansurairtemp", "Insert a value for Average Mean Surface Air Temperature", 0),
                ui.input_numeric("avmaxsurairtemp", "Insert a value for Average Maximum Surface Air Temperature", 0),
                ui.input_numeric("avminsurairtemp", "Insert a value for Average Minimum Surface Air Temperature", 0),
            ),
        ),
        ui.layout_columns(
            ui.card(
                ui.output_data_frame("input_data"),
                "The predicted malaria incidence is: ",
                ui.output_text_verbatim("prediction"),
            )
        )
    )


@module.server
def predict_server(
    input: Inputs,
    output: Outputs,
    session: Session,
    df: Callable[[], pd.DataFrame],
):

    @render.data_frame
    def input_data():
        X = pd.DataFrame({'year':[input.year()], 
                      'precipitation':[input.precipitation()], 
                      'AvMeanSurAirTemp':[input.avmeansurairtemp()],
                      'AvMaxSurAirTemp':[input.avmaxsurairtemp()], 
                      'AvMinSurAirTemp':[input.avminsurairtemp()], 
                      'longitude':[input.longitude()],
                      'latitude':[input.latitude()],
                     })
        return X

    
    @render.text  
    def prediction():

        X = pd.DataFrame({'year':[input.year()], 
                      'precipitation':[input.precipitation()], 
                      'AvMeanSurAirTemp':[input.avmeansurairtemp()],
                      'AvMaxSurAirTemp':[input.avmaxsurairtemp()], 
                      'AvMinSurAirTemp':[input.avminsurairtemp()], 
                      'longitude':[input.longitude()],
                      'latitude':[input.latitude()],
                     })
        
        # load models
        model = load_object(Path(__file__).parent / "artifacts/model.pkl")
        preprocessor = load_object(Path(__file__).parent / "artifacts/preprocessor.pkl")

        prediction = ""
        prediction = model.predict(preprocessor.transform(X))[0]
    
        return prediction
