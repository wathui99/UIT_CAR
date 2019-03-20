import numpy as np

#sap xep giam dan theo y
#arr = [[x1,y1],
#       [x2,y2], ...]
def partition_y(arr,low,high): 
    i = ( low-1 )         # index of smaller element 
    pivot = arr[high][1]     # pivot 
  
    for j in range(low , high): 
  
        # If current element is smaller than or 
        # equal to pivot 
        if   arr[j][1] >= pivot: 
          
            # increment index of smaller element 
            i = i+1 
            arr[i][1],arr[j][1] = arr[j][1],arr[i][1]
            arr[i][0],arr[j][0] = arr[j][0],arr[i][0] 
  
    arr[i+1][1],arr[high][1] = arr[high][1],arr[i+1][1]
    arr[i+1][0],arr[high][0] = arr[high][0],arr[i+1][0]
    return ( i+1 )
  
# Function to do Quick sort 
def quickSort_y(arr,low,high): 
    if low < high: 
  
        # pi is partitioning index, arr[p] is now 
        # at right place 
        pi = partition_y(arr,low,high) 
  
        # Separately sort elements before 
        # partition and after partition 
        quickSort_y(arr, low, pi-1) 
        quickSort_y(arr, pi+1, high)

#sap xep giam dan theo x
#arr = [[x1,y1],
#       [x2,y2], ...]
def partition_x(arr,low,high): 
    i = ( low-1 )         # index of smaller element 
    pivot = arr[high][0]     # pivot 
  
    for j in range(low , high): 
  
        # If current element is smaller than or 
        # equal to pivot 
        if   arr[j][0] >= pivot: 
          
            # increment index of smaller element 
            i = i+1 
            arr[i][1],arr[j][1] = arr[j][1],arr[i][1]
            arr[i][0],arr[j][0] = arr[j][0],arr[i][0] 
  
    arr[i+1][1],arr[high][1] = arr[high][1],arr[i+1][1]
    arr[i+1][0],arr[high][0] = arr[high][0],arr[i+1][0]
    return ( i+1 )
  
# Function to do Quick sort 
def quickSort_x(arr,low,high): 
    if low < high: 
  
        # pi is partitioning index, arr[p] is now 
        # at right place 
        pi = partition_x(arr,low,high) 
  
        # Separately sort elements before 
        # partition and after partition 
        quickSort_x(arr, low, pi-1) 
        quickSort_x(arr, pi+1, high) 

def do_lech_line(arr):
        ret=0
        for i in range(0, arr.shape[0]-1):
                ret+=arr[i][0]-arr[i+1][0]
        return ret
        
def remove_X(arr, left_or_right):
        if do_lech_line(arr) < 0:
                i=0
                while i < arr.shape[0]-1:
                        if (arr[i][1]==arr[i+1][1]):
                                if left_or_right==1: #line ben phai
                                        if(arr[i][0]< arr[i+1][0]):
                                                arr=np.delete(arr,i+1,0)
                                        else:
                                                arr=np.delete(arr,i,0)
                                elif left_or_right==0: #line ben trai
                                        if(arr[i][0]> arr[i+1][0]):
                                                arr=np.delete(arr,i+1,0)
                                        else:
                                                arr=np.delete(arr,i,0)
                                else: #midpoint
                                        if(arr[i][0]> arr[i+1][0]):
                                                arr=np.delete(arr,i+1,0)
                                        else:
                                                arr=np.delete(arr,i,0)
                                continue
                        i+=1
        else:
                i=0
                while i < arr.shape[0]-1:
                        if (arr[i][1]==arr[i+1][1]):
                                if left_or_right==1: #line ben phai
                                        if(arr[i][0] > arr[i+1][0]):
                                                arr=np.delete(arr,i+1,0)
                                        else:
                                                arr=np.delete(arr,i,0)
                                elif left_or_right==0: #line ben trai
                                        if(arr[i][0] < arr[i+1][0]):
                                                arr=np.delete(arr,i+1,0)
                                        else:
                                                arr=np.delete(arr,i,0)
                                else: #midpoint
                                        if(arr[i][0] > arr[i+1][0]):
                                                arr=np.delete(arr,i+1,0)
                                        else:
                                                arr=np.delete(arr,i,0)
                                continue
                        i+=1
        return arr
                                
                        


