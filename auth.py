import http.server
import socketserver
import webbrowser

import ee
import geemap

ee.Authenticate()
ee.Initialize(project="ee-matiasturkulainen")

# basemap
Map = geemap.Map(center=(40, -100), zoom=4)
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
dataset = ee.Image("DLR/WSF/WSF2015/v1")  # type: ignore
Map.addLayer(ee_object=dataset, vis_params=visualization, name="Human settlement areas")

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
