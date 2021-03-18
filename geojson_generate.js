// npm i cheerio got

// code is copied from here: https://juzraai.github.io/blog/2020/geojson-osszeallitasa-megyeterkephez/

const fs = require('fs')
const cheerio = require('cheerio')
const got = require('got')

async function getCountyOsmIds() {
	const res = await got('https://wiki.openstreetmap.org/wiki/Hungary/Boundaries')
	const $ = cheerio.load(res.body)
  const ids = $('h2:contains("Megyék") + table tr').toArray().map(tr => {
		return $('td a', tr).toArray().map(a => $(a).text())[2]
	}).filter(id => id);
  const names = $('h2:contains("Megyék") + table tr').toArray().map(tr => {
		return $('td a', tr).toArray().map(a => $(a).text())[0]
	}).filter(id => id);
  const data = [];
  for(let i=0; i<=ids.length; i++) {
    if (ids[i]) {
    let o = {
      id: ids[i],
      name: names[i]
    }
    data.push(o); 
    }
  }
	return data;
}

async function downloadGeoJson(osmId) {
	const geoJsonUrlTemplate = 'http://polygons.openstreetmap.fr/get_geojson.py?id=X&params=0'
	const res = await got(geoJsonUrlTemplate.replace('X', osmId))
	return res.body
}

async function getGeoJson(id) {
	const file = `${id}.json`
	if (fs.existsSync(file)) return fs.readFileSync(file)
	const json = await downloadGeoJson(id)
	fs.writeFileSync(file, json)
	return json
}

function fixGeometryCollection(geometry) {
	if (geometry.type === 'GeometryCollection' && geometry.geometries.length === 1) {
		return geometry.geometries[0]
	}
	return geometry
}

function feature(geometry, id, name) {
	return {
		type: 'Feature',
    id,
		properties: { id, name }, // will be useful :)
		geometry: fixGeometryCollection(geometry)
	}
}

async function getFeature(data) {
	const geometryJson = await getGeoJson(data.id)
	const geometry = JSON.parse(geometryJson)
	return feature(geometry, data.id, data.name)
}

function featureCollection(features) {
	return { type: 'FeatureCollection', features }
}

async function generateFeatureCollection(data, file) {
	const features = await Promise.all(data.map(getFeature))
	fs.writeFileSync(file, JSON.stringify(featureCollection(features)))
}

(async () => {
	const data = await getCountyOsmIds()
  console.log(data);
	await generateFeatureCollection(data, 'counties.json')
})()
