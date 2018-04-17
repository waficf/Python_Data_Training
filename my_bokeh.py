import pandas as pd

from bokeh.layouts import row, widgetbox
from bokeh.models import Select, ColumnDataSource, HoverTool
from bokeh.palettes import Spectral5
from bokeh.plotting import curdoc, figure

data = pd.read_csv('prosperLoanData.csv')

df = data[['Term', 'ListingCreationDate', 'LoanStatus', 'BorrowerAPR', 'ProsperRating (Alpha)', 'Occupation', 
'DebtToIncomeRatio', 'LoanOriginalAmount', 'StatedMonthlyIncome', 'BorrowerState']]

df = df.copy()

df = df.dropna()

df['ListingCreationDate'] = pd.to_datetime(df['ListingCreationDate'])

df['ListingCreationDate'] = df['ListingCreationDate'].dt.year

df_group = df.groupby(('ListingCreationDate', 'BorrowerState')).LoanOriginalAmount.agg({'Number_of_loans':'count', 
	'Total_Loans':'sum', 'Average_Loan':'mean'}).reset_index()


df_group['ListingCreationDate'] = df_group.ListingCreationDate.astype(str)
df_group['Average_Loan'] = df_group.Average_Loan.astype(int)


columns=sorted(df_group.columns)
continuous= [x for x in columns if df_group[x].dtype != object]
states = sorted(set(df_group.BorrowerState.unique()))
years = sorted(set(df_group.ListingCreationDate.unique()))
discrete = [x for x in columns if x not in continuous]

def create_figure():

	xs=df_group[x.value].values
	ys=df_group[y.value].values
	x_title = x.value.title()
	y_title = y.value.title()

	if state.value != 'ALL':
		selection = df_group[df_group['BorrowerState'] == state.value]
		xs=selection.ListingCreationDate
		ys = selection[y.value].values
	else:
		pass
	
	if year.value != 'ALL':
		selection_yr = df_group[df_group['ListingCreationDate'] == year.value]
		xs = selection_yr[x.value].values
	else:
		pass

	source = ColumnDataSource(data=dict(x=xs, y=ys, details=ys))

	hover = HoverTool(tooltips=[
    ("Details", "@details")])

	TITLE = "%s vs %s" % (x_title, y_title)

	p = figure(plot_width=950, plot_height=600, x_range= sorted(set(xs)),title=TITLE, toolbar_location=None,tools=[hover])
	p.xaxis.axis_label = x_title
	p.yaxis.axis_label = y_title

	p.vbar(x= 'x', top= 'y', color='navy', width=0.9, source=source)

	return p

def update(attr, old, new):
	layout.children[1] = create_figure()

year = Select(title='Years:', value='All', options=['ALL']+years)
year.on_change('value', update)

state = Select(title='States:', value='All', options=['ALL']+states)
state.on_change('value', update)

x = Select(title='X-Axis:', value='BorrowerState', options=discrete)
x.on_change('value', update)

y = Select(title='Y-Axis:', value='Number_of_loans', options=continuous)
y.on_change('value', update)




controls = widgetbox([state, year,  x, y], width=200)
layout = row(controls, create_figure())


curdoc().add_root(layout)
curdoc().title = "Prosper Loans Easy App"

