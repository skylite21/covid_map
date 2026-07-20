# pip install -r requirements.txt
import json
from io import StringIO

import pandas as pd
import requests
from urllib.request import urlopen
import plotly.graph_objects as go

geojson_url = '''
https://raw.githubusercontent.com/skylite21/csv_for_colab/master/megyek_uj.json
'''

# Wikipedia blocks requests without a browser-like User-Agent (403).
response = requests.get(
    'https://en.wikipedia.org/wiki/COVID-19_pandemic_in_Hungary',
    headers={'User-Agent': 'Mozilla/5.0'},
)
response.raise_for_status()
data = pd.read_html(StringIO(response.text))

datum = '2021.05.16.'

# The county infections table position on the page shifts as the article
# grows, so find it by a known column instead of a hardcoded index.
megye_adatok = next(
    t for t in data
    if 'Bács-Kiskun' in [c[0] if isinstance(c, tuple) else c for c in t.columns]
)
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
df.loc[5, 'megye'] = 'Csongrád megye'
df.loc[20, 'megye'] = 'Budapest'
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
