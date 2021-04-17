import rasterio
import rasterio.features
import rasterio.warp
from matplotlib import pyplot
import numpy as np
from PIL import Image as im

def normalize(array):
    array_min, array_max = array.min(), array.max()
    return (array - array_min) / (array_max - array_min)


with rasterio.open('../Hackathon/water_detect_input/17APR08224828-M3DS-013930604400_01_P002.tif') as dataset:

    # Read the dataset's valid data mask as a ndarray.
    mask = dataset.dataset_mask()
    print(dataset.height)
    print(dataset.width)
    print(dataset.indexes)

    band_1 = dataset.read(1)
    band_2 = dataset.read(2)
    band_3 = dataset.read(3)
    band_4 = dataset.read(4)
    band_5 = dataset.read(5) 
    band_6 = dataset.read(6)
    band_7 = dataset.read(7)
    print(band_5)

    band_1_norm = normalize(band_1)
    band_2_norm = normalize(band_2)
    band_3_norm = normalize(band_3)
    band_4_norm = normalize(band_4)
    band_5_norm = normalize(band_5)
    band_6_norm = normalize(band_6)
    band_7_norm = normalize(band_7)
    print(band_1_norm.shape)

    stack = np.dstack((band_4_norm, band_3_norm, band_2_norm))

    # rescaled = (255.0 / stack.max() * (stack - stack.min())).astype(np.uint8)
    # image = im.fromarray(rescaled)
    # image.save('Raster/754.png')
    # stack = np.dstack((band_4_norm, band_5_norm, band_1_norm))
    # rescaled = (255.0 / stack.max() * (stack - stack.min())).astype(np.uint8)
    # image = im.fromarray(rescaled)
    # image.save('Raster/451.png')
    # stack = np.dstack((band_5_norm, band_4_norm, band_3_norm))
    # rescaled = (255.0 / stack.max() * (stack - stack.min())).astype(np.uint8)
    # image = im.fromarray(rescaled)
    # image.save('Raster/543.png')
    # stack = np.dstack((band_5_norm, band_6_norm, band_4_norm))
    # rescaled = (255.0 / stack.max() * (stack - stack.min())).astype(np.uint8)
    # image = im.fromarray(rescaled)
    # image.save('Raster/564.png')


    # # f, axarr = pyplot.subplots(2, sharex = True)

    # # axarr[0].imshow(stack)
    # # axarr[1].imshow(dataset.read(5))
    pyplot.imshow(stack)
    pyplot.show()

    # Extract feature shapes and values from the array.
    for geom, val in rasterio.features.shapes(
            mask, transform=dataset.transform):

        # Transform shapes from the dataset's own coordinate
        # reference system to CRS84 (EPSG:4326).
        geom = rasterio.warp.transform_geom(
            dataset.crs, 'EPSG:4326', geom, precision=6)

        # Print GeoJSON shapes to stdout.
        print(geom)