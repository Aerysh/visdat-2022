import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from bokeh.io import curdoc

df = pd.read_csv("covid_19_indonesia_time_series_all.csv")

df['Date'] = pd.to_datetime(df['Date'])

df.drop(df.index[df['Location'] == 'Indonesia'], inplace=True)

from bokeh.plotting import figure, show
from bokeh.layouts import widgetbox
from bokeh.models.widgets import Dropdown

provinsi = df['Location']
provinsi = provinsi.drop_duplicates()
provinsi_list = provinsi.to_list()

df.set_index('Date', inplace=True)

from bokeh.plotting import figure, show
from bokeh.layouts import widgetbox
from bokeh.models.widgets import Dropdown

dropdown = Dropdown(label="Daftar Provinsi", button_type="warning", menu=provinsi_list)

def select_df (kota,tahun,bulan,y):
    tmp = df.loc[df['Location'] == kota]
    tmp = tmp.loc[(tmp.index >= pd.Timestamp(tahun,bulan,1)) & (tmp.index < pd.Timestamp(tahun,bulan+1,1))]
    return tmp[[y]]

temp_df = select_df("DKI Jakarta", 2021, 11, "Total Cases")

def show_plot(kota, tahun, bulan ,y):
    temp_df = select_df(kota, tahun, bulan ,y)

    p = figure(title="Covid Case", x_axis_label='Date', y_axis_label='Total Case')

    p.line(temp_df.index, temp_df['Total Cases'], legend_label="Temp.", line_width=2)

    curdoc().clear()
    curdoc().add_root(dropdown)
    curdoc().add_root(p)

def handler(event):
    show_plot(event.item, 2020, 3, "Total Cases")

dropdown.on_click(handler)

curdoc().add_root(dropdown)
