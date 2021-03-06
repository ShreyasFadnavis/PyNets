#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 10:40:07 2017
Copyright (C) 2017
@author: Derek Pisner
"""
import os
import nibabel as nib
import warnings
import indexed_gzip
import numpy as np
from pynets.registration import reg_utils as regutils
from nilearn.image import math_img
from nilearn.masking import intersect_masks
warnings.filterwarnings("ignore")
try:
    FSLDIR = os.environ['FSLDIR']
except KeyError:
    print('FSLDIR environment variable not set!')


def direct_streamline_norm(streams, fa_path, ap_path, dir_path, track_type, target_samples, conn_model, network,
                           node_size, dens_thresh, ID, roi, min_span_tree, disp_filt, parc, prune, atlas,
                           labels_im_file, uatlas, labels, coords, norm, binary, atlas_mni, basedir_path,
                           curv_thr_list, step_list, directget, min_length, error_margin):
    """
    A Function to perform normalization of streamlines tracked in native diffusion space to an
    FA template in MNI space.

    Parameters
    ----------
    streams : str
        File path to save streamline array sequence in .trk format.
    fa_path : str
        File path to FA Nifti1Image.
    ap_path : str
        File path to the anisotropic power Nifti1Image.
    dir_path : str
        Path to directory containing subject derivative data for a given pynets run.
    track_type : str
        Tracking algorithm used (e.g. 'local' or 'particle').
    target_samples : int
        Total number of streamline samples specified to generate streams.
    conn_model : str
        Connectivity reconstruction method (e.g. 'csa', 'tensor', 'csd').
    network : str
        Resting-state network based on Yeo-7 and Yeo-17 naming (e.g. 'Default')
        used to filter nodes in the study of brain subgraphs.
    node_size : int
        Spherical centroid node size in the case that coordinate-based centroids
        are used as ROI's for tracking.
    dens_thresh : bool
        Indicates whether a target graph density is to be used as the basis for
        thresholding.
    ID : str
        A subject id or other unique identifier.
    roi : str
        File path to binarized/boolean region-of-interest Nifti1Image file.
    min_span_tree : bool
        Indicates whether local thresholding from the Minimum Spanning Tree
        should be used.
    disp_filt : bool
        Indicates whether local thresholding using a disparity filter and
        'backbone network' should be used.
    parc : bool
        Indicates whether to use parcels instead of coordinates as ROI nodes.
    prune : bool
        Indicates whether to prune final graph of disconnected nodes/isolates.
    atlas : str
        Name of atlas parcellation used.
    labels_im_file : str
        File path to atlas parcellation Nifti1Image aligned to dwi space.
    uatlas : str
        File path to atlas parcellation Nifti1Image in MNI template space.
    labels : list
        List of string labels corresponding to graph nodes.
    coords : list
        List of (x, y, z) tuples corresponding to a coordinate atlas used or
        which represent the center-of-mass of each parcellation node.
    norm : int
        Indicates method of normalizing resulting graph.
    binary : bool
        Indicates whether to binarize resulting graph edges to form an
        unweighted graph.
    atlas_mni : str
        File path to atlas parcellation Nifti1Image in T1w-warped MNI space.
    basedir_path : str
        Path to directory to output direct-streamline normalized temp files and outputs.
    curv_thr_list : list
        List of integer curvature thresholds used to perform ensemble tracking.
    step_list : list
        List of float step-sizes used to perform ensemble tracking.
    directget : str
        The statistical approach to tracking. Options are: det (deterministic),
        closest (clos), boot (bootstrapped), and prob (probabilistic).
    min_length : int
        Minimum fiber length threshold in mm to restrict tracking.
    error_margin : int
        Distance (in the units of the streamlines, usually mm). If any
        coordinate in the streamline is within this distance from the center
        of any voxel in the ROI, the filtering criterion is set to True for
        this streamline, otherwise False. Defaults to the distance between
        the center of each voxel and the corner of the voxel.

    Returns
    -------
    streams_warp : str
        File path to normalized streamline array sequence in .trk format.
    dir_path : str
        Path to directory containing subject derivative data for a given pynets run.
    track_type : str
        Tracking algorithm used (e.g. 'local' or 'particle').
    target_samples : int
        Total number of streamline samples specified to generate streams.
    conn_model : str
        Connectivity reconstruction method (e.g. 'csa', 'tensor', 'csd').
    network : str
        Resting-state network based on Yeo-7 and Yeo-17 naming (e.g. 'Default')
        used to filter nodes in the study of brain subgraphs.
    node_size : int
        Spherical centroid node size in the case that coordinate-based centroids
        are used as ROI's for tracking.
    dens_thresh : bool
        Indicates whether a target graph density is to be used as the basis for
        thresholding.
    ID : str
        A subject id or other unique identifier.
    roi : str
        File path to binarized/boolean region-of-interest Nifti1Image file.
    min_span_tree : bool
        Indicates whether local thresholding from the Minimum Spanning Tree
        should be used.
    disp_filt : bool
        Indicates whether local thresholding using a disparity filter and
        'backbone network' should be used.
    parc : bool
        Indicates whether to use parcels instead of coordinates as ROI nodes.
    prune : bool
        Indicates whether to prune final graph of disconnected nodes/isolates.
    atlas : str
        Name of atlas parcellation used.
    uatlas : str
        File path to atlas parcellation Nifti1Image in MNI template space.
    labels : list
        List of string labels corresponding to graph nodes.
    coords : list
        List of (x, y, z) tuples corresponding to a coordinate atlas used or
        which represent the center-of-mass of each parcellation node.
    norm : int
        Indicates method of normalizing resulting graph.
    binary : bool
        Indicates whether to binarize resulting graph edges to form an
        unweighted graph.
    atlas_mni : str
        File path to atlas parcellation Nifti1Image in T1w-warped MNI space.
    directget : str
        The statistical approach to tracking. Options are: det (deterministic), closest (clos), boot (bootstrapped),
        and prob (probabilistic).
    warped_fa : str
        File path to MNI-space warped FA Nifti1Image.
    min_length : int
        Minimum fiber length threshold in mm to restrict tracking.
    error_margin : int
        Distance (in the units of the streamlines, usually mm). If any
        coordinate in the streamline is within this distance from the center
        of any voxel in the ROI, the filtering criterion is set to True for
        this streamline, otherwise False. Defaults to the distance between
        the center of each voxel and the corner of the voxel.
    References
    ----------
    .. [1] Greene, C., Cieslak, M., & Grafton, S. T. (2017). Effect of different
      spatial normalization approaches on tractography and structural
      brain networks. Network Neuroscience, 1-19.

    """
    import gc
    from dipy.tracking import utils
    from dipy.tracking.streamline import values_from_volume, transform_streamlines, Streamlines
    from pynets.registration import reg_utils as regutils
    from dipy.tracking._utils import _mapping_to_voxel
    from dipy.io.stateful_tractogram import Space, StatefulTractogram, Origin
    from dipy.io.streamline import save_tractogram
    # from pynets.plotting import plot_gen
    import pkg_resources
    import yaml
    import os.path as op
    from nilearn.image import resample_to_img
    from dipy.io.streamline import load_tractogram
    # from pynets.core.utils import missing_elements

    with open(pkg_resources.resource_filename("pynets", "runconfig.yaml"), 'r') as stream:
        try:
            hardcoded_params = yaml.load(stream)
            template_name = hardcoded_params['template'][0]
        except FileNotFoundError:
            print('Failed to parse runconfig.yaml')
    stream.close()

    dsn_dir = f"{basedir_path}/dmri_reg/DSN"
    if not op.isdir(dsn_dir):
        os.mkdir(dsn_dir)

    namer_dir = f"{dir_path}/tractography"
    if not op.isdir(namer_dir):
        os.mkdir(namer_dir)

    atlas_img = nib.load(labels_im_file)

    # Run SyN and normalize streamlines
    fa_img = nib.load(fa_path)
    vox_size = fa_img.header.get_zooms()[0]
    template_path = pkg_resources.resource_filename("pynets", f"templates/FA_{int(vox_size)}mm.nii.gz")
    template_anat_path = pkg_resources.resource_filename("pynets",
                                                         f"templates/{template_name}_brain_{int(vox_size)}mm.nii.gz")
    template_img = nib.load(template_path)
    brain_mask = np.asarray(template_img.dataobj).astype('bool')
    template_img.uncache()

    uatlas_mni_img = nib.load(uatlas)

    streams_mni = "%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s" % (namer_dir, '/streamlines_mni_',
                                                              '%s' % (network + '_' if network is not
                                                                                       None else ''),
                                                              '%s' % (op.basename(roi).split('.')[0] + '_'
                                                                      if roi is not None else ''),
                                                              conn_model, '_', target_samples,
                                                              '%s' % ("%s%s" % ('_' +
                                                                                str(node_size), 'mm_') if
                                                                      ((node_size != 'parc') and
                                                                       (node_size is not None)) else '_'),
                                                              'curv', str(curv_thr_list).replace(', ', '_'),
                                                              'step', str(step_list).replace(', ', '_'),
                                                              'tt-', track_type, '_dg-', directget, '_ml-',
                                                              min_length, '.trk')

    density_mni = "%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s" % (namer_dir, '/density_map_mni_',
                                                              '%s' % (network + '_' if network is not None else ''),
                                                              '%s' % (op.basename(roi).split('.')[0] + '_' if
                                                                      roi is not None else ''),
                                                              conn_model, '_', target_samples,
                                                              '%s' % ("%s%s" % ('_' + str(node_size), 'mm_') if
                                                                      ((node_size != 'parc') and (node_size is not
                                                                                                  None)) else '_'),
                                                              'curv', str(curv_thr_list).replace(', ', '_'),
                                                              'step', str(step_list).replace(', ', '_'), 'tt-',
                                                              track_type,
                                                              '_dg-', directget, '_ml-', min_length, '.nii.gz')

    # streams_warp_png = "%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s" % (dsn_dir, '/streamlines_mni_warp_',
    #                                                                '%s' % (network + '_' if network is not
    #                                                                                         None else ''),
    #                                                                '%s' % (op.basename(roi).split('.')[0] + '_' if
    #                                                                        roi is not None else ''),
    #                                                                conn_model, '_', target_samples,
    #                                                                '%s' % ("%s%s" %
    #                                                                        ('_' + str(node_size),
    #                                                                         'mm_') if ((node_size != 'parc') and
    #                                                                                    (node_size is not None)) else
    #                                                                        '_'),
    #                                                                'curv', str(curv_thr_list).replace(', ', '_'),
    #                                                                'step', str(step_list).replace(', ', '_'), 'tt-',
    #                                                                track_type,  '_dg-', directget, '_ml-', min_length,
    #                                                                '.png')

    # SyN FA->Template
    [mapping, affine_map, warped_fa] = regutils.wm_syn(template_path, fa_path, template_anat_path, ap_path, dsn_dir)

    tractogram = load_tractogram(streams, fa_img, to_space=Space.RASMM, to_origin=Origin.TRACKVIS,
                                 bbox_valid_check=False)
    fa_img.uncache()
    streamlines = tractogram.streamlines
    warped_fa_img = nib.load(warped_fa)
    warped_fa_affine = warped_fa_img.affine
    warped_fa_shape = warped_fa_img.shape

    streams_in_curr_grid = transform_streamlines(streamlines, warped_fa_affine)

    ref_grid_aff = vox_size*np.eye(4)
    ref_grid_aff[3][3] = 1

    # Create isocenter mapping where we anchor the origin transformation affine
    # to the corner of the FOV by scaling x, y, z offsets according to a multiplicative
    # van der Corput sequence with a base value equal to the voxel resolution
    def vdc(n, base=vox_size):
        vdc, denom = 0, 1
        while n:
            denom *= base
            n, remainder = divmod(n, base)
            vdc += remainder / denom
        return vdc

    [x_mul, y_mul, z_mul] = [vdc(i) for i in range(1, 4)]

    adjusted_affine = affine_map.affine.copy()
    adjusted_affine[0][3] = -adjusted_affine[0][3]*x_mul
    adjusted_affine[1][3] = -adjusted_affine[1][3]*y_mul
    adjusted_affine[2][3] = -adjusted_affine[2][3]*z_mul

    # Deform streamlines, isocenter, and remove streamlines outside brain
    streams_in_brain = [sum(d, s) for d, s in zip(values_from_volume(mapping.get_forward_field(), streams_in_curr_grid,
                                                                     ref_grid_aff), streams_in_curr_grid)]
    streams_final_filt = Streamlines(utils.target_line_based(
        transform_streamlines(transform_streamlines(streams_in_brain,
                                                    np.linalg.inv(adjusted_affine)),
                              np.linalg.inv(warped_fa_img.affine)), np.eye(4), brain_mask, include=True))

    # Remove streamlines with negative voxel indices
    lin_T, offset = _mapping_to_voxel(np.eye(4))
    streams_final_filt_final = []
    for sl in streams_final_filt:
        inds = np.dot(sl, lin_T)
        inds += offset
        if not inds.min().round(decimals=6) < 0:
            streams_final_filt_final.append(sl)

    # Save streamlines
    stf = StatefulTractogram(streams_final_filt_final, reference=uatlas_mni_img, space=Space.RASMM,
                             origin=Origin.TRACKVIS)
    stf.remove_invalid_streamlines()
    streams_final_filt_final = stf.streamlines
    save_tractogram(stf, streams_mni, bbox_valid_check=True)
    warped_fa_img.uncache()

    # DSN QC plotting
    # plot_gen.show_template_bundles(streams_final_filt_final, template_path, streams_warp_png)

    # Create and save MNI density map
    nib.save(nib.Nifti1Image(utils.density_map(streams_final_filt_final, affine=np.eye(4),
                                               vol_dims=warped_fa_shape), warped_fa_affine), density_mni)

    # Map parcellation from native space back to MNI-space and create an 'uncertainty-union' parcellation
    # with original mni-space uatlas

    warped_uatlas = affine_map.transform_inverse(mapping.transform(np.asarray(atlas_img.dataobj).astype('int'),
                                                                   interpolation='nearestneighbour'),
                                                 interp='nearest')
    atlas_img.uncache()
    warped_uatlas_img_res_data = np.asarray(resample_to_img(nib.Nifti1Image(warped_uatlas,
                                                                            affine=warped_fa_affine),
                                                            uatlas_mni_img, interpolation='nearest',
                                                            clip=False).dataobj)
    uatlas_mni_data = np.asarray(uatlas_mni_img.dataobj)
    uatlas_mni_img.uncache()
    overlap_mask = np.invert(warped_uatlas_img_res_data.astype('bool') * uatlas_mni_data.astype('bool'))
    os.makedirs(f"{dir_path}/parcellations", exist_ok=True)
    atlas_mni = f"{dir_path}/parcellations/{op.basename(uatlas).split('.nii')[0]}_liberal.nii.gz"

    nib.save(nib.Nifti1Image(warped_uatlas_img_res_data * overlap_mask.astype('int') +
                             uatlas_mni_data * overlap_mask.astype('int') +
                             np.invert(overlap_mask).astype('int') *
                             warped_uatlas_img_res_data.astype('int'), affine=uatlas_mni_img.affine), atlas_mni)

    del (tractogram, streamlines, warped_uatlas_img_res_data, uatlas_mni_data, overlap_mask, stf,
         streams_final_filt_final, streams_final_filt, streams_in_curr_grid, brain_mask, streams_in_brain)

    gc.collect()

    assert len(coords) == len(labels)

    # # Correct coords and labels
    # bad_idxs = missing_elements(list(np.unique(np.asarray(nib.load(atlas_mni).dataobj).astype('int'))))
    # bad_idxs = [i-1 for i in bad_idxs]
    # if len(bad_idxs) > 0:
    #     bad_idxs = sorted(list(set(bad_idxs)), reverse=True)
    #     for j in bad_idxs:
    #         del labels[j], coords[j]

    return (streams_mni, dir_path, track_type, target_samples, conn_model, network, node_size, dens_thresh, ID, roi,
            min_span_tree, disp_filt, parc, prune, atlas, uatlas, labels, coords, norm, binary, atlas_mni, directget,
            warped_fa, min_length, error_margin)


class DmriReg(object):
    """
    A Class for Registering an atlas to a subject's MNI-aligned T1w image in native diffusion space.

    References
    ----------
    .. [1] Adluru, N., Zhang, H., Tromp, D. P. M., & Alexander, A. L. (2013).
      Effects of DTI spatial normalization on white matter tract reconstructions.
      Medical Imaging 2013: Image Processing. https://doi.org/10.1117/12.2007130
    .. [2] Greve DN, Fischl B. Accurate and robust brain image alignment using
      boundary-based registration. Neuroimage. 2009 Oct;48(1):63–72.
      doi:10.1016/j.neuroimage.2009.06.060.
    .. [3] Zhang Y, Brady M, Smith S. Segmentation of brain MR images through a
      hidden Markov random field model and the expectation-maximization algorithm.
      IEEE Trans Med Imaging. 2001 Jan;20(1):45–57. doi:10.1109/42.906424.

    """

    def __init__(self, basedir_path, fa_path, ap_path, B0_mask, anat_file, mask, vox_size, template_name, simple):
        import pkg_resources
        import os.path as op
        self.simple = simple
        self.ap_path = ap_path
        self.fa_path = fa_path
        self.B0_mask = B0_mask
        self.t1w = anat_file
        self.mask = mask
        self.vox_size = vox_size
        self.template_name = template_name
        self.t1w_name = 't1w'
        self.dwi_name = 'dwi'
        self.basedir_path = basedir_path
        self.tmp_path = f"{basedir_path}{'/dmri_reg'}"
        self.reg_path = f"{basedir_path}{'/dmri_reg/reg'}"
        self.anat_path = f"{basedir_path}{'/anat_reg'}"
        self.reg_path_mat = f"{self.reg_path}{'/mats'}"
        self.reg_path_warp = f"{self.reg_path}{'/warps'}"
        self.reg_path_img = f"{self.reg_path}{'/imgs'}"
        self.t12mni_xfm_init = f"{self.reg_path_mat}{'/xfm_t1w2mni_init.mat'}"
        self.t12mni_xfm = f"{self.reg_path_mat}{'/xfm_t1w2mni.mat'}"
        self.mni2t1_xfm = f"{self.reg_path_mat}{'/xfm_mni2t1.mat'}"
        self.mni2t1w_warp = f"{self.reg_path_warp}{'/mni2t1w_warp.nii.gz'}"
        self.warp_t1w2mni = f"{self.reg_path_warp}{'/t1w2mni_warp.nii.gz'}"
        self.t1w2dwi = f"{self.reg_path_img}{'/'}{self.t1w_name}{'_in_dwi.nii.gz'}"
        self.t1_aligned_mni = f"{self.reg_path_img}{'/'}{self.t1w_name}{'_aligned_mni.nii.gz'}"
        self.t1w_brain = f"{self.anat_path}{'/'}{self.t1w_name}{'_brain.nii.gz'}"
        self.t1w_head = f"{self.anat_path}{'/'}{self.t1w_name}{'_head.nii.gz'}"
        self.t1w_brain_mask = f"{self.anat_path}{'/'}{self.t1w_name}{'_brain_mask.nii.gz'}"
        self.t1w_brain_mask_in_dwi = f"{self.anat_path}{'/'}{self.t1w_name}{'_brain_mask_in_dwi.nii.gz'}"
        self.dwi2t1w_xfm = f"{self.reg_path_mat}{'/dwi2t1w_xfm.mat'}"
        self.t1w2dwi_xfm = f"{self.reg_path_mat}{'/t1w2dwi_xfm.mat'}"
        self.t1w2dwi_bbr_xfm = f"{self.reg_path_mat}{'/t1w2dwi_bbr_xfm.mat'}"
        self.dwi2t1w_bbr_xfm = f"{self.reg_path_mat}{'/dwi2t1w_bbr_xfm.mat'}"
        self.t1wtissue2dwi_xfm = f"{self.reg_path_mat}{'/t1wtissue2dwi_xfm.mat'}"
        self.temp2dwi_xfm = f"{self.reg_path_mat}{'/'}{self.dwi_name}{'_xfm_temp2dwi.mat'}"
        self.map_name = f"{self.t1w_name}{'_seg'}"
        self.wm_mask = f"{self.anat_path}{'/'}{self.t1w_name}{'_wm.nii.gz'}"
        self.wm_mask_thr = f"{self.anat_path}{'/'}{self.t1w_name}{'_wm_thr.nii.gz'}"
        self.wm_edge = f"{self.anat_path}{'/'}{self.t1w_name}{'_wm_edge.nii.gz'}"
        self.csf_mask = f"{self.anat_path}{'/'}{self.t1w_name}{'_csf.nii.gz'}"
        self.gm_mask = f"{self.anat_path}{'/'}{self.t1w_name}{'_gm.nii.gz'}"
        self.xfm_roi2mni_init = f"{self.reg_path_mat}{'/roi_2_mni.mat'}"
        self.mni_vent_loc = pkg_resources.resource_filename("pynets",
                                                            f"templates/LateralVentricles_{vox_size}.nii.gz")
        self.csf_mask_dwi = f"{self.reg_path_img}{'/'}{self.t1w_name}{'_csf_mask_dwi.nii.gz'}"
        self.gm_in_dwi = f"{self.reg_path_img}{'/'}{self.t1w_name}{'_gm_in_dwi.nii.gz'}"
        self.wm_in_dwi = f"{self.reg_path_img}{'/'}{self.t1w_name}{'_wm_in_dwi.nii.gz'}"
        self.csf_mask_dwi_bin = f"{self.reg_path_img}{'/'}{self.t1w_name}{'_csf_mask_dwi_bin.nii.gz'}"
        self.gm_in_dwi_bin = f"{self.reg_path_img}{'/'}{self.t1w_name}{'_gm_in_dwi_bin.nii.gz'}"
        self.wm_in_dwi_bin = f"{self.reg_path_img}{'/'}{self.t1w_name}{'_wm_in_dwi_bin.nii.gz'}"
        self.vent_mask_dwi = f"{self.reg_path_img}{'/'}{self.t1w_name}{'_vent_mask_dwi.nii.gz'}"
        self.vent_csf_in_dwi = f"{self.reg_path_img}{'/'}{self.t1w_name}{'_vent_csf_in_dwi.nii.gz'}"
        self.vent_mask_mni = f"{self.reg_path_img}{'/vent_mask_mni.nii.gz'}"
        self.vent_mask_t1w = f"{self.reg_path_img}{'/vent_mask_t1w.nii.gz'}"
        self.input_mni = pkg_resources.resource_filename("pynets", f"templates/{self.template_name}_{vox_size}.nii.gz")
        self.input_mni_brain = pkg_resources.resource_filename("pynets",
                                                               f"templates/{self.template_name}_"
                                                               f"brain_{vox_size}.nii.gz")
        self.input_mni_mask = pkg_resources.resource_filename("pynets",
                                                              f"templates/{self.template_name}_"
                                                              f"brain_mask_{vox_size}.nii.gz")
        self.mni_atlas = pkg_resources.resource_filename("pynets",
                                                         f"core/atlases/HarvardOxford-sub-prob-{vox_size}.nii.gz")
        self.wm_gm_int_in_dwi = f"{self.reg_path_img}{'/'}{self.t1w_name}{'_wm_gm_int_in_dwi.nii.gz'}"
        self.wm_gm_int_in_dwi_bin = f"{self.reg_path_img}/{self.t1w_name}_wm_gm_int_in_dwi_bin.nii.gz"
        self.corpuscallosum = pkg_resources.resource_filename("pynets", f"templates/CorpusCallosum_{vox_size}.nii.gz")
        self.corpuscallosum_mask_t1w = f"{self.reg_path_img}{'/CorpusCallosum_t1wmask.nii.gz'}"
        self.corpuscallosum_dwi = f"{self.reg_path_img}{'/CorpusCallosum_dwi.nii.gz'}"

        # Create empty tmp directories that do not yet exist
        reg_dirs = [self.tmp_path, self.reg_path, self.anat_path, self.reg_path_mat, self.reg_path_warp,
                    self.reg_path_img]
        for i in range(len(reg_dirs)):
            if not op.isdir(reg_dirs[i]):
                os.mkdir(reg_dirs[i])

        if op.isfile(self.t1w_brain) is False:
            import shutil
            shutil.copyfile(self.t1w, self.t1w_head)

    def gen_tissue(self, overwrite=True):
        """
        A function to segment and threshold tissue types from T1w.
        """
        # from pynets.plotting.plot_gen import qa_fast_png
        import os.path as op
        import glob
        import shutil

        print(self.basedir_path)

        # Apply brain mask if detected as a separate file
        anat_mask_existing = glob.glob(self.basedir_path + '/*_desc-brain_mask.nii.gz')
        if len(anat_mask_existing) > 0:
            anat_mask_existing = anat_mask_existing[0]
            print(f"Using {anat_mask_existing}...")
        else:
            anat_mask_existing = None

        # Segment the t1w brain into probability maps
        # WM
        wm_mask_existing = glob.glob(self.basedir_path + '/*_label-WM_probseg.nii.gz')
        if len(wm_mask_existing) > 0:
            wm_mask_existing = wm_mask_existing[0]
        else:
            wm_mask_existing = None

        # GM
        gm_mask_existing = glob.glob(self.basedir_path + '/*_label-GM_probseg.nii.gz')
        if len(gm_mask_existing) > 0:
            gm_mask_existing = gm_mask_existing[0]
        else:
            gm_mask_existing = None

        # CSF
        csf_mask_existing = glob.glob(self.basedir_path + '/*_label-CSF_probseg.nii.gz')
        if len(csf_mask_existing) > 0:
            csf_mask_existing = csf_mask_existing[0]
            print(f"Using {csf_mask_existing}...")
        else:
            csf_mask_existing = None

        if not self.mask:
            # Check if already skull-stripped. If not, strip it.
            img = nib.load(self.t1w_head)
            t1w_data = img.get_fdata()
            perc_nonzero = np.count_nonzero(t1w_data) / np.count_nonzero(t1w_data == 0)
            # TODO find a better heuristic for determining whether a t1w image has already been skull-stripped
            if perc_nonzero > 0.25:
                import tensorflow as tf
                import logging
                from deepbrain import Extractor
                logger = tf.get_logger()
                logger.setLevel(logging.ERROR)
                os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
                ext = Extractor()
                prob = ext.run(t1w_data)
                mask = prob > 0.5
                self.mask = f"{op.dirname(self.t1w_head)}/deep_brain_mask.nii.gz"
                nib.save(nib.Nifti1Image(mask, affine=img.affine, header=img.header), self.mask)
                img.uncache()
            else:
                nib.save(nib.Nifti1Image(t1w_data.astype('bool'), affine=img.affine, header=img.header), self.mask)
        else:
            anat_mask_existing = self.mask

        try:
            os.system(f"fslmaths {self.t1w_head} -mas {anat_mask_existing} {self.t1w_brain} 2>/dev/null")
        except:
            try:
                from nilearn.image import resample_to_img
                nib.save(resample_to_img(nib.load(anat_mask_existing), nib.load(self.t1w_brain)),
                         anat_mask_existing)
                os.system(f"fslmaths {self.t1w_head} -mas {anat_mask_existing} {self.t1w_brain} 2>/dev/null")
            except ValueError:
                print('Cannot coerce mask to shape of T1w anatomical.')

        if wm_mask_existing and gm_mask_existing and csf_mask_existing and overwrite is False:
            if op.isfile(wm_mask_existing) and op.isfile(gm_mask_existing) and op.isfile(csf_mask_existing):
                print('Existing segmentations detected...')
                wm_mask = regutils.check_orient_and_dims(wm_mask_existing, self.basedir_path,
                                                         self.vox_size, overwrite=False)
                gm_mask = regutils.check_orient_and_dims(gm_mask_existing, self.basedir_path,
                                                         self.vox_size, overwrite=False)
                csf_mask = regutils.check_orient_and_dims(csf_mask_existing, self.basedir_path,
                                                          self.vox_size, overwrite=False)
            else:
                try:
                    maps = regutils.segment_t1w(self.t1w_brain, self.map_name)
                    wm_mask = maps['wm_prob']
                    gm_mask = maps['gm_prob']
                    csf_mask = maps['csf_prob']
                except RuntimeError:
                    print('Segmentation failed. Does the input anatomical image still contained skull?')
        else:
            try:
                maps = regutils.segment_t1w(self.t1w_brain, self.map_name)
                wm_mask = maps['wm_prob']
                gm_mask = maps['gm_prob']
                csf_mask = maps['csf_prob']
            except RuntimeError:
                print('Segmentation failed. Does the input anatomical image still contained skull?')

        # qa_fast_png(self.csf_mask, self.gm_mask, self.wm_mask, self.map_name)

        # Threshold WM to binary in dwi space
        t_img = nib.load(wm_mask)
        mask = math_img('img > 0.20', img=t_img)
        mask.to_filename(self.wm_mask_thr)

        # Threshold T1w brain to binary in anat space
        t_img = nib.load(self.t1w_brain)
        mask = math_img('img > 0.0', img=t_img)
        mask.to_filename(self.t1w_brain_mask)

        # Extract wm edge
        os.system(f"fslmaths {wm_mask} -edge -bin -mas {self.wm_mask_thr} {self.wm_edge} 2>/dev/null")

        shutil.copyfile(wm_mask, self.wm_mask)
        shutil.copyfile(gm_mask, self.gm_mask)
        shutil.copyfile(csf_mask, self.csf_mask)

        return

    def t1w2mni_align(self):
        """
        A function to perform alignment from T1w --> MNI template.
        """

        # Create linear transform/ initializer T1w-->MNI
        regutils.align(self.t1w_brain, self.input_mni_brain, xfm=self.t12mni_xfm_init, bins=None, interp="spline",
                       out=None, dof=12, cost='mutualinfo', searchrad=True)

        # Attempt non-linear registration of T1 to MNI template
        if self.simple is False:
            try:
                print(f"Learning a non-linear mapping from T1w --> {self.template_name} ...")
                # Use FNIRT to nonlinearly align T1 to MNI template
                regutils.align_nonlinear(self.t1w_brain, self.input_mni, xfm=self.t12mni_xfm_init,
                                         out=self.t1_aligned_mni, warp=self.warp_t1w2mni, ref_mask=self.input_mni_mask)

                # Get warp from MNI -> T1
                regutils.inverse_warp(self.t1w_brain, self.mni2t1w_warp, self.warp_t1w2mni)

                # Get mat from MNI -> T1
                os.system(f"convert_xfm -omat {self.mni2t1_xfm} -inverse {self.t12mni_xfm_init} 2>/dev/null")

            except:
                # Falling back to linear registration
                regutils.align(self.t1w_brain, self.input_mni_brain, xfm=self.mni2t1_xfm, init=self.t12mni_xfm_init,
                               bins=None, dof=12, cost='mutualinfo', searchrad=True, interp="spline",
                               out=self.t1_aligned_mni, sch=None)
                # Get mat from MNI -> T1
                os.system(f"convert_xfm -omat {self.t12mni_xfm} -inverse {self.mni2t1_xfm} 2>/dev/null")
        else:
            # Falling back to linear registration
            regutils.align(self.t1w_brain, self.input_mni_brain, xfm=self.t12mni_xfm, init=self.t12mni_xfm_init,
                           bins=None, dof=12, cost='mutualinfo', searchrad=True, interp="spline",
                           out=self.t1_aligned_mni, sch=None)
            # Get mat from MNI -> T1
            os.system(f"convert_xfm -omat {self.t12mni_xfm} -inverse {self.mni2t1_xfm} 2>/dev/null")

    def t1w2dwi_align(self):
        """
        A function to perform alignment from T1w_MNI --> DWI. Uses a local optimization
        cost function to get the two images close, and then uses bbr to obtain a good alignment of brain boundaries.
        Assumes input dwi is already preprocessed and brain extracted.
        """

        # Align T1w-->DWI
        regutils.align(self.ap_path, self.t1w_brain, xfm=self.t1w2dwi_xfm, bins=None, interp="spline", dof=6,
                       cost='mutualinfo', out=None, searchrad=True, sch=None)
        os.system(f"convert_xfm -omat {self.dwi2t1w_xfm} -inverse {self.t1w2dwi_xfm} 2>/dev/null")

        if self.simple is False:
            # Flirt bbr
            try:
                print('Learning a Boundary-Based Mapping from T1w-->DWI ...')
                regutils.align(self.fa_path, self.t1w_brain, wmseg=self.wm_edge, xfm=self.dwi2t1w_bbr_xfm,
                               init=self.dwi2t1w_xfm, bins=256, dof=7, searchrad=True, interp="spline", out=None,
                               cost='bbr', sch="${FSLDIR}/etc/flirtsch/bbr.sch")
                os.system(f"convert_xfm -omat {self.t1w2dwi_bbr_xfm} -inverse {self.dwi2t1w_bbr_xfm} 2>/dev/null")

                # Apply the alignment
                regutils.align(self.t1w_brain, self.ap_path, init=self.t1w2dwi_bbr_xfm, xfm=self.t1wtissue2dwi_xfm,
                               bins=None, interp="spline", dof=7, cost='mutualinfo', out=self.t1w2dwi, searchrad=True,
                               sch=None)
            except:
                # Apply the alignment
                regutils.align(self.t1w_brain, self.ap_path, init=self.t1w2dwi_xfm, xfm=self.t1wtissue2dwi_xfm,
                               bins=None, interp="spline", dof=7, cost='mutualinfo', out=self.t1w2dwi, searchrad=True,
                               sch=None)
        else:
            # Apply the alignment
            regutils.align(self.t1w_brain, self.ap_path, init=self.t1w2dwi_xfm, xfm=self.t1wtissue2dwi_xfm, bins=None,
                           interp="spline", dof=6, cost='mutualinfo', out=self.t1w2dwi, searchrad=True, sch=None)

        return

    def atlas2t1w2dwi_align(self, uatlas, uatlas_parcels, atlas):
        """
        A function to perform atlas alignment atlas --> T1 --> dwi.
        Tries nonlinear registration first, and if that fails, does a linear registration instead. For this to succeed,
        must first have called t1w2dwi_align.
        """
        from nilearn.image import resample_to_img
        from pynets.core.utils import checkConsecutive

        aligned_atlas_t1mni = f"{self.anat_path}{'/'}{atlas}{'_t1w_mni.nii.gz'}"
        aligned_atlas_skull = f"{self.anat_path}{'/'}{atlas}{'_t1w_skull.nii.gz'}"
        dwi_aligned_atlas = f"{self.reg_path_img}{'/'}{atlas}{'_dwi_track.nii.gz'}"
        dwi_aligned_atlas_wmgm_int = f"{self.reg_path_img}{'/'}{atlas}{'_dwi_track_wmgm_int.nii.gz'}"

        template_img = nib.load(self.t1_aligned_mni)
        if uatlas_parcels:
            uatlas_res_template = resample_to_img(nib.load(uatlas_parcels), template_img, interpolation='nearest')
        else:
            uatlas_res_template = resample_to_img(nib.load(uatlas), template_img, interpolation='nearest')
        uatlas_res_template_data = np.asarray(uatlas_res_template.dataobj)
        uatlas_res_template_data[uatlas_res_template_data != uatlas_res_template_data.astype(int)] = 0

        uatlas_res_template = nib.Nifti1Image(uatlas_res_template_data.astype('int32'),
                                              affine=uatlas_res_template.affine, header=uatlas_res_template.header)
        nib.save(uatlas_res_template, aligned_atlas_t1mni)

        if self.simple is False:
            try:
                regutils.apply_warp(self.t1w_brain, aligned_atlas_t1mni, aligned_atlas_skull,
                                    warp=self.mni2t1w_warp, interp='nn', sup=True, mask=self.t1w_brain_mask)

                # Apply linear transformation from template to dwi space
                regutils.align(aligned_atlas_skull, self.ap_path, init=self.t1w2dwi_bbr_xfm,
                               out=dwi_aligned_atlas, dof=6, searchrad=True, interp="nearestneighbour",
                               cost='mutualinfo')

            except:
                print("Warning: Atlas is not in correct dimensions, or input is low quality,\nusing linear template "
                      "registration.")

                regutils.align(aligned_atlas_t1mni, self.t1w_brain, init=self.mni2t1_xfm,
                               out=aligned_atlas_skull, dof=6, searchrad=True, interp="nearestneighbour",
                               cost='mutualinfo')

                regutils.align(aligned_atlas_skull, self.ap_path, init=self.t1w2dwi_bbr_xfm,
                               out=dwi_aligned_atlas, dof=6, searchrad=True, interp="nearestneighbour",
                               cost='mutualinfo')

        else:
            regutils.align(aligned_atlas_t1mni, self.t1w_brain, init=self.mni2t1_xfm,
                           out=aligned_atlas_skull, dof=6, searchrad=True, interp="nearestneighbour",
                           cost='mutualinfo')

            regutils.align(aligned_atlas_skull, self.ap_path, init=self.t1w2dwi_xfm,
                           out=dwi_aligned_atlas, dof=6, searchrad=True, interp="nearestneighbour",
                           cost='mutualinfo')

        atlas_img = nib.load(dwi_aligned_atlas)
        wm_gm_img = nib.load(self.wm_gm_int_in_dwi)
        wm_gm_mask_img = math_img('img > 0', img=wm_gm_img)
        atlas_mask_img = math_img('img > 0', img=atlas_img)

        uatlas_res_template_data = np.asarray(atlas_img.dataobj)
        uatlas_res_template_data[uatlas_res_template_data != uatlas_res_template_data.astype(int)] = 0

        atlas_img_corr = nib.Nifti1Image(uatlas_res_template_data.astype('uint32'),
                                         affine=atlas_img.affine, header=atlas_img.header)

        dwi_aligned_atlas_wmgm_int_img = intersect_masks([wm_gm_mask_img, atlas_mask_img], threshold=0,
                                                         connected=False)

        nib.save(atlas_img_corr, dwi_aligned_atlas)
        nib.save(dwi_aligned_atlas_wmgm_int_img, dwi_aligned_atlas_wmgm_int)

        final_dat = atlas_img_corr.get_fdata()
        unique_a = list(set(np.array(final_dat.flatten().tolist())))
        unique_a.sort()

        if not checkConsecutive(unique_a):
            print('Warning! Non-consecutive integers found in parcellation...')

        atlas_img.uncache()
        atlas_img_corr.uncache()
        atlas_mask_img.uncache()
        wm_gm_img.uncache()
        wm_gm_mask_img.uncache()

        return dwi_aligned_atlas_wmgm_int, dwi_aligned_atlas, aligned_atlas_t1mni

    def tissue2dwi_align(self):
        """
        A function to perform alignment of ventricle ROI's from MNI space --> dwi and CSF from T1w space --> dwi.
        First generates and performs dwi space alignment of avoidance/waypoint masks for tractography.
        First creates ventricle ROI. Then creates transforms from stock MNI template to dwi space.
        For this to succeed, must first have called both t1w2dwi_align.
        """
        import os.path as op

        # Register Lateral Ventricles and Corpus Callosum rois to t1w
        if not op.isfile(self.mni_atlas):
            raise ValueError('FSL atlas for ventricle reference not found!')

        # Create transform to MNI atlas to T1w using flirt. This will be use to transform the ventricles to dwi space.
        regutils.align(self.mni_atlas, self.input_mni_brain, xfm=self.xfm_roi2mni_init, init=None, bins=None, dof=6,
                       cost='mutualinfo', searchrad=True, interp="spline", out=None)

        # Create transform to align roi to mni and T1w using flirt
        regutils.applyxfm(self.input_mni_brain, self.mni_vent_loc, self.xfm_roi2mni_init, self.vent_mask_mni)

        if self.simple is False:
            # Apply warp resulting from the inverse MNI->T1w created earlier
            regutils.apply_warp(self.t1w_brain, self.vent_mask_mni, self.vent_mask_t1w, warp=self.mni2t1w_warp,
                                interp='nn', sup=True)

            regutils.apply_warp(self.t1w_brain, self.corpuscallosum, self.corpuscallosum_mask_t1w,
                                warp=self.mni2t1w_warp, interp="nn", sup=True)

        else:
            regutils.applyxfm(self.vent_mask_mni, self.t1w_brain, self.mni2t1_xfm, self.vent_mask_t1w)
            regutils.applyxfm(self.corpuscallosum, self.t1w_brain, self.mni2t1_xfm, self.corpuscallosum_mask_t1w)

        # Applyxfm tissue maps to dwi space
        if self.mask is not None:
            regutils.applyxfm(self.ap_path, self.mask, self.t1wtissue2dwi_xfm, self.t1w_brain_mask_in_dwi)
        regutils.applyxfm(self.ap_path, self.vent_mask_t1w, self.t1wtissue2dwi_xfm, self.vent_mask_dwi)
        regutils.applyxfm(self.ap_path, self.csf_mask, self.t1wtissue2dwi_xfm, self.csf_mask_dwi)
        regutils.applyxfm(self.ap_path, self.gm_mask, self.t1wtissue2dwi_xfm, self.gm_in_dwi)
        regutils.applyxfm(self.ap_path, self.wm_mask, self.t1wtissue2dwi_xfm, self.wm_in_dwi)
        regutils.applyxfm(self.ap_path, self.corpuscallosum_mask_t1w, self.t1wtissue2dwi_xfm, self.corpuscallosum_dwi)

        # Threshold WM to binary in dwi space
        thr_img = nib.load(self.wm_in_dwi)
        thr_img = math_img('img > 0.20', img=thr_img)
        nib.save(thr_img, self.wm_in_dwi_bin)

        # Threshold GM to binary in dwi space
        thr_img = nib.load(self.gm_in_dwi)
        thr_img = math_img('img > 0.15', img=thr_img)
        nib.save(thr_img, self.gm_in_dwi_bin)

        # Threshold CSF to binary in dwi space
        thr_img = nib.load(self.csf_mask_dwi)
        thr_img = math_img('img > 0.95', img=thr_img)
        nib.save(thr_img, self.csf_mask_dwi_bin)

        # Threshold WM to binary in dwi space
        os.system(f"fslmaths {self.wm_in_dwi} -mas {self.wm_in_dwi_bin} {self.wm_in_dwi} 2>/dev/null")

        # Threshold GM to binary in dwi space
        os.system(f"fslmaths {self.gm_in_dwi} -mas {self.gm_in_dwi_bin} {self.gm_in_dwi} 2>/dev/null")

        # Threshold CSF to binary in dwi space
        os.system(f"fslmaths {self.csf_mask_dwi} -mas {self.csf_mask_dwi_bin} {self.csf_mask_dwi} 2>/dev/null")

        # Create ventricular CSF mask
        print('Creating Ventricular CSF mask...')
        os.system(f"fslmaths {self.vent_mask_dwi} -kernel sphere 10 -ero -bin {self.vent_mask_dwi} 2>/dev/null")
        os.system(f"fslmaths {self.csf_mask_dwi} -add {self.vent_mask_dwi} -bin {self.vent_csf_in_dwi} 2>/dev/null")

        print("Creating Corpus Callosum mask...")
        os.system(f"fslmaths {self.corpuscallosum_dwi} -mas {self.wm_in_dwi_bin} -sub {self.vent_csf_in_dwi} "
                  f"-bin {self.corpuscallosum_dwi} 2>/dev/null")

        # Create gm-wm interface image
        os.system(f"fslmaths {self.gm_in_dwi_bin} -mul {self.wm_in_dwi_bin} -add {self.corpuscallosum_dwi} "
                  f"-mas {self.B0_mask} -bin {self.wm_gm_int_in_dwi} 2>/dev/null")

        return

    def waymask2dwi_align(self, waymask):
        """
        A function to perform alignment of a waymask from MNI space --> T1w --> dwi.
        """
        waymask_in_t1w = f"{self.reg_path_img}/waymask-{os.path.basename(waymask).split('.nii')[0]}_in_t1w.nii.gz"
        waymask_in_dwi = f"{self.reg_path_img}/waymask-{os.path.basename(waymask).split('.nii')[0]}_in_dwi.nii.gz"

        # Apply warp or transformer resulting from the inverse MNI->T1w created earlier
        if self.simple is False:
            regutils.apply_warp(self.t1w_brain, waymask, waymask_in_t1w, warp=self.mni2t1w_warp)
        else:
            regutils.applyxfm(self.t1w_brain, waymask, self.mni2t1_xfm, waymask_in_t1w)

        # Apply transform from t1w to native dwi space
        regutils.applyxfm(self.ap_path, waymask_in_t1w, self.t1wtissue2dwi_xfm, waymask_in_dwi)

        return waymask_in_dwi

    def roi2dwi_align(self, roi):
        """
        A function to perform alignment of a waymask from MNI space --> T1w --> dwi.
        """
        roi_in_t1w = f"{self.reg_path_img}/waymask-{os.path.basename(roi).split('.nii')[0]}_in_t1w.nii.gz"
        roi_in_dwi = f"{self.reg_path_img}/waymask-{os.path.basename(roi).split('.nii')[0]}_in_dwi.nii.gz"

        # Apply warp or transformer resulting from the inverse MNI->T1w created earlier
        if self.simple is False:
            regutils.apply_warp(self.t1w_brain, roi, roi_in_t1w, warp=self.mni2t1w_warp)
        else:
            regutils.applyxfm(self.t1w_brain, roi, self.mni2t1_xfm, roi_in_t1w)

        # Apply transform from t1w to native dwi space
        regutils.applyxfm(self.ap_path, roi_in_t1w, self.t1wtissue2dwi_xfm, roi_in_dwi)

        return roi_in_dwi


class FmriReg(object):
    """
    A Class for Registering an atlas to a subject's MNI-aligned T1w image in native epi space.

    References
    ----------
    .. [1] Brett M, Leff AP, Rorden C, Ashburner J (2001) Spatial Normalization
      of Brain Images with Focal Lesions Using Cost Function Masking.
      NeuroImage 14(2) doi:10.006/nimg.2001.0845.
    .. [2] Zhang Y, Brady M, Smith S. Segmentation of brain MR images through a
      hidden Markov random field model and the expectation-maximization algorithm.
      IEEE Trans Med Imaging. 2001 Jan;20(1):45–57. doi:10.1109/42.906424.

    """

    def __init__(self, basedir_path, anat_file, mask, vox_size, template_name, simple):
        import os.path as op
        import pkg_resources
        self.t1w = anat_file
        self.mask = mask
        self.vox_size = vox_size
        self.template_name = template_name
        self.t1w_name = 't1w'
        self.simple = simple
        self.basedir_path = basedir_path
        self.reg_path = f"{basedir_path}{'/reg'}"
        self.reg_path_mat = f"{self.reg_path}{'/mats'}"
        self.reg_path_warp = f"{self.reg_path}{'/warps'}"
        self.reg_path_img = f"{self.reg_path}{'/imgs'}"
        self.t1w2epi_xfm = f"{self.reg_path_mat}{'/t1w2epi_xfm.mat'}"
        self.t12mni_xfm_init = f"{self.reg_path_mat}{'/xfm_t1w2mni_init.mat'}"
        self.t12mni_xfm = f"{self.reg_path_mat}{'/xfm_t1w2mni.mat'}"
        self.mni2t1_xfm = f"{self.reg_path_mat}{'/xfm_mni2t1.mat'}"
        self.mni2t1w_warp = f"{self.reg_path_warp}{'/mni2t1w_warp.nii.gz'}"
        self.warp_t1w2mni = f"{self.reg_path_warp}{'/t1w2mni_warp.nii.gz'}"
        self.t1_aligned_mni = f"{self.reg_path_img}{'/'}{self.t1w_name}{'_aligned_mni.nii.gz'}"
        self.t1w_brain = f"{self.reg_path_img}{'/'}{self.t1w_name}{'_brain.nii.gz'}"
        self.t1w_head = f"{self.reg_path_img}{'/'}{self.t1w_name}{'_head.nii.gz'}"
        self.t1w_brain_mask = f"{self.reg_path_img}{'/'}{self.t1w_name}{'_brain_mask.nii.gz'}"
        self.map_name = f"{self.reg_path_img}{'/'}{self.t1w_name}{'_seg'}"
        self.gm_mask = f"{self.reg_path_img}{'/'}{self.t1w_name}{'_gm.nii.gz'}"
        self.gm_mask_thr = f"{self.reg_path_img}{'/'}{self.t1w_name}{'_gm_thr.nii.gz'}"
        self.wm_mask = f"{self.reg_path_img}{'/'}{self.t1w_name}{'_wm.nii.gz'}"
        self.wm_mask_thr = f"{self.reg_path_img}{'/'}{self.t1w_name}{'_wm_thr.nii.gz'}"
        self.wm_edge = f"{self.reg_path_img}{'/'}{self.t1w_name}{'_wm_edge.nii.gz'}"
        self.input_mni = pkg_resources.resource_filename("pynets",
                                                         f"templates/{self.template_name}_{vox_size}.nii.gz")
        self.input_mni_brain = pkg_resources.resource_filename("pynets",
                                                               f"templates/{self.template_name}_"
                                                               f"brain_{vox_size}.nii.gz")
        self.input_mni_mask = pkg_resources.resource_filename("pynets",
                                                              f"templates/{self.template_name}_"
                                                              f"brain_mask_{vox_size}.nii.gz")

        # Create empty tmp directories that do not yet exist
        reg_dirs = [self.reg_path, self.reg_path_mat, self.reg_path_warp, self.reg_path_img]
        for i in range(len(reg_dirs)):
            if not op.isdir(reg_dirs[i]):
                os.mkdir(reg_dirs[i])

        if op.isfile(self.t1w_brain) is False:
            import shutil
            shutil.copyfile(self.t1w, self.t1w_head)

    def gen_tissue(self, overwrite=False):
        """
        A function to segment and threshold tissue types from T1w.
        """
        import glob
        import os.path as op

        # Apply brain mask if detected as a separate file
        print(self.basedir_path)
        anat_mask_existing = glob.glob(self.basedir_path + '/*_desc-brain_mask.nii.gz')
        if len(anat_mask_existing) > 0:
            anat_mask_existing = anat_mask_existing[0]
            print(f"Using {anat_mask_existing}...")
        else:
            anat_mask_existing = None

        # Segment the t1w brain into probability maps
        # WM
        wm_mask_existing = glob.glob(self.basedir_path + '/*_label-WM_probseg.nii.gz')
        if len(wm_mask_existing) > 0:
            wm_mask_existing = wm_mask_existing[0]
        else:
            wm_mask_existing = None

        # GM
        gm_mask_existing = glob.glob(self.basedir_path + '/*_label-GM_probseg.nii.gz')
        if len(gm_mask_existing) > 0:
            gm_mask_existing = gm_mask_existing[0]
        else:
            gm_mask_existing = None

        if not self.mask:
            # Check if already skull-stripped. If not, strip it.
            img = nib.load(self.t1w_head)
            t1w_data = img.get_fdata()
            perc_nonzero = np.count_nonzero(t1w_data) / np.count_nonzero(t1w_data == 0)
            # TODO find a better heuristic for determining whether a t1w image has already been skull-stripped
            if perc_nonzero > 0.25:
                import tensorflow as tf
                import logging
                from deepbrain import Extractor
                logger = tf.get_logger()
                logger.setLevel(logging.ERROR)
                os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
                ext = Extractor()
                prob = ext.run(t1w_data)
                mask = prob > 0.5
                self.mask = f"{op.dirname(self.t1w_head)}/deep_brain_mask.nii.gz"
                nib.save(nib.Nifti1Image(mask, affine=img.affine, header=img.header), self.mask)
                img.uncache()
            else:
                nib.save(nib.Nifti1Image(t1w_data.astype('bool'), affine=img.affine, header=img.header), self.mask)
        else:
            anat_mask_existing = self.mask

        try:
            os.system(f"fslmaths {self.t1w_head} -mas {anat_mask_existing} {self.t1w_brain} 2>/dev/null")
        except:
            try:
                from nilearn.image import resample_to_img
                nib.save(resample_to_img(nib.load(anat_mask_existing), nib.load(self.t1w_brain)),
                         anat_mask_existing)
                os.system(f"fslmaths {self.t1w_head} -mas {anat_mask_existing} {self.t1w_brain} 2>/dev/null")
            except ValueError:
                print('Cannot coerce mask to shape of T1w anatomical.')

        if wm_mask_existing and gm_mask_existing:
            if op.isfile(gm_mask_existing) and overwrite is False:
                print('Existing segmentations detected...')
                gm_mask = regutils.check_orient_and_dims(gm_mask_existing, self.basedir_path, self.vox_size,
                                                         overwrite=False)
                wm_mask = regutils.check_orient_and_dims(wm_mask_existing, self.basedir_path, self.vox_size,
                                                         overwrite=False)
            else:
                try:
                    maps = regutils.segment_t1w(self.t1w_brain, self.map_name)
                    gm_mask = maps['gm_prob']
                    wm_mask = maps['wm_prob']
                except RuntimeError:
                    print('Segmentation failed. Does the input anatomical image still contained skull?')
        else:
            try:
                maps = regutils.segment_t1w(self.t1w_brain, self.map_name)
                gm_mask = maps['gm_prob']
                wm_mask = maps['wm_prob']
            except RuntimeError:
                print('Segmentation failed. Does the input anatomical image still contained skull?')

        # Threshold T1w brain to binary in anat space
        t_img = nib.load(self.t1w_brain)
        mask = math_img('img > 0.0', img=t_img)
        mask.to_filename(self.t1w_brain_mask)

        # Threshold GM to binary in func space
        t_img = nib.load(gm_mask)
        mask = math_img('img > 0.05', img=t_img)
        mask.to_filename(self.gm_mask_thr)
        os.system(f"fslmaths {gm_mask} -mas {self.gm_mask_thr} {self.gm_mask} 2>/dev/null")

        # Threshold WM to binary in dwi space
        t_img = nib.load(wm_mask)
        mask = math_img('img > 0.50', img=t_img)
        mask.to_filename(self.wm_mask_thr)

        # Extract wm edge
        os.system(f"fslmaths {wm_mask} -edge -bin -mas {self.wm_mask_thr} {self.wm_edge} 2>/dev/null")

        return

    def t1w2mni_align(self):
        """
        A function to perform alignment from T1w --> MNI.
        """

        # Create linear transform/ initializer T1w-->MNI
        regutils.align(self.t1w_brain, self.input_mni_brain, xfm=self.t12mni_xfm_init, bins=None, interp="spline",
                       out=None, dof=12, cost='mutualinfo', searchrad=True)

        # Attempt non-linear registration of T1 to MNI template
        if self.simple is False:
            try:
                print(f"Learning a non-linear mapping from T1w --> {self.template_name} ...")
                # Use FNIRT to nonlinearly align T1w to MNI template
                regutils.align_nonlinear(self.t1w_brain, self.input_mni, xfm=self.t12mni_xfm_init,
                                         out=self.t1_aligned_mni, warp=self.warp_t1w2mni,
                                         ref_mask=self.input_mni_mask)

                # Get warp from T1w --> MNI
                regutils.inverse_warp(self.t1w_brain, self.mni2t1w_warp, self.warp_t1w2mni)

                # Get mat from MNI -> T1w
                os.system(f"convert_xfm -omat {self.mni2t1_xfm} -inverse {self.t12mni_xfm_init} 2>/dev/null")

            except:
                # Falling back to linear registration
                regutils.align(self.t1w_brain, self.input_mni_brain, xfm=self.t12mni_xfm, init=self.t12mni_xfm_init,
                               bins=None, dof=12, cost='mutualinfo', searchrad=True, interp="spline",
                               out=self.t1_aligned_mni, sch=None)
                # Get mat from MNI -> T1w
                os.system(f"convert_xfm -omat {self.t12mni_xfm} -inverse {self.mni2t1_xfm} 2>/dev/null")
        else:
            # Falling back to linear registration
            regutils.align(self.t1w_brain, self.input_mni_brain, xfm=self.t12mni_xfm, init=self.t12mni_xfm_init,
                           bins=None, dof=12, cost='mutualinfo', searchrad=True, interp="spline",
                           out=self.t1_aligned_mni, sch=None)
            # Get mat from MNI -> T1w
            os.system(f"convert_xfm -omat {self.t12mni_xfm} -inverse {self.mni2t1_xfm} 2>/dev/null")
        return

    def roi2t1w_align(self, roi):
        """
        A function to perform alignment of a roi from MNI space --> T1w.
        """

        roi_in_t1w = f"{self.reg_path_img}/roi-{os.path.basename(roi).split('.nii')[0]}_in_t1w.nii.gz"

        # Apply warp or transformer resulting from the inverse MNI->T1w created earlier
        if self.simple is False:
            regutils.apply_warp(self.t1w_brain, roi, roi_in_t1w, warp=self.mni2t1w_warp)
        else:
            regutils.applyxfm(self.t1w_brain, roi, self.mni2t1_xfm, roi_in_t1w)

        return roi_in_t1w

    def atlas2t1w_align(self, uatlas, uatlas_parcels, atlas):
        """
        A function to perform atlas alignment from atlas --> T1w.
        """
        from nilearn.image import resample_to_img
        from pynets.core.utils import checkConsecutive

        aligned_atlas_t1mni = f"{self.reg_path_img}{'/'}{atlas}{'_t1w_mni.nii.gz'}"
        aligned_atlas_skull = f"{self.reg_path_img}{'/'}{atlas}{'_t1w_skull.nii.gz'}"
        aligned_atlas_gm = f"{self.reg_path_img}{'/'}{atlas}{'_gm.nii.gz'}"

        template_img = nib.load(self.t1_aligned_mni)
        if uatlas_parcels:
            uatlas_res_template = resample_to_img(nib.load(uatlas_parcels), template_img, interpolation='nearest')
        else:
            uatlas_res_template = resample_to_img(nib.load(uatlas), template_img, interpolation='nearest')
        uatlas_res_template_data = np.asarray(uatlas_res_template.dataobj)
        uatlas_res_template_data[uatlas_res_template_data != uatlas_res_template_data.astype(int)] = 0

        uatlas_res_template = nib.Nifti1Image(uatlas_res_template_data.astype('uint16'),
                                              affine=uatlas_res_template.affine, header=uatlas_res_template.header)
        nib.save(uatlas_res_template, aligned_atlas_t1mni)

        if self.simple is False:
            try:
                regutils.apply_warp(self.t1w_brain, aligned_atlas_t1mni, aligned_atlas_skull,
                                    warp=self.mni2t1w_warp, interp='nn', sup=True, mask=self.t1w_brain_mask)

            except:
                print("Warning: Atlas is not in correct dimensions, or input is low quality,\nusing linear template "
                      "registration.")

                regutils.align(aligned_atlas_t1mni, self.t1w_brain, init=self.mni2t1_xfm,
                               out=aligned_atlas_skull, dof=6, searchrad=True, interp="nearestneighbour",
                               cost='mutualinfo')

        else:
            regutils.align(aligned_atlas_t1mni, self.t1w_brain, init=self.mni2t1_xfm,
                           out=aligned_atlas_skull, dof=6, searchrad=True, interp="nearestneighbour",
                           cost='mutualinfo')

        os.system(f"fslmaths {aligned_atlas_skull} -mas {self.gm_mask} {aligned_atlas_gm} 2>/dev/null")
        atlas_img = nib.load(aligned_atlas_gm)

        uatlas_res_template_data = np.asarray(atlas_img.dataobj)
        uatlas_res_template_data[uatlas_res_template_data != uatlas_res_template_data.astype(int)] = 0
        atlas_img_corr = nib.Nifti1Image(uatlas_res_template_data.astype('uint32'),
                                         affine=atlas_img.affine, header=atlas_img.header)
        nib.save(atlas_img_corr, aligned_atlas_gm)
        final_dat = nib.load(aligned_atlas_gm).get_fdata()
        unique_a = list(set(np.array(final_dat.flatten().tolist())))
        unique_a.sort()

        if not checkConsecutive(unique_a):
            print('Warning! Non-consecutive integers found in parcellation...')

        template_img.uncache()

        return aligned_atlas_gm, aligned_atlas_skull
