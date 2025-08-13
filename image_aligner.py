"""image alignement"""
import numpy as np
import cv2
import matplotlib.pyplot as plt

def align(base_img_path, unaligned_img_path, saveFilePath = None):
    
    aligned = cv2.imread(base_img_path, cv2.IMREAD_COLOR)
    unaligned = cv2.imread(unaligned_img_path, cv2.IMREAD_COLOR)

    #resizing unaligned
    height,width,channel = aligned.shape
    unaligned = cv2.resize(unaligned, (width,height))

    #make key points detector
    orb = cv2.ORB_create(500)
    #make feture matcher
    matcher = cv2.DescriptorMatcher_create(
        cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)

    #get keypnts and desc
    keypnts_al, desc_al = orb.detectAndCompute(aligned,None)
    keypnts_ual, desc_ual = orb.detectAndCompute(unaligned,None)

    #match desc
    matches = list(matcher.match(desc_al, desc_ual))
    #sort them so best matches are first
    matches.sort(key = lambda x: x.distance, reverse = False)
    #keep 10% of best matches
    matches = matches[:int(len(matches)*0.1)]

    #get position of best matches
    pnts_al = np.empty((len(matches),2))
    pnts_ual = np.empty((len(matches),2))

    for i,match in enumerate(matches):
        pnts_al[i,:] = keypnts_al[match.queryIdx].pt
        pnts_ual[i,:] = keypnts_ual[match.trainIdx].pt

    #get homoraphy
    h,mask = cv2.findHomography(pnts_ual, pnts_al, cv2.RANSAC)

    #align image :)
    res = cv2.warpPerspective(unaligned,h,(width,height))

    #save img
    if(saveFilePath):
        cv2.imwrite(saveFilePath, res)

    #show res :)
    plt.subplot(131);plt.title("unaligned");plt.imshow(unaligned)
    plt.subplot(132);plt.title("base img");plt.imshow(aligned)
    plt.subplot(133);plt.title("aligned");plt.imshow(res)
    plt.show()
