"""Download ORN Composite segments intersecting a buffered Searchmont study window."""
import urllib.request,urllib.parse,json,datetime,collections
from pathlib import Path
root=Path(__file__).resolve().parents[1]
url='https://services1.arcgis.com/TJH5KDher0W13Kgo/arcgis/rest/services/Ontario_Road_Network_Composite_Service_GeoHub_View_EN/FeatureServer/5'
envelope='-84.264,46.642,-83.765,46.884'
params={'f':'geojson','where':'1=1','geometry':envelope,'geometryType':'esriGeometryEnvelope','inSR':'4326','outSR':'4326','spatialRel':'esriSpatialRelIntersects','outFields':'*','returnGeometry':'true','orderByFields':'OBJECTID','resultRecordCount':2000}
features=[];offset=0
while True:
 params['resultOffset']=offset
 with urllib.request.urlopen(url+'/query?'+urllib.parse.urlencode(params),timeout=60) as response:data=json.load(response)
 if 'error' in data:raise RuntimeError(data['error'])
 batch=data['features'];features.extend(batch);offset+=len(batch)
 if len(batch)<2000:break
assert len({f['properties']['OBJECTID'] for f in features})==len(features)
data={'type':'FeatureCollection','name':'Ontario Road Network Composite — Searchmont study window','source':url,'source_page':'https://geohub.lio.gov.on.ca/maps/7c00e0fef49a41b9b708986dba5ce241/about','license':'Open Government Licence – Ontario','attribution':'Contains information licensed under the Open Government Licence – Ontario. © King’s Printer for Ontario.','retrieved':datetime.datetime.now(datetime.timezone.utc).isoformat(),'selection':'Full segments intersecting longitude/latitude envelope '+envelope+'. This is a rectangular study window around the uploaded Response Area, not a township boundary.','features':features}
(root/'dist/roads.geojson').write_text(json.dumps(data,separators=(',',':')))
print('segments',len(features),'bytes',(root/'dist/roads.geojson').stat().st_size)
for field in ['ROAD_CLASS','ROAD_ELEMENT_TYPE','SPEED_LIMIT','PAVEMENT_STATUS','DIRECTION_OF_TRAFFIC_FLOW']:print(field,dict(collections.Counter(f['properties'].get(field) for f in features)))
for f in features[:3]:print(json.dumps(f['properties']))
print('coordinate_count',sum(len(f['geometry']['coordinates']) if f['geometry']['type']=='LineString' else sum(map(len,f['geometry']['coordinates'])) for f in features))
