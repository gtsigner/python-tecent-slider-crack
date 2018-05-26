#!/usr/bin/env python    
# encoding: utf-8    
import cv2    
import numpy as np   
import pandas as pd 
import matplotlib.pyplot as plt  
import math 

# x方向一阶导中值
def get_dx_median(dx,x,y,w,h):
    return np.median(dx[y:(y+h),x])    

# 预处理
def pre_process(img_path):         
    img = cv2.imread(img_path,1)     
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV) 
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)  # 转成灰度图像  

    dx = cv2.Sobel(img,-1,1,0,ksize=5) 
    dy = cv2.Sobel(img,-1,0,1,ksize=5)   
    h,w = img.shape[:2]   
      
    ret, binary = cv2.threshold(img_gray,127,255,cv2.THRESH_BINARY) #将灰度图像转成二值图像     
    # binary = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,3,7)  
    _,contours, hierarchy = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) # 查找轮廓   
    #cv2.drawContours(gray,contours,-1,(255,255,255),2)    
    
    gray = np.zeros_like(img_gray) 
    cv2.drawContours(gray,contours,-1,(0,0,255),1)    
     
    gray = np.zeros_like(gray) 
    rect_area = []
    rect_arclength = []  
    cnt_infos = {}

    colors = plt.cm.Spectral(np.linspace(0, 1, len(contours)))  
    for i,cnt in enumerate(contours): 
        if cv2.contourArea(cnt) < 5000  or cv2.contourArea(cnt) > 25000:
            continue  

        x, y, w, h = cv2.boundingRect(cnt)  
        cnt_infos[i] = {'rect_area': w*h,  # 矩形面积
                        'rect_arclength': 2*(w+h), #矩形周长
                        'cnt_area':cv2.contourArea(cnt) , #轮廓面积
                        'cnt_arclength':cv2.arcLength(cnt,True) , #轮廓周长
                        'cnt':cnt , #轮廓
                        'w':w,
                        'h':h,
                        'x':x,
                        'y':y,
                        'mean':np.mean(np.min(img[y:(y+h),x:(x+w)],axis=2)), # 矩形内像素平均
                       }  
        rect_area.append(w*h)   
        rect_arclength.append(2*(w+h))  
        cv2.rectangle(img, (x, y), (x+w, y+h), colors[i], 1)  
        
    # plt.imshow(img)  
    return img,dx,cnt_infos

def qq_mark_detect(img_path):
    img,dx,cnt_infos = pre_process(img_path) 
    h,w = img.shape[:2]   
    df = pd.DataFrame(cnt_infos).T 
    df.head() 
    df['dx_mean']=df.apply(lambda x : get_dx_median(dx,x['x'],x['y'],x['w'],x['h']),axis=1)    
    df['rect_ratio']= df.apply(lambda v:v['rect_arclength']/4/math.sqrt(v['rect_area']+1) ,axis = 1)  
    df['area_ratio']= df.apply(lambda v:v['rect_area']/v['cnt_area'] ,axis = 1)  
    # df.query('w>100').query('h>100').sort_values('area_ratio') 
    df['score'] = df.apply(lambda x: abs(x['rect_ratio']-1),axis=1)      
    result = df.query('x>0').query('area_ratio<2').query('rect_area>5000').query('rect_area<20000').sort_values(['mean','score','dx_mean']).head(2) 
    #print(result)
    if len(result):
        x_left=result.x.values[0]
        cv2.line(img,(x_left,0),(x_left,h),color=(255,0,255))
        plt.imshow(img)  
        plt.show() 
    return result 

if __name__ == "__main__":
    img_path =  "/Users/robin/Downloads/txy02.jpg"   
    res = qq_mark_detect(img_path)
    print(res.x) 

