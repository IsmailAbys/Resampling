import os
import torch
import glob
import numpy as np
import scipy.ndimage
import nibabel as nib
from torchvision import transforms
from torch.utils.data import Dataset


path_dir_train = "__path__"
os.environ["KMP_DUPLICATE_LIB_OK"] = "True"
images_train = sorted(glob.glob(os.path.join(path_dir_train,  "*.nii.gz")))




class MyDataset(Dataset):
    def __init__(self, path):
        # load all nii handle in a list
        self.images_list = [nib.load(image_path) for image_path in path]
    
    def __len__(self):
        return len(self.images_list)

    def __getitem__(self, idx):
        nii_image = self.images_list[idx]
        data = np.asarray(nii_image.dataobj)
        return data

train_data = MyDataset(images_train)

train_data = list(train_data)

################################ z mean #######################################################
# compute z_mean
def z_mean(data):
    z = []
    for i in range(len(data)):
        z_ = data[i].shape[2]
        z.append(z_)
    
    z = np.asarray(z)
    
    z_Mean = np.mean(z)

    return z_Mean

z_m = z_mean(train_data)

################################################ Resampling with z mean ####################################
# compute the scale foctor of each image
def z_scale_factor(data):
    z_scale_factors = []
    scale_factors = []
    for i in range(len(data)):

        z_sc_f = z_m / data[i].shape[2]
        z_scale_factors.append(z_sc_f)


    for i in range(len(data)):
        scale_factor = [1, 1, z_scale_factors[i]]
        scale_factors.append(scale_factor)
    return scale_factors


scale_factors = z_scale_factor(train_data)
scale_factors = np.asarray(np.asarray(scale_factors))


# resampling
def resampling(data):
    zoom_factors = []
    data_list = []
    for i in range(len(train_data)):
        new_shape = data[i].shape * scale_factors[i]
        new_shape = np.round(new_shape)
        
        zoom_factor = new_shape / data[i].shape
        zoom_factors.append(zoom_factor)
    
        data_ = scipy.ndimage.zoom(data[i], zoom_factors[i], order=1, prefilter=True) 
        data_list.append(data_)
    return data_list

resampled_data = resampling(train_data)


index = np.random.randint(0, len(resampled_data)-1)
nifti_file = nib.Nifti1Image(resampled_data[index], np.eye(4))
nib.save(nifti_file, os.path.join("output path to save the resampled image", '__filname__.nii.gz')) 
