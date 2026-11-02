const assert=require('node:assert/strict');
const {buildRoadGraph,shortestTimes}=require('../dist/network.js');
const km=(a,b)=>Math.hypot(a[0]-b[0],a[1]-b[1]);
function at(nodes,p){return nodes.findIndex(n=>km(n.p,p)<1e-6)}
const road=(coords,extra={})=>({coords,speed:60,status:'Open',...extra});
let g=buildRoadGraph([road([[0,0],[1,0]]),road([[1,0],[1,1]]),road([[1,1],[2,1]],{status:'Closed'})],km);
let d=shortestTimes(g.nodes,at(g.nodes,[0,0]),5,1);
assert(Math.abs(d[at(g.nodes,[1,1])]-2)<1e-9);
assert.equal(at(g.nodes,[2,1]),-1);
let slow=shortestTimes(g.nodes,at(g.nodes,[0,0]),5,.5);
assert(Math.abs(slow[at(g.nodes,[1,1])]-4)<1e-9);
g=buildRoadGraph([road([[-1,0],[1,0]]),road([[0,-1],[0,1]])],km);
d=shortestTimes(g.nodes,at(g.nodes,[-1,0]),5,1);
assert.equal(d[at(g.nodes,[0,1])],Infinity,'Geometric crossings must not connect');
g=buildRoadGraph([road([[0,0],[1,0]],{direction:'forward'})],km);
d=shortestTimes(g.nodes,at(g.nodes,[1,0]),5,1);
assert.equal(d[at(g.nodes,[0,0])],Infinity,'Forward-only edge must not route backward');
console.log('Network checks passed: shared junction, closed exclusion, speed factor, disconnected crossing, one-way direction.');
