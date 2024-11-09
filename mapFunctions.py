import ee
import geemap

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

