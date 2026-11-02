"""Extract Microsoft footprints with polygon centres inside the uploaded study outline."""
import json,zipfile,hashlib,math,sys
from pathlib import Path
project=Path(__file__).resolve().parents[1]
areas=json.loads((project/'dist/study-areas.js').read_text().split(' = ',1)[1].rstrip(';\n'))
ring=areas['features'][0]['geometry']['coordinates'][0]
minx,maxx=min(p[0] for p in ring),max(p[0] for p in ring)
miny,maxy=min(p[1] for p in ring),max(p[1] for p in ring)
def inside(x,y):
 flag=False
 for a,b in zip(ring,ring[1:]):
  if (a[1]>y)!=(b[1]>y) and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:flag=not flag
 return flag
def centroid(r):
 cross=[a[0]*b[1]-b[0]*a[1] for a,b in zip(r,r[1:])];area=sum(cross)
 if abs(area)<1e-12:return [sum(p[0] for p in r[:-1])/(len(r)-1),sum(p[1] for p in r[:-1])/(len(r)-1)]
 return [sum((a[0]+b[0])*c for a,b,c in zip(r,r[1:],cross))/(3*area),sum((a[1]+b[1])*c for a,b,c in zip(r,r[1:],cross))/(3*area)]
features=[];scanned=0
archive=sys.argv[1] if len(sys.argv)>1 else 'Ontario.zip'
with zipfile.ZipFile(archive) as z:
 with z.open('Ontario.geojson') as data:
  for line in data:
   line=line.strip().rstrip(b',')
   if not line.startswith(b'{"type":"Feature"'):continue
   scanned+=1;f=json.loads(line);r=f['geometry']['coordinates'][0]
   if max(p[0] for p in r)<minx or min(p[0] for p in r)>maxx or max(p[1] for p in r)<miny or min(p[1] for p in r)>maxy:continue
   x,y=centroid(r)
   if not inside(x,y):continue
   fid='ms-'+hashlib.sha256(json.dumps(f['geometry'],sort_keys=True).encode()).hexdigest()[:16]
   f['id']=fid;f['properties']={'id':fid,'classification':'Unknown structure','centre':[x,y],'source':'Microsoft Canadian Building Footprints','source_url':'https://github.com/microsoft/CanadianBuildingFootprints','license':'ODbL-1.0','imagery_date':'Unknown; varies by imagery source','selection':'Footprint centre inside uploaded Response Area outline'};features.append(f)
out={'type':'FeatureCollection','name':'Microsoft building footprints — Searchmont Response Area','attribution':'© Microsoft. Available under the Open Database License (ODbL).','license':'https://opendatacommons.org/licenses/odbl/1-0/','source':'https://github.com/microsoft/CanadianBuildingFootprints','description':'Machine-generated building outlines, not verified dwellings. Full footprints retained where centre lies within the uploaded Response Area outline. Individual imagery dates unknown.','features':features}
(project/'dist/buildings.geojson').write_text(json.dumps(out,separators=(',',':')))
print(json.dumps({'scanned':scanned,'selected':len(features),'size':(project/'dist/buildings.geojson').stat().st_size}))
