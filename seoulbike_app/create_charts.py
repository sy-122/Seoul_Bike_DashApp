from pathlib import Path
import pandas as pd
import plotly.express as px

# Import Data
BIKE_DATA_FILEPATH = Path(__file__).parent.joinpath('data', 'Bike_data_adjusted.csv')
df_bike = pd.read_csv(BIKE_DATA_FILEPATH, encoding='unicode_escape')

# Convert 'Count' to integer
df_bike['Count'] = df_bike['Count'].astype(int)

# Dataframe with percent of holiday in each month for bar graph
bar_original_df = df_bike.groupby(['Month']).mean('Count').reset_index()
Month_Holiday = df_bike.groupby(['Month'])['Holiday']. \
    value_counts(normalize=True).reset_index(name='Holiday%')
Month_Holiday = Month_Holiday[Month_Holiday.Holiday == 'Holiday']
Month_Holiday['Holiday%'] = Month_Holiday['Holiday%'].apply(lambda x: x * 100)
Month_Holiday['Holiday%'] = Month_Holiday['Holiday%'].apply(lambda x: '{0:1.2f}%'.format(x))
bar_new_df = pd.merge(bar_original_df, Month_Holiday, how='left', on='Month')


# Line plot for Hour VS Bicycle Rented
hour_line_plot = px.line(
    data_frame=df_bike.groupby(['DayofWeek', 'Hour']).mean('Count').reset_index(),
    x='Hour',
    y='Count',
    category_orders={'DayofWeek': ['Sunday', 'Monday', 'Tuesday',
                                   'Wednesday', 'Thurday', 'Friday',
                                   'Saturday']},
    color='DayofWeek',
    labels={'Hour': 'Time', 'Count': 'Average Bike Rented'},
    markers=True,
    template='simple_white'
)


# Make bar graph for Month vs Bicycle Rented
def month_bar_graph(df=bar_original_df, bar_text=None):
    fig = px.bar(
        data_frame=df,
        x='Month',
        y='Count',
        text=bar_text,
        labels={'Month': 'Month',
                'Count': 'Average Bike Rented per hour'},
        template='simple_white'
    )
    return fig


# Make Scatter Plot with different x-variables
def scatter_plot(x_var):
    fig = px.scatter(
        data_frame=df_bike,
        x=x_var,
        y='Count',
        trendline='ols',
        trendline_color_override='red',
        opacity=0.3,
        labels={'x': x_var,
                'Count': 'Bike Rented'},
        template='simple_white'
    )
    return fig
