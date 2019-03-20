#cac ham find first point la tim diem bat dau
#cac ham detect line => lay ra toan bo cac toa do cua 2 lines
#ham find point in line => tim ra toa do cua line trong 1 histogram
#ham find line => liet ke ra cac cap toa do line co the co trong 1 khung histogram
#ham fill points => co gang lap day cac lo trong trong line



import numpy as np
import cv2
#import matplotlib.pyplot as plt
#import matplotlib.image as mpimg
from fillter import get_processed_img
import time
import math

#co gang lap day cac lo trong:
#dua vao diem dau va diem cuoi
def fill_points(points,distance_2Points=2):
	first_point_flag=False
	first_point=-1
	pos_first_point=-1
	conti=False
	for i in range(points.shape[0]):

		if (points[i][0] != -1) and (first_point_flag==False):
			first_point_flag = True
			pos_first_point = i
			first_point = points[i][0]
		if (points[i][0] != -1) and first_point_flag:
			if pos_first_point == i:
				continue
			for iPoint in range(distance_2Points):
				if (i+iPoint) >= points.shape[0]:
					conti = True
					break
				if (points[i+iPoint][0] == -1):
					first_point_flag=True
					pos_first_point = i
					first_point = points[i][0]
					continue

			if conti:
				conti=False
				continue

			if (i-pos_first_point) == 0:
				first_point_flag=False
				continue

			distance = (points[i][0] - first_point) / (i-pos_first_point)
			
			for j in range(pos_first_point+1, i):
				points[j][0] = points[j-1][0] + distance
			first_point_flag=False
			
#tim diem dau tien de bat dau tim line
#arr la histogram
#startPos la diem bat dau tim
#endPos la gioi han tim kiem
#left_or_right:
  #0 -> tim line trai
  #1 -> tim line phai
#step cang cao toc do cang nhanh -> chinh xac giam

def find_1_first_point (arr, startPos, endPos, left_or_right, windowLength_line=7, windowLength_empty=20, step=2, threshold_empty=15, threshold_line=50):
	#ben phai vi tri lan luot la:
	# ....00000012321....
	if left_or_right == 1: #nhan dien ben phai		
		for iPos in range (0,endPos-startPos,step):
			#diem bat dau
			#tim phan khong co line truoc
			if (startPos+iPos+windowLength_empty-1) >= endPos:
				#vuot qua gioi han -> thoat luon
				return None,None
			sum_window_empty = np.sum(arr[startPos+iPos:startPos+iPos+windowLength_empty])
			#tim phan co line
			sum_wimdow_line=0
			if (startPos+iPos+windowLength_empty+windowLength_line-1 >= endPos):
				sum_wimdow_line=np.sum(arr[startPos+iPos+windowLength_empty:endPos])
				if sum_wimdow_line < threshold_line:
					#cham bien nhung khong tim thay line => thoat luon
					return None,None
			else:
				sum_wimdow_line=np.sum(arr[startPos+iPos+windowLength_empty:startPos+iPos+windowLength_empty+windowLength_line])
			
			if (sum_window_empty <= threshold_empty) and (sum_wimdow_line >= threshold_line):
				return (startPos+iPos+windowLength_empty-1) + int(windowLength_line/2), sum_wimdow_line
	
	#ben trai vi tri lan luot la:
	# ....12321000000....
	if left_or_right == 0: #nhan dien ben trai
		for iPos in range (0,endPos-startPos,step):
			#diem bat dau
			#tim phan khong co line truoc
			if (startPos+iPos+windowLength_line+windowLength_empty-1) >= endPos:
				#vuot qua gioi han -> thoat luon
				return None,None
			sum_window_empty = np.sum(arr[startPos+iPos+windowLength_line : startPos+iPos+windowLength_empty+windowLength_line])
			#tim phan co line
			sum_wimdow_line=0
			if (startPos+iPos+windowLength_line-1 >= endPos):
				sum_wimdow_line=np.sum(arr[startPos+iPos:endPos])
				if sum_wimdow_line < threshold_line:
					#cham bien nhung khong tim thay line => thoat luon
					return None,None
			else:
				sum_wimdow_line=np.sum(arr[startPos+iPos:startPos+iPos+windowLength_line])
			
			if (sum_window_empty <= threshold_empty) and (sum_wimdow_line >= threshold_line):
				return (startPos+iPos) + int(windowLength_line/2), sum_wimdow_line
	
	return None,None

#tim 2 diem dau tien de bat dau tim line
#arr la histogram
#step cang cao toc do cang nhanh -> chinh xac giam
def find_2_first_points (arr, range_search=256, distance_2Points=50, length_arr=320, windowLength_line=7, windowLength_empty=30, step=2, threshold_empty=15, threshold_line=50):
	left_point=right_point=-1
	for iPos in range (0,range_search,step): #chi tim trong pham vi 4/5 khung anh
		
		if(left_point==-1 and right_point==-1): #chua co point nao bi phat hien
			if(length_arr-iPos*2 < distance_2Points): #2 diem qua gan nhau
				if(left_point!=-1 and right_point!=-1):
					return left_point,right_point
				elif (left_point!=-1):
					return left_point,None
				elif (right_point!=-1):
					return None,right_point
				else:
					return None,None
		else:
			distance=0
			x1=0
			x2 = 0
			if (left_point!=-1): #chi co left point duoc phat hien
				x1=left_point
			else:
				x1=iPos
			if (right_point!=-1): #chi co right point duoc phat hien
				x2=right_point
			else:
				x2=length_arr-iPos-1
			distance=x2-x1
			if(distance<distance_2Points):
				if(left_point!=-1 and right_point!=-1):
					return left_point,right_point
				elif (left_point!=-1):
					return left_point,None
				elif (right_point!=-1):
					return None,right_point
				else:
					return None,None

		if (iPos+windowLength_line+windowLength_empty-1) > range_search: #vuot qua gioi han
			if(left_point!=-1 and right_point!=-1):
				return left_point,right_point
			elif (left_point!=-1):
				return left_point,None
			elif (right_point!=-1):
				return None,right_point
			else:
				return None,None
				
		#line trai
		if(left_point==-1):
			#tim phan khong line
			sum_window_empty_left = np.sum(arr[iPos+windowLength_line : iPos+windowLength_empty+windowLength_line+1])
			#tim phan co line
			if(sum_window_empty_left<=threshold_empty): #kiem tra phan khong line truoc
				sum_wimdow_line=np.sum(arr[iPos:iPos+windowLength_line+1])
				if(sum_wimdow_line>=threshold_line):
					left_point=int(windowLength_line/2) + iPos
		#line phai
		if(right_point==-1):
			#tim phan khong line
			sum_window_empty_right = np.sum(arr[length_arr-iPos-windowLength_line-windowLength_empty-1 : length_arr-iPos-windowLength_line])
			#tim phan co line
			if(sum_window_empty_right<=threshold_empty): #kiem tra phan khong line truoc
				sum_wimdow_line=np.sum(arr[length_arr-iPos-windowLength_line-1:length_arr-iPos])
				if(sum_wimdow_line>=threshold_line):
					right_point=length_arr-1-iPos-int(windowLength_line/2)
		#co du left va right point
		if(left_point!=-1 and right_point!=-1):
			return left_point,right_point
	return None,None


def find_point_in_line (arr,start_point, left_or_right, step=1, distance_2Points=10, threshold_line=13, windowLength_line=7, threshold_empty=5, windowLength_empty=20):
	width = arr.shape[0]
	#line trai ...1230000...
	if left_or_right == 0: #line trai
		for iPos in range(0,distance_2Points+1,step):
			#side ben phai line==================================================

			#tinh empty
			#tranh vuot qua bien ben phai
			if (start_point+iPos+int(windowLength_line/2)+windowLength_empty) < width:
				#tong diem bat dau tinh empty => diem bat dau + windowLength_empty 
				sum_window_empty=np.sum(arr[start_point+iPos+int(windowLength_line/2)+1 : start_point+iPos+int(windowLength_line/2)+1+windowLength_empty])

				#tinh diem line
				sum_wimdow_line=0
				#vuot qua bien ben trai
				if (start_point+iPos-int(windowLength_line/2)) < 0:
					sum_wimdow_line=np.sum(arr[0 : start_point+iPos+int(windowLength_line/2)+1])
				else:
					sum_wimdow_line=np.sum(arr[start_point+iPos-int(windowLength_line/2) : start_point+iPos+int(windowLength_line/2)+1])
				if (sum_window_empty <= threshold_empty) and (sum_wimdow_line >= threshold_line):
					return start_point+iPos

			#side ben trai line===================================================

			#tinh empty
			#tranh vuot qua bien ben phai
			if (start_point-iPos+int(windowLength_line/2)+windowLength_empty) < width:
				#tong diem bat dau tinh empty => diem bat dau + windowLength_empty 
				sum_window_empty=np.sum(arr[start_point-iPos+int(windowLength_line/2)+1 : start_point-iPos+int(windowLength_line/2)+1+windowLength_empty])

				#tinh diem line
				#vuot qua bien ben trai
				sum_wimdow_line=0
				if (start_point-iPos-int(windowLength_line/2)) < 0:
					sum_wimdow_line=np.sum(arr[0 : start_point-iPos+int(windowLength_line/2)+1])
				else:
					sum_wimdow_line=np.sum(arr[start_point-iPos-int(windowLength_line/2) : start_point-iPos+int(windowLength_line/2)+1])
				if (sum_window_empty <= threshold_empty) and (sum_wimdow_line >= threshold_line):
					return start_point-iPos
	#line phai ...0000123...
	if left_or_right == 1: #line phai
		for iPos in range(0,distance_2Points+1,step):
			#side ben phai line==================================================

			#tinh empty
			start_pos_empty = start_point+iPos-int(windowLength_line/2)-windowLength_empty
			end_pos_empty = start_pos_empty+windowLength_empty
			#tranh vuot qua bien ben trai
			if (start_pos_empty < 0):
				start_pos_empty=0
			
			sum_window_empty=0
			#tranh vuot bien phai
			if (end_pos_empty <= width) and (end_pos_empty>=0):
				sum_window_empty = np.sum(arr[start_pos_empty:end_pos_empty])
				#neu thoa dieu kien khong phai line
				if (sum_window_empty <= threshold_empty):
					start_pos_line=end_pos_empty
					end_pos_line = start_pos_line + windowLength_line
					if end_pos_line > width:
						end_pos_line = width
					if (end_pos_line > start_pos_line):
						sum_wimdow_line = np.sum(arr[start_pos_line:end_pos_line])
						if (sum_wimdow_line >= threshold_line):
							return int((end_pos_line - start_pos_line)/2+start_pos_line)

			#side ben trai line==================================================

			#tinh empty
			start_pos_empty = start_point-iPos-int(windowLength_line/2)-windowLength_empty
			end_pos_empty = start_pos_empty+windowLength_empty
			#tranh vuot qua bien ben trai
			if (start_pos_empty < 0):
				start_pos_empty=0
			
			sum_window_empty=0
			#tranh vuot bien phai
			if (end_pos_empty <= width) and (end_pos_empty>=0):
				sum_window_empty = np.sum(arr[start_pos_empty:end_pos_empty])
				#neu thoa dieu kien khong phai line
				if (sum_window_empty <= threshold_empty):
					start_pos_line=end_pos_empty
					end_pos_line = start_pos_line + windowLength_line
					if end_pos_line > width:
						end_pos_line = width
					if (end_pos_line > start_pos_line):
						sum_wimdow_line = np.sum(arr[start_pos_line:end_pos_line])
						if (sum_wimdow_line >= threshold_line):
							return int((end_pos_line - start_pos_line)/2+start_pos_line)
					
	#deo' tim ra diem nao thoa
	return -1

