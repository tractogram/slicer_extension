# -*- coding: utf-8 -*-
"""
Created on 2016-12-20

@author: YE WU and Jianzhong He
"""
import numpy as np
import nibabel as nib
from dipy.viz import window, actor
from dipy.tracking.streamline import transform_streamlines
from nibabel import trackvis as tv
from dipy.viz import fvtk

class FileError(Exception):
	""" Error in  streamline file
	"""

def transform(streamlines, affine):
	"""Apply affine transformation to streamlines

	Parameter
	-----------
	streamlines : list,
		streamlines matrix
	affine : (4, 4) array-like,
		Homogenous affine

	Returns
	--------
	new_streamlines : list,
		List of the transformed
	"""
	new_streamlines = []
	lin = affine[:3, :3]
	offset = affine[:3, 3]
	for s in streamlines:
		s = s + offset
		new_streamlines.append(s)
	bundle_native = transform_streamlines(new_streamlines, np.linalg.inv(affine))

	return bundle_native

def color(streamfile, pigment, bar=True, hue=(0.8,0), saturation=(1,1)):
	"""Paint streamline

	Parameter
	-----------
	streamfile : trk,
		trk file path.
	pigment : Nifti file path
		nii file(3D).
	bar : bool,
		color bar.
	hue : tuple of floats,
		HSV values (min 0 and max 1). Default is (0.8, 0).
	saturation : tuple of floats,
		HSV values (min 0 and max 1). Default is (1, 1).
	"""
	if streamfile[-3:] != 'trk':
		raise FileError('Streamline file suffix must be .trk')
	streams, hdr = tv.read(streamfile)
	streamlines = [s[0] for s in streams]
	pigment_img = nib.load(pigment)
	pigment_data = pigment_img.get_data()
	affine = pigment_img.get_affine()
	lut_cmap = actor.colormap_lookup_table(hue_range=hue, saturation_range=saturation)
	if np.ndim(pigment_data) != 3:
		raise ValueError("Input array can only be 3d")
	'''
	vol_actor1 = fvtk.slicer(pigment_data)
	vol_actor1.display(None, None, 38)
	vol_actor2 = fvtk.slicer(pigment_data)
	vol_actor2.display(None, 53, None)
	vol_actor3 = fvtk.slicer(pigment_data)
	vol_actor3.display(40, None, None)
	'''
	new_streamlines = transform(streamlines, affine)
	stream_actor = actor.line(new_streamlines, pigment_data, linewidth=0.1, lookup_colormap=lut_cmap)
	renderer = window.Renderer()
	renderer.add(stream_actor)
	'''
	renderer.add(vol_actor1)
	renderer.add(vol_actor2)
	renderer.add(vol_actor3)
	'''
	if bar:
		bar = actor.scalar_bar(lut_cmap)
		renderer.add(bar)
	fvtk.show(renderer)

#test
streamfile = 'test.trk'
pigment = 'test.nii.gz'
bar = False
color(streamfile, pigment, bar)
