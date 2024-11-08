import ee
import geemap
import time
import webbrowser

ee.Authenticate()
ee.Initialize(project='ee-matiasturkulainen')

Map = geemap.Map(center=(40, -100), zoom=4)

Map.add_basemap('SATELLITE')

output_file = 'map_export.html'
Map.save(output_file)

webbrowser.open(output_file)


