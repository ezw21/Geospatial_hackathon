import rasterio
import rasterio.features
import rasterio.warp
from rasterio.plot import show
from matplotlib import pyplot
import numpy as np
from PIL import Image as im
import time 
import csv 
import cv2 as cv

pyplot.rcParams['figure.figsize'] = [20, 15]
pyplot.rcParams['figure.dpi'] = 200 # 200 e.g. is really fine, but slower
fields = ["x", "y"]
rows = []
filename = "./Raster/flood_record.csv"

def normalize(array):
    array_min, array_max = array.min(), array.max()
    print(array_min, array_max)
    return (array - array_min) / (array_max - array_min)


with rasterio.open('../Hackathon/water_detect_input/17APR08224828-M3DS-013930604400_01_P002.tif') as dataset:

    # Read the dataset's valid data mask as a ndarray.
    mask = dataset.dataset_mask()

    band_1 = dataset.read(1)
    band_2 = dataset.read(2)
    band_3 = dataset.read(3)
    band_4 = dataset.read(4)
    band_5 = dataset.read(5) 
    band_6 = dataset.read(6)
    band_7 = dataset.read(7)

    band_1_norm = normalize(band_1)
    band_2_norm = normalize(band_2)
    band_3_norm = normalize(band_3)
    band_4_norm = normalize(band_4)
    band_5_norm = normalize(band_5)
    band_6_norm = normalize(band_6)
    band_7_norm = normalize(band_7)

    stack = np.dstack((band_5_norm, band_6_norm, band_4_norm))
    
    t0 = time.time()
    with open("./Raster/water_record.csv") as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        # print(csv_reader)
        next(csv_reader)
        for row in csv_reader:
          x = float(row[0])
          y = float(row[1])
          if x > dataset.bounds.left and x < dataset.bounds.right and y > dataset.bounds.bottom and y < dataset.bounds.top:
              row, col = dataset.index(x, y)
              stack[row][col] = [0,0,1]
    
    t1 = time.time()
    total = t1 - t0
    print(total)


    t0 = time.time()
    for i in range(dataset.height):
        for j in range(dataset.width):
            if not (stack[i][j][0] >= 0.105 and stack[i][j][1] >= 0.073 and stack[i][j][2] >= 0.105 and stack[i][j][0] <= 0.233 and stack[i][j][1] <= 0.245 and stack[i][j][2] <= 0.217):
                stack[i][j] = [0, 0, 0]
            elif (stack[i][j][0] != 0 and stack[i][j][1] != 0 and stack[i][j][2] != 1):
                stack[i][j] = [1, 0, 0]
                x, y = dataset.transform * (j, i)
                rows.append([x, y])

    t1 = time.time()
    total = t1 - t0
    print(total)
    
    with open(filename, 'w', newline='') as csvfile:
      csvwriter = csv.writer(csvfile)
      csvwriter.writerow(fields)
      csvwriter.writerows(rows)
        
    stack = stack.astype(int)

    img1 = cv.imread('./Raster/base.jpg')
    img1 = np.array(img1, dtype=np.uint8)
    img2 = np.array(stack[:,:,0], dtype=np.uint8)
    

    #find all your connected components (white blobs in your image)
    nb_components, output, stats, centroids = cv.connectedComponentsWithStats(img2, connectivity=8)
    #connectedComponentswithStats yields every seperated component with information on each of them, such as size
    #the following part is just taking out the background which is also considered a component, but most of the time we don't want that.
    sizes = stats[1:, -1]; nb_components = nb_components - 1

    # minimum size of particles we want to keep (number of pixels)
    #here, it's a fixed value, but you can set it as you want, eg the mean of the sizes or whatever
    min_size = 300  

    #your answer image
    tmp_img = np.zeros((output.shape))
    #for every component in the image, you keep it only if it's above min_size
    for i in range(0, nb_components):
        if sizes[i] >= min_size:
            tmp_img[output == i + 1] = 255

    img2 = np.array(tmp_img, dtype=np.uint8)
    # Initiate SIFT detector
    sift = cv.ORB_create()
    
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)

    # FLANN parameters
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks=50)   # or pass empty dictionary
    flann = cv.FlannBasedMatcher(index_params,search_params)
    matches = flann.knnMatch(np.asarray(des1,np.float32),np.asarray(des2,np.float32),k=2)
    # Need to draw only good matches, so create a mask
    matchesMask = [[0,0] for i in range(len(matches))]
    # ratio test as per Lowe's paper
    for i,(m,n) in enumerate(matches):
        if m.distance < 0.5 * n.distance:
            matchesMask[i]=[1,0]
    draw_params = dict(matchColor = (0,255,0),
                      singlePointColor = (255,0,0),
                      matchesMask = matchesMask,
                      flags = cv.DrawMatchesFlags_DEFAULT)
    img3 = cv.drawMatchesKnn(img1,kp1,img2,kp2,matches,None,**draw_params)
    pyplot.imshow(img3,),pyplot.show()

#     print("Number of matches :",len(matchesMask) )
    if len(matchesMask) >5 :
        print("Is flooded")

    pyplot.imshow(stack)
    pyplot.show()
    cv.imwrite('/content/output/output2.jpg', img2) 


    # Extract feature shapes and values from the array.
    for geom, val in rasterio.features.shapes(
            mask, transform=dataset.transform):

        # Transform shapes from the dataset's own coordinate
        # reference system to CRS84 (EPSG:4326).
        geom = rasterio.warp.transform_geom(
            dataset.crs, 'EPSG:4326', geom, precision=6)

        # Print GeoJSON shapes to stdout.
        print(geom)
