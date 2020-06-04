import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# ####### Helping Function
def my_agg(x):
    names = {
        'Count': x['Request Id'].count()
    }
    return pd.Series(names, index=['Count'])


# #########TO Fetch Data from CSV File###########################
allRecords = pd.read_csv("C:\Dev\Learning\Data\OpportunityData.csv")
columns = allRecords.columns
minDate = min(allRecords["Deal Clouser Date"])
maxDate = max(allRecords["Deal Clouser Date"])
dateSeries2MonthFreq = pd.date_range(start=minDate, end=maxDate, freq='6m')
dateSeries = pd.DataFrame({'Start': [dateSeries2MonthFreq[index] for index in range(len(dateSeries2MonthFreq) - 1)],
                           'End': [dateSeries2MonthFreq[index + 1] for index in range(len(dateSeries2MonthFreq) - 1)]})

# Step 1 : Get the X-Axis Values in list
# 1. X-Axis :
# ######### Distinct List Of Team to Show on X-Axis i.e.
# ######### i.e. ['USA', 'T&FS UK', 'CF&RS France', 'France', 'UK Specialist Sector'] ###########################
listOfTeams = list(set(allRecords["Team"]))

# Step 2 : Get the list of values used for grouping and need to show in the table and used to Stack bar on one another
# 2. Rows of table, we need to show below graph
# ######## below is the list of 3 (could be any duration or any thing) date duration,
# ######## for which we want count of opportunity Closed during this period for each Origination Team
# ######## ['01/31/2019 - 07/31/2019', '07/31/2019 - 01/31/2020', '01/31/2020 - 07/31/2020']
rows = [pd.to_datetime(str(x[0])).strftime('%m/%d/%Y') + ' - ' + pd.to_datetime(str(x[1])).strftime('%m/%d/%Y') for x in
        dateSeries.values]

# Step 3 : Get the data point to plot graph. as this is stacked bar chart it should be,
# (N X M, where N = Rows coming in table below graph, M = length of Team name for x-Axis)
# 3. To find out Data points
# ####### This should be matrix of (N X M, where N = Rows coming in table below graph,
# M = length of Team name for x-Axis) ####### i.e. [[1, 0, 1, 3, 4], [4, 2, 4, 1, 1], [1, 0, 1, 1, 0]]
result = [[allRecords.where((allRecords['Deal Clouser Date'] > pd.to_datetime(str(s[0])).strftime('%m/%d/%Y')) & (
        allRecords['Deal Clouser Date'] < pd.to_datetime(str(s[1])).strftime('%m/%d/%Y'))).fillna(0).groupby(
    ["Team"]).apply(my_agg)] for s in dateSeries.values]
result = [[result[index][0].reindex(listOfTeams, fill_value=0)] for index in range(len(result))]
data = [[t[0] for t in result[ind][0].values] for ind in range(len(result))]


# Step 4 : Basic setting and colors
# ########### Now can generate the desired graph

# Basic Settings
# Get some pastel shades for the colors
colors = plt.cm.BuPu(np.linspace(0, 1, len(rows)))
n_rows = len(data)
index = np.arange(len(columns)) + 0.3
bar_width = 0.4

# Initialize the vertical-offset for the stacked bar chart.
y_offset = np.zeros(len(listOfTeams), dtype=int)

# Plot bars and create text labels for the table
cell_text = []

# Step 5 : plot graphs, multiple times (number of rows in table) and calculate bottom starting point for each bar,
# i.e y_offset does in below example
# # Here we are actually plotting the graph
# # we are generating 3 (number of Rows in table below graph) bar chart, but key here is setting bottom offset
# # i.e. it start with 0, and then add value fo Y axis to to previous value to get new bottom value for each Team (x - Axis)
# # also, it generates the content for all cell values that need to show in table below graph
for row in range(len(rows)):
    plt.bar(listOfTeams, np.array(data[row]), bar_width, bottom=y_offset, color=colors[row])
    y_offset = y_offset + np.array(data[row])
    cell_text.append(['%1.1f' % x for x in y_offset])

# # just to match the color and order of values in the graph
cell_text.reverse()
colors = colors[::-1]

# Step 6 : Draw table below graph
# Here we are crating table just below the graph
# cellText are same value which used in data point
# row Lebels are like duration or whatever used for grouping i.e. ['01/31/2019 - 07/31/2019', '07/31/2019 - 01/31/2020', '01/31/2020 - 07/31/2020']
# ColLables are Values for X - Axis
the_table = plt.table(cellText=cell_text,
                      rowLabels=rows,
                      rowColours=colors,
                      colLabels=listOfTeams,
                      loc='bottom')
plt.subplots_adjust(left=0.3, bottom=0.3)
plt.xticks([])
plt.show()
