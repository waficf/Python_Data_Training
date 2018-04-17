from os.path import dirname, join

import pandas as pd

from bokeh.layouts import row, widgetbox
from bokeh.models import Select
from bokeh.palettes import Spectral5
from bokeh.plotting import curdoc, figure


autompg = pd.read_csv(join(dirname(__file__), 'auto-mpg.csv'))

autompg_clean = autompg.copy()

autompg_clean['mfr'] = [x.split()[0] for x in autompg_clean.name]
autompg_clean.loc[autompg_clean.mfr=='chevy', 'mfr'] = 'chevrolet'
autompg_clean.loc[autompg_clean.mfr=='chevroelt', 'mfr'] = 'chevrolet'
autompg_clean.loc[autompg_clean.mfr=='maxda', 'mfr'] = 'mazda'
autompg_clean.loc[autompg_clean.mfr=='mercedes-benz', 'mfr'] = 'mercedes'
autompg_clean.loc[autompg_clean.mfr=='toyouta', 'mfr'] = 'toyota'
autompg_clean.loc[autompg_clean.mfr=='vokswagen', 'mfr'] = 'volkswagen'
autompg_clean.loc[autompg_clean.mfr=='vw', 'mfr'] = 'volkswagen'

ORIGINS = ['North America', 'Europe', 'Asia']

autompg_clean.origin = [ORIGINS[x-1] for x in autompg_clean.origin]

df = autompg_clean

df = df[['mpg', 'cyl', 'displ', 'hp', 'weight', 'accel', 'yr', 'origin', 'mfr']].copy()

df.cyl = df.cyl.astype(str)
df.yr = df.yr.astype(str)

SIZES = list(range(6, 22, 3))

columns = sorted(df.columns)
discrete = [i for i in columns if df[i].dtype == object]
continuous = [i for i in columns if i not in discrete]


def create_figure():
	xs = df[x.value].values
	ys = df[y.value].values
	x_title = x.value.title()
	y_title = y.value.title()
	
	kw = dict()
	if x.value in discrete:
		kw['x_range'] = sorted(set(xs))
	if y.value in discrete:
		kw['y_range'] = sorted(set(ys))
	kw['title'] = "%s vs %s" % (x_title, y_title)

	p = figure(plot_width=800, plot_height=600, tools='pan,box_zoom,reset', **kw)
	p.xaxis.axis_label = x_title
	p.yaxis.axis_label = y_title

	sz=9
	if size.value != None:
		groups = pd.qcut(df[size.value].values, len(SIZES))
		sz = [SIZES[xx] for xx in groups.codes]


	p.circle(x= xs, y= ys, size = sz, color='blue', fill_color="navy", fill_alpha=0.5)

	return p

def update(attr, old, new):
	layout.children[1] = create_figure()

x = Select(title="X-Axis:", value="mpg", options=columns)
x.on_change('value', update)

y = Select(title="Y-Axis:", value="hp", options=columns)
y.on_change('value', update)

size = Select(title="Size:", value=None, options=['None'] + continuous)
size.on_change('value', update)

controls = widgetbox([x, y, size], width=200)
layout = row(controls, create_figure())


curdoc().add_root(layout)
curdoc().title = "Crossfit"