#tim cac vi tri co the xuat hien cua duong line

def find_line (eyeBird_binary,nWindows,first_point, left_or_right, bottom_or_top):
	img_heigh = eyeBird_binary.shape[0]
	img_width = eyeBird_binary.shape[1]
	#chieu cao cua window
	window_heigh = int(img_heigh/nWindows)

	pre_line = first_point
	pre_line_pos = 1 #dung de gia tang pham vi tim kiem

	points_line=None
	nPoints_line=0

	for iWindow in range(1,nWindows+1):
		#neu tim tu bottom len
		sub_his=None
		if bottom_or_top == 0:
			sub_his = np.sum(eyeBird_binary[img_heigh - iWindow*window_heigh:img_heigh - (iWindow - 1)*window_heigh,:], axis=0)
		#neu tim tu top xuong
		if bottom_or_top == 1:
			sub_his = np.sum(eyeBird_binary[(iWindow-1)*window_heigh:iWindow*window_heigh,:], axis=0)
		x=find_point_in_line (arr=sub_his,start_point=pre_line, left_or_right=left_or_right, 
								step=2, distance_2Points=30+(iWindow-pre_line_pos)*2, 
								threshold_line=8, windowLength_line=7, 
								threshold_empty=3, windowLength_empty=20)
		if points_line is None:
			if bottom_or_top == 0:
				y = img_heigh - window_heigh*iWindow
			if bottom_or_top == 1:
				y = window_heigh*iWindow
			points_line=np.array([[x,y]])
		else:
			if bottom_or_top == 0:
				y = img_heigh - window_heigh*iWindow
			if bottom_or_top == 1:
				y = window_heigh*iWindow
			coo = np.array([[x,y]])
			points_line = np.append(points_line,coo,axis=0) #them vao left line
		#cap nhat vi tri line moi
		if (x!=-1): #neu tim thay vi tri moi thi -> cap nhat
			pre_line = x
			pre_line_pos = iWindow
			nPoints_line += 1
	if (bottom_or_top==0):
		return points_line,nPoints_line
	if (bottom_or_top==1):
		#temp = points_line[::-1]
		return points_line[::-1],nPoints_line

#case = 0: ben trai truoc
#case = 1: ben phai truoc

#return left_line, right_line
#(None,None),(None,right_line),(left_line,None): neu khong nhan dien duoc diem dau

def get_line (eyeBird_binary,case,threshold_num_point=5):
	img_heigh = eyeBird_binary.shape[0]
	img_width = eyeBird_binary.shape[1]
	if case == 0:
		#lay tong cua nua phan duoi
		half_bottom_histogram = np.sum(eyeBird_binary[int(img_heigh/2):img_heigh,:], axis=0)
		#tim vi tri dau tien line ben trai
		#nua duoi ben trai -> 1/2
		right_x,_=find_first_point (arr=half_bottom_histogram, 
				startPos=160, 
				endPos=int(img_width), left_or_right=1, 
				windowLength_line=7, windowLength_empty=20, step=2, 
				threshold_empty=15, threshold_line=50)
		if right_x is not None:
			#nua duoi ke tu line trai qua phai -> cuoi
			left_x,_=find_first_point (arr=half_bottom_histogram, 
					startPos=50, 
					endPos=right_x, left_or_right=1, 
					windowLength_line=7, windowLength_empty=20, step=2, 
					threshold_empty=15, threshold_line=50)
			#tim thay diem bat dau line phai
			if left_x is not None:
				#do line phai tu duoi len
				right_line, nRight = find_line (eyeBird_binary=eyeBird_binary,nWindows=16,first_point=right_x, 
							left_or_right=1, bottom_or_top=0)
				#do line trai tu duoi len
				left_line, nLeft = find_line (eyeBird_binary=eyeBird_binary,nWindows=16,first_point=left_x, 
							left_or_right=0, bottom_or_top=0)
				#kiem tra xem so diem do duoc co thoa threshold_num_point hay ko
				if nRight >= threshold_num_point and nLeft >= threshold_num_point:
					fill_points(left_line)
					fill_points(right_line)
					return left_line,right_line
				if nRight >= threshold_num_point:
					#fill_points(right_line)
					return None,right_line
				if nLeft >= threshold_num_point:
					#fill_points(left_line)
					return left_line,None

	if case == 1:
		#lay tong cua nua phan duoi
		half_bottom_histogram = np.sum(eyeBird_binary[int(img_heigh/2):img_heigh,:], axis=0)
		#tim vi tri dau tien line ben trai
		#nua duoi ben trai -> 1/2
		right_x,_=find_first_point (arr=half_bottom_histogram, 
				startPos=int(img_width/2)-20, 
				endPos=img_width, left_or_right=1, 
				windowLength_line=7, windowLength_empty=20, step=2, 
				threshold_empty=15, threshold_line=50)
		if right_x is not None:
			#nua duoi ke tu line trai qua phai -> cuoi
			left_x,_=find_first_point (arr=half_bottom_histogram, 
					startPos=0, 
					endPos=right_x, left_or_right=0, 
					windowLength_line=7, windowLength_empty=20, step=2, 
					threshold_empty=15, threshold_line=50)
			#tim thay diem bat dau line phai
			if left_x is not None:
				#do line phai tu duoi len
				right_line, nRight = find_line (eyeBird_binary=eyeBird_binary,nWindows=16,first_point=right_x, 
							left_or_right=1, bottom_or_top=0)
				#do line trai tu duoi len
				left_line, nLeft = find_line (eyeBird_binary=eyeBird_binary,nWindows=16,first_point=left_x, 
							left_or_right=0, bottom_or_top=0)
				#kiem tra xem so diem do duoc co thoa threshold_num_point hay ko
				if nRight >= threshold_num_point and nLeft >= threshold_num_point:
					fill_points(left_line)
					fill_points(right_line)
					return left_line,right_line
				if nRight >= threshold_num_point:
					#fill_points(right_line)
					return None,right_line
				if nLeft >= threshold_num_point:
					#fill_points(left_line)
					return left_line,None

	#khong thoa bat cu dieu gi
	return None,None

def get_2_lines(eyeBird_binary,case,threshold_num_point=5):
	img_heigh = eyeBird_binary.shape[0]
	img_width = eyeBird_binary.shape[1]

	#lay tong cua nua phan duoi
	half_bottom_histogram = np.sum(eyeBird_binary[int(img_heigh/2):img_heigh,:], axis=0)

	left_x, right_x = find_2_first_points(half_bottom_histogram, range_search=256, distance_2Points=50, length_arr=img_width, windowLength_line=7, windowLength_empty=30, step=2, threshold_empty=15, threshold_line=50)

	left_line=right_line=None

	if(left_x is not None):
		#do line trai tu duoi len
		left_line, nLeft = find_line (eyeBird_binary=eyeBird_binary,nWindows=16,first_point=left_x, 
					left_or_right=0, bottom_or_top=0)
	if(right_x is not None):
		#do line phai tu duoi len
		right_line, nRight = find_line (eyeBird_binary=eyeBird_binary,nWindows=16,first_point=right_x, 
					left_or_right=1, bottom_or_top=0)
		
	#kiem tra xem so diem do duoc co thoa threshold_num_point hay ko
	if nRight >= threshold_num_point and nLeft >= threshold_num_point:
		#fill_points(left_line)
		#fill_points(right_line)
		return left_line,right_line
	if nRight >= threshold_num_point:
		#fill_points(right_line)
		return None,right_line
	if nLeft >= threshold_num_point:
		#fill_points(left_line)
		return left_line,None

#tra ve 1 mang gom left line va right line
#
# left = ([[xleft,yleft],[x2,y2],...])
# right = ([[xright,yright],[x2,y2],...]), .... nWindows

def detect_line(eyeBird_binary,threshold_num_point=8):

	line_detect = np.dstack((eyeBird_binary, eyeBird_binary, eyeBird_binary))*255

	left_line, right_line = get_line (eyeBird_binary,case=0,threshold_num_point=threshold_num_point)

	if (left_line is not None) and (right_line is not None):
		for point_right, point_left in zip(right_line,left_line):
			if (point_right[0]!=-1):
				cv2.circle(line_detect,(point_right[0],point_right[1]), 5, (0,255,0), -1)
			if (point_left[0]!=-1):
				cv2.circle(line_detect,(point_left[0],point_left[1]), 5, (0,0,255), -1)

	else:
	#if left_line is None or right_line is None:
		left_line, right_line = get_line (eyeBird_binary,case=1,threshold_num_point=threshold_num_point)
		if (left_line is not None) and (right_line is not None):
			for point_right, point_left in zip(right_line,left_line):
				if (point_right[0]!=-1):
					cv2.circle(line_detect,(point_right[0],point_right[1]), 5, (0,255,0), -1)
				if (point_left[0]!=-1):
					cv2.circle(line_detect,(point_left[0],point_left[1]), 5, (0,0,255), -1)
	
	if left_line is None or right_line is None:
		return None,None,line_detect
	fill_line_left=None
	fill_line_right=None
	for i in range(left_line.shape[0]):
		if (left_line[i][0] != -1):
			if (fill_line_left is not None):
				temp=np.array([[left_line[i][0],left_line[i][1]]])
				fill_line_left=np.append(fill_line_left,temp,axis=0)
			else:
				fill_line_left=np.array([[left_line[i][0],left_line[i][1]]])
		if (right_line[i][0] != -1):
			if (fill_line_right is not None):
				temp=np.array([[right_line[i][0],right_line[i][1]]])
				fill_line_right=np.append(fill_line_right,temp,axis=0)
			else:
				fill_line_right=np.array([[right_line[i][0],right_line[i][1]]])

	cv2.imshow('line_detect',line_detect)
	return fill_line_left,fill_line_right,line_detect


	
