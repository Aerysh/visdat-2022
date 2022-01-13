from bokeh.core.property.dataspec import Value
from bokeh.events import ButtonClick
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from bokeh.io import curdoc

df = pd.read_csv("covid_19_indonesia_time_series_all.csv")

df['Date'] = pd.to_datetime(df['Date'])

df.drop(df.index[df['Location'] == 'Indonesia'], inplace=True)

from bokeh.plotting import figure, show
from bokeh.layouts import widgetbox
from bokeh.models.widgets import Dropdown, Button

provinsi = df['Location']
provinsi = provinsi.drop_duplicates()
provinsi_list = provinsi.to_list()

df.set_index('Date', inplace=True)

from bokeh.plotting import figure, show
from bokeh.layouts import widgetbox
from bokeh.models.widgets import Dropdown

tahun_list=['2020','2021']
bulan_list=['1','2','3','4','5','6','7','8','9','10','11','12']
y_list=['Total Cases','Total Deaths','Total Recovered']

dropdown = Dropdown(label="Daftar Provinsi", button_type="warning", menu=provinsi_list, value='DKI Jakarta')
dropdown2 = Dropdown(label="Tahun", button_type="warning", menu=tahun_list, value='2021')
dropdown3 = Dropdown(label="Bulan", button_type="warning", menu=bulan_list, value='1')
dropdown4 = Dropdown(label="Y-Label", button_type="warning", menu=y_list, value='Total Cases')
button = Button(label="Show Plot")

def select_df (kota,tahun,bulan,y):
    tahun = int(tahun)
    bulan = int(bulan)
    tmp = df.loc[df['Location'] == kota]
    tmp = tmp.loc[(tmp.index >= pd.Timestamp(tahun,bulan,1)) & (tmp.index < pd.Timestamp(tahun,bulan+1,1))]
    return tmp[[y]]

temp_df = select_df('DKI Jakarta','2020','3','Total Cases')

def show_plot(kota, tahun, bulan ,y):
    temp_df = select_df(kota, tahun, bulan ,y)

    p = figure(title="Covid Case", x_axis_label='Date', y_axis_label='Total Case')

    p.line(temp_df.index, temp_df['Total Cases'], legend_label="Temp.", line_width=2)

    curdoc().clear()
    curdoc().add_root(dropdown)
    curdoc().add_root(dropdown2)
    curdoc().add_root(dropdown3)
    curdoc().add_root(dropdown4)
    curdoc().add_root(button)
    curdoc().add_root(p)

def handler(event):
    return event.item
def handler2(event):
    return event.item
def handler3(event):
    return event.item
def handler4(event):
    return event.item

a = dropdown.on_click(handler)
b = dropdown2.on_click(handler2)
c = dropdown3.on_click(handler3)
d = dropdown4.on_click(handler4)
button.on_click(show_plot(a,b,c,d))

curdoc().add_root(dropdown)
curdoc().add_root(dropdown2)
curdoc().add_root(dropdown3)
curdoc().add_root(dropdown4)
curdoc().add_root(button)
