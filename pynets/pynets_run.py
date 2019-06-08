#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on Tue Nov  7 10:40:07 2017
# Copyright (C) 2018
# @author: Derek Pisner (dPys)


def get_parser():
    import argparse
    # Parse args
    parser = argparse.ArgumentParser(description='PyNets: A Fully-Automated Workflow for Reproducible Ensemble '
                                                 'Graph Analysis of Functional and Structural Connectomes')
    parser.add_argument('-id',
                        metavar='A subject id (can be any arbitrary identifier)',
                        default=None,
                        required=True,
                        help='An arbitrary subject identifier OR list of subject identifiers, separated by comma and of '
                             'equivalent length to the list of input files indicated with the -func flag. If functional '
                             'and structural connectomes are being generated simultaneously, then comma-separated id\'s '
                             'need to be repeated to match the total input file count.\n')
    parser.add_argument('-mod',
                        metavar='Graph estimation method',
                        default='partcorr',
                        required=True,
                        nargs='+',
                        choices=['corr', 'sps', 'cov', 'partcorr', 'QuicGraphicalLasso', 'QuicGraphicalLassoCV',
                                 'QuicGraphicalLassoEBIC', 'AdaptiveQuicGraphicalLasso', 'csa', 'tensor', 'csd'],
                        help='Specify matrix estimation type. For fMRI, possible models include: corr for correlation, '
                             'cov for covariance, sps for precision covariance, partcorr for partial correlation. '
                             'sps type is used by default. If skgmm is installed (https://github.com/skggm/skggm), '
                             'then QuicGraphicalLasso, QuicGraphicalLassoCV, QuicGraphicalLassoEBIC, and '
                             'AdaptiveQuicGraphicalLasso. Default is partcorr for fMRI. For dMRI, models include csa'
                             'tensor, and csd.\n')
    parser.add_argument('-g',
                        metavar='Path to graph file input.',
                        default=None,
                        help='In either .txt or .npy format. This skips fMRI and dMRI graph estimation workflows and '
                             'begins at the graph analysis stage.\n')
    parser.add_argument('-func',
                        metavar='Path to input functional file (required for functional connectomes)',
                        default=None,
                        help='Specify either a path to a preprocessed functional image in '
                              'standard space and in .nii or .nii.gz format OR multiple paths '
                              'to multiple preprocessed functional images in standard '
                              'space and in .nii or .nii.gz format, separated by commas OR the '
                              'path to a text file containing a list of paths to subject files.\n')
    parser.add_argument('-conf',
                        metavar='Confound regressor file (.tsv/.csv format)',
                        default=None,
                        help='Optionally specify a path to a confound regressor file to reduce noise in the time-series '
                             'estimation for the graph. This can also be a list of paths in the case of running multiple '
                             'subjects, which requires separated by comma and of equivalent length to the list of input '
                             'files indicated with the -func flag.\n')
    parser.add_argument('-dwi',
                        metavar='Path to diffusion-weighted imaging data file (required for structural connectomes)',
                        default=None,
                        help='Specify either a path to a preprocessed structural diffusion image in native diffusion '
                             'space and in .nii or .nii.gz format OR multiple paths to multiple preprocessed structural '
                             'diffusion images in native diffusion space and in .nii or .nii.gz format.\n')
    parser.add_argument('-bval',
                        metavar='Path to b-values file (required for structural connectomes)',
                        default=None,
                        help='Specify either a path to a b-values text file containing gradient shell values per '
                             'diffusion direction OR multiple paths to multiple b-values text files in the order of '
                             'accompanying b-vectors and dwi files.\n')
    parser.add_argument('-bvec',
                        metavar='Path to b-vectors file (required for structural connectomes)',
                        default=None,
                        help='Specify either a path to a b-vectors text file containing gradient directions (x,y,z) '
                             'per diffusion direction OR multiple paths to multiple b-vectors text files in the order '
                             'of accompanying b-values and dwi files.\n')
    parser.add_argument('-anat',
                        metavar='Path to preprocessed anatomical image',
                        default=None,
                        help='Required for structural and/or functional connectomes. Multiple paths to multiple '
                             'anatomical files text in the order of accompanying functional and/or structural files. '
                             'If functional and structural connectomes are being generated simultaneously, then '
                             'comma-separated anatomical image paths need to be repeated.\n')
    parser.add_argument('-m',
                        metavar='Path to binarized mask image to apply to regions before extracting signals',
                        default=None,
                        help='Specify either a path to a binarized brain mask image in standard space and in .nii or '
                             '.nii.gz format OR multiple paths to multiple brain mask images in the case of running '
                             'multiple participants, in which case paths should be separated by comma. If no brain '
                             'mask is supplied, a default MNI152 template mask will be used\n')
    parser.add_argument('-roi',
                        metavar='Path to binarized roi image',
                        default=None,
                        help='Optionally specify a thresholded binarized ROI mask and retain only those nodes contained '
                             'within that mask for functional connectome estimation, or constrain the tractography '
                             'in the case of structural connectome estimation.\n')
    parser.add_argument('-cm',
                        metavar='Cluster mask',
                        default=None,
                        help='Specify the path to the mask within which to perform clustering. ' 
                             'If specifying a list of paths to multiple cluster masks, separate '
                             'them by comma.\n')
    parser.add_argument('-ua',
                        metavar='Path to parcellation file',
                        default=None,
                        help='Optionally specify a path to a parcellation/atlas file in nifti format. If specifying a '
                             'list of paths to multiple user atlases, separate them by comma.\n')
    parser.add_argument('-ref',
                        metavar='Atlas reference file path',
                        default=None,
                        help='Specify the path to the atlas reference .txt file.\n')
    parser.add_argument('-a',
                        metavar='Atlas',
                        default=None,
                        nargs='+',
                        choices=['atlas_aal', 'atlas_talairach_gyrus', 'atlas_talairach_ba', 'atlas_talairach_lobe',
                                 'atlas_harvard_oxford', 'atlas_destrieux_2009', 'atlas_msdl', 'coords_dosenbach_2010',
                                 'coords_power_2011', 'atlas_pauli_2017'],
                        help='Specify a coordinate atlas parcellation from those made publically available in nilearn. '
                             'If you wish to iterate your pynets run over multiple nilearn atlases, separate them by '
                             'space. Available nilearn atlases are:'
                             '\n\natlas_aal\natlas_talairach_gyrus\natlas_talairach_ba\natlas_talairach_lobe\n'
                             'atlas_harvard_oxford\natlas_destrieux_2009\natlas_msdl\ncoords_dosenbach_2010\n'
                             'coords_power_2011\natlas_pauli_2017.\n')
    parser.add_argument('-parc',
                        default=False,
                        action='store_true',
                        help='Include this flag to use parcels instead of coordinates as nodes.\n')
    parser.add_argument('-names',
                        default=False,
                        action='store_true',
                        help='Optionally use this flag if you wish to perform automated anatomical labeling of nodes.\n')
    parser.add_argument('-ns',
                        metavar='Spherical centroid node size',
                        default=4,
                        nargs='+',
                        help='Optionally specify coordinate-based node radius size(s). Default is 4 mm for fMRI and 8mm '
                             'for dMRI. If you wish to iterate the pipeline across multiple node sizes, separate the '
                             'list by space (e.g. 2 4 6).\n')
    parser.add_argument('-k',
                        metavar='Number of k clusters',
                        default=None,
                        help='Specify a number of clusters to produce.\n')
    parser.add_argument('-k_min',
                        metavar='Min k clusters',
                        default=None,
                        help='Specify the minimum k clusters.\n')
    parser.add_argument('-k_max',
                        metavar='Max k clusters',
                        default=None,
                        help='Specify the maximum k clusters.\n')
    parser.add_argument('-k_step',
                        metavar='K cluster step size',
                        default=None,
                        help='Specify the step size of k cluster iterables.\n')
    parser.add_argument('-ct',
                        metavar='Clustering type',
                        default='ncut',
                        nargs='+',
                        choices=['ncut', 'ward', 'kmeans', 'complete', 'average'],
                        help='Specify the types of clustering to use. Options include ncut, '
                             'ward, kmeans, complete, and average. If specifying a list of '
                             'clustering types, separate them by space.\n')
    parser.add_argument('-n',
                        metavar='Resting-state network',
                        default=None,
                        nargs='+',
                        choices=['Vis', 'SomMot', 'DorsAttn', 'SalVentAttn', 'Limbic', 'Cont', 'Default', 'VisCent',
                                 'VisPeri', 'SomMotA', 'SomMotB', 'DorsAttnA', 'DorsAttnB', 'SalVentAttnA',
                                 'SalVentAttnB', 'LimbicOFC', 'LimbicTempPole', 'ContA', 'ContB', 'ContC', 'DefaultA',
                                 'DefaultB', 'DefaultC', 'TempPar'],
                        help='Optionally specify the name of any of the 2017 Yeo-Schaefer RSNs (7-network or 17-network): '
                             'Vis, SomMot, DorsAttn, SalVentAttn, Limbic, Cont, Default, VisCent, VisPeri, SomMotA, '
                             'SomMotB, DorsAttnA, DorsAttnB, SalVentAttnA, SalVentAttnB, LimbicOFC, LimbicTempPole, '
                             'ContA, ContB, ContC, DefaultA, DefaultB, DefaultC, TempPar. If listing multiple '
                             'RSNs, separate them by space. (e.g. -n \'Default\' \'Cont\' \'SalVentAttn\')\'.\n')
    parser.add_argument('-sm',
                        metavar='Smoothing value (mm fwhm)',
                        default=0,
                        nargs='+',
                        help='Optionally specify smoothing width(s). Default is 0 / no smoothing. ' 
                             'If you wish to iterate the pipeline across multiple smoothing '
                             'values, separate the list by space (e.g. 2 4 6).\n')
    parser.add_argument('-b',
                        metavar='Number of bootstraps (integer)',
                        default=0,
                        nargs='+',
                        help='Optionally specify the number of bootstraps with this flag if you wish to apply '
                             'circular-block bootstrapped resampling of the node-extracted time-series. Size of '
                             'blocks can be specified using the -bs flag.\n')
    parser.add_argument('-bs',
                        metavar='Size bootstrap blocks (integer)',
                        default=None,
                        nargs='+',
                        help='If using the -b flag, you may manually specify a bootstrap block size for circular-block '
                             'resampling of the node-extracted time-series.\n')
    parser.add_argument('-p',
                        metavar='Pruning strategy',
                        default=1,
                        help='Include this flag to prune the resulting graph of any isolated (1) or isolated + fully '
                             'disconnected (2) nodes. Default pruning=1 and removes isolated nodes. Include -p 0 to '
                             'disable pruning.\n')
    parser.add_argument('-bin',
                        default=False,
                        action='store_true',
                        help='Include this flag to binarize the resulting graph such that edges are boolean and not '
                             'weighted.\n')
    parser.add_argument('-s',
                        metavar='Number of samples',
                        default='1000000',
                        help='Include this flag to manually specify a number of cumulative streamline samples for '
                             'tractography. Default is 1000000.\n')
    parser.add_argument('-ml',
                        metavar='Maximum fiber length for tracking',
                        default='200',
                        help='Include this flag to manually specify a maximum tract length (mm) for structural '
                             'connectome tracking. Default is 200.\n')
    parser.add_argument('-tt',
                        metavar='Tracking algorithm',
                        default='local',
                        nargs=1,
                        choices=['local', 'particle'],
                        help='Include this flag to manually specify a tracking algorithm for structural connectome '
                             'estimation. Options are: local and particle. Default is local.\n')
    parser.add_argument('-dg',
                        metavar='Direction getter',
                        default='det',
                        nargs='+',
                        choices=['det', 'prob', 'clos', 'boot'],
                        help='Include this flag to manually specify the statistical approach to tracking for structural '
                             'connectome estimation. Options are: det (deterministic), closest (clos), '
                             'boot (bootstrapped), and prob (probabilistic). '
                             'Default is det.\n')
    parser.add_argument('-tc',
                        metavar='Tissue classification method',
                        default='wb',
                        nargs=1,
                        choices=['wb', 'cmc', 'act', 'bin'],
                        help='Include this flag to manually specify a tissue classification method for structural '
                             'connectome estimation. Options are: cmc (continuous), act (anatomically-constrained), '
                             'wb (whole-brain mask), and bin (binary to white-matter only). Default is wb.\n')
    parser.add_argument('-thr',
                        metavar='Graph threshold',
                        default='1.00',
                        help='Optionally specify a threshold indicating a proportion of weights to preserve in the graph. '
                             'Default is proportional thresholding. If omitted, no thresholding will be applied.\n')
    parser.add_argument('-min_thr',
                        metavar='Multi-thresholding minimum threshold',
                        default=None,
                        help='Minimum threshold for multi-thresholding.\n')
    parser.add_argument('-max_thr',
                        metavar='Multi-thresholding maximum threshold',
                        default=None,
                        help='Maximum threshold for multi-thresholding.')
    parser.add_argument('-step_thr',
                        metavar='Multi-thresholding step size',
                        default=None,
                        help='Threshold step value for multi-thresholding. Default is 0.01.\n')
    parser.add_argument('-norm',
                        metavar='Normalization strategy for resulting graph(s)',
                        default=0,
                        nargs=1,
                        choices=[0, 1, 2],
                        help='Include this flag to normalize the resulting graph to (1) values between 0-1 or (2) using '
                             'log10. Default is (0) no normalization.\n')
    parser.add_argument('-dt',
                        default=False,
                        action='store_true',
                        help='Optionally use this flag if you wish to threshold to achieve a given density or densities '
                             'indicated by the -thr and -min_thr, -max_thr, -step_thr flags, respectively.\n')
    parser.add_argument('-mst',
                        default=False,
                        action='store_true',
                        help='Optionally use this flag if you wish to apply local thresholding via the Minimum Spanning '
                             'Tree approach. -thr values in this case correspond to a target density (if the -dt flag is '
                             'also included), otherwise a target proportional threshold.\n')
    parser.add_argument('-df',
                        default=False,
                        action='store_true',
                        help='Optionally use this flag if you wish to apply local thresholding via the disparity filter '
                             'approach. -thr values in this case correspond to α.\n')
    #    parser.add_argument('-at',
    #        default=False,
    #        action='store_true',
    #        help='Optionally use this flag if you wish to activate adaptive thresholding')
    parser.add_argument('-embed',
                        default=False,
                        action='store_true',
                        help='Optionally use this flag if you wish to embed the ensemble produced into a set of omnibus '
                             'feature vectors.\n')
    parser.add_argument('-plt',
                        default=False,
                        action='store_true',
                        help='Optionally use this flag if you wish to activate plotting of adjacency matrices, '
                             'connectomes, and time-series.\n')
    parser.add_argument('-pm',
                        metavar='Cores,memory',
                        default='2,4',
                        help='Number of cores to use, number of GB of memory to use for single subject run, entered as '
                             'two integers seperated by a comma.\n')
    parser.add_argument('-plug',
                        metavar='Scheduler type',
                        default='MultiProc',
                        nargs=1,
                        choices=['Linear', 'MultiProc', 'SGE', 'PBS', 'SLURM', 'SGEgraph', 'SLURMgraph'],
                        help='Include this flag to specify a workflow plugin other than the default MultiProc.\n')
    parser.add_argument('-v',
                        default=False,
                        action='store_true',
                        help='Verbose print for debugging.\n')
    return parser


