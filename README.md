# Searchmont Water & Access

Interactive GIS learning and planning prototype for the Searchmont area, Algoma District, Ontario.

## Run locally

Static HTML and JavaScript; no build step or API keys required.

```sh
python3 -m http.server 8000 --directory dist
```

Open http://localhost:8000. Internet access loads the Esri basemap; analysis uses the included local data.

## Features

- Water inventory: 20 user-reported water locations plus the Searchmont Fire Hall.
- Ontario Road Network: 162 segments, source attributes and local access/speed overrides.
- Microsoft building footprints: 546 detected structures inside the supplied study outline.
- Road travel coverage with explicit speed assumptions.
- Building-to-resort-hydrant road distance and estimated driving time.
- Fixed-radius clustering with editable minimum building count and radius.
- Proposed storage areas and CSV, JSON and GeoJSON exports.

Edits remain in browser localStorage, not a shared database. Browser-only edits are not included in this source snapshot; use the application's exports to retain them separately.

## Default analysis and limits

The baseline uses shortest road distance, assumed speeds of 40 km/h paved and 25 km/h unpaved (capped at source speed limits), and a 250 m maximum point-to-road gap. Of 546 structures, 509 received road routes and 37 exceeded the building-to-road gap limit.

The hydrant lies approximately 230 m from the nearest included road line. Road metrics exclude that access leg, building access gaps, filling, turnaround, traffic and vehicle-specific constraints. They are not complete tanker-cycle or validated emergency-response estimates.

A 500 m radius with minimum five structures produces 28 fixed-radius groups containing 480 structures. Each structure belongs to at most one group. Circles use straight-line distance and may span physical barriers.

Footprints are not confirmed occupied homes. Road access, topology, bridge/load restrictions, current conditions and access paths require local validation. Supplied study outlines are not verified township or service-jurisdiction boundaries.

## Data and attribution

- [Microsoft Canadian Building Footprints](https://github.com/microsoft/CanadianBuildingFootprints): extracted Ontario subset under [ODbL](https://opendatacommons.org/licenses/odbl/1-0/). Individual imagery dates are unknown; detection is imperfect.
- [Ontario Road Network Composite](https://geohub.lio.gov.on.ca/maps/7c00e0fef49a41b9b708986dba5ce241/about): contains information licensed under the Open Government Licence – Ontario. Full segments intersecting the documented study window are retained.
- Water locations and study outlines: user-supplied project data; descriptions retained.
- Leaflet 1.9.4: vendored library under its included licence; see THIRD_PARTY_NOTICES.md.
- Esri topographic tiles load remotely with map attribution; tiles are not bundled.

GeoJSON files carry source information. Data licences remain separate from application-source licensing. No additional source-code licence has been selected for this project.

## Tests and reproducible analysis

Node.js runs the tests and baseline analysis without installing packages:

```sh
node tests/network.cjs
node tests/evaluation.cjs
node scripts/run-building-analysis.cjs
```

The last command regenerates `dist/baseline-analysis.json` and verifies routed geometry distances.

Refresh extracts using Python 3:

```sh
python3 scripts/extract-roads.py
python3 scripts/extract-buildings.py /path/to/Ontario.zip
```

Obtain the Ontario ZIP from the Microsoft repository's download table. Extraction also uses `dist/study-areas.js`. Refreshes can change counts and short B-number labels; footprint IDs derive from geometry.

## Files

- `dist/`: static application, local data and map library.
- `scripts/`: extraction and analysis scripts.
- `tests/`: routing and clustering checks.

ChatGPT Sites deployment identity and credentials are excluded from this snapshot.
