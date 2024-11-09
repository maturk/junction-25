import http.server
import socketserver
import webbrowser

import ee
import geemap

import mapFunctions




ee.Authenticate()
ee.Initialize(project="ee-matiasturkulainen")

# basemap
Map = geemap.Map(center=(60.25, 24.85), zoom=10)
Map.add_basemap("SATELLITE")

# overlay
# https://developers.google.com/earth-engine/datasets/catalog/DLR_WSF_WSF2015_v1
opacity = 0.75
blackBackground = ee.Image(0)  # type: ignore

Map.addLayer(blackBackground, None, "Black background", True, opacity)

datasets = [i[0] for i in mapFunctions.datasetList]
names = [i[1] for i in mapFunctions.datasetList]




#for i in meanSets:
    #Map.addLayer(i,vis-params,"test",True,opacity)
visualization = {
    min: 0,
    max: 1,
}

visualization = {
    'min': 0.0,
    'max': 1.0,
    'palette': ['0c0c0c', '071aff', 'ff0000', 'ffbd03', 'fbff05', 'fffdfd']
}


# html
output_file = "map_export.html"
Map.save(output_file)
webbrowser.open(f"http://localhost:8000/{output_file}")
# Serve the HTML file in browser
PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    httpd.serve_forever()