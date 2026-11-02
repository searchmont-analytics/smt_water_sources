'use strict';
const boundaryStyle={color:'#496a92',weight:2,dashArray:'8 5',fillOpacity:.035,interactive:false};
const responseBoundary=L.geoJSON(studyAreas.features[0],{style:boundaryStyle}).addTo(map);
const regionalBoundary=L.geoJSON(studyAreas.features[1],{style:{...boundaryStyle,color:'#b47a36',fillOpacity:.015}});
function toggleBoundary(id,layer){$(id).onchange=()=>{if($(id).checked)layer.addTo(map);else map.removeLayer(layer)}}
toggleBoundary('responseboundary',responseBoundary);toggleBoundary('regionalboundary',regionalBoundary);
$('fitresponse').onclick=()=>map.fitBounds(responseBoundary.getBounds(),{padding:[45,45]});$('fitregional').onclick=()=>map.fitBounds(regionalBoundary.getBounds(),{padding:[45,45]});
L.DomEvent.disableClickPropagation(document.querySelector('.studycontrols'));L.DomEvent.disableScrollPropagation(document.querySelector('.studycontrols'));
function insideOutline(coord,ring){const x=coord[1],y=coord[0];let inside=false;for(let i=0,j=ring.length-1;i<ring.length;j=i++){const [xi,yi]=ring[i],[xj,yj]=ring[j];if(((yi>y)!==(yj>y))&&(x<(xj-xi)*(y-yi)/(yj-yi)+xi))inside=!inside}return inside}
function showStudyCounts(){const actual=state.water.filter(w=>!w.demo&&w.coord),inside=actual.filter(w=>insideOutline(w.coord,studyAreas.features[0].geometry.coordinates[0])).length;$('studycounts').textContent=`Uploaded Response Area outline: ${inside} water locations inside · ${actual.length-inside} outside. All locations remain available on the map. This outline is not a verified service boundary.`}
const beforeStudyRender=render;render=function(){beforeStudyRender();showStudyCounts()};showStudyCounts();
map.fitBounds(responseBoundary.getBounds(),{padding:[45,45]});
