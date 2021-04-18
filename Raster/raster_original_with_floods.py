import rasterio
import rasterio.features
import rasterio.warp
from rasterio.plot import show
from matplotlib import pyplot
import numpy as np
from PIL import Image as im
import time 
import csv

fields = ["x", "y"]
rows = []
filename = "./Raster/water_record.csv"

def normalize(array):
    array_min, array_max = array.min(), array.max()
    print(array_min, array_max)
    return (array - array_min) / (array_max - array_min)


with rasterio.open('../Hackathon/water_detect_input/20MAR28221842-M3DS-013930604400_01_P001.tif') as dataset:

    # Read the dataset's valid data mask as a ndarray.
    print(dataset)
    print(dataset.bounds)
    print("here")
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
    print(band_4_norm.shape)
    print(band_3_norm.shape)
    print(band_2_norm.shape)

    stack = np.dstack((band_4, band_3, band_2))

    stack_min = stack.min()
    stack_max = stack.max()

    t0 = time.time()
    with open("./Raster/flood_record.csv") as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        print(csv_reader)
        next(csv_reader)
        for row in csv_reader:
            x = float(row[0])
            y = float(row[1])
            if x > dataset.bounds.left and x < dataset.bounds.right and y > dataset.bounds.bottom and y < dataset.bounds.top:
                row, col = dataset.index(x, y)
    
                stack[row][col][0] = stack_max
    t1 = time.time()
    total = t1 - t0
    print(total)
    
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