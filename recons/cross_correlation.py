import numpy as np
import scipy.signal as sig
import matplotlib.pyplot as plt
from pathlib import Path
import os
import tifffile as ti

un = "" # change this from "" to "un" to change from stabilized images to unstabilized
out_name1 = un + "stable8.tiff" # name that the output images are named
out_name2 = un + "stable9.tiff"

psi = 'psi.tiff'
im1 = np.array(ti.imread(Path(os.getcwd(), os.path.dirname(__file__), un+'stabilized8', psi)))
im2 = np.array(ti.imread(Path(os.getcwd(), os.path.dirname(__file__), un+'stabilized9', psi)))


# These images have high backgrounds, this will help fix problems that come from that
im1 = im1 - np.average(im1)
im2 = im2 - np.average(im2)

if False: # test to make sure this code works by adding huge obvious shift
    im2[:,:-100] = im2[:,100:]

    f, ax = plt.subplots(1,2)
    ax[0].imshow(im1)
    ax[1].imshow(im2)
    plt.show()



# Crops image
def CropImage(img,crop):
    return img[crop[0][0]:crop[0][1] , crop[1][0]:crop[1][1]]

# Shows what region of the image will be cropped, given the coordinates
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

small_tester = (567, 20, 550, 20)
entire_star = (300, 650, 350, 600) # unstabilized 2
crisp_center23 = (555, 165, 550, 165)
crisp_center45 = (540,165,530,165)
crisp_center67 = (560,145,550,145)
crisp_center89 = (550,155,540,155)


top, vrad, left, hrad = crisp_center89

im1_cropping = ((top,top+vrad),(left,left+hrad))


if False: # used for cropping down to desired region: shouldn't need to go on until that region is finalized
    CropImageThenShow(im1, im1_cropping)
    exit()


# ------------------------------------------------------------------------------------------------------------------
# Now that the images are extracted, and image 1 is cropped down to the region of interest, time to cross-correlate!

print ("starting correlation")
correlate_arr = sig.correlate(im2, im1, method='fft')
peak_index = np.unravel_index(correlate_arr.argmax(), correlate_arr.shape)
dif = tuple(map(lambda x,y: x-y, peak_index, im2.shape))
print ("finished correlation - shifting by", dif, "pixels")


orig_im1 = im1
im1 = CropImage(im1, im1_cropping)
orig_im2 = im2
im2 = CropImage(im2, ((top+dif[0],top+dif[0]+vrad), (left+dif[1], left+dif[1]+hrad)))


if True: # Plot correlated images side by side
    f, ax = plt.subplots(1,2)
    ax[0].imshow(im1)
    ax[1].imshow(im2)
    plt.show()

# Save images as tiff images for FRC analysis
if True:
    ti.imwrite(Path(os.getcwd(), os.path.dirname(__file__), 'Correlated Images', out_name1), im1)
    ti.imwrite(Path(os.getcwd(), os.path.dirname(__file__), 'Correlated Images', out_name2), im2)

