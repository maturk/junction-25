import ee
import geemap.core as geemap
import time

ee.Authenticate()
ee.Initialize(project='ee-matiasturkulainen')

# Initialize a map object.
Map = geemap.Map(center=(40, -100), zoom=4)
Map.show()


time.sleep(10000)
