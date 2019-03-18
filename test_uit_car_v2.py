# numpy and scipy
import numpy as np
# OpenCV
import cv2
#matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
#user module
from fillter import get_processed_img
from nhan_dien_duong_line import find_2_first_points, find_start_point, find_line_2
from algorithm import quickSort, do_lech_line , remove_X

if __name__ == '__main__':
	img=cv2.imread('/home/chaa/UIT_Car2019/git_res/UIT_CAR/fx_UIT_Car_2.png')

	img = cv2.resize(img,(320,240))
	"""plt.imshow(img)
	plt.title('raw')
	plt.xticks([])
	plt.yticks([])"""

	#lay cac anh da duoc xu li (dang binary)
	res_binary,roi_binary,eyeBird_binary,_=get_processed_img(img)

	img_heigh = eyeBird_binary.shape[0]
	img_width = eyeBird_binary.shape[1]

	half_bottom_histogram = np.sum(eyeBird_binary[135:,:], axis=0)
	
	leftPoint, rightPoint = find_2_first_points (half_bottom_histogram, range_search=256, distance_2Points=30, length_arr=320, windowLength_line=8, windowLength_empty=30, step=2, threshold_empty=3, threshold_line=20)
	startLeft = None
	startRight = None
	if (leftPoint is not None):
		startLeft = find_start_point (eyeBird_binary, left_or_right=0, startX=leftPoint, bottonY=240, topY=135, heigh=15, threshold_line=13, windowLength_line=8, threshold_empty=5, windowLength_empty=20)
	if (rightPoint is not None):
		startRight = find_start_point (eyeBird_binary, left_or_right=1, startX=rightPoint, bottonY=240, topY=135, heigh=15, threshold_line=13, windowLength_line=8, threshold_empty=5, windowLength_empty=20)
	
	eyeBird_binary_img=np.dstack((eyeBird_binary, eyeBird_binary, eyeBird_binary))*255

	pointsRight=None
	
	if startRight is not None:
		pointsRight=np.array([[startRight[0],startRight[1]]])
		pointsRightUp=find_line_2(eyeBird_binary, left_or_right=1, up_or_down=0, startPos=startRight, heigh=10, rangeSearch=30, step=2, threshold_line=15, windowLength_line=10, threshold_empty=30, windowLength_empty=70)
		if pointsRightUp is not None:
			pointsRight=np.append(pointsRight, pointsRightUp, axis=0)
		pointsRightDown=find_line_2(eyeBird_binary, left_or_right=1, up_or_down=1, startPos=startRight, heigh=10, rangeSearch=30, step=2, threshold_line=15, windowLength_line=10, threshold_empty=30, windowLength_empty=70)
		if pointsRightDown is not None:
			pointsRight=np.append(pointsRightDown, pointsRight, axis=0)
		np.arange(1, 5, dtype=np.int16)

	if pointsRight is not None:
		quickSort(pointsRight, 0, pointsRight.shape[0]-1)
		#loc nhieu cho line phai o day
		pointsRight=remove_X(pointsRight, 1)
		for point in pointsRight:
			cv2.circle(eyeBird_binary_img,(point[0],point[1]), 3, (0,255,0), -1)
	

	pointsLeft=None

	if startLeft is not None:
		pointsLeft=np.array([[startLeft[0],startLeft[1]]])
		pointsLeftUp=find_line_2(eyeBird_binary, left_or_right=0, up_or_down=0, startPos=startLeft, heigh=10, rangeSearch=30, step=2, threshold_line=15, windowLength_line=10, threshold_empty=30, windowLength_empty=70)
		if pointsLeftUp is not None:
			pointsLeft=np.append(pointsLeft, pointsLeftUp, axis=0)
		pointsLeftDown=find_line_2(eyeBird_binary, left_or_right=0, up_or_down=1, startPos=startLeft, heigh=10, rangeSearch=30, step=2, threshold_line=15, windowLength_line=10, threshold_empty=30, windowLength_empty=70)
		if pointsLeftDown is not None:
			pointsLeft=np.append(pointsLeftDown, pointsLeft, axis=0)

	if pointsLeft is not None:
		quickSort(pointsLeft, 0, pointsLeft.shape[0]-1)
		#loc nhieu cho line trai o day
		pointsLeft=remove_X(pointsLeft, 0)
		for point in pointsLeft:
			cv2.circle(eyeBird_binary_img,(point[0],point[1]), 3, (255,0,0), -1)
	""" sub_histogram = np.sum(eyeBird_binary[int(img_heigh/16*10):int(img_heigh/16*11),:], axis=0)

	left_line, nLeft = find_line (eyeBird_binary=eyeBird_binary,nWindows=16,first_point=leftPoint, 
					left_or_right=0, bottom_or_top=0)

	right_line, nRight = find_line (eyeBird_binary=eyeBird_binary,nWindows=16,first_point=rightPoint, 
					left_or_right=1, bottom_or_top=0) """

	#phan nay cho hien thi anh ra, 1*255
	binary_img=np.dstack((res_binary, res_binary, res_binary))*255

	roi_binary_img=np.dstack((roi_binary, roi_binary, roi_binary))*255

	#show anh
	""" plt.imshow(binary_img)
	plt.title('binary')
	plt.xticks([])
	plt.yticks([])

	plt.imshow(roi_binary_img)
	plt.title('roi')
	plt.xticks([])
	plt.yticks([]) """

	plt.imshow(eyeBird_binary_img.astype(int))
	#plt.imshow(eyeBird_binary_img.astype(int))
	plt.title('eyeBird')
	plt.show()

	pass
