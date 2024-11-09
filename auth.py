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
visualization = {
    min: 0,
    max: 1,
}
# ds2 = ee.ImageCollection("ESA/WorldCover/v200").select("Map").mean()

dataset = ee.ImageCollection("CSP/HM/GlobalHumanModification").mean().select("gHM")

dataset = mapFunctions.reduceRes(dataset, 10000)
Map.addLayer(ee_object=dataset, vis_params=visualization, name="resolution reduced gHM")

ds2 = ee.ImageCollection("COPERNICUS/S5P/NRTI/L3_CO").mean().select("CO_column_number_density")
ds2 = mapFunctions.normalize(ds2,-279, 4.64)
ds2 = mapFunctions.reduceRes(ds2, 10000)
ds2 = ee.Image(1).subtract(ds2)


visualization = {
    'min': 0.0,
    'max': 1.0,
    'palette': ['0c0c0c', '071aff', 'ff0000', 'ffbd03', 'fbff05', 'fffdfd']
}

# dot_product = dataset.multiply(ee.Image(1).subtract(so2))
# dot_product = dataset.multiply(ds2)

Map.addLayer(ee_object=mapFunctions.combineMaps([dataset,ds2]), vis_params=visualization, name="Combined")



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
