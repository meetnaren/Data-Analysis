from initialize import *

c=connect_db()

# No. of nodes
query = 'SELECT COUNT(*) FROM NODES'
print "No. of nodes: ", execute_query(c,query)[[0]][0][0]

# No. of ways
query = 'SELECT COUNT(*) FROM WAYS'
print "No. of ways: ", execute_query(c,query)[[0]][0][0]

# No. of distinct users from both nodes and ways tables
query = 'SELECT COUNT(*) FROM (SELECT DISTINCT(UID) FROM NODES UNION SELECT DISTINCT(UID) FROM WAYS)'
print "No. of unique users: ", execute_query(c,query)[[0]][0][0]

#------------------------------------------------------------------------------------------------------------------------
# Helper function to plot "group by" query data
def groupByPlot(df,title,xlabel):
    """ Plot a barchart based on the group by query results passed
    Args:
        df (DataFrame)  : results of the query in a Pandas DataFrame format
        title (str)     : title of the barchart
        xlabel (str)    : X-Axis title
    Returns:
        None
    """
    plt.figure(figsize=(16,4))
    plt.bar(range(len(df)),df[1].tolist())
    plt.xticks(range(len(df)),df[0].tolist(),rotation='vertical')
    plt.ylabel('Count')
    plt.xlabel(xlabel)
    plt.title(title)
    return None
    
#------------------------------------------------------------------------------------------------------------------------

# Top amenities by count
query = 'SELECT VALUE, COUNT(*) FROM NODES_TAGS WHERE KEY="amenity" GROUP BY VALUE ORDER BY COUNT(*) DESC LIMIT 10'
df=pd.DataFrame(execute_query(c,query))

groupByPlot(df,'Most common amenities','Amenity')

#------------------------------------------------------------------------------------------------------------------------

# Total bicycle parking capacity
query = 'SELECT VALUE FROM NODES_TAGS WHERE KEY="capacity" AND ID IN (SELECT ID FROM NODES_TAGS WHERE KEY="amenity" AND VALUE="bicycle_parking")'
df=execute_query(c,query)

print "Total biccycle parking capacity: ",sum(pd.to_numeric(df[0]))

#------------------------------------------------------------------------------------------------------------------------

# No. of amenities by zipcode
def amenities_by_zipcode(c,amenity):
    query='SELECT VALUE, COUNT(*) FROM NODES_TAGS WHERE KEY="postcode" AND ID IN (SELECT ID FROM NODES_TAGS WHERE KEY="amenity" AND VALUE="'+amenity+'") GROUP BY VALUE ORDER BY COUNT(*) DESC'
    return execute_query(c,query)

amenities=['restaurant','cafe','bar']

for i in range(len(amenities)):
    plt.figure(i)
    df=amenities_by_zipcode(c,amenities[i])
    groupByPlot(df,'No. of '+amenities[i]+'s by zipcode','Zipcode')

#------------------------------------------------------------------------------------------------------------------------

# No. of one-ways
query = 'SELECT VALUE, COUNT(*) FROM WAYS_TAGS WHERE KEY="oneway" AND VALUE IN ("yes","no") GROUP BY VALUE'
df=execute_query(c,query)
df.columns=['One-way?','Count']
print df

#------------------------------------------------------------------------------------------------------------------------

# Ways with the highest no. of nodes associated with them
query = 'SELECT A.ID, B.VALUE, COUNT(*) FROM WAYS_NODES A, WAYS_TAGS B WHERE A.ID=B.ID AND B.KEY="name" GROUP BY A.ID ORDER BY COUNT(*) DESC LIMIT 10'
df=execute_query(c,query)
df.columns=['ID','Name','No. of nodes']
print df

#------------------------------------------------------------------------------------------------------------------------

# Ways with the highest no. of tags associated with them
query = 'SELECT A.ID, B.VALUE, COUNT(*) FROM WAYS_TAGS A, WAYS_TAGS B WHERE A.ID=B.ID AND B.KEY="name" GROUP BY A.ID ORDER BY COUNT(*) DESC LIMIT 10'
df=execute_query(c,query)
df.columns=['ID','Name','No. of tags']
print df

#------------------------------------------------------------------------------------------------------------------------

# Geographical plotting using plotly
query = 'SELECT A.LAT, A.LON, B.VALUE, C.VALUE FROM NODES A, NODES_TAGS B, NODES_TAGS C WHERE A.ID=B.ID AND B.ID=C.ID AND B.KEY="amenity" AND B.VALUE IN ("restaurant", "cafe", "bar") AND C.KEY="name"'
df=execute_query(c,query)
df.columns=['Lat','Lon','Amenity_type','Name']

data=Data([
    Scattermapbox(
        lat=df['Lat'],
        lon=df['Lon'],
        mode='markers',
        marker=Marker(
            size=5,
            color=df['Amenity_type'].astype('category').cat.codes.values,
            colorscale='Viridis',
            colorbar=dict(
                tickmode='array',
                tickvals=[0,1,2],
                ticktext=['bar','cafe','restaurant'],
                ticks='inside'
            )
        ),
        text=df['Name']        
    )
])

layout=Layout(
    autosize=True,
    hovermode='closest',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=40.71955,
            lon=-73.9858
        ),
        pitch=0,
        zoom=12
    ),
    showlegend=False
)

fig = dict(data=data, layout=layout)

pltly.plotly.iplot(fig)
