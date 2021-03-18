import json
from urllib.request import urlopen
import pandas as pd
import plotly.graph_objects as go

datum = '2021.03.15.'

data = pd.read_html(
    'https://en.wikipedia.org/wiki/COVID-19_pandemic_in_Hungary')

megye_adatok = data[4]
megye_adatok.columns = megye_adatok.columns.droplevel(-1)

megye_adatok = megye_adatok.dropna()
megye_adatok = megye_adatok.drop(['all', 'Hospitalized', 'Ventilated'], axis=1)

df = megye_adatok.loc[megye_adatok['Date'] == datum].drop(['Date'], axis=1)

megye_nevek = [
    megye+' megye' for megye in list(df.columns) if megye != 'Budapest']

ertekek = list(df.loc[349].values)

geo_url = '''
https://raw.githubusercontent.com/skylite21/csv_for_colab/master/megyek_uj.json
'''
with urlopen(geo_url) as response:
    megyek = json.load(response)


df2 = df.transpose()
df2.reset_index(inplace=True)
df2.columns = ['district', 'covid']
df2['district'] = df2['district'].astype(str) + ' megye'
df2['district'][19] = 'Budapest'
df2['district'][4] = 'Csongrád megye'

fig = go.Figure(go.Choroplethmapbox(locations=df2['district'], z=df2['covid'],
                                    colorscale="Rainbow",
                                    marker={'line': {'width': 2},
                                            'opacity': 0.5},
                                    geojson=megyek,
                                    hoverlabel={'namelength': -1},
                                    featureidkey="properties.name"
                                    ))

fig.update_layout(
    mapbox={
        'style': "carto-positron",
        'center': {'lon': 19.30, 'lat': 47.30},
        'zoom': 6, 'layers': [{
            # 'source': megyek,
            'type': "fill", 'below': "traces", 'color': "royalblue"}]},
    margin={'l': 0, 'r': 0, 'b': 0, 't': 0})

fig.show()
