import pandas as pd
import plotly.graph_objs as go
from plotly.offline import plot

data=pd.read_csv('Classifiers.csv',encoding = "ISO-8859-1")

trace=go.Scatter(x=data['Precision'],
                 y=data['Recall'],
                 text=data['Classifier'],
                 mode='markers+text'
                 )
layout=go.Layout(title='Precision and Recall of classifiers',
                 xaxis=dict(title='Precision'),
                 yaxis=dict(title='Recall'),
                 )
fig=go.Figure(data=[trace], layout=layout)
plot(fig, filename='Classifiers scatterplot.html')
                 
