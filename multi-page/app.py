from pathlib import Path

import pandas as pd
from modules import data_view_server, data_view_ui, map_view_server, map_view_ui, predict_server, predict_ui

from shiny import App, Inputs, Outputs, Session, reactive, ui

df = pd.read_csv(Path(__file__).parent / "data/viz-data.csv")

country_choices = list(df["country"].unique())
year_choices = [ str(num) for num in df["year"].unique()]

app_ui = ui.page_navbar(
    data_view_ui("tab1"),
    map_view_ui("tab2"),
    predict_ui("tab3"),
    sidebar=ui.sidebar(
        ui.input_select(
            "country",
            "Country",
            choices=country_choices,
        ),
        ui.input_select(
            "year",
            "Year",
            choices=year_choices,
        ),
        width="300px",
    ),
    header=ui.include_css(Path(__file__).parent / "styles.css"),
    id="tabs",
    title="Malaria Incidence Predictor",
)


def server(input: Inputs, output: Outputs, session: Session):
    @reactive.calc()
    def filtered_country() -> pd.DataFrame:
        return df.loc[df["country"] == input.country()]

    @reactive.calc()
    def filtered_year() -> pd.DataFrame:
        return df.loc[df["year"].astype("str") == input.year()]

    @reactive.calc()
    def filtered_country_year() -> pd.DataFrame:
        return df.loc[df["year"].astype("str") == input.year()].loc[df["year"].astype("str") == input.year()]

    data_view_server(id="tab1", df=filtered_country)
    map_view_server(id="tab2", df=filtered_year)
    predict_server(id="tab3", df=filtered_country_year)


app = App(app_ui, server)
