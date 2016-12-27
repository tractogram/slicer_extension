import os
import sys
import types
import nibabel as nib
import numpy as np
import dipy.reconst.dti as dti
from dipy.viz.colormap import line_colors
from dipy.viz import fvtk
from os.path import join as pjoin
from dipy.denoise.nlmeans import nlmeans
from dipy.core.gradients import gradient_table
from dipy.io.gradients import read_bvals_bvecs
from dipy.denoise.noise_estimate import estimate_sigma
from dipy.direction import peaks_from_model
from dipy.reconst.csdeconv import ConstrainedSphericalDeconvModel
from dipy.reconst.csdeconv import auto_response
from dipy.tracking.eudx import EuDX
from dipy.data import get_sphere
from dipy.tracking import utils
from dipy.io.trackvis import save_trk
from dipy.tracking.local import LocalTracking
from dipy.tracking.local import ThresholdTissueClassifier
from dipy.reconst.dti import fractional_anisotropy

fraw = '/Users/nandatetadashi/Desktop/HARDI/HARDI150/HARDI150.nii'
fbval = '/Users/nandatetadashi/Desktop/HARDI/HARDI150.bval'
fbvec = '/Users/nandatetadashi/Desktop/HARDI/HARDI150.bvec'
fmask = '/Users/nandatetadashi/Desktop/HARDI/aparc-reduced.nii.gz'

img = nib.load(fraw)
mask_img = nib.load(fmask)
bvals, bvecs = read_bvals_bvecs(fbval, fbvec)
sphere = get_sphere('symmetric724')
data = img.get_data()
mask = mask_img.get_data()
affine = img.get_affine()
zooms = img.get_header().get_zooms()[:3]
gtab = gradient_table(bvals, bvecs)

response, ratio = auto_response(gtab, data, roi_radius=10, fa_thr=0.7)

tenmodel = dti.TensorModel(gtab)
tenfit = tenmodel.fit(data, mask=data[..., 0] > 200)


FA = fractional_anisotropy(tenfit.evals)
csd_model = ConstrainedSphericalDeconvModel(gtab, response)
csdpeaks = peaks_from_model(model=csd_model,
                             data=data,
                             sphere=sphere,
                             mask=mask,
                             relative_peak_threshold=.5,
                             min_separation_angle=25,
                             parallel=False)

eu = EuDX(csdpeaks.gfa,
          csdpeaks.peak_indices[..., 0],
          seeds=10000,
          odf_vertices=sphere.vertices,
          a_low=0.2)
csd_streamlines = [streamline for streamline in eu]
hdr = nib.trackvis.empty_header()
hdr['voxel_size'] = (2., 2., 2.)
hdr['voxel_order'] = 'LAS'
hdr['dim'] = csdpeaks.gfa.shape[:3]

csd_streamlines_trk = ((sl, None, None) for sl in csd_streamlines)
csd_sl_fname = 'test.trk'
nib.trackvis.write(csd_sl_fname, csd_streamlines_trk, hdr, points_space='voxel')

FA_img = nib.Nifti1Image(FA.astype(np.float32), affine)
FA_file = 'test.nii.gz'
nib.save(FA_img, FA_file)
