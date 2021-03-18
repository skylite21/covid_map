# covid adatok


Egy gyors hacky megoldás magyarország covid adatainak vizualizálására megyékre lebontva

## használat

készíts virtualenv-et, majd aktiváld:

```
virtualenv -p python3 venv; source venv/bin/activate
```
telepitsd a dependency-ket:

```
pip install -r requirements.txt
```

futtasd:
```
python3 megye.py
```

Az adatok [errol](https://en.wikipedia.org/wiki/COVID-19_pandemic_in_Hungary) az oldalról vannak letöltve

a megyékhez szükséges geojson file előállításához [ezt](https://juzraai.github.io/blog/2020/geojson-osszeallitasa-megyeterkephez/) a nodejs scriptet használtam fel, picit módosítva, hogy a megye nevek is szerepeljenek a file-ban.

