import numpy as np
import math

def distance_2_points (x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)

def find_mid_points (leftPoints, rightPoints, thresholdVertical=17, thresholdHorizontal=17, limit_distance=180):
    ret = None
    for leftPoint in leftPoints:
        for rightPoint in rightPoints:
            #horizonal
            if(abs(leftPoint[0]-rightPoint[0]) <= thresholdHorizontal):
                if (distance_2_points(leftPoint[0], leftPoint[1], rightPoint[0], rightPoint[1]) <= 180):
                    if ret is not None:
                        coo=np.array([[int((leftPoint[0]+rightPoint[0])/2),int((leftPoint[1]+rightPoint[1])/2)]])
                        ret=np.append(ret, coo, axis=0)
                    else:
                        ret=np.array([[int((leftPoint[0]+rightPoint[0])/2),int((leftPoint[1]+rightPoint[1])/2)]])
            #vertical
            if(abs(leftPoint[1]-rightPoint[1]) <= thresholdVertical):
                if (distance_2_points(leftPoint[0], leftPoint[1], rightPoint[0], rightPoint[1]) <= 180):
                    if ret is not None:
                        coo=np.array([[int((leftPoint[0]+rightPoint[0])/2),int((leftPoint[1]+rightPoint[1])/2)]])
                        ret=np.append(ret, coo, axis=0)
                    else:
                        ret=np.array([[int((leftPoint[0]+rightPoint[0])/2),int((leftPoint[1]+rightPoint[1])/2)]])
    return ret

def caculate_angle_mid_point (ImgShapeX,ImgShapeY,midPoint,ratio):
	AB=abs(ImgShapeY-midPoint[1])
	AC=abs(ImgShapeX/2 - midPoint[0])
	#BC=math.sqrt(float(AB*AB) + AC*AC)
	angle=0
	if midPoint[0] > ImgShapeX/2:
		angle=1 #be ben phai
	elif midPoint[0] < ImgShapeX/2:
		angle=-1 #be ben trai
	else:
		return 0
	return angle * np.arctan(float(AC)/AB)/np.pi*180 * (ImgShapeY-midPoint[1])/float(ImgShapeY/ratio)
def get_Speed_angle(do_lech):
    if (abs(do_lech) > 6.0):
        angle=45
        speed=10
    elif (abs(do_lech) > 5.5):
        angle=40
        speed=15
    elif (abs(do_lech) > 5.0):
        angle=35
        speed=18
    elif (abs(do_lech) > 4.5):
        angle=30
        speed=30
    elif (abs(do_lech) > 4.0):
        angle=25
        speed=35
    elif (abs(do_lech) > 3.5):
        angle=20
        speed=40
    elif (abs(do_lech) > 3.0):
        angle=15
        speed=45
    elif (abs(do_lech) > 2.5):
        angle=10
        speed=50
    elif (abs(do_lech) > 2.0):
        angle=8
        speed=55
    elif (abs(do_lech) > 1.0):
        angle=4
        speed=60
    elif (abs(do_lech) > 0.2):
        angle=2
        speed=65
    else:
        angle=0
        speed=80
    if do_lech > 0:
        angle*=(-1)
    return speed,angle