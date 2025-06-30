import numpy as np
import scipy.signal as sig
import matplotlib.pyplot as plt
from pathlib import Path
import os
from PIL import Image as im

out_name1 = "unstable2.tiff" # name that the output images are named
out_name2 = "unstable3.tiff"

psi = 'psi.tiff'
im1 = im.open(Path(os.getcwd(), os.path.dirname(__file__), 'unstabilized2', psi))
im2 = im.open(Path(os.getcwd(), os.path.dirname(__file__), 'unstabilized3', psi))

breakpoint() # 

im1 = np.array(im1, dtype='int32')
im2 = np.array(im2, dtype='int32')

def CropImage(img,crop):
    return img[crop[0][0]:crop[0][1] , crop[1][0]:crop[1][1]]

def CropImageThenShow(img,crop):
    outlined_img = np.copy(img) # let's make a box around the cropped region
    mx = np.max(img) # used to draw the box lines on the graph
    n = int(img.shape[0]*.002) # how thick to make the lines
    outlined_img[crop[0][0]:crop[0][1] , crop[1][0]-n:crop[1][0]+n] = mx
    outlined_img[crop[0][0]:crop[0][1] , crop[1][1]-n:crop[1][1]+n] = mx
    outlined_img[crop[0][0]-n:crop[0][0]+n , crop[1][0]:crop[1][1]] = mx
    outlined_img[crop[0][1]-n:crop[0][1]+n , crop[1][0]:crop[1][1]] = mx

    f,ax = plt.subplots(1,2, figsize=(10,5))
    ax[0].imshow(outlined_img) # plot the entire image, with the cropped part outlined
    ax[1].imshow(CropImage(img,crop)) # plot only the cropped region
    plt.show()





# crop im1 to the desired region, and we'll crop im2 after cross-correlation
# ((top,bottom),(left,right))
top, vrad, left, hrad = (555, 165, 550, 165) #(300, 650, 350, 600) # unstabilized 2
im1_cropping = ((top,top+vrad),(left,left+hrad))


if False: # used for cropping down to desired region: shouldn't need to go on until that region is finalized
    CropImageThenShow(im1, im1_cropping)
    exit()

orig_im1 = im1
im1 = CropImage(im1,im1_cropping)


# ------------------------------------------------------------------------------------------------------------------
# Now that the images are extracted, and image 1 is cropped down to the region of interest, time to cross-correlate!

print ("starting correlation")
correlate_arr = sig.correlate2d(im2, im1, mode='valid')
print ("finished correlation")

peak_index = np.unravel_index(correlate_arr.argmax(), correlate_arr.shape)
print("Max correlation at", peak_index)

orig_im2 = im2
im2 = CropImage(im2, ((peak_index[0], peak_index[0]+vrad), (peak_index[1], peak_index[1]+hrad)))

if True: # Plot correlated images side by side
    f, ax = plt.subplots(1,2)
    ax[0].imshow(im1)
    ax[1].imshow(im2)
    plt.show()

if True:
    out1 = im.fromarray(im1)
    out2 = im.fromarray(im2)
    out1.save(Path(os.getcwd(), os.path.dirname(__file__), 'Correlated Images', out_name1), 'TIFF')
    out2.save(Path(os.getcwd(), os.path.dirname(__file__), 'Correlated Images', out_name2), 'TIFF')

breakpoint()

