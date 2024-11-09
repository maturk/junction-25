import http.server
import socketserver
import webbrowser

import ee
import geemap

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
dataset = ee.ImageCollection('CSP/HM/GlobalHumanModification').select("gHM").mean()
ds2 = ee.ImageCollection("ESA/WorldCover/v200").select("Map").mean()


def reduceRes(img):
    img = img.setDefaultProjection(
        crs='EPSG:4326',  # Use the WGS84 coordinate system
        scale=10000  # Set an appropriate scale in meters
    )

    return img.reduceResolution(
        reducer= ee.Reducer.mean(),
        bestEffort=True
    ).reproject(
        crs= img.projection(),
        scale= 10000  # in meters
    )

dataset = reduceRes(dataset)
Map.addLayer(ee_object=dataset, vis_params=visualization, name="resolution reduced gHM")


visualization = {
    'min': 0.0,
    'max': 1.0,
    'palette': ['0c0c0c', '071aff', 'ff0000', 'ffbd03', 'fbff05', 'fffdfd']
}

# dot_product = dataset.multiply(ee.Image(1).subtract(so2))
# dot_product = dataset.multiply(ds2)

# Map.addLayer(ee_object=dot_product, vis_params=visualization, name="SO2 penaliced")



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
