import ee
import geemap

# Doesn't contain visParams, yet...
# Note that e.g. 'Human Settlement' greatly overlaps with 'Built Area' as the prior has a band for buildings...
# 3rd object of tuple contains visualParams...
# So one can do
#   Map.addLayer(layer, 3rd, 2nd);
#   var layer = dataset.select(3rd);
datasetList = [
    (ee.ImageCollection("NASA/FLDAS/NOAH01/C/GL/M/V001"), "Famine Early Warning",'famine'),
    (ee.ImageCollection("IDAHO_EPSCOR/TERRACLIMATE"), "Climate and Climatic Water Balance for Global Terrestrial Surfaces", 'waterBalance'),
    (ee.ImageCollection("CSIC/SPEI/2_9"), "Drought index", 'drought'),
    (ee.ImageCollection("CIESIN/GPWv411/GPW_Basic_Demographic_Characteristics"), "Demographic Characteristics", 'demographic'),
    (ee.ImageCollection("JRC/GHSL/P2023A/GHS_POP"), "Population Surfaces", 'population'),
    (ee.ImageCollection("COPERNICUS/S5P/NRTI/L3_SO2"), "SO2", 'SO2'),
    (ee.ImageCollection("COPERNICUS/S5P/NRTI/L3_HCHO"), "CH2O", 'CH2O'),
    (ee.ImageCollection("COPERNICUS/S5P/NRTI/L3_CO"), "CO", 'CO'),
    (ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_CH4"), "CH4", 'CH4'),
    #(ee.Image("UMD/hansen/global_forest_change_2023_v1_11"), "Forest Change"),
    (ee.ImageCollection("CSP/HM/GlobalHumanModification"), "Human Modification", 'HumanMod'),
    #(ee.Image("DLR/WSF/WSF2015/v1"), "World Settlement Footprint"),
    (ee.ImageCollection("BNU/FGS/CCNL/v1"), "Nighttime Light", 'nightTime'),
    #(ee.ImageCollection("ESA/WorldCover/v200"), "Built Area"),
    (ee.ImageCollection("JRC/GHSL/P2023A/GHS_BUILT_H"), "Building Height", 'buildHeight'),
    #(ee.ImageCollection("JRC/GHSL/P2023A/GHS_BUILT_C"), "Human Settlement"),
    #(ee.ImageCollection("JRC/GHSL/P2023A/GHS_SMOD_V2-0"), "Degree of Urbanization"),
    #(ee.Image("CSP/ERGo/1_0/Global/ALOS_topoDiversity"), "Biodiversity"),
    (ee.ImageCollection("MODIS/061/MCD15A3H"), "Leaf Area", 'leafArea')
    ]

#Helper functions

def normalize(image, min:int, max:int): #normalize a single image of data (1 img) to between 0 and 1 of the values are continuous
    normalized_image = image.subtract(min).divide(max - min)
    return normalized_image


#Map functions

def getMap(dataset:str):
    dataset =ee.ImageCollection(dataset).filterDate('2016-04-01') #This needs to be changed as we cannot average all years.
    image = dataset.mean()
    
    # Check if the image has any bands
    if image.bandNames().size().getInfo() == 0:
        raise ValueError("The dataset does not contain any bands.")

    return dataset.mean()

def reduceRes(img, newScale): #reduce the resolution of data (img) to a meter based scale
    img = img.setDefaultProjection(
        crs='EPSG:4326',  # Use the WGS84 coordinate system
        scale=newScale  # Set an appropriate scale in meters
    )

    return img.reduceResolution(
        reducer= ee.Reducer.mean(),
        bestEffort=True
    ).reproject(
        crs= img.projection(),
        scale= newScale  # in meters
    )

def combineMaps(imgs):
    defWeight = 1/len(imgs)
    res = ee.Image(0)
    for i in imgs:
        res = res.add(i.multiply(defWeight))
    return res
