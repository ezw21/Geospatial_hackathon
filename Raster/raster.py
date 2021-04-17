import rasterio
import rasterio.features
import rasterio.warp
from matplotlib import pyplot

with rasterio.open('../Hackathon/water_detect_input/17APR08224828-M3DS-013930604400_01_P002.tif') as dataset:

    # Read the dataset's valid data mask as a ndarray.
    mask = dataset.dataset_mask()
    print(dataset.read(3))
    print(dataset.read(5))
    f, axarr = pyplot.subplots(2, sharex = True)

    axarr[0].imshow(dataset.read(3))
    axarr[1].imshow(dataset.read(5))
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