import math

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
import numpy as np
from scipy import signal
from statistics import mean
from math import sqrt
from PIL import Image, ImageDraw
from scipy.ndimage import label, find_objects

img = cv2.imread('shapes.png')

def imshow(img):
    cv2.imshow("deneme", img)
    cv2.waitKey()

def RGB2GRAY(img):
    r, g, b = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

    return gray
def threshold(img, thresh=100):
    image=img
    image[image > thresh] = 255
    image[image <= thresh] = 0
    return image


def harrisCornerDetector(img):
    float_img = img.astype(np.float64)
    hx = np.array([[1, 0, -1],
                   [2, 0, -2],
                   [1, 0, -1]],
                  dtype="int32")
    hy = np.array([[1, 2, 1],
                   [0, 0, 0],
                   [-1, -2, -1]],
                  dtype="int32")
    GAUSS = np.array((
        [1 / 16, 2 / 16, 1 / 16],
        [2 / 16, 4 / 16, 2 / 16],
        [1 / 16, 2 / 16, 1 / 16]), dtype="float64")

    sobel_x = signal.convolve2d(float_img, hx, mode="same")
    sobel_y = signal.convolve2d(float_img, hy, mode="same")

    Ix2 = np.square(sobel_x)
    Iy2 = np.square(sobel_y)
    Ixy = sobel_x * sobel_y

    g_x2 = signal.convolve2d(Ix2, GAUSS, mode="same")
    g_y2 = signal.convolve2d(Iy2, GAUSS, mode="same")
    g_xy = signal.convolve2d(Ixy, GAUSS, mode="same")

    threshold=0.4
    harris = g_x2 * g_y2 - np.square(g_xy) - 0.06 * np.square(g_x2 + g_y2)  # r(harris) = det - k*(trace**2)
    cv2.normalize(harris, harris, 0, 1, cv2.NORM_MINMAX)

    loc = np.where(harris >= threshold)
    corners=np.zeros_like(img)
    for pt in zip(*loc[::-1]):
        corners[pt[1],pt[0]]=1
    return corners

def edgeDetection(img):
    h=np.array([[0,-1,0],[-1,4,-1],[0,-1,0]],dtype="float")
    float_img = img.astype(np.float64)
    edges=signal.convolve2d(float_img, h)
    labeled_array, num_features = label(edges)
    contours = find_objects(labeled_array)
    imshow(edges)
    # Group contours based on proximity
    grouped_contours = []
    min_distance = 30  # Minimum distance to consider contours as part of the same group

    for idx, contour in enumerate(contours):
        # Calculate the center of the contour bounding box
        center_x = int((contour[1].start +contour[0].start) / 2)
        center_y = int((contour[1].stop +contour[0].stop) / 2)

        # Check if this contour belongs to any existing group
        found_group = False
        for group_idx, group in enumerate(grouped_contours):
            group_center = np.mean(group, axis=0)
            distance = np.sqrt((center_x - group_center[0]) ** 2 + (center_y - group_center[1]) ** 2)

            if distance < min_distance:
                grouped_contours[group_idx].append((center_x, center_y))
                found_group = True
                break

        # If contour doesn't belong to any existing group, create a new group
        if not found_group:
            grouped_contours.append([(center_x, center_y)])


    return grouped_contours




grayImg=RGB2GRAY(img)
thresholdImg=threshold(grayImg)
contours=edgeDetection(thresholdImg)
corners=harrisCornerDetector(thresholdImg)
print(contours)