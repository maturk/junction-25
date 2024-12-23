import ee
import geemap

# Doesn't contain visParams, yet...
# Note that e.g. 'Human Settlement' greatly overlaps with 'Built Area' as the prior has a band for buildings...
# 3rd object of tuple contains visualParams...
# So one can do
#   Map.addLayer(layer, 3rd, 2nd);
#   var layer = dataset.select(3rd);
ee.Initialize(project="ee-matiasturkulainen")


def normalize(image, min:int, max:int): #normalize a single image of data (1 img) to between 0 and 1 of the values are continuous
    normalized_image = image.subtract(min).divide(max - min)
    return normalized_image

def getMap(dataset, change=None):
    newData =dataset.filterDate('2012-01-01') #This needs to be changed as we cannot average all years.
    
    if (change is not None and change == True):
        return newData.formaTrend()
    else:
        return newData.mean()
        
    #we can also use change speed
    


datasetList = [
    (normalize(getMap(ee.ImageCollection("NASA/FLDAS/NOAH01/C/GL/M/V001").select('Evap_tavg')), 0.0, 0.00005), "Famine Early Warning", 'famine'),
    (normalize(getMap(ee.ImageCollection("IDAHO_EPSCOR/TERRACLIMATE").select('pdsi')), -1000.0, 1000.0), "Climate and Climatic Water Balance for Global Terrestrial Surfaces", 'waterBalance'),
    (normalize(getMap(ee.ImageCollection("CSIC/SPEI/2_9").select("SPEI_12_month")), -2.33, 2.33), "Drought index", 'drought'),
    (normalize(getMap(ee.ImageCollection("CIESIN/GPWv411/GPW_Basic_Demographic_Characteristics").select('basic_demographic_characteristics')), 0, 1), "Demographic Characteristics", 'demographic'),
    (normalize(getMap(ee.ImageCollection("JRC/GHSL/P2023A/GHS_POP").select('population_count')), 0.0, 100.0), "Population Surfaces", 'population'),
    (normalize(getMap(ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_SO2").select('SO2_column_number_density')), 0.0, 0.0005), "SO2", 'SO2'),
    (normalize(getMap(ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_HCHO").select('tropospheric_HCHO_column_number_density')), -0.02, 0.001), "CH2O", 'CH2O'),
    (normalize(getMap(ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_CO").select('CO_column_number_density')), 0, 0.05), "CO", 'CO'),
    (normalize(getMap(ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_CH4").select('CH4_column_volume_mixing_ratio_dry_air')), 1750, 1900), "CH4", 'CH4'),
    (normalize(getMap(ee.ImageCollection("CSP/HM/GlobalHumanModification").select('gHM')), 0.0, 1.0), "Human Modification", 'HumanMod'),
    (normalize(getMap(ee.ImageCollection("BNU/FGS/CCNL/v1").select('b1')), 3.0, 60.0), "Nighttime Light", 'nightTime'),
    (normalize(getMap(ee.ImageCollection("JRC/GHSL/P2023A/GHS_BUILT_H").select('built_height')), 0.0, 12.0), "Building Height", 'buildHeight'),
    (normalize(getMap(ee.ImageCollection("MODIS/061/MCD15A3H").select('Fpar')), 0.0, 100.0), "Leaf Area", 'leafArea')
]

# lambda_i should be \lamda_i = 1 EXCEPT for these critical cases:
# famine 3
# drought 3
# HumanMod 2
# BioDiversity 0.5

weights = [3, 1, 3, 1, 1, 1, 1, 1, 1, 2, 1, 0.5, 1]


#Map functions



def reduceRes(img, newScale): #reduce the resolution of data (img) to a meter based scale
    img = img.setDefaultProjection(
        crs='EPSG:4326',  # WGS84 coordinate system
        scale=newScale  # appropriate scale in meters
    )

    return img.reduceResolution(
        reducer= ee.Reducer.mean(),
        bestEffort=True
    ).reproject(
        crs= img.projection(),
        scale= newScale  # in meters
    )

def combineMaps(imgs, weights=None):
    # Weight is 1 if not provided
    if weights is None:
        weights = [1/len(imgs)] * len(imgs)
    elif len(weights) != len(imgs):
        raise ValueError("Weights list must match the number of images.")

    # zeros so if no data its inited as 0
    res = ee.Image(0)
    for img, weight in zip(imgs, weights):
        res = res.add(img.multiply(weight))
    return res