def build_workflow(args, retval):
    import os
    import os.path as op
    import sys
    import timeit
    import numpy as np
    from pathlib import Path
    import types
    import warnings
    warnings.filterwarnings("ignore")
    np.warnings.filterwarnings('ignore')
    import yaml
    try:
        import pynets
    except ImportError:
        print('PyNets not installed! Ensure that you are using the correct python version.')
    from pynets.utils import do_dir_path

    # Start time clock
    start_time = timeit.default_timer()

    # Set Arguments to global variables
    func_file = args.func
    mask = args.m
    dwi_file = args.dwi
    fbval = args.bval
    fbvec = args.bvec
    graph_pre = args.g
    graph = list(str(graph_pre).split(','))
    if graph:
        if len(graph) > 1:
            multi_graph = graph
            graph = None
        elif graph == ['None']:
            graph = None
            multi_graph = None
        else:
            graph = graph[0]
            multi_graph = None
    else:
        multi_graph = None
    ID = args.id
    resources = args.pm
    if resources:
        procmem = list(eval(str(resources)))
    else:
        from multiprocessing import cpu_count
        nthreads = cpu_count()
        procmem = [int(nthreads), int(float(nthreads)*2)]
    thr = float(args.thr)
    node_size_pre = args.ns
    node_size = node_size_pre
    if node_size:
        if (type(node_size) is list) and (len(node_size) > 1):
            node_size_list = node_size
            node_size = None
        elif node_size == ['None']:
            node_size = None
            node_size_list = None
        elif type(node_size) is list:
            node_size = node_size[0]
            node_size_list = None
        else:
            node_size = None
            node_size_list = None
    else:
        node_size_list = None
    smooth_pre = args.sm
    smooth = smooth_pre
    if smooth:
        if (type(smooth) is list) and (len(smooth) > 1):
            smooth_list = smooth
            smooth = 0
        elif smooth == ['None']:
            smooth = 0
            smooth_list = None
        elif type(smooth) is list:
            smooth = smooth[0]
            smooth_list = None
        else:
            smooth = 0
            smooth_list = None
    else:
        smooth_list = None
    c_boot = args.b
    block_size = args.bs
    roi = args.roi
    conn_model_pre = args.mod
    conn_model = conn_model_pre
    if conn_model:
        if (type(conn_model) is list) and (len(conn_model) > 1):
            conn_model_list = conn_model
        elif conn_model == ['None']:
            conn_model_list = None
        elif type(conn_model) is list:
            conn_model = conn_model[0]
            conn_model_list = None
        else:
            conn_model_list = None
    else:
        conn_model_list = None
    conf = args.conf
    dens_thresh = args.dt
    min_span_tree = args.mst
    disp_filt = args.df
    clust_type_pre = args.ct
    clust_type = clust_type_pre
    if clust_type:
        if (type(clust_type) is list) and len(clust_type) > 1:
            clust_type_list = clust_type
            clust_type = None
        elif clust_type == ['None']:
            clust_type = None
            clust_type_list = None
        elif type(clust_type) is list:
            clust_type = clust_type[0]
            clust_type_list = None
        else:
            clust_type = None
            clust_type_list = None
    else:
        clust_type_list = None
    # adapt_thresh=args.at
    adapt_thresh = False
    plot_switch = args.plt
    min_thr = args.min_thr
    max_thr = args.max_thr
    step_thr = args.step_thr
    anat_file = args.anat
    num_total_samples = args.s
    parc = args.parc
    if parc is True:
        node_size = None
        node_size_list = None
    else:
        if node_size:
            if node_size is None:
                if (func_file is not None) and (dwi_file is None):
                    node_size = 4
                elif (func_file is None) and (dwi_file is not None):
                    node_size = 8
    ref_txt = args.ref
    k = args.k
    k_min = args.k_min
    k_max = args.k_max
    k_step = args.k_step
    clust_mask_pre = args.cm
    prune = args.p
    norm = args.norm
    if type(norm) is list:
        norm = norm[0]
    binary = args.bin
    plugin_type = args.plug
    if type(plugin_type) is list:
        plugin_type = plugin_type[0]
    use_AAL_naming = args.names
    verbose = args.v
    clust_mask = list(str(clust_mask_pre).split(','))
    if len(clust_mask) > 1:
        clust_mask_list = clust_mask
        clust_mask = None
    elif clust_mask == ['None']:
        clust_mask = None
        clust_mask_list = None
    else:
        clust_mask = clust_mask[0]
        clust_mask_list = None
    network_pre = args.n
    network = network_pre
    if network:
        if (type(network) is list) and (len(network) > 1):
            multi_nets = network
            network = None
        elif network == ['None']:
            network = None
            multi_nets = None
        elif type(network) is list:
            network = network[0]
            multi_nets = None
        else:
            network = None
            multi_nets = None
    else:
        multi_nets = None
    uatlas_select_pre = args.ua
    atlas_select_pre = args.a
    uatlas_select = list(str(uatlas_select_pre).split(','))
    if len(uatlas_select) > 1:
        user_atlas_list = uatlas_select
        uatlas_select = None
    elif uatlas_select == ['None']:
        uatlas_select = None
        user_atlas_list = None
    else:
        uatlas_select = uatlas_select[0]
        user_atlas_list = None
    atlas_select = atlas_select_pre
    if atlas_select:
        if (type(atlas_select) is list) and (len(atlas_select) > 1):
            multi_atlas = atlas_select
            atlas_select = None
        elif atlas_select == ['None']:
            multi_atlas = None
            atlas_select = None
        elif type(atlas_select) is list:
            atlas_select = atlas_select[0]
            multi_atlas = None
        else:
            atlas_select = None
            multi_atlas = None
    else:
        multi_atlas = None
    target_samples = args.s
    max_length = args.ml
    track_type = args.tt
    if type(track_type) is list:
        track_type = track_type[0]
    tiss_class = args.tc
    if type(tiss_class) is list:
        tiss_class = tiss_class[0]
    if track_type == 'particle':
        tiss_class = 'cmc'
    directget = args.dg
    if directget:
        if (type(directget) is list) and (len(directget) > 1):
            multi_directget = directget
        elif type(directget) is list:
            directget = directget[0]
            multi_directget = None
        else:
            multi_directget = None
    else:
        multi_directget = None
    embed = args.embed

    print('\n\n\n------------------------------------------------------------------------\n')

    # Hard-coded:
    with open("%s%s" % (str(Path(__file__).parent), '/runconfig.yaml'), 'r') as stream:
        try:
            hardcoded_params = yaml.load(stream)
            maxcrossing = hardcoded_params['maxcrossing'][0]
            min_length = hardcoded_params['min_length'][0]
            overlap_thr = hardcoded_params['overlap_thr'][0]
            overlap_thr_list = hardcoded_params['overlap_thr_list'][0]
            step_list = hardcoded_params['step_list']
            curv_thr_list = hardcoded_params['curv_thr_list']
            life_run = hardcoded_params['life_run'][0]
            nilearn_parc_atlases = hardcoded_params['nilearn_parc_atlases']
            nilearn_coord_atlases = hardcoded_params['nilearn_coord_atlases']
            nilearn_prob_atlases = hardcoded_params['nilearn_prob_atlases']
            runtime_dict = {'fetch_nodes_and_labels_node': (1, 1), 'extract_ts_node': (1, 4), 'node_gen_node': (1, 1),
                            'clustering_node': (1, 4), 'get_conn_matrix_node': (1, 1), 'thresh_func_node': (1, 1),
                            'register_node': (1, 2), 'get_fa_node': (1, 1), 'run_tracking_node': (1, 4),
                            'thresh_diff_node': (1, 1), 'dsn_node': (1, 2), 'streams2graph_node': (1, 2)}
        except FileNotFoundError:
            print('Failed to parse runconfig.yaml')

    if (min_thr is not None) and (max_thr is not None) and (step_thr is not None):
        multi_thr = True
    elif (min_thr is not None) or (max_thr is not None) or (step_thr is not None):
        raise ValueError('Error: Missing either min_thr, max_thr, or step_thr flags!')
    else:
        multi_thr = False

    # Check required inputs for existence, and configure run
    if func_file:
        if func_file.endswith('.txt'):
            with open(func_file) as f:
                func_subjects_list = f.read().splitlines()
        elif ',' in func_file:
            func_subjects_list = list(str(func_file).split(','))
        else:
            func_subjects_list = None
    else:
        func_subjects_list = None

    if dwi_file and (not anat_file and not fbval and not fbvec):
        raise ValueError('ERROR: Anatomical image(s) (-anat), b-values file(s) (-fbval), and b-vectors file(s) (-fbvec) '
                         'must be specified for structural connectometry.')

    if dwi_file:
        if dwi_file.endswith('.txt'):
            with open(func_file) as f:
                struct_subjects_list = f.read().splitlines()
        elif ',' in dwi_file:
            struct_subjects_list = list(str(dwi_file).split(','))
        else:
            struct_subjects_list = None
    else:
        struct_subjects_list = None

    if (func_file is None) and (dwi_file is None) and (graph is None) and (multi_graph is None):
        raise ValueError("\nError: You must include a file path to either a standard space functional image in .nii or "
                         ".nii.gz format with the -func flag.")

    if (ID is None) and (func_subjects_list is None):
        raise ValueError("\nError: You must include a subject ID in your command line call.")

    if func_subjects_list and ',' in ID:
        ID = list(str(ID).split(','))
        if len(ID) != len(func_subjects_list):
            raise ValueError("Error: Length of ID list does not correspond to length of input func file list.")

    if conf:
        if ',' in conf:
            conf = list(str(conf).split(','))
            if len(conf) != len(func_subjects_list):
                raise ValueError("Error: Length of confound regressor list does not correspond to length of input file "
                                 "list.")

    if struct_subjects_list and ',' in ID:
        ID = list(str(ID).split(','))
        if len(ID) != len(struct_subjects_list):
            raise ValueError("Error: Length of ID list does not correspond to length of input dwi file list.")

    if fbval:
        if ',' in fbval:
            fbval = list(str(fbval).split(','))
            if len(fbval) != len(struct_subjects_list):
                raise ValueError("Error: Length of fbval list does not correspond to length of input dwi file list.")

    if fbvec:
        if ',' in fbvec:
            fbvec = list(str(fbval).split(','))
            if len(fbvec) != len(struct_subjects_list):
                raise ValueError("Error: Length of fbvec list does not correspond to length of input dwi file list.")

    if anat_file:
        if ',' in anat_file:
            anat_file = list(str(anat_file).split(','))
            if len(anat_file) != len(struct_subjects_list):
                raise ValueError("Error: Length of anat list does not correspond to length of input dwi file list.")

    if (c_boot and not block_size) or (block_size and not c_boot):
        raise ValueError("Error: Both number of bootstraps (-b) and block size (-bs) must be specified to run "
                         "bootstrapped resampling.")

    if mask:
        if not roi:
            roi = mask
        if ',' in mask:
            mask = list(str(mask).split(','))
            if len(mask) != len(func_subjects_list):
                raise ValueError("Error: Length of brain mask list does not correspond to length of input file list.")

    if multi_thr is True:
        thr = None
    else:
        min_thr = None
        max_thr = None
        step_thr = None

    if (k_min is not None and k_max is not None) and k is None and clust_mask_list is not None and clust_type_list is not None:
        k_clustering = 8
    elif k is not None and (k_min is None and k_max is None) and clust_mask_list is not None and clust_type_list is not None:
        k_clustering = 7
    elif (k_min is not None and k_max is not None) and k is None and clust_mask_list is None and clust_type_list is not None:
        k_clustering = 6
    elif k is not None and (k_min is None and k_max is None) and clust_mask_list is None and clust_type_list is not None:
        k_clustering = 5
    elif (k_min is not None and k_max is not None) and k is None and clust_mask_list is not None and clust_type_list is None:
        k_clustering = 4
    elif k is not None and (k_min is None and k_max is None) and clust_mask_list is not None and clust_type_list is None:
        k_clustering = 3
    elif (k_min is not None and k_max is not None) and k is None and clust_mask_list is None and clust_type_list is None:
        k_clustering = 2
    elif k is not None and (k_min is None and k_max is None) and clust_mask_list is None and clust_type_list is None:
        k_clustering = 1
    else:
        k_clustering = 0

    if func_subjects_list or struct_subjects_list:
        print('\nRunning workflow of workflows across multiple subjects:')
    elif func_subjects_list is None and struct_subjects_list is None:
        print('\nRunning workflow across single subject:')
    print(str(ID))

    if func_file:
        if (uatlas_select is not None) and (k_clustering == 0) and (user_atlas_list is None):
            atlas_select_par = uatlas_select.split('/')[-1].split('.')[0]
            print("%s%s" % ("\nUser atlas: ", atlas_select_par))
            if func_subjects_list:
                for func_file in func_subjects_list:
                    do_dir_path(atlas_select_par, func_file)
            else:
                do_dir_path(atlas_select_par, func_file)
        elif (uatlas_select is not None) and (user_atlas_list is None) and (k_clustering == 0):
            atlas_select_par = uatlas_select.split('/')[-1].split('.')[0]
            print("%s%s" % ("\nUser atlas: ", atlas_select_par))
            if func_subjects_list:
                for func_file in func_subjects_list:
                    do_dir_path(atlas_select_par, func_file)
            else:
                do_dir_path(atlas_select_par, func_file)
        elif user_atlas_list is not None:
            print('\nIterating across multiple user atlases...')
            if func_subjects_list:
                for uatlas_select in user_atlas_list:
                    atlas_select_par = uatlas_select.split('/')[-1].split('.')[0]
                    print(atlas_select_par)
                    for func_file in func_subjects_list:
                        do_dir_path(atlas_select_par, func_file)
            else:
                for uatlas_select in user_atlas_list:
                    atlas_select_par = uatlas_select.split('/')[-1].split('.')[0]
                    print(atlas_select_par)
                    do_dir_path(atlas_select_par, func_file)
        if k_clustering == 1:
            cl_mask_name = op.basename(clust_mask).split('.nii.gz')[0]
            atlas_select_clust = "%s%s%s%s%s" % (cl_mask_name, '_', clust_type, '_k', k)
            print("%s%s" % ("\nCluster atlas: ", atlas_select_clust))
            print("\nClustering within mask at a single resolution...")
            if func_subjects_list:
                for func_file in func_subjects_list:
                    do_dir_path(atlas_select_clust, func_file)
            else:
                do_dir_path(atlas_select_clust, func_file)
        elif k_clustering == 2:
            k_list = np.round(np.arange(int(k_min), int(k_max), int(k_step)), decimals=0).tolist() + [int(k_max)]
            print("\nClustering within mask at multiple resolutions...")
            if func_subjects_list:
                for k in k_list:
                    cl_mask_name = op.basename(clust_mask).split('.nii.gz')[0]
                    atlas_select_clust = "%s%s%s%s%s" % (cl_mask_name, '_', clust_type, '_k', k)
                    print("%s%s" % ("Cluster atlas: ", atlas_select_clust))
                    for func_file in func_subjects_list:
                        do_dir_path(atlas_select_clust, func_file)
            else:
                for k in k_list:
                    cl_mask_name = op.basename(clust_mask).split('.nii.gz')[0]
                    atlas_select_clust = "%s%s%s%s%s" % (cl_mask_name, '_', clust_type, '_k', k)
                    print("%s%s" % ("Cluster atlas: ", atlas_select_clust))
                    do_dir_path(atlas_select_clust, func_file)
        elif k_clustering == 3:
            print("\nClustering within multiple masks at a single resolution...")
            if func_subjects_list:
                for clust_mask in clust_mask_list:
                    cl_mask_name = op.basename(clust_mask).split('.nii.gz')[0]
                    atlas_select_clust = "%s%s%s%s%s" % (cl_mask_name, '_', clust_type, '_k', k)
                    for func_file in func_subjects_list:
                        do_dir_path(atlas_select_clust, func_file)
            else:
                for clust_mask in clust_mask_list:
                    cl_mask_name = op.basename(clust_mask).split('.nii.gz')[0]
                    atlas_select_clust = "%s%s%s%s%s" % (cl_mask_name, '_', clust_type, '_k', k)
                    do_dir_path(atlas_select_clust, func_file)
            clust_mask = None
        elif k_clustering == 4:
            print("\nClustering within multiple masks at multiple resolutions...")
            k_list = np.round(np.arange(int(k_min), int(k_max), int(k_step)), decimals=0).tolist() + [int(k_max)]
            if func_subjects_list:
                for clust_mask in clust_mask_list:
                    for k in k_list:
                        cl_mask_name = op.basename(clust_mask).split('.nii.gz')[0]
                        atlas_select_clust = "%s%s%s%s%s" % (cl_mask_name, '_', clust_type, '_k', k)
                        for func_file in func_subjects_list:
                            do_dir_path(atlas_select_clust, func_file)
            else:
                for clust_mask in clust_mask_list:
                    for k in k_list:
                        cl_mask_name = op.basename(clust_mask).split('.nii.gz')[0]
                        atlas_select_clust = "%s%s%s%s%s" % (cl_mask_name, '_', clust_type, '_k', k)
                        do_dir_path(atlas_select_clust, func_file)
            clust_mask = None
        elif k_clustering == 5:
            for clust_type in clust_type_list:
                cl_mask_name = op.basename(clust_mask).split('.nii.gz')[0]
                atlas_select_clust = "%s%s%s%s%s" % (cl_mask_name, '_', clust_type, '_k', k)
                print("%s%s" % ("\nCluster atlas: ", atlas_select_clust))
                print("\nClustering within mask at a single resolution using multiple clustering methods...")
                if func_subjects_list:
                    for func_file in func_subjects_list:
                        do_dir_path(atlas_select_clust, func_file)
                else:
                    do_dir_path(atlas_select_clust, func_file)
            clust_type = None
        elif k_clustering == 6:
            k_list = np.round(np.arange(int(k_min), int(k_max), int(k_step)), decimals=0).tolist() + [int(k_max)]
            print("\nClustering within mask at multiple resolutions using multiple clustering methods...")
            if func_subjects_list:
                for clust_type in clust_type_list:
                    for k in k_list:
                        cl_mask_name = op.basename(clust_mask).split('.nii.gz')[0]
                        atlas_select_clust = "%s%s%s%s%s" % (cl_mask_name, '_', clust_type, '_k', k)
                        print("%s%s" % ("Cluster atlas: ", atlas_select_clust))
                        for func_file in func_subjects_list:
                            do_dir_path(atlas_select_clust, func_file)
            else:
                for clust_type in clust_type_list:
                    for k in k_list:
                        cl_mask_name = op.basename(clust_mask).split('.nii.gz')[0]
                        atlas_select_clust = "%s%s%s%s%s" % (cl_mask_name, '_', clust_type, '_k', k)
                        print("%s%s" % ("Cluster atlas: ", atlas_select_clust))
                        do_dir_path(atlas_select_clust, func_file)
            clust_type = None
        elif k_clustering == 7:
            print("\nClustering within multiple masks at a single resolution using multiple clustering methods...")
            if func_subjects_list:
                for clust_type in clust_type_list:
                    for clust_mask in clust_mask_list:
                        cl_mask_name = op.basename(clust_mask).split('.nii.gz')[0]
                        atlas_select_clust = "%s%s%s%s%s" % (cl_mask_name, '_', clust_type, '_k', k)
                        print("%s%s" % ("Cluster atlas: ", atlas_select_clust))
                        for func_file in func_subjects_list:
                            do_dir_path(atlas_select_clust, func_file)
            else:
                for clust_type in clust_type_list:
                    for clust_mask in clust_mask_list:
                        cl_mask_name = op.basename(clust_mask).split('.nii.gz')[0]
                        atlas_select_clust = "%s%s%s%s%s" % (cl_mask_name, '_', clust_type, '_k', k)
                        do_dir_path(atlas_select_clust, func_file)
            clust_mask = None
            clust_type = None
        elif k_clustering == 8:
            print("\nClustering within multiple masks at multiple resolutions using multiple clustering methods...")
            k_list = np.round(np.arange(int(k_min), int(k_max), int(k_step)), decimals=0).tolist() + [int(k_max)]
            if func_subjects_list:
                for clust_type in clust_type_list:
                    for clust_mask in clust_mask_list:
                        for k in k_list:
                            cl_mask_name = op.basename(clust_mask).split('.nii.gz')[0]
                            atlas_select_clust = "%s%s%s%s%s" % (cl_mask_name, '_', clust_type, '_k', k)
                            print("%s%s" % ("Cluster atlas: ", atlas_select_clust))
                            for func_file in func_subjects_list:
                                do_dir_path(atlas_select_clust, func_file)
            else:
                for clust_type in clust_type_list:
                    for clust_mask in clust_mask_list:
                        for k in k_list:
                            cl_mask_name = op.basename(clust_mask).split('.nii.gz')[0]
                            atlas_select_clust = "%s%s%s%s%s" % (cl_mask_name, '_', clust_type, '_k', k)
                            do_dir_path(atlas_select_clust, func_file)
            clust_mask = None
            clust_type = None
        elif (user_atlas_list is not None or uatlas_select is not None) and (k_clustering == 4 or k_clustering == 3 or
                                                                             k_clustering == 2 or
                                                                             k_clustering == 1) and atlas_select is None:
            print('Error: the -ua flag cannot be used alone with the clustering option. Use the -cm flag instead.')
            sys.exit(0)

        if multi_atlas is not None:
            print('\nIterating across multiple predefined atlases...')
            if func_subjects_list:
                for func_file in func_subjects_list:
                    for atlas_select in multi_atlas:
                        if (parc is True) and (atlas_select in nilearn_coord_atlases or atlas_select in nilearn_prob_atlases):
                            raise ValueError("%s%s%s" % ('\nERROR: ', atlas_select,
                                                         ' is a coordinate atlas and cannot be combined with the -parc flag.'))
                        else:
                            print(atlas_select)
                            do_dir_path(atlas_select, func_file)
            else:
                for atlas_select in multi_atlas:
                    if (parc is True) and (atlas_select in nilearn_coord_atlases or atlas_select in nilearn_prob_atlases):
                        raise ValueError("%s%s%s" % ('\nERROR: ', atlas_select,
                                                     ' is a coordinate atlas and cannot be combined with the -parc flag.'))
                    else:
                        print(atlas_select)
                        do_dir_path(atlas_select, func_file)
        elif atlas_select is not None:
            if (parc is True) and (atlas_select in nilearn_coord_atlases or atlas_select in nilearn_prob_atlases):
                raise ValueError("%s%s%s" % ('\nERROR: ', atlas_select,
                                             ' is a coordinate atlas and cannot be combined with the -parc flag.'))
            else:
                print("%s%s" % ("\nPredefined atlas: ", atlas_select))
                if func_subjects_list:
                    for func_file in func_subjects_list:
                        do_dir_path(atlas_select, func_file)
                else:
                    do_dir_path(atlas_select, func_file)
        else:
            if (uatlas_select is None) and (k == 0):
                raise KeyError('\nERROR: No atlas specified!')
            else:
                pass

    elif graph or multi_graph:
        network = 'custom_graph'
        thr = 0
        roi = 'None'
        k_clustering = 0
        node_size = 'None'
        smooth = 'None'
        conn_model = 'None'
        c_boot = 'None'
        if multi_graph:
            print('\nUsing multiple custom input graphs...')
            conn_model = None
            conn_model_list = []
            i = 1
            for graph in multi_graph:
                conn_model_list.append(str(i))
                if '.txt' in graph:
                    graph_name = op.basename(graph).split('.txt')[0]
                elif '.npy' in graph:
                    graph_name = op.basename(graph).split('.npy')[0]
                else:
                    print('Error: input graph file format not recognized. See -help for supported formats.')
                    sys.exit(0)
                print(graph_name)
                atlas_select = "%s%s%s" % (graph_name, '_', ID)
                do_dir_path(atlas_select, graph)
                i = i + 1
        else:
            if '.txt' in graph:
                graph_name = op.basename(graph).split('.txt')[0]
            elif '.npy' in graph:
                graph_name = op.basename(graph).split('.npy')[0]
            else:
                print('Error: input graph file format not recognized. See -help for supported formats.')
                sys.exit(0)
            print('\nUsing single custom graph input...')
            print(graph_name)
            atlas_select = "%s%s%s" % (graph_name, '_', ID)
            do_dir_path(atlas_select, graph)

    if graph is None and multi_graph is None:
        if network is not None:
            print("%s%s" % ('\nUsing resting-state network pipeline for: ', network))
        elif multi_nets is not None:
            network = multi_nets[0]
            print("%s%d%s%s%s" % ('\nIterating workflow across ', len(multi_nets), ' networks: ',
                                  str(', '.join(str(n) for n in multi_nets)), '...'))
        else:
            print("\nUsing whole-brain pipeline...")

        if node_size_list:
            print("%s%s%s" % ('\nGrowing spherical nodes across multiple radius sizes: ',
                              str(', '.join(str(n) for n in node_size_list)), '...'))
        elif parc is True:
            print("\nUsing parcels as nodes...")
        else:
            if node_size is None:
                node_size = 4
            print("%s%s%s" % ("\nUsing node size of: ", node_size, 'mm...'))

        if smooth_list:
            print("%s%s%s" % ('\nApplying smoothing to node signal at multiple FWHM mm values: ',
                              str(', '.join(str(n) for n in smooth_list)), '...'))
        elif float(smooth) > 0:
            print("%s%s%s" % ("\nApplying smoothing to node signal at: ", smooth, 'FWHM mm...'))
        else:
            smooth = 0

        if func_file:
            if float(c_boot) > 0:
                try:
                    c_boot = int(c_boot)
                    try:
                        block_size = int(block_size)
                    except ValueError:
                        print('ERROR: size of bootstrap blocks indicated with the -bs flag must be an integer > 0.')
                except ValueError:
                    print('ERROR: number of boostraps indicated with the -b flag must be an integer > 0.')
                print("%s%s%s%s" % ('Applying circular block bootstrapping to the node-extracted time-series using: ',
                                    int(c_boot), ' bootstraps with block size ', int(block_size)))

        if conn_model_list:
            print("%s%s%s" % ('\nIterating graph estimation across multiple connectivity models: ',
                              str(', '.join(str(n) for n in conn_model_list)), '...'))
        else:
            print("%s%s%s" % ("\nUsing connectivity model:\n", conn_model, '\n'))

    if dwi_file:
        if network is not None:
            print("%s%s" % ('\nRSN: ', network))
        if user_atlas_list is not None:
            print('\nIterating across multiple user atlases...')
            if struct_subjects_list:
                for dwi_file in struct_subjects_list:
                    for uatlas_select in user_atlas_list:
                        atlas_select_par = uatlas_select.split('/')[-1].split('.')[0]
                        print(atlas_select_par)
                        do_dir_path(atlas_select_par, dwi_file)
            else:
                for uatlas_select in user_atlas_list:
                    atlas_select_par = uatlas_select.split('/')[-1].split('.')[0]
                    print(atlas_select_par)
                    do_dir_path(atlas_select_par, dwi_file)
        elif (uatlas_select is not None) and (user_atlas_list is None):
            atlas_select_par = uatlas_select.split('/')[-1].split('.')[0]
            ref_txt = "%s%s" % (uatlas_select.split('/')[-1:][0].split('.')[0], '.txt')
            if struct_subjects_list:
                for dwi_file in struct_subjects_list:
                    do_dir_path(atlas_select_par, dwi_file)
            else:
                do_dir_path(atlas_select_par, dwi_file)
        if multi_atlas is not None:
            print('\nIterating across multiple predefined atlases...')
            if struct_subjects_list:
                for dwi_file in struct_subjects_list:
                    for atlas_select in multi_atlas:
                        if (parc is True) and (atlas_select in nilearn_coord_atlases):
                            raise ValueError("%s%s%s" % ('\nERROR: ', atlas_select,
                                                         ' is a coordinate atlas and cannot be combined with the -parc flag.'))
                        else:
                            print(atlas_select)
                            do_dir_path(atlas_select, dwi_file)
            else:
                for atlas_select in multi_atlas:
                    if (parc is True) and (atlas_select in nilearn_coord_atlases):
                        raise ValueError("%s%s%s" % ('\nERROR: ', atlas_select,
                                                     ' is a coordinate atlas and cannot be combined with the -parc flag.'))
                    else:
                        print(atlas_select)
                        do_dir_path(atlas_select, dwi_file)
        elif atlas_select is not None:
            if (parc is True) and (atlas_select in nilearn_coord_atlases):
                raise ValueError("%s%s%s" % ('\nERROR: ', atlas_select,
                                             ' is a coordinate atlas and cannot be combined with the -parc flag.'))
            else:
                print("%s%s" % ("\nNilearn atlas: ", atlas_select))
                if struct_subjects_list:
                    for dwi_file in struct_subjects_list:
                        do_dir_path(atlas_select, dwi_file)
                else:
                    do_dir_path(atlas_select, dwi_file)
        else:
            if uatlas_select is None:
                raise KeyError('\nERROR: No atlas specified!')
            else:
                pass

    elif graph or multi_graph:
        network = 'custom_graph'
        thr = 0
        roi = 'None'
        k_clustering = 0
        node_size = 'None'
        smooth = 'None'
        conn_model = 'None'
        c_boot = 'None'
        if multi_graph:
            print('\nUsing multiple custom input graphs...')
            conn_model = None
            conn_model_list = []
            i = 1
            for graph in multi_graph:
                conn_model_list.append(str(i))
                if '.txt' in graph:
                    graph_name = op.basename(graph).split('.txt')[0]
                elif '.npy' in graph:
                    graph_name = op.basename(graph).split('.npy')[0]
                else:
                    print('Error: input graph file format not recognized. See -help for supported formats.')
                    sys.exit(0)
                print(graph_name)
                atlas_select = "%s%s%s" % (graph_name, '_', ID)
                do_dir_path(atlas_select, graph)
                i = i + 1
        else:
            if '.txt' in graph:
                graph_name = op.basename(graph).split('.txt')[0]
            elif '.npy' in graph:
                graph_name = op.basename(graph).split('.npy')[0]
            else:
                print('Error: input graph file format not recognized. See -help for supported formats.')
                sys.exit(0)
            print('\nUsing single custom graph input...')
            print(graph_name)
            atlas_select = "%s%s%s" % (graph_name, '_', ID)
            do_dir_path(atlas_select, graph)

    if dwi_file:
        if network:
            print("%s%s" % ('\nRSN: ', network))
        if user_atlas_list:
            print('\nIterating across multiple user atlases...')
            if struct_subjects_list:
                for dwi_file in struct_subjects_list:
                    for uatlas_select in user_atlas_list:
                        atlas_select_par = uatlas_select.split('/')[-1].split('.')[0]
                        print(atlas_select_par)
                        do_dir_path(atlas_select_par, dwi_file)
            else:
                for uatlas_select in user_atlas_list:
                    atlas_select_par = uatlas_select.split('/')[-1].split('.')[0]
                    print(atlas_select_par)
                    do_dir_path(atlas_select_par, dwi_file)
        elif (uatlas_select is not None) and (user_atlas_list is None):
            atlas_select_par = uatlas_select.split('/')[-1].split('.')[0]
            ref_txt = "%s%s" % (uatlas_select.split('/')[-1:][0].split('.')[0], '.txt')
            if struct_subjects_list:
                for dwi_file in struct_subjects_list:
                    do_dir_path(atlas_select_par, dwi_file)
            else:
                do_dir_path(atlas_select_par, dwi_file)
        if multi_atlas:
            print('\nIterating across multiple predefined atlases...')
            if struct_subjects_list:
                for dwi_file in struct_subjects_list:
                    for atlas_select in multi_atlas:
                        if (parc is True) and (atlas_select in nilearn_coord_atlases):
                            raise ValueError("%s%s%s" % ('\nERROR: ', atlas_select,
                                                         ' is a coordinate atlas and cannot be combined with the -parc flag.'))
                        else:
                            print(atlas_select)
                            do_dir_path(atlas_select, dwi_file)
            else:
                for atlas_select in multi_atlas:
                    if (parc is True) and (atlas_select in nilearn_coord_atlases):
                        raise ValueError("%s%s%s" % ('\nERROR: ', atlas_select,
                                                     ' is a coordinate atlas and cannot be combined with the -parc flag.'))
                    else:
                        print(atlas_select)
                        do_dir_path(atlas_select, dwi_file)
        elif atlas_select:
            if (parc is True) and (atlas_select in nilearn_coord_atlases):
                raise ValueError("%s%s%s" % ('\nERROR: ', atlas_select,
                                             ' is a coordinate atlas and cannot be combined with the -parc flag.'))
            else:
                print("%s%s" % ("\nNilearn atlas: ", atlas_select))
                if struct_subjects_list:
                    for dwi_file in struct_subjects_list:
                        do_dir_path(atlas_select, dwi_file)
                else:
                    do_dir_path(atlas_select, dwi_file)
        else:
            if uatlas_select is None:
                raise KeyError('\nERROR: No atlas specified!')
            else:
                pass
        if target_samples:
            print("%s%s%s" % ('Using ', target_samples, ' samples...'))
        if max_length:
            print("%s%s%s" % ('Using ', max_length, ' maximum length of streamlines...'))

    if dwi_file and not func_file:
        print('\nRunning structural connectometry only...')
        if struct_subjects_list:
            for (dwi_file, fbval, fbvec, anat_file) in struct_subjects_list:
                print("%s%s" % ('Diffusion-Weighted Image:\n', dwi_file))
                print("%s%s" % ('B-Values:\n', fbval))
                print("%s%s" % ('B-Vectors:\n', fbvec))
                print("%s%s" % ('Anatomical Image:\n', anat_file))
        else:
            print("%s%s" % ('Diffusion-Weighted Image:\n', dwi_file))
            print("%s%s" % ('B-Values:\n', fbval))
            print("%s%s" % ('B-Vectors:\n', fbvec))
            print("%s%s" % ('Anatomical Image:\n', anat_file))
        conf = None
        k = None
        clust_mask = None
        k_min = None
        k_max = None
        k_step = None
        k_clustering = None
        clust_mask_list = None
        smooth = None
        clust_type = None
        clust_type_list = None
        c_boot = None
        block_size = None
    elif func_file and dwi_file is None:
        print('\nRunning functional connectometry only...')
        if func_subjects_list:
            for func_file in func_subjects_list:
                print("%s%s" % ('Functional file: ', func_file))
        else:
            print("%s%s" % ('Functional file: ', func_file))
    elif func_file and dwi_file:
        print('\nRunning joint structural-functional connectometry...')
        print("%s%s" % ('Functional file:\n', func_file))
        print("%s%s" % ('Diffusion-Weighted Image:\n', dwi_file))
        print("%s%s" % ('B-Values:\n', fbval))
        print("%s%s" % ('B-Vectors:\n', fbvec))
        print("%s%s" % ('Anatomical Image:\n', anat_file))
    print('\n-------------------------------------------------------------------------\n\n')

    # print('\n\n\n\n\n')
    # print("%s%s" % ('ID: ', ID))
    # print("%s%s" % ('atlas_select: ', atlas_select))
    # print("%s%s" % ('network: ', network))
    # print("%s%s" % ('node_size: ', node_size))
    # print("%s%s" % ('smooth: ', smooth))
    # print("%s%s" % ('roi: ', roi))
    # print("%s%s" % ('thr: ', thr))
    # print("%s%s" % ('uatlas_select: ', uatlas_select))
    # print("%s%s" % ('conn_model: ', conn_model))
    # print("%s%s" % ('dens_thresh: ', dens_thresh))
    # print("%s%s" % ('conf: ', conf))
    # print("%s%s" % ('plot_switch: ', plot_switch))
    # print("%s%s" % ('multi_thr: ', multi_thr))
    # print("%s%s" % ('multi_atlas: ', multi_atlas))
    # print("%s%s" % ('min_thr: ', min_thr))
    # print("%s%s" % ('max_thr: ', max_thr))
    # print("%s%s" % ('step_thr: ', step_thr))
    # print("%s%s" % ('parc: ', parc))
    # print("%s%s" % ('ref_txt: ', ref_txt))
    # print("%s%s" % ('procmem: ', procmem))
    # print("%s%s" % ('k: ', k))
    # print("%s%s" % ('clust_mask: ', clust_mask))
    # print("%s%s" % ('k_min: ', k_min))
    # print("%s%s" % ('k_max: ', k_max))
    # print("%s%s" % ('k_step: ', k_step))
    # print("%s%s" % ('k_clustering: ', k_clustering))
    # print("%s%s" % ('user_atlas_list: ', user_atlas_list))
    # print("%s%s" % ('clust_mask_list: ', clust_mask_list))
    # print("%s%s" % ('prune: ', prune))
    # print("%s%s" % ('node_size_list: ', node_size_list))
    # print("%s%s" % ('smooth_list: ', smooth_list))
    # print("%s%s" % ('clust_type: ', clust_type))
    # print("%s%s" % ('clust_type_list: ', clust_type_list))
    # print("%s%s" % ('c_boot: ', c_boot))
    # print("%s%s" % ('block_size: ', block_size))
    # print("%s%s" % ('mask: ', mask))
    # print("%s%s" % ('norm: ', norm))
    # print("%s%s" % ('binary: ', binary))
    # print("%s%s" % ('embed: ', embed))
    # print("%s%s" % ('track_type: ', track_type))
    # print("%s%s" % ('tiss_class: ', tiss_class))
    # print("%s%s" % ('directget: ', directget))
    # print("%s%s" % ('multi_directget: ', multi_directget))
    # print('\n\n\n\n\n')
    # import sys
    # sys.exit(0)

    # Import wf core and interfaces
    import random
    from pynets.utils import CollectPandasDfs, Export2Pandas, ExtractNetStats, CollectPandasJoin
    from nipype.pipeline import engine as pe
    from nipype.interfaces import utility as niu
    from pynets.workflows import workflow_selector

    def init_wf_single_subject(ID, func_file, atlas_select, network, node_size, roi, thr, uatlas_select,
                               multi_nets, conn_model, dens_thresh, conf, adapt_thresh, plot_switch, dwi_file,
                               multi_thr, multi_atlas, min_thr, max_thr, step_thr, anat_file, parc, ref_txt, procmem, k,
                               clust_mask, k_min, k_max, k_step, k_clustering, user_atlas_list, clust_mask_list, prune,
                               node_size_list, num_total_samples, graph, conn_model_list, min_span_tree, verbose,
                               plugin_type, use_AAL_naming, multi_graph, smooth, smooth_list, disp_filt, clust_type,
                               clust_type_list, c_boot, block_size, mask, norm, binary, fbval, fbvec, target_samples,
                               curv_thr_list, step_list, overlap_thr, overlap_thr_list, track_type, max_length,
                               maxcrossing, life_run, min_length, directget, tiss_class, runtime_dict, embed,
                               multi_directget):

        if (func_file is not None) and (dwi_file is None):
            wf = pe.Workflow(name="%s%s%s%s" % ('Wf_single_sub_', ID, '_fmri_', random.randint(1, 1000)))
        elif (dwi_file is not None) and (func_file is None):
            wf = pe.Workflow(name="%s%s%s%s" % ('Wf_single_sub_', ID, '_dmri_', random.randint(1, 1000)))
        else:
            wf = pe.Workflow(name="%s%s%s%s" % ('Wf_single_sub_', ID, '_', random.randint(1, 1000)))
        import_list = ["import sys", "import os", "import numpy as np", "import networkx as nx",
                       "import nibabel as nib", "import warnings", "warnings.filterwarnings(\"ignore\")",
                       "np.warnings.filterwarnings(\"ignore\")"]
        inputnode = pe.Node(niu.IdentityInterface(fields=['ID', 'network', 'thr', 'node_size', 'roi', 'multi_nets',
                                                          'conn_model', 'plot_switch', 'graph', 'prune',
                                                          'norm', 'binary']),
                            name='inputnode', imports=import_list)
        if verbose is True:
            from nipype import config, logging
            cfg_v = dict(logging={'workflow_level': 'DEBUG', 'utils_level': 'DEBUG', 'log_to_file': True,
                                  'interface_level': 'DEBUG'},
                         monitoring={'enabled': True, 'sample_frequency': '0.1', 'summary_append': True})
            logging.update_logging(config)
            config.update_config(cfg_v)
            config.enable_debug_mode()
            config.enable_resource_monitor()

        cfg = dict(execution={'stop_on_first_crash': False, 'crashfile_format': 'txt', 'parameterize_dirs': True,
                              'display_variable': ':0', 'matplotlib_backend': 'Agg',
                              'plugin': str(plugin_type), 'use_relative_paths': True, 'keep_inputs': True,
                              'remove_unnecessary_outputs': True, 'remove_node_directories': False})
        for key in cfg.keys():
            for setting, value in cfg[key].items():
                wf.config[key][setting] = value

        inputnode.inputs.ID = ID
        inputnode.inputs.network = network
        inputnode.inputs.thr = thr
        inputnode.inputs.node_size = node_size
        inputnode.inputs.roi = roi
        inputnode.inputs.multi_nets = multi_nets
        inputnode.inputs.conn_model = conn_model
        inputnode.inputs.plot_switch = plot_switch
        inputnode.inputs.graph = graph
        inputnode.inputs.prune = prune
        inputnode.inputs.norm = norm
        inputnode.inputs.binary = binary

        meta_wf = workflow_selector(func_file, ID, atlas_select, network, node_size, roi, thr, uatlas_select,
                                    multi_nets, conn_model, dens_thresh, conf, adapt_thresh, plot_switch, dwi_file,
                                    anat_file, parc, ref_txt, procmem, multi_thr, multi_atlas, max_thr, min_thr,
                                    step_thr, k, clust_mask, k_min, k_max, k_step, k_clustering, user_atlas_list,
                                    clust_mask_list, prune, node_size_list, num_total_samples, conn_model_list,
                                    min_span_tree, verbose, plugin_type, use_AAL_naming, smooth, smooth_list, disp_filt,
                                    clust_type, clust_type_list, c_boot, block_size, mask, norm, binary, fbval, fbvec,
                                    target_samples, curv_thr_list, step_list, overlap_thr, overlap_thr_list, track_type,
                                    max_length, maxcrossing, life_run, min_length, directget, tiss_class, runtime_dict,
                                    embed, multi_directget)
        wf.add_nodes([meta_wf])

        # Set resource restrictions at level of the meta-meta wf
        if func_file:
            wf_selected = "%s%s" % ('functional_connectometry_', ID)
            for node_name in wf.get_node(meta_wf.name).get_node(wf_selected).list_node_names():
                if node_name in runtime_dict:
                    wf.get_node(meta_wf.name).get_node(wf_selected).get_node(node_name)._n_procs = runtime_dict[node_name][0]
                    wf.get_node(meta_wf.name).get_node(wf_selected).get_node(node_name)._mem_gb = runtime_dict[node_name][1]
            if k_clustering > 0:
                wf.get_node(meta_wf.name).get_node(wf_selected).get_node('clustering_node')._n_procs = 1
                wf.get_node(meta_wf.name).get_node(wf_selected).get_node('clustering_node')._mem_gb = 4

        if dwi_file:
            wf_selected = "%s%s" % ('structural_connectometry_', ID)
            for node_name in wf.get_node(meta_wf.name).get_node(wf_selected).list_node_names():
                if node_name in runtime_dict:
                    wf.get_node(meta_wf.name).get_node(wf_selected).get_node(node_name)._n_procs = runtime_dict[node_name][0]
                    wf.get_node(meta_wf.name).get_node(wf_selected).get_node(node_name)._mem_gb = runtime_dict[node_name][1]

        # Fully-automated graph analysis
        net_mets_node = pe.MapNode(interface=ExtractNetStats(), name="ExtractNetStats",
                                   iterfield=['ID', 'network', 'thr', 'conn_model', 'est_path',
                                              'roi', 'prune', 'node_size', 'norm', 'binary'], nested=True,
                                   imports=import_list)

        # Export graph analysis results to pandas dataframes
        export_to_pandas_node = pe.MapNode(interface=Export2Pandas(), name="Export2Pandas",
                                           iterfield=['csv_loc', 'ID', 'network', 'roi'], nested=True,
                                           imports=import_list)

        # Aggregate list of paths to pandas dataframe pickles
        collect_pd_list_net_pickles_node = pe.Node(niu.Function(input_names=['net_pickle_mt'],
                                                                output_names=['net_pickle_mt_out'],
                                                                function=CollectPandasJoin),
                                                   name="AggregatePandasPickles",
                                                   imports=import_list)

        # Combine dataframes across models
        collect_pandas_dfs_node = pe.Node(interface=CollectPandasDfs(), name="CollectPandasDfs",
                                          input_names=['network', 'ID', 'net_pickle_mt_list', 'plot_switch',
                                                       'multi_nets'], imports=import_list)

        handshake_node = meta_wf.get_node('pass_meta_outs_node')

        wf.connect([
            (handshake_node, net_mets_node, [('est_path_iterlist', 'est_path'),
                                             ('network_iterlist', 'network'),
                                             ('thr_iterlist', 'thr'),
                                             ('ID_iterlist', 'ID'),
                                             ('conn_model_iterlist', 'conn_model'),
                                             ('roi_iterlist', 'roi'),
                                             ('prune_iterlist', 'prune'),
                                             ('node_size_iterlist', 'node_size'),
                                             ('norm_iterlist', 'norm'),
                                             ('binary_iterlist', 'binary')]),
            (handshake_node, export_to_pandas_node, [('network_iterlist', 'network'),
                                                     ('ID_iterlist', 'ID'),
                                                     ('roi_iterlist', 'roi')]),
            (net_mets_node, export_to_pandas_node, [('out_file', 'csv_loc')]),
            (inputnode, collect_pandas_dfs_node, [('network', 'network'),
                                                  ('ID', 'ID'),
                                                  ('plot_switch', 'plot_switch'),
                                                  ('multi_nets', 'multi_nets')]),
            (export_to_pandas_node, collect_pd_list_net_pickles_node, [('net_pickle_mt', 'net_pickle_mt')]),
            (collect_pd_list_net_pickles_node, collect_pandas_dfs_node, [('net_pickle_mt_out', 'net_pickle_mt_list')])
        ])

        # Raw graph case
        if graph or multi_graph:
            wf.disconnect([(handshake_node, net_mets_node,
                            [('est_path_iterlist', 'est_path'),
                             ('network_iterlist', 'network'),
                             ('thr_iterlist', 'thr'),
                             ('ID_iterlist', 'ID'),
                             ('conn_model_iterlist', 'conn_model'),
                             ('roi_iterlist', 'roi'),
                             ('prune_iterlist', 'prune'),
                             ('node_size_iterlist', 'node_size'),
                             ('norm_iterlist', 'norm'),
                             ('binary_iterlist', 'binary')])
                           ])
            wf.disconnect([(handshake_node, export_to_pandas_node,
                            [('network_iterlist', 'network'),
                             ('ID_iterlist', 'ID'),
                             ('roi_iterlist', 'roi')])
                           ])
            wf.remove_nodes([meta_wf])
            # Multiple raw graphs
            if multi_graph:
                net_mets_node.inputs.est_path = multi_graph
                net_mets_node.inputs.ID = [ID] * len(multi_graph)
                net_mets_node.inputs.roi = [roi] * len(multi_graph)
                net_mets_node.inputs.node_size = [node_size] * len(multi_graph)
                net_mets_node.inputs.thr = [thr] * len(multi_graph)
                net_mets_node.inputs.prune = [prune] * len(multi_graph)
                net_mets_node.inputs.network = [network] * len(multi_graph)
                net_mets_node.inputs.conn_model = conn_model_list
                net_mets_node.inputs.norm = [norm] * len(multi_graph)
                net_mets_node.inputs.binary = [binary] * len(multi_graph)
                export_to_pandas_node.inputs.ID = [ID] * len(multi_graph)
                export_to_pandas_node.inputs.roi = [roi] * len(multi_graph)
                export_to_pandas_node.inputs.network = [network] * len(multi_graph)
            else:
                wf.connect([(inputnode, net_mets_node, [('network', 'network'),
                                                        ('thr', 'thr'),
                                                        ('ID', 'ID'),
                                                        ('conn_model', 'conn_model'),
                                                        ('roi', 'roi'),
                                                        ('prune', 'prune'),
                                                        ('node_size', 'node_size'),
                                                        ('graph', 'est_path'),
                                                        ('norm', 'norm'),
                                                        ('binary', 'binary')])
                            ])
                wf.connect([(inputnode, export_to_pandas_node, [('network', 'network'),
                                                                ('ID', 'ID'),
                                                                ('roi', 'roi')])
                            ])

        return wf

    # Multi-subject pipeline
    def wf_multi_subject(ID, func_subjects_list, struct_subjects_list, atlas_select, network, node_size, roi, thr,
                         uatlas_select, multi_nets, conn_model, dens_thresh, conf, adapt_thresh, plot_switch, dwi_file,
                         multi_thr, multi_atlas, min_thr, max_thr, step_thr, anat_file, parc, ref_txt, procmem, k,
                         clust_mask, k_min, k_max, k_step, k_clustering, user_atlas_list, clust_mask_list, prune,
                         node_size_list, num_total_samples, graph, conn_model_list, min_span_tree, verbose, plugin_type,
                         use_AAL_naming, multi_graph, smooth, smooth_list, disp_filt, clust_type, clust_type_list,
                         c_boot, block_size, mask, norm, binary, fbval, fbvec, target_samples, curv_thr_list, step_list,
                         overlap_thr, overlap_thr_list, track_type, max_length, maxcrossing, life_run, min_length,
                         directget, tiss_class, runtime_dict, embed, multi_directget):

        wf_multi = pe.Workflow(name="%s%s" % ('Wf_multisub_', random.randint(1001, 9000)))

        if func_subjects_list and not struct_subjects_list:
            struct_subjects_list = len(func_subjects_list) * [None]
        elif struct_subjects_list and not func_subjects_list:
            func_subjects_list = len(struct_subjects_list) * [None]
        else:
            pass

        i = 0
        for dwi_file, func_file in zip(struct_subjects_list, func_subjects_list):
            if conf and func_file:
                conf_sub = conf[i]
            else:
                conf_sub = None
            if fbval and dwi_file:
                fbval_sub = fbval[i]
            else:
                fbval_sub = None
            if fbvec and dwi_file:
                fbvec_sub = fbvec[i]
            else:
                fbvec_sub = None
            if mask:
                mask_sub = mask[i]
            else:
                mask_sub = None
            wf_single_subject = init_wf_single_subject(
                ID=ID[i], func_file=func_file, atlas_select=atlas_select,
                network=network, node_size=node_size, roi=roi, thr=thr, uatlas_select=uatlas_select,
                multi_nets=multi_nets, conn_model=conn_model, dens_thresh=dens_thresh, conf=conf_sub,
                adapt_thresh=adapt_thresh, plot_switch=plot_switch, dwi_file=dwi_file, multi_thr=multi_thr,
                multi_atlas=multi_atlas, min_thr=min_thr, max_thr=max_thr, step_thr=step_thr, anat_file=anat_file,
                parc=parc, ref_txt=ref_txt, procmem='auto', k=k, clust_mask=clust_mask, k_min=k_min, k_max=k_max,
                k_step=k_step, k_clustering=k_clustering, user_atlas_list=user_atlas_list,
                clust_mask_list=clust_mask_list, prune=prune, node_size_list=node_size_list,
                num_total_samples=num_total_samples, graph=graph, conn_model_list=conn_model_list,
                min_span_tree=min_span_tree, verbose=verbose, plugin_type=plugin_type, use_AAL_naming=use_AAL_naming,
                multi_graph=multi_graph, smooth=smooth, smooth_list=smooth_list, disp_filt=disp_filt,
                clust_type=clust_type, clust_type_list=clust_type_list, c_boot=c_boot, block_size=block_size,
                mask=mask_sub, norm=norm, binary=binary, fbval=fbval_sub, fbvec=fbvec_sub, target_samples=target_samples,
                curv_thr_list=curv_thr_list, step_list=step_list, overlap_thr=overlap_thr,
                overlap_thr_list=overlap_thr_list, track_type=track_type, max_length=max_length, maxcrossing=maxcrossing,
                life_run=life_run, min_length=min_length, directget=directget, tiss_class=tiss_class,
                runtime_dict=runtime_dict, embed=embed, multi_directget=multi_directget)
            wf_multi.add_nodes([wf_single_subject])
            # Restrict nested meta-meta wf resources at the level of the group wf
            if func_file:
                wf_selected = "%s%s" % ('functional_connectometry_', ID[i])
                meta_wf_name = "%s%s" % ('Meta_wf_', ID[i])
                for node_name in wf_multi.get_node(wf_single_subject.name).get_node(meta_wf_name).get_node(wf_selected).list_node_names():
                    if node_name in runtime_dict:
                        wf_multi.get_node(wf_single_subject.name).get_node(meta_wf_name).get_node(wf_selected).get_node(node_name)._n_procs = runtime_dict[node_name][0]
                        wf_multi.get_node(wf_single_subject.name).get_node(meta_wf_name).get_node(wf_selected).get_node(node_name)._mem_gb = runtime_dict[node_name][1]
                if k_clustering > 0:
                    wf_multi.get_node(wf_single_subject.name).get_node(meta_wf_name).get_node(wf_selected).get_node('clustering_node')._n_procs = 1
                    wf_multi.get_node(wf_single_subject.name).get_node(meta_wf_name).get_node(wf_selected).get_node('clustering_node')._mem_gb = 4

            if dwi_file:
                wf_selected = "%s%s" % ('structural_connectometry_', ID)
                meta_wf_name = "%s%s" % ('Meta_wf_', ID[i])
                for node_name in wf_multi.get_node(wf_single_subject.name).get_node(meta_wf_name).get_node(wf_selected).list_node_names():
                    if node_name in runtime_dict:
                        wf_multi.get_node(wf_single_subject.name).get_node(meta_wf_name).get_node(wf_selected).get_node(node_name)._n_procs = runtime_dict[node_name][0]
                        wf_multi.get_node(wf_single_subject.name).get_node(meta_wf_name).get_node(wf_selected).get_node(node_name)._mem_gb = runtime_dict[node_name][1]

            i = i + 1

        return wf_multi

    # Workflow generation
    # Multi-subject workflow generator
    if (func_subjects_list or struct_subjects_list) or (func_subjects_list and struct_subjects_list):
        wf_multi = wf_multi_subject(ID, func_subjects_list, struct_subjects_list, network, node_size, roi,
                                    thr, uatlas_select, multi_nets, conn_model, dens_thresh,
                                    conf, adapt_thresh, plot_switch, dwi_file, multi_thr,
                                    multi_atlas, min_thr, max_thr, step_thr, anat_file, parc,
                                    ref_txt, procmem, k, clust_mask, k_min, k_max, k_step,
                                    k_clustering, user_atlas_list, clust_mask_list, prune,
                                    node_size_list, num_total_samples, graph, conn_model_list,
                                    min_span_tree, verbose, plugin_type, use_AAL_naming, multi_graph,
                                    smooth, smooth_list, disp_filt, clust_type, clust_type_list, c_boot,
                                    block_size, mask, norm, binary, fbval, fbvec, target_samples, curv_thr_list,
                                    step_list, overlap_thr, overlap_thr_list, track_type, max_length, maxcrossing,
                                    life_run, min_length, directget, tiss_class, runtime_dict, embed, multi_directget)

        import shutil
        wf_multi.base_dir = '/tmp/Wf_multi_subject'
        if op.exists(wf_multi.base_dir):
            shutil.rmtree(wf_multi.base_dir)
        os.mkdir(wf_multi.base_dir)

        if verbose is True:
            from nipype import config, logging
            cfg_v = dict(logging={'workflow_level': 'DEBUG', 'utils_level': 'DEBUG', 'interface_level': 'DEBUG',
                                  'log_directory': str(wf_multi.base_dir), 'log_to_file': True},
                         monitoring={'enabled': True, 'sample_frequency': '0.1', 'summary_append': True,
                                     'summary_file': str(wf_multi.base_dir)})
            logging.update_logging(config)
            config.update_config(cfg_v)
            config.enable_debug_mode()
            config.enable_resource_monitor()

            import logging
            callback_log_path = "%s%s" % (wf_multi.base_dir, '/run_stats.log')
            logger = logging.getLogger('callback')
            logger.setLevel(logging.DEBUG)
            handler = logging.FileHandler(callback_log_path)
            logger.addHandler(handler)

        cfg = dict(execution={'stop_on_first_crash': False, 'crashdump_dir': str(wf_multi.base_dir),
                              'crashfile_format': 'txt', 'parameterize_dirs': True, 'display_variable': ':0',
                              'job_finished_timeout': 120, 'matplotlib_backend': 'Agg', 'plugin': str(plugin_type),
                              'use_relative_paths': True, 'keep_inputs': True, 'remove_unnecessary_outputs': False,
                              'remove_node_directories': False, 'raise_insufficient': True})
        for key in cfg.keys():
            for setting, value in cfg[key].items():
                wf_multi.config[key][setting] = value
        try:
            wf_multi.write_graph(graph2use="colored", format='png')
        except:
            pass
        if procmem != 'auto':
            if verbose is True:
                from nipype.utils.profiler import log_nodes_cb
                plugin_args = {'n_procs': int(procmem[0]), 'memory_gb': int(procmem[1]), 'status_callback': log_nodes_cb}
            else:
                plugin_args = {'n_procs': int(procmem[0]), 'memory_gb': int(procmem[1])}
            print("%s%s%s" % ('\nRunning with ', str(plugin_args), '\n'))
            wf_multi.run(plugin=plugin_type, plugin_args=plugin_args)
        else:
            wf_multi.run(plugin=plugin_type)
        if verbose is True:
            from nipype.utils.draw_gantt_chart import generate_gantt_chart
            print('Plotting resource profile from run...')
            generate_gantt_chart('/tmp/Wf_multi_subject/multi_sub_run_stats.log', cores=int(procmem[0]))

    # Single-subject workflow generator
    else:
        # Single-subject pipeline
        wf = init_wf_single_subject(ID, func_file, atlas_select, network, node_size, roi, thr, uatlas_select,
                                    multi_nets, conn_model, dens_thresh, conf, adapt_thresh, plot_switch, dwi_file,
                                    multi_thr, multi_atlas, min_thr, max_thr, step_thr, anat_file, parc, ref_txt,
                                    procmem, k, clust_mask, k_min, k_max, k_step, k_clustering, user_atlas_list,
                                    clust_mask_list, prune, node_size_list, num_total_samples, graph, conn_model_list,
                                    min_span_tree, verbose, plugin_type, use_AAL_naming, multi_graph, smooth,
                                    smooth_list, disp_filt, clust_type, clust_type_list, c_boot, block_size, mask,
                                    norm, binary, fbval, fbvec, target_samples, curv_thr_list, step_list, overlap_thr,
                                    overlap_thr_list, track_type, max_length, maxcrossing, life_run, min_length,
                                    directget, tiss_class, runtime_dict, embed, multi_directget)

        import shutil
        import os
        if (func_file is not None) and (dwi_file is None):
            base_dirname = "%s%s" % ('Wf_single_subject_fmri_', str(ID))
        elif (dwi_file is not None) and (func_file is None):
            base_dirname = "%s%s" % ('Wf_single_subject_dmri_', str(ID))
        else:
            base_dirname = "%s%s" % ('Wf_single_subject', str(ID))

        if func_file:
            func_dir = os.path.dirname(func_file)
            if os.path.exists("%s%s%s" % (func_dir, '/', base_dirname)):
                shutil.rmtree("%s%s%s" % (func_dir, '/', base_dirname))
            os.mkdir("%s%s%s" % (func_dir, '/', base_dirname))
            wf.base_dir = "%s%s%s" % (func_dir, '/', base_dirname)
        elif dwi_file:
            dwi_dir = os.path.dirname(dwi_file)
            if os.path.exists("%s%s%s" % (dwi_dir, '/', base_dirname)):
                shutil.rmtree("%s%s%s" % (dwi_dir, '/', base_dirname))
            os.mkdir("%s%s%s" % (dwi_dir, '/', base_dirname))
            wf.base_dir = "%s%s%s" % (dwi_dir, '/', base_dirname)

        if verbose is True:
            from nipype import config, logging
            cfg_v = dict(logging={'workflow_level': 'DEBUG', 'utils_level': 'DEBUG', 'interface_level': 'DEBUG',
                                  'log_directory': str(wf.base_dir), 'log_to_file': True},
                         monitoring={'enabled': True, 'sample_frequency': '0.1', 'summary_append': True,
                                     'summary_file': str(wf.base_dir)})
            logging.update_logging(config)
            config.update_config(cfg_v)
            config.enable_debug_mode()
            config.enable_resource_monitor()

            import logging
            callback_log_path = "%s%s" % (wf.base_dir, '/run_stats.log')
            logger = logging.getLogger('callback')
            logger.setLevel(logging.DEBUG)
            handler = logging.FileHandler(callback_log_path)
            logger.addHandler(handler)

        cfg = dict(execution={'stop_on_first_crash': False, 'crashdump_dir': str(wf.base_dir),
                              'parameterize_dirs': True, 'crashfile_format': 'txt', 'display_variable': ':0',
                              'job_finished_timeout': 120, 'matplotlib_backend': 'Agg', 'plugin': str(plugin_type),
                              'use_relative_paths': True, 'keep_inputs': True, 'remove_unnecessary_outputs': False,
                              'remove_node_directories': False, 'raise_insufficient': True})
        for key in cfg.keys():
            for setting, value in cfg[key].items():
                wf.config[key][setting] = value
        try:
            wf.write_graph(graph2use="colored", format='png')
        except:
            pass
        if procmem != 'auto':
            if verbose is True:
                from nipype.utils.profiler import log_nodes_cb
                plugin_args = {'n_procs': int(procmem[0]), 'memory_gb': int(procmem[1]), 'status_callback': log_nodes_cb}
            else:
                plugin_args = {'n_procs': int(procmem[0]), 'memory_gb': int(procmem[1])}
            print("%s%s%s" % ('\nRunning with ', str(plugin_args), '\n'))
            wf.run(plugin=plugin_type, plugin_args=plugin_args)
        else:
            wf.run(plugin=plugin_type)
        if verbose is True:
            from nipype.utils.draw_gantt_chart import generate_gantt_chart
            print('Plotting resource profile from run...')
            generate_gantt_chart("%s%s" % (wf.base_dir, '/run_stats.log'), cores=int(procmem[0]))

    if verbose is True:
        handler.close()
        logger.removeHandler(handler)

    print('\n\n------------NETWORK COMPLETE-----------')
    print('Execution Time: ', timeit.default_timer() - start_time)
    print('---------------------------------------')

    return


def main():
    import sys
    import warnings
    warnings.filterwarnings("ignore")
    try:
        from pynets.utils import do_dir_path
    except ImportError:
        print('PyNets not installed! Ensure that you are using the correct python version.')

    if len(sys.argv) < 1:
        print("\nMissing command-line inputs! See help options with the -h flag.\n")
        sys.exit()

    args = get_parser().parse_args()

    try:
        from multiprocessing import set_start_method, Process, Manager
        set_start_method('forkserver')
        with Manager() as mgr:
            retval = mgr.dict()
            p = Process(target=build_workflow, args=(args, retval))
            p.start()
            p.join()

            if p.exitcode != 0:
                sys.exit(p.exitcode)
    except:
        print('\nWARNING: Upgrade to python3 for forkserver functionality...')
        retval = dict()
        build_workflow(args, retval)


if __name__ == '__main__':
    import warnings
    warnings.filterwarnings("ignore")
    __spec__ = "ModuleSpec(name='builtins', loader=<class '_frozen_importlib.BuiltinImporter'>)"
    main()