def find_start_point (eyeBird_binary, left_or_right, startX, bottonY=240, topY=135, heigh=15, threshold_line=13, windowLength_line=8, threshold_empty=5, windowLength_empty=20):
	#=================================================line phai========================================================
	if (left_or_right==1):
		for iWindow in range(int((bottonY-topY)/heigh)):
			#sub histogram
			sub_his = np.sum(eyeBird_binary[topY + iWindow*heigh:topY + (iWindow+1)*heigh,:], axis=0)
			#empty tracking
			sum_window_empty=np.sum(sub_his[startX - int(windowLength_line/2) - windowLength_empty: startX - int(windowLength_line/2)])
			if (sum_window_empty <= threshold_empty) :
				sum_window_line=np.sum(sub_his[startX - int(windowLength_line/2) : startX + int(windowLength_line/2) + 1])
				if (sum_window_line>=threshold_line):
					return np.array([startX,topY+iWindow*heigh])
	if (left_or_right==0):
		for iWindow in range(int((bottonY-topY)/heigh)):
			#sub histogram
			sub_his = np.sum(eyeBird_binary[topY + iWindow*heigh: topY + (iWindow+1)*heigh,:], axis=0)
			#empty tracking
			sum_window_empty=np.sum(sub_his[startX + int(windowLength_line/2) + 1: startX + int(windowLength_line/2) + 1 + windowLength_empty])
			if (sum_window_empty <= threshold_empty) :
				sum_window_line=np.sum(sub_his[startX - int(windowLength_line/2) : startX + int(windowLength_line/2) + 1])
				if (sum_window_line>=threshold_line):
					return np.array([startX,topY+iWindow*heigh])
	return None

