# -*- coding: utf-8 -*-
"""
Created on 2016-12-20

@author: YE WU and Jianzhong He
"""
from nibabel import trackvis as tv
from dipy.tracking.eudx import EuDX
from dipy.reconst import peaks, shm
from dipy.tracking import utils
import matplotlib.pyplot as plt
import numpy as np
import nibabel as nib

def Cal_connectivity(fraw, streamfile, fmask, num):
	"""Paint streamline

	Parameter
	-----------
	fraw : str,
		data file path(use for track).
	streamfile : trk,
		trk file path.
	fmask : str,
		mask file path.
	num : int,
		brain region num.
	"""
	img = nib.load(fraw)
	affine  = img.get_affine()
	label_img = nib.load(fmask)
	label = label_img.get_data()
	tar_slice = label == num

	streams, hdr = tv.read(streamfile)
	streamlines = [s[0] for s in streams]
	tar_streamlines = utils.target(streamlines, tar_slice, affine=affine)
	tar_streamlines = list(tar_streamlines)
	
	M, grouping = utils.connectivity_matrix(tar_streamlines, label, 
							 affine=affine,
							 return_mapping=True,
							 mapping_as_streamlines=True)
	M[:3, :] = 0
	M[:, :3] = 0
	plt.imshow(np.log1p(M), interpolation='nearest')
	plt.show()


#test
fraw = 'HARDI150.nii'
streamfile = 'test.trk'
fmask = 'test_mask.nii.gz'
num = 2
Cal_connectivity(fraw, streamfile, fmask, num)
