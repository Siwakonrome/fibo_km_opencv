import pyrealsense2 as rs
import cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw
import math
from decimal import Decimal, ROUND_HALF_UP
from scipy.spatial.transform import Rotation as R
import os



def rotation_matrix_to_quaternion(rotation_matrix):
    rotation = R.from_matrix(rotation_matrix)
    return rotation.as_quat()

center_coordinates_array = [] # [(x1, y1), (x2, y2), (x3, y3)]
theta = 0
font = cv2.FONT_HERSHEY_SIMPLEX
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
pipeline = rs.pipeline()
profile = pipeline.start(config)
align_to = rs.stream.color
align = rs.align(align_to)
intr = profile.get_stream(rs.stream.color).as_video_stream_profile().get_intrinsics()
this_location = os.path.dirname(os.path.abspath(__file__))
img = cv2.imread("{path}/image/test.jpg".format(path=this_location), cv2.IMREAD_GRAYSCALE)  
sift = cv2.SIFT_create() 
kp_image, desc_image = sift.detectAndCompute(img, None)
index_params = dict(algorithm=0, trees=5)
search_params = dict()
flann = cv2.FlannBasedMatcher(index_params, search_params)

while True:
    frames = pipeline.wait_for_frames()
    aligned_frames = align.process(frames)
    color_frame = aligned_frames.get_color_frame()
    depth_frame = aligned_frames.get_depth_frame()
    if not depth_frame or not color_frame:
        continue
    frames_color_image = np.asanyarray(color_frame.get_data())
    grayframe = cv2.cvtColor(frames_color_image, cv2.COLOR_BGR2GRAY)  
    kp_grayframe, desc_grayframe = sift.detectAndCompute(grayframe, None)
    matches = flann.knnMatch(desc_image, desc_grayframe, k=2)
    good_points = []
    for m, n in matches:
        if m.distance < 0.6 * n.distance:
            good_points.append(m)
    if len(good_points) > 10:
        try:
            query_pts = np.float32([kp_image[m.queryIdx].pt for m in good_points]).reshape(-1, 1, 2)
            train_pts = np.float32([kp_grayframe[m.trainIdx].pt for m in good_points]).reshape(-1, 1, 2)
            matrix, mask = cv2.findHomography(query_pts, train_pts, cv2.RANSAC, 5.0)
            matches_mask = mask.ravel().tolist()
            h, w = img.shape
            pts = np.float32([[0, 0], [0, h], [w, h], [w, 0]]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, matrix)
            quat = rotation_matrix_to_quaternion(matrix)
            M = cv2.moments(dst)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            homography = cv2.polylines(frames_color_image, [np.int32(dst)], True, (255, 0, 0), 3)
            homography = cv2.circle(homography, (cX, cY), 5, (0, 0, 255), -1)
            dist = depth_frame.get_distance(cX, cY)*1000 
            Xtemp = dist*(cX -intr.ppx)/intr.fx
            Ytemp = dist*(cY -intr.ppy)/intr.fy
            Ztemp = dist
            Xtarget = Xtemp - 13 # 13 is RGB camera module offset from the center of the realsense
            Ytarget = -(Ztemp*math.sin(theta) + Ytemp*math.cos(theta))
            Ztarget = Ztemp*math.cos(theta) + Ytemp*math.sin(theta)
            print("x: ",Xtarget)
            print("y: ",Ytarget)
            print("z: ",Ztarget)
            print("rx: ", quat[0])
            print("ry: ", quat[1])
            print("rz: ", quat[2])
            print("w: ", quat[3])
            print("_________________________________________________________________________________")
            cv2.imshow("Homography", homography)
        except:
            cv2.imshow("Homography", frames_color_image)
    else:
        cv2.imshow("Homography", frames_color_image)
    key = cv2.waitKey(1)
    if key == 27:
        break