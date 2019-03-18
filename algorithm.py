import numpy as np

#sap xep giam dan theo y
#arr = [[x1,y1],
#       [x2,y2], ...]
def partition(arr,low,high): 
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
def quickSort(arr,low,high): 
    if low < high: 
  
        # pi is partitioning index, arr[p] is now 
        # at right place 
        pi = partition(arr,low,high) 
  
        # Separately sort elements before 
        # partition and after partition 
        quickSort(arr, low, pi-1) 
        quickSort(arr, pi+1, high) 

def do_lech_line(arr):
        ret=0
        for i in range(0, arr.shape[0]-1):
                ret+=arr[i][0]-arr[i+1][0]
        return ret
