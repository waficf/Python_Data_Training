import pandas as pd

from bokeh.layouts import row, widgetbox
from bokeh.models import Select, ColumnDataSource
from bokeh.palettes import Spectral5
from bokeh.plotting import curdoc, figure

data = pd.read_csv('prosperLoanData.csv')

df = data[['Term', 'ListingCreationDate', 'LoanStatus', 'BorrowerAPR', 'ProsperRating (Alpha)', 'Occupation', 
'DebtToIncomeRatio', 'LoanOriginalAmount', 'StatedMonthlyIncome', 'BorrowerState']]

df = df.copy()

df = df.dropna()

df = df.rename(columns={"ProsperRating (Alpha)": "ProsperRating"})

df['Term'] = df.Term.astype(str)

df['ListingCreationDate'] = pd.to_datetime(df['ListingCreationDate'])

df['ListingCreationDate'] = df['ListingCreationDate'].dt.year



columns = sorted(df.columns)
discrete = [x for x in columns if df[x].dtype == object]
continuous = [x for x in columns if x not in discrete]

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

	p = figure(plot_width=900, plot_height=600, tools='pan,box_zoom,reset', **kw)
	p.xaxis.axis_label = x_title
	p.yaxis.axis_label = y_title

	p.circle(x= xs, y= ys, color='blue', fill_color="navy", fill_alpha=0.5)

	return p


def update(attr, old, new):
	layout.children[1] = create_figure()


# Set up the widgets here

x = Select(title="X-Axis:", value="DebtToIncomeRatio", options=continuous)
x.on_change('value', update)

y = Select(title="Y-Axis:", value="BorrowerAPR", options=continuous)
y.on_change('value', update)

controls = widgetbox([x, y], width=200)
layout = row(controls, create_figure())


curdoc().add_root(layout)
curdoc().title = "Prosper Loans"