# pip install numpy pandas plotly lxml
import json
import pandas as pd
from urllib.request import urlopen
import plotly.graph_objects as go

geojson_url = '''
https://raw.githubusercontent.com/skylite21/csv_for_colab/master/megyek_uj.json
'''

data = pd.read_html(
    'https://en.wikipedia.org/wiki/COVID-19_pandemic_in_Hungary'
)

datum = '2021.05.16.'

# print(data)
megye_adatok = data[4]
megye_adatok.columns = megye_adatok.columns.droplevel(-1)
# print(megye_adatok)

megye_adatok = megye_adatok.dropna()
megye_adatok = megye_adatok.drop(['all', 'Hospitalized', 'Ventilated'], axis=1)


df = megye_adatok.loc[megye_adatok['Date'] == datum]

df = df.transpose()
df.reset_index(inplace=True)
df.columns = ['megye', 'covid']
df = df[1:]
df['megye'] = df['megye'].astype(str) + ' megye'
df['megye'][5] = 'Csongrád megye'
df['megye'][20] = 'Budapest'
# print(df)

with urlopen(geojson_url) as response:
    megyek = json.load(response)


data = dict(
    type='choroplethmapbox',
    locations=df['megye'],
    z=df['covid'],
    colorscale='Rainbow',
    geojson=megyek,
    hoverlabel={'namelength': -1},
    featureidkey='properties.name',
    marker={'line': {'width': 2}, 'opacity': 0.5}
)

layout = dict(
    mapbox=dict(
        style='carto-positron',
        center={'lon': 19.30, 'lat': 47.30},
        zoom=6
    ),
    margin={'l': 0, 'r': 0, 'b': 0, 't': 0}
)

fig = go.Figure(data=data, layout=layout)

fig.show()
