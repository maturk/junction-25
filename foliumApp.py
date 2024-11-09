#satellite map
#tile = folium.TileLayer(
 #       tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
  #      attr = 'Esri',
   #     name = 'Esri Satellite',
    #    overlay = False,
     #   control = True
     #  ).add_to(map_1)
import http.server
import socketserver
import webbrowser
import folium

import mapFunctions

# basemap
map_center = [60.25, 24.85] 
folium_map = folium.Map(location=map_center, zoom_start=10, tiles="OpenStreetMap")
visualization = {
    'min': 0.0,
    'max': 1.0,
    'palette': ['0c0c0c', '071aff', 'ff0000', 'ffbd03', 'fbff05', 'fffdfd']
}

# dot_product = dataset.multiply(ee.Image(1).subtract(so2))
# dot_product = dataset.multiply(ds2)
dataset_map_id = dataset.getMapId(visualization)
folium.TileLayer(
    tiles=dataset_map_id['tile_fetcher'].url_format,
    attr="Google Earth Engine - Global Human Modification",
    overlay=True,
    name="Human Modification Index"
).add_to(folium_map)

#Map.addLayer(ee_object=mapFunctions.combineMaps([dataset,ds2]), vis_params=visualization, name="Combined")

combined_layer = dataset
combined_map_id = combined_layer.getMapId(visualization)

# Add the combined layer to Folium map
folium.TileLayer(
    tiles=combined_map_id['tile_fetcher'].url_format,
    attr="Google Earth Engine - Combined Layer",
    overlay=True,
    name="Combined Layer"
).add_to(folium_map)

# Add layer control
folium.LayerControl().add_to(folium_map)

# Display the map locally
def serve_map():
    # Save the map as an HTML file
    folium_map.save("map.html")

    # Define server to host the map
    port = 8000
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), handler)

    # Automatically open the map in the browser
    webbrowser.open(f"http://localhost:{port}/map.html")

    # Start server
    print(f"Serving map at http://localhost:{port}/map.html")
    httpd.serve_forever()

# Call the function to serve the map
serve_map()