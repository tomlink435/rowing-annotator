# Copyright (c) OpenMMLab. All rights reserved.
import logging
import mimetypes
import os
import time
from argparse import ArgumentParser

import cv2
import json_tricks as json
import mmcv
import mmengine
import numpy as np
from mmengine.logging import print_log

from mmpose.apis import inference_topdown
from mmpose.apis import init_model as init_pose_estimator
from mmpose.evaluation.functional import nms
from mmpose.registry import VISUALIZERS
from mmpose.structures import merge_data_samples, split_instances
from mmpose.utils import adapt_mmdet_pipeline

try:
    from mmdet.apis import inference_detector, init_detector
    has_mmdet = True
except (ImportError, ModuleNotFoundError):
    has_mmdet = False


def process_one_image(img,
                      detector,
                      pose_estimator,
                      visualizer=None,
                      show_interval=0):
    """Visualize predicted keypoints (and heatmaps) of one image."""

    # predict bbox
    det_result = inference_detector(detector, img)
    pred_instance = det_result.pred_instances.cpu().numpy()
    bboxes = np.concatenate(
        (pred_instance.bboxes, pred_instance.scores[:, None]), axis=1)
    bboxes = bboxes[np.logical_and(pred_instance.labels == 0,
                                   pred_instance.scores > 0.3)]
    bboxes = bboxes[nms(bboxes, 0.3), :4]

    # predict keypoints
    pose_results = inference_topdown(pose_estimator, img, bboxes)
    data_samples = merge_data_samples(pose_results)

    # show the results
    if isinstance(img, str):
        img = mmcv.imread(img, channel_order='rgb')
    elif isinstance(img, np.ndarray):
        img = mmcv.bgr2rgb(img)

    if visualizer is not None:
        visualizer.add_datasample(
            'result',
            img,
            data_sample=data_samples,
            draw_gt=False,
            draw_heatmap=False,
            draw_bbox=False,
            show_kpt_idx=False,
            skeleton_style='mmpose',
            show=False,
            wait_time=show_interval,
            kpt_thr=0.3)

    # if there is no instance detected, return None
    return data_samples.get('pred_instances', None)


def main():
    
    #输出路径
    output_root = ''
    #输入路径
    input = 'E://20221207single-1.mp4'
    
    if output_root:
        mmengine.mkdir_or_exist(output_root)
        output_file = os.path.join(output_root,
                                   os.path.basename(input))
        if input == 'webcam':
            output_file += '.mp4'
        
    # build detector
    detector = init_detector(
        'demo/mmdetection_cfg/rtmdet_m_640-8xb32_coco-person.py', 
        'https://download.openmmlab.com/mmpose/v1/projects/rtmpose/rtmdet_m_8xb32-100e_coco-obj365-person-235e8209.pth',
       device='cpu')
    detector.cfg = adapt_mmdet_pipeline(detector.cfg)

    # build pose estimator
    pose_estimator = init_pose_estimator(
        'demo/mmdetection_cfg/rtmdet_m_640-8xb32_coco-person.py',
        'https://download.openmmlab.com/mmpose/v1/projects/rtmpose/rtmdet_m_8xb32-100e_coco-obj365-person-235e8209.pth',
      device='cpu',
        cfg_options=dict(
            model=dict(test_cfg=dict(output_heatmaps=False))))

    # build visualizer
    pose_estimator.cfg.visualizer.radius = 3
    pose_estimator.cfg.visualizer.alpha = 0.8
    pose_estimator.cfg.visualizer.line_width = 1
    visualizer = VISUALIZERS.build(pose_estimator.cfg.visualizer)
    # the dataset_meta is loaded from the checkpoint and
    # then pass to the model in init_pose_estimator
    visualizer.set_dataset_meta(
        pose_estimator.dataset_meta, skeleton_style='mmpose')

    if input == 'webcam':
        input_type = 'webcam'
    else:
        input_type = mimetypes.guess_type(input)[0].split('/')[0]

    if input_type == 'image':

        # inference
        pred_instances = process_one_image(input, detector,
                                           pose_estimator, visualizer)

        if output_file:
            img_vis = visualizer.get_image()
            mmcv.imwrite(mmcv.rgb2bgr(img_vis), output_file)

    elif input_type in ['webcam', 'video']:
        if input == 'webcam':
            cap = cv2.VideoCapture(0)
        else:
            cap = cv2.VideoCapture(input)
        video_writer = None
        pred_instances_list = []
        frame_idx = 0
        while cap.isOpened():
            success, frame = cap.read()
            frame_idx += 1

            if not success:
                break

            # topdown pose estimation
            pred_instances = process_one_image(frame, detector,
                                               pose_estimator, visualizer,
                                               0.001)
            pred_instances_list.append(pred_instances.keypoints)
         
        if video_writer:
            video_writer.release()

        cap.release()

    else:
        raise ValueError(
            f'file {os.path.basename(input)} has invalid format.')
    
    print(pred_instances_list)

if __name__ == '__main__':
    main()
