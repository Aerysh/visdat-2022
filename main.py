import numpy as np
import pandas as pd
from bokeh.io import curdoc
from bokeh.plotting import figure, show
from bokeh.models import Select
from bokeh.events import ButtonClick
from bokeh.models.widgets import Button

df = pd.read_csv("covid_19_indonesia_time_series_all.csv")

df['Date'] = pd.to_datetime(df['Date'])

df.drop(df.index[df['Location'] == 'Indonesia'], inplace=True)

provinsi = df['Location']
provinsi = provinsi.drop_duplicates()
provinsi_list = provinsi.to_list()

df.set_index('Date', inplace=True)

tahun_list=['2020','2021']
bulan_list=['1','2','3','4','5','6','7','8','9','10','11','12']
y_list=['Total Cases','Total Deaths','Total Recovered']

select_provinsi = Select(options=provinsi_list, value='DKI Jakarta')
select_tahun = Select(options=tahun_list, value='2020')
select_bulan = Select(options=bulan_list, value='3')
select_y = Select(options=y_list, value='Total Cases')
button = Button(label="Show Plot")

def select_df (kota,tahun,bulan,y):
    tmp = df.loc[df['Location'] == kota]
    tmp = tmp.loc[(tmp.index >= pd.Timestamp(tahun,bulan,1)) & (tmp.index < pd.Timestamp(tahun,bulan+1,1))]
    return tmp[[y]]

def show_plot(kota, tahun, bulan ,y):
    temp_df = select_df(kota, tahun, bulan ,y)

    p = figure(title="Covid Case", x_axis_label='Date', y_axis_label=y, x_axis_type="datetime")

    p.line(temp_df.index, temp_df[y], legend_label=y, line_width=2)

    curdoc().clear()
    curdoc().add_root(select_provinsi)
    curdoc().add_root(select_tahun)
    curdoc().add_root(select_bulan)
    curdoc().add_root(select_y)
    curdoc().add_root(button)
    curdoc().add_root(p)

def handler(attr, old, new):
    return select_provinsi.value
def handler2(attr, old, new):
    return int(select_tahun.value)
def handler3(attr, old, new):
    return int(select_bulan.value)
def handler4(attr, old, new):
    return select_y.value

a = select_provinsi.on_change('value', handler)
b = select_tahun.on_change('value', handler2)
c = select_bulan.on_change('value', handler3)
d = select_y.on_change('value', handler4)

def callback(event):
    show_plot(select_provinsi.value, int(select_tahun.value), int(select_bulan.value), select_y.value)

button.on_event(ButtonClick, callback)

curdoc().add_root(select_provinsi)
curdoc().add_root(select_tahun)
curdoc().add_root(select_bulan)
curdoc().add_root(select_y)
curdoc().add_root(button)
