import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import nibabel as nib
import scipy.ndimage





class ArrayView(object):

    
    # Ported from the Python2 code found in:
    # http://nbarbey.github.io/2011/07/08/matplotlib-slider.html



    # remove erroneous line breaks
    def view3DArray(cube, axis=2, **kwargs):

        
        # generate figure
        fig = plt.figure()
        ax = plt.subplot(111)
        fig.subplots_adjust(left=0.25, bottom=0.25)
    
        # select first image
        s = [slice(0, 1) if i == axis else slice(None) for i in range(3)]
        im = cube[tuple(s)].squeeze()
    
        # display imagecc
        l = ax.imshow(im)
        fig.colorbar(l, ax=ax)
        # define slider


        ax = fig.add_axes([0.25, 0.1, 0.65, 0.03]) #  , axisbg=axcolor)
    
        slider = Slider(ax, 'Axis %i index' % axis, 0, cube.shape[axis] - 1, valinit=0, valfmt='%i')
    
        def update(val):
            ind = int(slider.val)
            s = [slice(ind, ind + 1) if i == axis else slice(None) for i in range(3)]
            im = cube[tuple(s)].squeeze()
            l.set_data(im )
            fig.canvas.draw()
    
        slider.on_changed(update)
    
        plt.show()
        
        
        
if __name__ == "__main__":

    data = nib.load(r"C:\Users\Utilisateur\OneDrive - ABYS MEDICAL\Bureau\projet\DataAugmentation\data\Test_Patient2.nii.gz").get_fdata()

    #visualization 3D
    ArrayView.view3DArray(data)