def find_line_2(eyeBird_binary, left_or_right, up_or_down, startPos, heigh=15, rangeSearch=15, step=2, threshold_line=13, windowLength_line=8, threshold_empty=5, windowLength_empty=20):
	points_line=None
	img_heigh = eyeBird_binary.shape[0]
	img_width = eyeBird_binary.shape[1]
	pre_Y=startPos[1]
	pre_X=startPos[0]
	if (left_or_right==1):
		if (up_or_down==0):
			while True:
				#calculate each square
				#botton left square
				left_edge=pre_X-int(windowLength_line/2)-windowLength_line
				if(left_edge<0):
					left_edge=0

				right_edge=pre_X-int(windowLength_line/2)+1
				if(right_edge>img_width):
					right_edge=img_width

				top_edge=pre_Y
				if(top_edge<0):
					top_edge=0

				bot_edge=pre_Y+heigh+1
				if(bot_edge>img_heigh):
					bot_edge=img_heigh

				sum_square=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
				if(sum_square>=threshold_line):
					#check empty top
					bot_edge=top_edge
					top_edge=bot_edge-windowLength_empty
					if(top_edge<0):
						top_edge=0
					sum_window_empty_top=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					#check empty left
					top_edge=bot_edge
					bot_edge=pre_Y+heigh+1
					if(bot_edge>img_heigh):
						bot_edge=img_heigh
					right_edge=left_edge+1
					if(right_edge>img_width):
						right_edge=img_width
					left_edge=left_edge-windowLength_empty
					if(left_edge<0):
						left_edge=0
					sum_window_empty_left=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					if(sum_window_empty_top<=threshold_empty or sum_window_empty_left<=threshold_empty):
						x=right_edge-1+int(windowLength_line/2)
						y=top_edge
						if points_line is not None:
							#phong truong hop lap lai
							if(points_line.shape[0]>=2):
								distanceX=abs(x - points_line[points_line.shape[0]-2][0])
								distanceY=abs(y - points_line[points_line.shape[0]-2][1])
								if(distanceX >= int(windowLength_line/2) or distanceY >= int(heigh/2)): #khong bi trung diem phia truoc
									coo=np.array([[x,y]])
									points_line=np.append(points_line,coo,axis=0)
									#update value and continue
									pre_X=x
									pre_Y=y
									continue
							else:
								coo=np.array([[x,y]])
								points_line=np.append(points_line,coo,axis=0)
								#update value and continue
								pre_X=x
								pre_Y=y
								continue
						else:
							points_line=np.array([[x,y]])
							#update value and continue
							pre_X=x
							pre_Y=y
							continue
				#left midle square
				left_edge=pre_X-int(windowLength_line/2)-windowLength_line
				if(left_edge<0):
					left_edge=0

				right_edge=pre_X-int(windowLength_line/2)+1
				if(right_edge>img_width):
					right_edge=img_width

				top_edge=pre_Y-int(heigh/2)
				if(top_edge<0):
					top_edge=0

				bot_edge=pre_Y+int(heigh/2)+1
				if(bot_edge>img_heigh):
					bot_edge=img_heigh

				sum_square=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
				if(sum_square>=threshold_line):
					#check empty top
					bot_edge=top_edge
					top_edge=bot_edge-windowLength_empty
					if(top_edge<0):
						top_edge=0
					sum_window_empty_top=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					#check empty left
					top_edge=bot_edge
					bot_edge=pre_Y+heigh+1
					if(bot_edge>img_heigh):
						bot_edge=img_heigh
					right_edge=left_edge+1
					if(right_edge>img_width):
						right_edge=img_width
					left_edge=left_edge-windowLength_empty
					if(left_edge<0):
						left_edge=0
					sum_window_empty_left=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					if(sum_window_empty_top<=threshold_empty or sum_window_empty_left<=threshold_empty):
						x=right_edge-1+int(windowLength_line/2)
						y=top_edge
						if points_line is not None:
							#phong truong hop lap lai
							if(points_line.shape[0]>=2):
								distanceX=abs(x - points_line[points_line.shape[0]-2][0])
								distanceY=abs(y - points_line[points_line.shape[0]-2][1])
								if(distanceX >= int(windowLength_line/2) or distanceY >= int(heigh/2)): #khong bi trung diem phia truoc
									coo=np.array([[x,y]])
									points_line=np.append(points_line,coo,axis=0)
									#update value and continue
									pre_X=x
									pre_Y=y
									continue
							else:
								coo=np.array([[x,y]])
								points_line=np.append(points_line,coo,axis=0)
								#update value and continue
								pre_X=x
								pre_Y=y
								continue
						else:
							points_line=np.array([[x,y]])
							#update value and continue
							pre_X=x
							pre_Y=y
							continue
				#left top square
				left_edge=pre_X-int(windowLength_line/2)-windowLength_line
				if(left_edge<0):
					left_edge=0

				right_edge=pre_X-int(windowLength_line/2)+1
				if(right_edge>img_width):
					right_edge=img_width

				top_edge=pre_Y-heigh
				if(top_edge<0):
					top_edge=0

				bot_edge=pre_Y+1
				if(bot_edge>img_heigh):
					bot_edge=img_heigh

				sum_square=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
				if(sum_square>=threshold_line):
					#check empty top
					bot_edge=top_edge
					top_edge=bot_edge-windowLength_empty
					if(top_edge<0):
						top_edge=0
					sum_window_empty_top=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					#check empty left
					top_edge=bot_edge
					bot_edge=pre_Y+heigh+1
					if(bot_edge>img_heigh):
						bot_edge=img_heigh
					right_edge=left_edge+1
					if(right_edge>img_width):
						right_edge=img_width
					left_edge=left_edge-windowLength_empty
					if(left_edge<0):
						left_edge=0
					sum_window_empty_left=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					if(sum_window_empty_top<=threshold_empty or sum_window_empty_left<=threshold_empty):
						x=right_edge-1+int(windowLength_line/2)
						y=top_edge
						if points_line is not None:
							#phong truong hop lap lai
							if(points_line.shape[0]>=2):
								distanceX=abs(x - points_line[points_line.shape[0]-2][0])
								distanceY=abs(y - points_line[points_line.shape[0]-2][1])
								if(distanceX >= int(windowLength_line/2) or distanceY >= int(heigh/2)): #khong bi trung diem phia truoc
									coo=np.array([[x,y]])
									points_line=np.append(points_line,coo,axis=0)
									#update value and continue
									pre_X=x
									pre_Y=y
									continue
							else:
								coo=np.array([[x,y]])
								points_line=np.append(points_line,coo,axis=0)
								#update value and continue
								pre_X=x
								pre_Y=y
								continue
						else:
							points_line=np.array([[x,y]])
							#update value and continue
							pre_X=x
							pre_Y=y
							continue
				#top square
				left_edge=pre_X-int(windowLength_line/2)
				if(left_edge<0):
					left_edge=0

				right_edge=pre_X+int(windowLength_line/2)+1
				if(right_edge>img_width):
					right_edge=img_width

				top_edge=pre_Y-heigh
				if(top_edge<0):
					top_edge=0

				bot_edge=pre_Y+1
				if(bot_edge>img_heigh):
					bot_edge=img_heigh

				sum_square=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
				if(sum_square>=threshold_line):
					#check empty top
					bot_edge=top_edge
					top_edge=bot_edge-windowLength_empty
					if(top_edge<0):
						top_edge=0
					sum_window_empty_top=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					#check empty left
					top_edge=bot_edge
					bot_edge=pre_Y+heigh+1
					if(bot_edge>img_heigh):
						bot_edge=img_heigh
					right_edge=left_edge+1
					if(right_edge>img_width):
						right_edge=img_width
					left_edge=left_edge-windowLength_empty
					if(left_edge<0):
						left_edge=0
					sum_window_empty_left=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					if(sum_window_empty_top<=threshold_empty or sum_window_empty_left<=threshold_empty):
						x=right_edge-1+int(windowLength_line/2)
						y=top_edge
						if points_line is not None:
							#phong truong hop lap lai
							if(points_line.shape[0]>=2):
								distanceX=abs(x - points_line[points_line.shape[0]-2][0])
								distanceY=abs(y - points_line[points_line.shape[0]-2][1])
								if(distanceX >= int(windowLength_line/2) or distanceY >= int(heigh/2)): #khong bi trung diem phia truoc
									coo=np.array([[x,y]])
									points_line=np.append(points_line,coo,axis=0)
									#update value and continue
									pre_X=x
									pre_Y=y
									continue
							else:
								coo=np.array([[x,y]])
								points_line=np.append(points_line,coo,axis=0)
								#update value and continue
								pre_X=x
								pre_Y=y
								continue
						else:
							points_line=np.array([[x,y]])
							#update value and continue
							pre_X=x
							pre_Y=y
							continue
				#botton right square
				left_edge=pre_X+int(windowLength_line/2)
				if(left_edge<0):
					left_edge=0

				right_edge=pre_X+int(windowLength_line/2)+windowLength_line+1
				if(right_edge>img_width):
					right_edge=img_width

				top_edge=pre_Y
				if(top_edge<0):
					top_edge=0

				bot_edge=pre_Y+heigh+1
				if(bot_edge>img_heigh):
					bot_edge=img_heigh

				sum_square=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
				if(sum_square>=threshold_line):
					#check empty top
					bot_edge=top_edge
					top_edge=bot_edge-windowLength_empty
					if(top_edge<0):
						top_edge=0
					sum_window_empty_top=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					#check empty left
					top_edge=bot_edge
					bot_edge=pre_Y+heigh+1
					if(bot_edge>img_heigh):
						bot_edge=img_heigh
					right_edge=left_edge+1
					if(right_edge>img_width):
						right_edge=img_width
					left_edge=left_edge-windowLength_empty
					if(left_edge<0):
						left_edge=0
					sum_window_empty_left=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					if(sum_window_empty_top<=threshold_empty or sum_window_empty_left<=threshold_empty):
						x=right_edge-1+int(windowLength_line/2)
						y=top_edge
						if points_line is not None:
							#phong truong hop lap lai
							if(points_line.shape[0]>=2):
								distanceX=abs(x - points_line[points_line.shape[0]-2][0])
								distanceY=abs(y - points_line[points_line.shape[0]-2][1])
								if(distanceX >= int(windowLength_line/2) or distanceY >= int(heigh/2)): #khong bi trung diem phia truoc
									coo=np.array([[x,y]])
									points_line=np.append(points_line,coo,axis=0)
									#update value and continue
									pre_X=x
									pre_Y=y
									continue
							else:
								coo=np.array([[x,y]])
								points_line=np.append(points_line,coo,axis=0)
								#update value and continue
								pre_X=x
								pre_Y=y
								continue
						else:
							points_line=np.array([[x,y]])
							#update value and continue
							pre_X=x
							pre_Y=y
							continue
				#right midle square
				left_edge=pre_X+int(windowLength_line/2)
				if(left_edge<0):
					left_edge=0

				right_edge=pre_X+int(windowLength_line/2)+windowLength_line+1
				if(right_edge>img_width):
					right_edge=img_width

				top_edge=pre_Y-int(heigh/2)
				if(top_edge<0):
					top_edge=0

				bot_edge=pre_Y+int(heigh/2)+1
				if(bot_edge>img_heigh):
					bot_edge=img_heigh

				sum_square=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
				if(sum_square>=threshold_line):
					#check empty top
					bot_edge=top_edge
					top_edge=bot_edge-windowLength_empty
					if(top_edge<0):
						top_edge=0
					sum_window_empty_top=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					#check empty left
					top_edge=bot_edge
					bot_edge=pre_Y+heigh+1
					if(bot_edge>img_heigh):
						bot_edge=img_heigh
					right_edge=left_edge+1
					if(right_edge>img_width):
						right_edge=img_width
					left_edge=left_edge-windowLength_empty
					if(left_edge<0):
						left_edge=0
					sum_window_empty_left=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					if(sum_window_empty_top<=threshold_empty or sum_window_empty_left<=threshold_empty):
						x=right_edge-1+int(windowLength_line/2)
						y=top_edge
						if points_line is not None:
							#phong truong hop lap lai
							if(points_line.shape[0]>=2):
								distanceX=abs(x - points_line[points_line.shape[0]-2][0])
								distanceY=abs(y - points_line[points_line.shape[0]-2][1])
								if(distanceX >= int(windowLength_line/2) or distanceY >= int(heigh/2)): #khong bi trung diem phia truoc
									coo=np.array([[x,y]])
									points_line=np.append(points_line,coo,axis=0)
									#update value and continue
									pre_X=x
									pre_Y=y
									continue
							else:
								coo=np.array([[x,y]])
								points_line=np.append(points_line,coo,axis=0)
								#update value and continue
								pre_X=x
								pre_Y=y
								continue
						else:
							points_line=np.array([[x,y]])
							#update value and continue
							pre_X=x
							pre_Y=y
							continue
				#left top square
				left_edge=pre_X+int(windowLength_line/2)
				if(left_edge<0):
					left_edge=0

				right_edge=pre_X+int(windowLength_line/2)+windowLength_line+1
				if(right_edge>img_width):
					right_edge=img_width

				top_edge=pre_Y-heigh
				if(top_edge<0):
					top_edge=0

				bot_edge=pre_Y+1
				if(bot_edge>img_heigh):
					bot_edge=img_heigh

				sum_square=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
				if(sum_square>=threshold_line):
					#check empty top
					bot_edge=top_edge
					top_edge=bot_edge-windowLength_empty
					if(top_edge<0):
						top_edge=0
					sum_window_empty_top=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					#check empty left
					top_edge=bot_edge
					bot_edge=pre_Y+heigh+1
					if(bot_edge>img_heigh):
						bot_edge=img_heigh
					right_edge=left_edge+1
					if(right_edge>img_width):
						right_edge=img_width
					left_edge=left_edge-windowLength_empty
					if(left_edge<0):
						left_edge=0
					sum_window_empty_left=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					if(sum_window_empty_top<=threshold_empty or sum_window_empty_left<=threshold_empty):
						x=right_edge-1+int(windowLength_line/2)
						y=top_edge
						if points_line is not None:
							#phong truong hop lap lai
							if(points_line.shape[0]>=2):
								distanceX=abs(x - points_line[points_line.shape[0]-2][0])
								distanceY=abs(y - points_line[points_line.shape[0]-2][1])
								if(distanceX >= int(windowLength_line/2) or distanceY >= int(heigh/2)): #khong bi trung diem phia truoc
									coo=np.array([[x,y]])
									points_line=np.append(points_line,coo,axis=0)
									#update value and continue
									pre_X=x
									pre_Y=y
									continue
							else:
								coo=np.array([[x,y]])
								points_line=np.append(points_line,coo,axis=0)
								#update value and continue
								pre_X=x
								pre_Y=y
								continue
						else:
							points_line=np.array([[x,y]])
							#update value and continue
							pre_X=x
							pre_Y=y
							continue
				break
		if (up_or_down==1):
			while True:
				#calculate each square
				#botton left square
				left_edge=pre_X-int(windowLength_line/2)-windowLength_line
				if(left_edge<0):
					left_edge=0

				right_edge=pre_X-int(windowLength_line/2)+1
				if(right_edge>img_width):
					right_edge=img_width

				top_edge=pre_Y+heigh
				if(top_edge>img_heigh):
					top_edge=img_heigh

				bot_edge=pre_Y+heigh*2
				if(bot_edge>img_heigh):
					bot_edge=img_heigh

				sum_square=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
				if(sum_square>=threshold_line):
					#check empty top
					bot_edge=top_edge
					top_edge=bot_edge-windowLength_empty
					if(top_edge<0):
						top_edge=0
					sum_window_empty_top=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					#check empty left
					top_edge=bot_edge
					bot_edge=pre_Y+2*heigh
					if(bot_edge>img_heigh):
						bot_edge=img_heigh
					right_edge=left_edge+1
					if(right_edge>img_width):
						right_edge=img_width
					left_edge=left_edge-windowLength_empty
					if(left_edge<0):
						left_edge=0
					sum_window_empty_left=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					if(sum_window_empty_top<=threshold_empty or sum_window_empty_left<=threshold_empty):
						x=right_edge-1+int(windowLength_line/2)
						y=top_edge
						if points_line is not None:
							#phong truong hop lap lai
							if(points_line.shape[0]>=2):
								distanceX=abs(x - points_line[points_line.shape[0]-2][0])
								distanceY=abs(y - points_line[points_line.shape[0]-2][1])
								if(distanceX >= int(windowLength_line/2) or distanceY >= int(heigh/2)): #khong bi trung diem phia truoc
									coo=np.array([[x,y]])
									points_line=np.append(points_line,coo,axis=0)
									#update value and continue
									pre_X=x
									pre_Y=y
									continue
							else:
								coo=np.array([[x,y]])
								points_line=np.append(points_line,coo,axis=0)
								#update value and continue
								pre_X=x
								pre_Y=y
								continue
						else:
							points_line=np.array([[x,y]])
							#update value and continue
							pre_X=x
							pre_Y=y
							continue
				#left midle square
				left_edge=pre_X-int(windowLength_line/2)-windowLength_line
				if(left_edge<0):
					left_edge=0

				right_edge=pre_X-int(windowLength_line/2)+1
				if(right_edge>img_width):
					right_edge=img_width

				top_edge=pre_Y+int(heigh/2)
				if(top_edge>img_heigh):
					top_edge=img_heigh

				bot_edge=pre_Y+int(heigh*3/2)+1
				if(bot_edge>img_heigh):
					bot_edge=img_heigh

				sum_square=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
				if(sum_square>=threshold_line):
					#check empty top
					bot_edge=top_edge
					top_edge=bot_edge-windowLength_empty
					if(top_edge<0):
						top_edge=0
					sum_window_empty_top=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					#check empty left
					top_edge=bot_edge
					bot_edge=pre_Y+int(heigh*3/2)+1
					if(bot_edge>img_heigh):
						bot_edge=img_heigh
					right_edge=left_edge+1
					if(right_edge>img_width):
						right_edge=img_width
					left_edge=left_edge-windowLength_empty
					if(left_edge<0):
						left_edge=0
					sum_window_empty_left=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					if(sum_window_empty_top<=threshold_empty or sum_window_empty_left<=threshold_empty):
						x=right_edge-1+int(windowLength_line/2)
						y=top_edge
						if points_line is not None:
							#phong truong hop lap lai
							if(points_line.shape[0]>=2):
								distanceX=abs(x - points_line[points_line.shape[0]-2][0])
								distanceY=abs(y - points_line[points_line.shape[0]-2][1])
								if(distanceX >= int(windowLength_line/2) or distanceY >= int(heigh/2)): #khong bi trung diem phia truoc
									coo=np.array([[x,y]])
									points_line=np.append(points_line,coo,axis=0)
									#update value and continue
									pre_X=x
									pre_Y=y
									continue
							else:
								coo=np.array([[x,y]])
								points_line=np.append(points_line,coo,axis=0)
								#update value and continue
								pre_X=x
								pre_Y=y
								continue
						else:
							points_line=np.array([[x,y]])
							#update value and continue
							pre_X=x
							pre_Y=y
							continue
				#left top square
				left_edge=pre_X-int(windowLength_line/2)-windowLength_line
				if(left_edge<0):
					left_edge=0

				right_edge=pre_X-int(windowLength_line/2)+1
				if(right_edge>img_width):
					right_edge=img_width

				top_edge=pre_Y
				if(top_edge>=img_heigh):
					top_edge=img_heigh

				bot_edge=pre_Y+heigh
				if(bot_edge>img_heigh):
					bot_edge=img_heigh

				sum_square=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
				if(sum_square>=threshold_line):
					#check empty top
					bot_edge=top_edge
					top_edge=bot_edge-windowLength_empty
					if(top_edge<0):
						top_edge=0
					sum_window_empty_top=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					#check empty left
					top_edge=bot_edge
					bot_edge=pre_Y+heigh
					if(bot_edge>img_heigh):
						bot_edge=img_heigh
					right_edge=left_edge+1
					if(right_edge>img_width):
						right_edge=img_width
					left_edge=left_edge-windowLength_empty
					if(left_edge<0):
						left_edge=0
					sum_window_empty_left=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					if(sum_window_empty_top<=threshold_empty or sum_window_empty_left<=threshold_empty):
						x=right_edge-1+int(windowLength_line/2)
						y=top_edge
						if points_line is not None:
							#phong truong hop lap lai
							if(points_line.shape[0]>=2):
								distanceX=abs(x - points_line[points_line.shape[0]-2][0])
								distanceY=abs(y - points_line[points_line.shape[0]-2][1])
								if(distanceX >= int(windowLength_line/2) or distanceY >= int(heigh/2)): #khong bi trung diem phia truoc
									coo=np.array([[x,y]])
									points_line=np.append(points_line,coo,axis=0)
									#update value and continue
									pre_X=x
									pre_Y=y
									continue
							else:
								coo=np.array([[x,y]])
								points_line=np.append(points_line,coo,axis=0)
								#update value and continue
								pre_X=x
								pre_Y=y
								continue
						else:
							points_line=np.array([[x,y]])
							#update value and continue
							pre_X=x
							pre_Y=y
							continue
				#botton square
				left_edge=pre_X-int(windowLength_line/2)
				if(left_edge<0):
					left_edge=0

				right_edge=pre_X+int(windowLength_line/2)+1
				if(right_edge>img_width):
					right_edge=img_width

				top_edge=pre_Y+heigh
				if(top_edge>img_heigh):
					top_edge=img_heigh

				bot_edge=pre_Y+2*heigh
				if(bot_edge>img_heigh):
					bot_edge=img_heigh

				sum_square=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
				if(sum_square>=threshold_line):
					#check empty top
					bot_edge=top_edge
					top_edge=bot_edge-windowLength_empty
					if(top_edge<0):
						top_edge=0
					sum_window_empty_top=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					#check empty left
					top_edge=bot_edge
					bot_edge=pre_Y+2*heigh
					if(bot_edge>img_heigh):
						bot_edge=img_heigh
					right_edge=left_edge+1
					if(right_edge>img_width):
						right_edge=img_width
					left_edge=left_edge-windowLength_empty
					if(left_edge<0):
						left_edge=0
					sum_window_empty_left=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					if(sum_window_empty_top<=threshold_empty or sum_window_empty_left<=threshold_empty):
						x=right_edge-1+int(windowLength_line/2)
						y=top_edge
						if points_line is not None:
							#phong truong hop lap lai
							if(points_line.shape[0]>=2):
								distanceX=abs(x - points_line[points_line.shape[0]-2][0])
								distanceY=abs(y - points_line[points_line.shape[0]-2][1])
								if(distanceX >= int(windowLength_line/2) or distanceY >= int(heigh/2)): #khong bi trung diem phia truoc
									coo=np.array([[x,y]])
									points_line=np.append(points_line,coo,axis=0)
									#update value and continue
									pre_X=x
									pre_Y=y
									continue
							else:
								coo=np.array([[x,y]])
								points_line=np.append(points_line,coo,axis=0)
								#update value and continue
								pre_X=x
								pre_Y=y
								continue
						else:
							points_line=np.array([[x,y]])
							#update value and continue
							pre_X=x
							pre_Y=y
							continue
				#botton right square
				left_edge=pre_X+int(windowLength_line/2)
				if(left_edge<0):
					left_edge=0

				right_edge=pre_X+int(windowLength_line/2)+windowLength_line+1
				if(right_edge>img_width):
					right_edge=img_width

				top_edge=pre_Y+heigh
				if(top_edge>img_heigh):
					top_edge=img_heigh

				bot_edge=pre_Y+heigh*2
				if(bot_edge>img_heigh):
					bot_edge=img_heigh

				sum_square=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
				if(sum_square>=threshold_line):
					#check empty top
					bot_edge=top_edge
					top_edge=bot_edge-windowLength_empty
					if(top_edge<0):
						top_edge=0
					sum_window_empty_top=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					#check empty left
					top_edge=bot_edge
					bot_edge=pre_Y+heigh*2
					if(bot_edge>img_heigh):
						bot_edge=img_heigh
					right_edge=left_edge+1
					if(right_edge>img_width):
						right_edge=img_width
					left_edge=left_edge-windowLength_empty
					if(left_edge<0):
						left_edge=0
					sum_window_empty_left=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					if(sum_window_empty_top<=threshold_empty or sum_window_empty_left<=threshold_empty):
						x=right_edge-1+int(windowLength_line/2)
						y=top_edge
						if points_line is not None:
							#phong truong hop lap lai
							if(points_line.shape[0]>=2):
								distanceX=abs(x - points_line[points_line.shape[0]-2][0])
								distanceY=abs(y - points_line[points_line.shape[0]-2][1])
								if(distanceX >= int(windowLength_line/2) or distanceY >= int(heigh/2)): #khong bi trung diem phia truoc
									coo=np.array([[x,y]])
									points_line=np.append(points_line,coo,axis=0)
									#update value and continue
									pre_X=x
									pre_Y=y
									continue
							else:
								coo=np.array([[x,y]])
								points_line=np.append(points_line,coo,axis=0)
								#update value and continue
								pre_X=x
								pre_Y=y
								continue
						else:
							points_line=np.array([[x,y]])
							#update value and continue
							pre_X=x
							pre_Y=y
							continue
				#right midle square
				left_edge=pre_X+int(windowLength_line/2)
				if(left_edge<0):
					left_edge=0

				right_edge=pre_X+int(windowLength_line/2)+windowLength_line+1
				if(right_edge>img_width):
					right_edge=img_width

				top_edge=pre_Y+int(heigh/2)
				if(top_edge>img_heigh):
					top_edge=img_heigh

				bot_edge=pre_Y+int(heigh*3/2)+1
				if(bot_edge>img_heigh):
					bot_edge=img_heigh

				sum_square=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
				if(sum_square>=threshold_line):
					#check empty top
					bot_edge=top_edge
					top_edge=bot_edge-windowLength_empty
					if(top_edge<0):
						top_edge=0
					sum_window_empty_top=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					#check empty left
					top_edge=bot_edge
					bot_edge=pre_Y+int(heigh*3/2)+1
					if(bot_edge>img_heigh):
						bot_edge=img_heigh
					right_edge=left_edge+1
					if(right_edge>img_width):
						right_edge=img_width
					left_edge=left_edge-windowLength_empty
					if(left_edge<0):
						left_edge=0
					sum_window_empty_left=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					if(sum_window_empty_top<=threshold_empty or sum_window_empty_left<=threshold_empty):
						x=right_edge-1+int(windowLength_line/2)
						y=top_edge
						if points_line is not None:
							#phong truong hop lap lai
							if(points_line.shape[0]>=2):
								distanceX=abs(x - points_line[points_line.shape[0]-2][0])
								distanceY=abs(y - points_line[points_line.shape[0]-2][1])
								if(distanceX >= int(windowLength_line/2) or distanceY >= int(heigh/2)): #khong bi trung diem phia truoc
									coo=np.array([[x,y]])
									points_line=np.append(points_line,coo,axis=0)
									#update value and continue
									pre_X=x
									pre_Y=y
									continue
							else:
								coo=np.array([[x,y]])
								points_line=np.append(points_line,coo,axis=0)
								#update value and continue
								pre_X=x
								pre_Y=y
								continue
						else:
							points_line=np.array([[x,y]])
							#update value and continue
							pre_X=x
							pre_Y=y
							continue
				#left top square
				left_edge=pre_X+int(windowLength_line/2)
				if(left_edge<0):
					left_edge=0

				right_edge=pre_X+int(windowLength_line/2)+windowLength_line+1
				if(right_edge>img_width):
					right_edge=img_width

				top_edge=pre_Y
				if(top_edge>img_heigh):
					top_edge=img_heigh

				bot_edge=pre_Y+heigh+1
				if(bot_edge>img_heigh):
					bot_edge=img_heigh

				sum_square=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
				if(sum_square>=threshold_line):
					#check empty top
					bot_edge=top_edge
					top_edge=bot_edge-windowLength_empty
					if(top_edge<0):
						top_edge=0
					sum_window_empty_top=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					#check empty left
					top_edge=bot_edge
					bot_edge=pre_Y+heigh+1
					if(bot_edge>img_heigh):
						bot_edge=img_heigh
					right_edge=left_edge+1
					if(right_edge>img_width):
						right_edge=img_width
					left_edge=left_edge-windowLength_empty
					if(left_edge<0):
						left_edge=0
					sum_window_empty_left=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					if(sum_window_empty_top<=threshold_empty or sum_window_empty_left<=threshold_empty):
						x=right_edge-1+int(windowLength_line/2)
						y=top_edge
						if points_line is not None:
							#phong truong hop lap lai
							if(points_line.shape[0]>=2):
								distanceX=abs(x - points_line[points_line.shape[0]-2][0])
								distanceY=abs(y - points_line[points_line.shape[0]-2][1])
								if(distanceX >= int(windowLength_line/2) or distanceY >= int(heigh/2)): #khong bi trung diem phia truoc
									coo=np.array([[x,y]])
									points_line=np.append(points_line,coo,axis=0)
									#update value and continue
									pre_X=x
									pre_Y=y
									continue
							else:
								coo=np.array([[x,y]])
								points_line=np.append(points_line,coo,axis=0)
								#update value and continue
								pre_X=x
								pre_Y=y
								continue
						else:
							points_line=np.array([[x,y]])
							#update value and continue
							pre_X=x
							pre_Y=y
							continue
				break

	#====================================================line trai==========================================
	if (left_or_right==0):
		if (up_or_down==0):
			while True:
				#calculate each square
				#botton left square
				left_edge=pre_X-int(windowLength_line/2)-windowLength_line
				if(left_edge<0):
					left_edge=0

				right_edge=pre_X-int(windowLength_line/2)+1
				if(right_edge>img_width):
					right_edge=img_width

				top_edge=pre_Y
				if(top_edge<0):
					top_edge=0

				bot_edge=pre_Y+heigh+1
				if(bot_edge>img_heigh):
					bot_edge=img_heigh

				sum_square=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
				if(sum_square>=threshold_line):
					#check empty top
					bot_edge=top_edge
					top_edge=bot_edge-windowLength_empty
					if(top_edge<0):
						top_edge=0
					sum_window_empty_top=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					#check empty right
					top_edge=bot_edge
					bot_edge=pre_Y+heigh+1
					if(bot_edge>img_heigh):
						bot_edge=img_heigh
					left_edge=right_edge
					if(left_edge>img_width):
						left_edge=img_width
					right_edge+=windowLength_empty
					if(right_edge>img_width):
						right_edge=img_width
					sum_window_empty_left=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					if(sum_window_empty_top<=threshold_empty or sum_window_empty_left<=threshold_empty):
						x=left_edge-int(windowLength_line/2)
						y=top_edge
						if points_line is not None:
							#phong truong hop lap lai
							if(points_line.shape[0]>=2):
								distanceX=abs(x - points_line[points_line.shape[0]-2][0])
								distanceY=abs(y - points_line[points_line.shape[0]-2][1])
								if(distanceX >= int(windowLength_line/2) or distanceY >= int(heigh/2)): #khong bi trung diem phia truoc
									coo=np.array([[x,y]])
									points_line=np.append(points_line,coo,axis=0)
									#update value and continue
									pre_X=x
									pre_Y=y
									continue
							else:
								coo=np.array([[x,y]])
								points_line=np.append(points_line,coo,axis=0)
								#update value and continue
								pre_X=x
								pre_Y=y
								continue
						else:
							points_line=np.array([[x,y]])
							#update value and continue
							pre_X=x
							pre_Y=y
							continue
				#left midle square
				left_edge=pre_X-int(windowLength_line/2)-windowLength_line
				if(left_edge<0):
					left_edge=0

				right_edge=pre_X-int(windowLength_line/2)+1
				if(right_edge>img_width):
					right_edge=img_width

				top_edge=pre_Y-int(heigh/2)
				if(top_edge<0):
					top_edge=0

				bot_edge=pre_Y+int(heigh/2)+1
				if(bot_edge>img_heigh):
					bot_edge=img_heigh

				sum_square=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
				if(sum_square>=threshold_line):
					#check empty top
					bot_edge=top_edge
					top_edge=bot_edge-windowLength_empty
					if(top_edge<0):
						top_edge=0
					sum_window_empty_top=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					#check empty right
					top_edge=bot_edge
					bot_edge=pre_Y+heigh+1
					if(bot_edge>img_heigh):
						bot_edge=img_heigh
					left_edge=right_edge
					if(left_edge>img_width):
						left_edge=img_width
					right_edge+=windowLength_empty
					if(right_edge>img_width):
						right_edge=img_width
					sum_window_empty_left=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					if(sum_window_empty_top<=threshold_empty or sum_window_empty_left<=threshold_empty):
						x=left_edge-int(windowLength_line/2)
						y=top_edge
						if points_line is not None:
							#phong truong hop lap lai
							if(points_line.shape[0]>=2):
								distanceX=abs(x - points_line[points_line.shape[0]-2][0])
								distanceY=abs(y - points_line[points_line.shape[0]-2][1])
								if(distanceX >= int(windowLength_line/2) or distanceY >= int(heigh/2)): #khong bi trung diem phia truoc
									coo=np.array([[x,y]])
									points_line=np.append(points_line,coo,axis=0)
									#update value and continue
									pre_X=x
									pre_Y=y
									continue
							else:
								coo=np.array([[x,y]])
								points_line=np.append(points_line,coo,axis=0)
								#update value and continue
								pre_X=x
								pre_Y=y
								continue
						else:
							points_line=np.array([[x,y]])
							#update value and continue
							pre_X=x
							pre_Y=y
							continue
				#left top square
				left_edge=pre_X-int(windowLength_line/2)-windowLength_line
				if(left_edge<0):
					left_edge=0

				right_edge=pre_X-int(windowLength_line/2)+1
				if(right_edge>img_width):
					right_edge=img_width

				top_edge=pre_Y-heigh
				if(top_edge<0):
					top_edge=0

				bot_edge=pre_Y+1
				if(bot_edge>img_heigh):
					bot_edge=img_heigh

				sum_square=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
				if(sum_square>=threshold_line):
					#check empty top
					bot_edge=top_edge
					top_edge=bot_edge-windowLength_empty
					if(top_edge<0):
						top_edge=0
					sum_window_empty_top=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					#check empty right
					top_edge=bot_edge
					bot_edge=pre_Y+heigh+1
					if(bot_edge>img_heigh):
						bot_edge=img_heigh
					left_edge=right_edge
					if(left_edge>img_width):
						left_edge=img_width
					right_edge+=windowLength_empty
					if(right_edge>img_width):
						right_edge=img_width
					sum_window_empty_left=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					if(sum_window_empty_top<=threshold_empty or sum_window_empty_left<=threshold_empty):
						x=left_edge-int(windowLength_line/2)
						y=top_edge
						if points_line is not None:
							#phong truong hop lap lai
							if(points_line.shape[0]>=2):
								distanceX=abs(x - points_line[points_line.shape[0]-2][0])
								distanceY=abs(y - points_line[points_line.shape[0]-2][1])
								if(distanceX >= int(windowLength_line/2) or distanceY >= int(heigh/2)): #khong bi trung diem phia truoc
									coo=np.array([[x,y]])
									points_line=np.append(points_line,coo,axis=0)
									#update value and continue
									pre_X=x
									pre_Y=y
									continue
							else:
								coo=np.array([[x,y]])
								points_line=np.append(points_line,coo,axis=0)
								#update value and continue
								pre_X=x
								pre_Y=y
								continue
						else:
							points_line=np.array([[x,y]])
							#update value and continue
							pre_X=x
							pre_Y=y
							continue
				#top square
				left_edge=pre_X-int(windowLength_line/2)
				if(left_edge<0):
					left_edge=0

				right_edge=pre_X+int(windowLength_line/2)+1
				if(right_edge>img_width):
					right_edge=img_width

				top_edge=pre_Y-heigh
				if(top_edge<0):
					top_edge=0

				bot_edge=pre_Y+1
				if(bot_edge>img_heigh):
					bot_edge=img_heigh

				sum_square=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
				if(sum_square>=threshold_line):
					#check empty top
					bot_edge=top_edge
					top_edge=bot_edge-windowLength_empty
					if(top_edge<0):
						top_edge=0
					sum_window_empty_top=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					#check empty right
					top_edge=bot_edge
					bot_edge=pre_Y+heigh+1
					if(bot_edge>img_heigh):
						bot_edge=img_heigh
					left_edge=right_edge
					if(left_edge>img_width):
						left_edge=img_width
					right_edge+=windowLength_empty
					if(right_edge>img_width):
						right_edge=img_width
					sum_window_empty_left=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					if(sum_window_empty_top<=threshold_empty or sum_window_empty_left<=threshold_empty):
						x=left_edge-int(windowLength_line/2)
						y=top_edge
						if points_line is not None:
							#phong truong hop lap lai
							if(points_line.shape[0]>=2):
								distanceX=abs(x - points_line[points_line.shape[0]-2][0])
								distanceY=abs(y - points_line[points_line.shape[0]-2][1])
								if(distanceX >= int(windowLength_line/2) or distanceY >= int(heigh/2)): #khong bi trung diem phia truoc
									coo=np.array([[x,y]])
									points_line=np.append(points_line,coo,axis=0)
									#update value and continue
									pre_X=x
									pre_Y=y
									continue
							else:
								coo=np.array([[x,y]])
								points_line=np.append(points_line,coo,axis=0)
								#update value and continue
								pre_X=x
								pre_Y=y
								continue
						else:
							points_line=np.array([[x,y]])
							#update value and continue
							pre_X=x
							pre_Y=y
							continue
				#botton right square
				left_edge=pre_X+int(windowLength_line/2)
				if(left_edge<0):
					left_edge=0

				right_edge=pre_X+int(windowLength_line/2)+windowLength_line+1
				if(right_edge>img_width):
					right_edge=img_width

				top_edge=pre_Y
				if(top_edge<0):
					top_edge=0

				bot_edge=pre_Y+heigh+1
				if(bot_edge>img_heigh):
					bot_edge=img_heigh

				sum_square=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
				if(sum_square>=threshold_line):
					#check empty top
					bot_edge=top_edge
					top_edge=bot_edge-windowLength_empty
					if(top_edge<0):
						top_edge=0
					sum_window_empty_top=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					#check empty right
					top_edge=bot_edge
					bot_edge=pre_Y+heigh+1
					if(bot_edge>img_heigh):
						bot_edge=img_heigh
					left_edge=right_edge
					if(left_edge>img_width):
						left_edge=img_width
					right_edge+=windowLength_empty
					if(right_edge>img_width):
						right_edge=img_width
					sum_window_empty_left=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					if(sum_window_empty_top<=threshold_empty or sum_window_empty_left<=threshold_empty):
						x=left_edge-int(windowLength_line/2)
						y=top_edge
						if points_line is not None:
							#phong truong hop lap lai
							if(points_line.shape[0]>=2):
								distanceX=abs(x - points_line[points_line.shape[0]-2][0])
								distanceY=abs(y - points_line[points_line.shape[0]-2][1])
								if(distanceX >= int(windowLength_line/2) or distanceY >= int(heigh/2)): #khong bi trung diem phia truoc
									coo=np.array([[x,y]])
									points_line=np.append(points_line,coo,axis=0)
									#update value and continue
									pre_X=x
									pre_Y=y
									continue
							else:
								coo=np.array([[x,y]])
								points_line=np.append(points_line,coo,axis=0)
								#update value and continue
								pre_X=x
								pre_Y=y
								continue
						else:
							points_line=np.array([[x,y]])
							#update value and continue
							pre_X=x
							pre_Y=y
							continue
				#right midle square
				left_edge=pre_X+int(windowLength_line/2)
				if(left_edge<0):
					left_edge=0

				right_edge=pre_X+int(windowLength_line/2)+windowLength_line+1
				if(right_edge>img_width):
					right_edge=img_width

				top_edge=pre_Y-int(heigh/2)
				if(top_edge<0):
					top_edge=0

				bot_edge=pre_Y+int(heigh/2)+1
				if(bot_edge>img_heigh):
					bot_edge=img_heigh

				sum_square=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
				if(sum_square>=threshold_line):
					#check empty top
					bot_edge=top_edge
					top_edge=bot_edge-windowLength_empty
					if(top_edge<0):
						top_edge=0
					sum_window_empty_top=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					#check empty right
					top_edge=bot_edge
					bot_edge=pre_Y+heigh+1
					if(bot_edge>img_heigh):
						bot_edge=img_heigh
					left_edge=right_edge
					if(left_edge>img_width):
						left_edge=img_width
					right_edge+=windowLength_empty
					if(right_edge>img_width):
						right_edge=img_width
					sum_window_empty_left=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					if(sum_window_empty_top<=threshold_empty or sum_window_empty_left<=threshold_empty):
						x=left_edge-int(windowLength_line/2)
						y=top_edge
						if points_line is not None:
							#phong truong hop lap lai
							if(points_line.shape[0]>=2):
								distanceX=abs(x - points_line[points_line.shape[0]-2][0])
								distanceY=abs(y - points_line[points_line.shape[0]-2][1])
								if(distanceX >= int(windowLength_line/2) or distanceY >= int(heigh/2)): #khong bi trung diem phia truoc
									coo=np.array([[x,y]])
									points_line=np.append(points_line,coo,axis=0)
									#update value and continue
									pre_X=x
									pre_Y=y
									continue
							else:
								coo=np.array([[x,y]])
								points_line=np.append(points_line,coo,axis=0)
								#update value and continue
								pre_X=x
								pre_Y=y
								continue
						else:
							points_line=np.array([[x,y]])
							#update value and continue
							pre_X=x
							pre_Y=y
							continue
				#left top square
				left_edge=pre_X+int(windowLength_line/2)
				if(left_edge<0):
					left_edge=0

				right_edge=pre_X+int(windowLength_line/2)+windowLength_line+1
				if(right_edge>img_width):
					right_edge=img_width

				top_edge=pre_Y-heigh
				if(top_edge<0):
					top_edge=0

				bot_edge=pre_Y+1
				if(bot_edge>img_heigh):
					bot_edge=img_heigh

				sum_square=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
				if(sum_square>=threshold_line):
					#check empty top
					bot_edge=top_edge
					top_edge=bot_edge-windowLength_empty
					if(top_edge<0):
						top_edge=0
					sum_window_empty_top=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					#check empty right
					top_edge=bot_edge
					bot_edge=pre_Y+heigh+1
					if(bot_edge>img_heigh):
						bot_edge=img_heigh
					left_edge=right_edge
					if(left_edge>img_width):
						left_edge=img_width
					right_edge+=windowLength_empty
					if(right_edge>img_width):
						right_edge=img_width
					sum_window_empty_left=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					if(sum_window_empty_top<=threshold_empty or sum_window_empty_left<=threshold_empty):
						x=left_edge-int(windowLength_line/2)
						y=top_edge
						if points_line is not None:
							#phong truong hop lap lai
							if(points_line.shape[0]>=2):
								distanceX=abs(x - points_line[points_line.shape[0]-2][0])
								distanceY=abs(y - points_line[points_line.shape[0]-2][1])
								if(distanceX >= int(windowLength_line/2) or distanceY >= int(heigh/2)): #khong bi trung diem phia truoc
									coo=np.array([[x,y]])
									points_line=np.append(points_line,coo,axis=0)
									#update value and continue
									pre_X=x
									pre_Y=y
									continue
							else:
								coo=np.array([[x,y]])
								points_line=np.append(points_line,coo,axis=0)
								#update value and continue
								pre_X=x
								pre_Y=y
								continue
						else:
							points_line=np.array([[x,y]])
							#update value and continue
							pre_X=x
							pre_Y=y
							continue
				break
		if (up_or_down==1):
			while True:
				#calculate each square
				#botton left square
				left_edge=pre_X-int(windowLength_line/2)-windowLength_line
				if(left_edge<0):
					left_edge=0

				right_edge=pre_X-int(windowLength_line/2)+1
				if(right_edge>img_width):
					right_edge=img_width

				top_edge=pre_Y+heigh
				if(top_edge>img_heigh):
					top_edge=img_heigh

				bot_edge=pre_Y+heigh*2
				if(bot_edge>img_heigh):
					bot_edge=img_heigh

				sum_square=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
				if(sum_square>=threshold_line):
					#check empty top
					bot_edge=top_edge
					top_edge=bot_edge-windowLength_empty
					if(top_edge<0):
						top_edge=0
					sum_window_empty_top=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					#check empty right
					top_edge=bot_edge
					bot_edge=pre_Y+heigh+1
					if(bot_edge>img_heigh):
						bot_edge=img_heigh
					left_edge=right_edge
					if(left_edge>img_width):
						left_edge=img_width
					right_edge+=windowLength_empty
					if(right_edge>img_width):
						right_edge=img_width
					sum_window_empty_left=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					if(sum_window_empty_top<=threshold_empty or sum_window_empty_left<=threshold_empty):
						x=left_edge-int(windowLength_line/2)
						y=top_edge
						if points_line is not None:
							#phong truong hop lap lai
							if(points_line.shape[0]>=2):
								distanceX=abs(x - points_line[points_line.shape[0]-2][0])
								distanceY=abs(y - points_line[points_line.shape[0]-2][1])
								if(distanceX >= int(windowLength_line/2) or distanceY >= int(heigh/2)): #khong bi trung diem phia truoc
									coo=np.array([[x,y]])
									points_line=np.append(points_line,coo,axis=0)
									#update value and continue
									pre_X=x
									pre_Y=y
									continue
							else:
								coo=np.array([[x,y]])
								points_line=np.append(points_line,coo,axis=0)
								#update value and continue
								pre_X=x
								pre_Y=y
								continue
						else:
							points_line=np.array([[x,y]])
							#update value and continue
							pre_X=x
							pre_Y=y
							continue
				#left midle square
				left_edge=pre_X-int(windowLength_line/2)-windowLength_line
				if(left_edge<0):
					left_edge=0

				right_edge=pre_X-int(windowLength_line/2)+1
				if(right_edge>img_width):
					right_edge=img_width

				top_edge=pre_Y+int(heigh/2)
				if(top_edge>img_heigh):
					top_edge=img_heigh

				bot_edge=pre_Y+int(heigh*3/2)+1
				if(bot_edge>img_heigh):
					bot_edge=img_heigh

				sum_square=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
				if(sum_square>=threshold_line):
					#check empty top
					bot_edge=top_edge
					top_edge=bot_edge-windowLength_empty
					if(top_edge<0):
						top_edge=0
					sum_window_empty_top=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					#check empty right
					top_edge=bot_edge
					bot_edge=pre_Y+heigh+1
					if(bot_edge>img_heigh):
						bot_edge=img_heigh
					left_edge=right_edge
					if(left_edge>img_width):
						left_edge=img_width
					right_edge+=windowLength_empty
					if(right_edge>img_width):
						right_edge=img_width
					sum_window_empty_left=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					if(sum_window_empty_top<=threshold_empty or sum_window_empty_left<=threshold_empty):
						x=left_edge-int(windowLength_line/2)
						y=top_edge
						if points_line is not None:
							#phong truong hop lap lai
							if(points_line.shape[0]>=2):
								distanceX=abs(x - points_line[points_line.shape[0]-2][0])
								distanceY=abs(y - points_line[points_line.shape[0]-2][1])
								if(distanceX >= int(windowLength_line/2) or distanceY >= int(heigh/2)): #khong bi trung diem phia truoc
									coo=np.array([[x,y]])
									points_line=np.append(points_line,coo,axis=0)
									#update value and continue
									pre_X=x
									pre_Y=y
									continue
							else:
								coo=np.array([[x,y]])
								points_line=np.append(points_line,coo,axis=0)
								#update value and continue
								pre_X=x
								pre_Y=y
								continue
						else:
							points_line=np.array([[x,y]])
							#update value and continue
							pre_X=x
							pre_Y=y
							continue
				#left top square
				left_edge=pre_X-int(windowLength_line/2)-windowLength_line
				if(left_edge<0):
					left_edge=0

				right_edge=pre_X-int(windowLength_line/2)+1
				if(right_edge>img_width):
					right_edge=img_width

				top_edge=pre_Y
				if(top_edge>=img_heigh):
					top_edge=img_heigh

				bot_edge=pre_Y+heigh
				if(bot_edge>img_heigh):
					bot_edge=img_heigh

				sum_square=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
				if(sum_square>=threshold_line):
					#check empty top
					bot_edge=top_edge
					top_edge=bot_edge-windowLength_empty
					if(top_edge<0):
						top_edge=0
					sum_window_empty_top=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					#check empty right
					top_edge=bot_edge
					bot_edge=pre_Y+heigh+1
					if(bot_edge>img_heigh):
						bot_edge=img_heigh
					left_edge=right_edge
					if(left_edge>img_width):
						left_edge=img_width
					right_edge+=windowLength_empty
					if(right_edge>img_width):
						right_edge=img_width
					sum_window_empty_left=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					if(sum_window_empty_top<=threshold_empty or sum_window_empty_left<=threshold_empty):
						x=left_edge-int(windowLength_line/2)
						y=top_edge
						if points_line is not None:
							#phong truong hop lap lai
							if(points_line.shape[0]>=2):
								distanceX=abs(x - points_line[points_line.shape[0]-2][0])
								distanceY=abs(y - points_line[points_line.shape[0]-2][1])
								if(distanceX >= int(windowLength_line/2) or distanceY >= int(heigh/2)): #khong bi trung diem phia truoc
									coo=np.array([[x,y]])
									points_line=np.append(points_line,coo,axis=0)
									#update value and continue
									pre_X=x
									pre_Y=y
									continue
							else:
								coo=np.array([[x,y]])
								points_line=np.append(points_line,coo,axis=0)
								#update value and continue
								pre_X=x
								pre_Y=y
								continue
						else:
							points_line=np.array([[x,y]])
							#update value and continue
							pre_X=x
							pre_Y=y
							continue
				#botton square
				left_edge=pre_X-int(windowLength_line/2)
				if(left_edge<0):
					left_edge=0

				right_edge=pre_X+int(windowLength_line/2)+1
				if(right_edge>img_width):
					right_edge=img_width

				top_edge=pre_Y+heigh
				if(top_edge>img_heigh):
					top_edge=img_heigh

				bot_edge=pre_Y+2*heigh
				if(bot_edge>img_heigh):
					bot_edge=img_heigh

				sum_square=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
				if(sum_square>=threshold_line):
					#check empty top
					bot_edge=top_edge
					top_edge=bot_edge-windowLength_empty
					if(top_edge<0):
						top_edge=0
					sum_window_empty_top=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					#check empty right
					top_edge=bot_edge
					bot_edge=pre_Y+heigh+1
					if(bot_edge>img_heigh):
						bot_edge=img_heigh
					left_edge=right_edge
					if(left_edge>img_width):
						left_edge=img_width
					right_edge+=windowLength_empty
					if(right_edge>img_width):
						right_edge=img_width
					sum_window_empty_left=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					if(sum_window_empty_top<=threshold_empty or sum_window_empty_left<=threshold_empty):
						x=left_edge-int(windowLength_line/2)
						y=top_edge
						if points_line is not None:
							#phong truong hop lap lai
							if(points_line.shape[0]>=2):
								distanceX=abs(x - points_line[points_line.shape[0]-2][0])
								distanceY=abs(y - points_line[points_line.shape[0]-2][1])
								if(distanceX >= int(windowLength_line/2) or distanceY >= int(heigh/2)): #khong bi trung diem phia truoc
									coo=np.array([[x,y]])
									points_line=np.append(points_line,coo,axis=0)
									#update value and continue
									pre_X=x
									pre_Y=y
									continue
							else:
								coo=np.array([[x,y]])
								points_line=np.append(points_line,coo,axis=0)
								#update value and continue
								pre_X=x
								pre_Y=y
								continue
						else:
							points_line=np.array([[x,y]])
							#update value and continue
							pre_X=x
							pre_Y=y
							continue
				#botton right square
				left_edge=pre_X+int(windowLength_line/2)
				if(left_edge<0):
					left_edge=0

				right_edge=pre_X+int(windowLength_line/2)+windowLength_line+1
				if(right_edge>img_width):
					right_edge=img_width

				top_edge=pre_Y+heigh
				if(top_edge>img_heigh):
					top_edge=img_heigh

				bot_edge=pre_Y+heigh*2
				if(bot_edge>img_heigh):
					bot_edge=img_heigh

				sum_square=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
				if(sum_square>=threshold_line):
					#check empty top
					bot_edge=top_edge
					top_edge=bot_edge-windowLength_empty
					if(top_edge<0):
						top_edge=0
					sum_window_empty_top=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					#check empty right
					top_edge=bot_edge
					bot_edge=pre_Y+heigh+1
					if(bot_edge>img_heigh):
						bot_edge=img_heigh
					left_edge=right_edge
					if(left_edge>img_width):
						left_edge=img_width
					right_edge+=windowLength_empty
					if(right_edge>img_width):
						right_edge=img_width
					sum_window_empty_left=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					if(sum_window_empty_top<=threshold_empty or sum_window_empty_left<=threshold_empty):
						x=left_edge-int(windowLength_line/2)
						y=top_edge
						if points_line is not None:
							#phong truong hop lap lai
							if(points_line.shape[0]>=2):
								distanceX=abs(x - points_line[points_line.shape[0]-2][0])
								distanceY=abs(y - points_line[points_line.shape[0]-2][1])
								if(distanceX >= int(windowLength_line/2) or distanceY >= int(heigh/2)): #khong bi trung diem phia truoc
									coo=np.array([[x,y]])
									points_line=np.append(points_line,coo,axis=0)
									#update value and continue
									pre_X=x
									pre_Y=y
									continue
							else:
								coo=np.array([[x,y]])
								points_line=np.append(points_line,coo,axis=0)
								#update value and continue
								pre_X=x
								pre_Y=y
								continue
						else:
							points_line=np.array([[x,y]])
							#update value and continue
							pre_X=x
							pre_Y=y
							continue
				#right midle square
				left_edge=pre_X+int(windowLength_line/2)
				if(left_edge<0):
					left_edge=0

				right_edge=pre_X+int(windowLength_line/2)+windowLength_line+1
				if(right_edge>img_width):
					right_edge=img_width

				top_edge=pre_Y+int(heigh/2)
				if(top_edge>img_heigh):
					top_edge=img_heigh

				bot_edge=pre_Y+int(heigh*3/2)+1
				if(bot_edge>img_heigh):
					bot_edge=img_heigh

				sum_square=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
				if(sum_square>=threshold_line):
					#check empty top
					bot_edge=top_edge
					top_edge=bot_edge-windowLength_empty
					if(top_edge<0):
						top_edge=0
					sum_window_empty_top=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					#check empty right
					top_edge=bot_edge
					bot_edge=pre_Y+heigh+1
					if(bot_edge>img_heigh):
						bot_edge=img_heigh
					left_edge=right_edge
					if(left_edge>img_width):
						left_edge=img_width
					right_edge+=windowLength_empty
					if(right_edge>img_width):
						right_edge=img_width
					sum_window_empty_left=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					if(sum_window_empty_top<=threshold_empty or sum_window_empty_left<=threshold_empty):
						x=left_edge-int(windowLength_line/2)
						y=top_edge
						if points_line is not None:
							#phong truong hop lap lai
							if(points_line.shape[0]>=2):
								distanceX=abs(x - points_line[points_line.shape[0]-2][0])
								distanceY=abs(y - points_line[points_line.shape[0]-2][1])
								if(distanceX >= int(windowLength_line/2) or distanceY >= int(heigh/2)): #khong bi trung diem phia truoc
									coo=np.array([[x,y]])
									points_line=np.append(points_line,coo,axis=0)
									#update value and continue
									pre_X=x
									pre_Y=y
									continue
							else:
								coo=np.array([[x,y]])
								points_line=np.append(points_line,coo,axis=0)
								#update value and continue
								pre_X=x
								pre_Y=y
								continue
						else:
							points_line=np.array([[x,y]])
							#update value and continue
							pre_X=x
							pre_Y=y
							continue
				#left top square
				left_edge=pre_X+int(windowLength_line/2)
				if(left_edge<0):
					left_edge=0

				right_edge=pre_X+int(windowLength_line/2)+windowLength_line+1
				if(right_edge>img_width):
					right_edge=img_width

				top_edge=pre_Y
				if(top_edge>img_heigh):
					top_edge=img_heigh

				bot_edge=pre_Y+heigh+1
				if(bot_edge>img_heigh):
					bot_edge=img_heigh

				sum_square=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
				if(sum_square>=threshold_line):
					#check empty top
					bot_edge=top_edge
					top_edge=bot_edge-windowLength_empty
					if(top_edge<0):
						top_edge=0
					sum_window_empty_top=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					#check empty right
					top_edge=bot_edge
					bot_edge=pre_Y+heigh+1
					if(bot_edge>img_heigh):
						bot_edge=img_heigh
					left_edge=right_edge
					if(left_edge>img_width):
						left_edge=img_width
					right_edge+=windowLength_empty
					if(right_edge>img_width):
						right_edge=img_width
					sum_window_empty_left=np.sum(eyeBird_binary[top_edge:bot_edge,left_edge:right_edge])
					if(sum_window_empty_top<=threshold_empty or sum_window_empty_left<=threshold_empty):
						x=left_edge-int(windowLength_line/2)
						y=top_edge
						if points_line is not None:
							#phong truong hop lap lai
							if(points_line.shape[0]>=2):
								distanceX=abs(x - points_line[points_line.shape[0]-2][0])
								distanceY=abs(y - points_line[points_line.shape[0]-2][1])
								if(distanceX >= int(windowLength_line/2) or distanceY >= int(heigh/2)): #khong bi trung diem phia truoc
									coo=np.array([[x,y]])
									points_line=np.append(points_line,coo,axis=0)
									#update value and continue
									pre_X=x
									pre_Y=y
									continue
							else:
								coo=np.array([[x,y]])
								points_line=np.append(points_line,coo,axis=0)
								#update value and continue
								pre_X=x
								pre_Y=y
								continue
						else:
							points_line=np.array([[x,y]])
							#update value and continue
							pre_X=x
							pre_Y=y
							continue
				break
	return points_line


"""
135->120
120->105
105->90
90->75
75->60
60->45
45->30
30->15
15->0
"""

cap = cv2.VideoCapture('outpy.avi')
if __name__ == '__main__':
	n=0
	#arr=np.array([[-1,0],[2,1],[3,2],[-1,3],[-1,4],[6,5],[-1,6],[-1,7]])
	#fill_points(arr)
	#print (arr)
	side=-1
	while(cap.isOpened()):
		stime = time.time()
		ret, image_np = cap.read()
		#image_np=cv2.imread('difficult.png')
		res_binary,roi_binary,eyeBird_binary=get_processed_img(image_np)
		img_heigh = eyeBird_binary.shape[0]
		img_width = eyeBird_binary.shape[1]
		
		detect_line(eyeBird_binary=eyeBird_binary,threshold_num_point=8)

		cv2.imshow('raw',image_np)
		#print ('{} FPS'.format(1.0/(time.time() - stime)))

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	cap.release()
	cv2.destroyAllWindows()
