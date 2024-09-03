import base64
import json
import socket
from threading import Thread
import numpy as np
import cv2
import os
import pickle
import logging
from argparse import ArgumentParser
import mmengine
import numpy as np
from mmcv.image import imread
from mmengine.logging import print_log
import mimetypes
from mmpose.apis import inference_topdown, init_model
from mmpose.registry import VISUALIZERS
from mmpose.structures import merge_data_samples
from mmpose.apis import inference_topdown
from mmpose.apis import init_model as init_pose_estimator
from mmpose.evaluation.functional import nms
from mmpose.registry import VISUALIZERS
from mmpose.structures import merge_data_samples, split_instances
from mmpose.utils import adapt_mmdet_pipeline
from demo.video_mmpose import process_one_image

try:
    from mmdet.apis import inference_detector, init_detector

    has_mmdet = True
except (ImportError, ModuleNotFoundError):
    has_mmdet = False


# 服务器初始化和配置：通过TcpNetworkServer类创建一个TCP服务器，它监听指定的主机和端口，等待客户端连接并处理请求。
# 从配置文件创建服务器实例：使用create_from_config类方法，可以从JSON配置文件中读取服务器的配置参数（如主机地址、端口号和缓冲区大小），并创建服务器实例。
# 处理客户端请求：服务器在接收到客户端连接后，会启动一个新线程处理请求。处理函数process_request根据接收到的消息类型（视频或图像路径），选择合适的处理方式。
# 姿态估计：使用mmpose和mmdet进行姿态估计。首先，使用目标检测模型（如果提供了视频或图像路径）检测图像中的人物，然后对检测到的人物应用姿态估计模型。
# 数据接收和发送：服务器使用recv_data和send_data方法接收和发送数据。数据在发送前使用base64编码，接收后进行解码。
class TcpNetworkServer:
    def __init__(self, host, port, buffer_size):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.cache = []

        # create socket for listening
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # make sure the port is released in 1 second.(milli seconds in Windows)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen()
        print("Tcp server {}:{} started. Waiting for connection.".format(
            self.host, self.port))

        self.request = None
        self.client_address = None
        self.is_connected = False
        self.running = True

    @classmethod
    def create_from_config(cls, config_filename=r'config_network_config.json'):
        """
        another constructor (implemented by classmethod)
        """
        # load config from file
        with open(config_filename, mode="r") as f:
            param = json.load(f)
            return cls(param["tcp"]['host'], param['tcp']["port"], param['tcp']["buffer_size"])

    def wait_for_request(self):
        try:
            self.request, self.client_address = self.sock.accept()
        except OSError as err:
            print('socket closed.')
            self.is_connected = False
            return
        print("Client {} connected.".format(self.client_address))
        self.is_connected = True

    def serve_forever(self, process_request):
        while self.running:
            # wait for client request
            request, client_address = self.sock.accept()
            print("Client {} connected.".format(client_address))
            self.is_connected = True

            # start a thread to process this request
            t = Thread(target=process_request, args=(request, client_address))
            t.start()

    def decompose_sensor_message(self, msg):
        pos = msg.find('}{')
        return msg[:pos + 1], msg[pos + 1:]

    # recv msg is Json format, return is dict (header, body)
    def recv_sensor_message(self):
        # receive header
        msg = self.recv_data()
        if msg is None:
            return None, None
        msg = msg.decode()
        # print('******debug******:recv_sensor_message={}'.format(msg))
        msg_header, msg_body = self.decompose_sensor_message(msg)
        msg_header = json.loads(msg_header)
        # print(msg_header)
        msg_body = json.loads(msg_body)
        # print(msg_body)
        return msg_header, msg_body

    # send len(data) bytes data, return number of bytes sent
    def send_data(self, data):
        data = base64.standard_b64encode(data)
        data += b'#'
        total_sent = 0
        while total_sent < len(data):
            print('in send_data while')
            nsent = self.request.send(data[total_sent:])
            print('nsent={}'.format(nsent))
            if nsent == 0:
                # raise RuntimeError("tcp socket connection broken")
                self.is_connected = False
                break
            total_sent += nsent
        return total_sent

    # receive count bytes data, return the data buffer
    def recv_data_stream(self, count):
        chunks = []
        total_recv = 0
        while total_recv < count:
            chunk = self.request.recv(
                min(self.buffer_size, count - total_recv))
            if chunk == b"":
                raise RuntimeError("tcp socket connection broken")
            chunks.append(chunk)
            total_recv += len(chunk)
        return b"".join(chunks)

    # receive a single data
    # receive count bytes data, return the data buffer
    def recv_data(self):
        # previous left data are in cache
        chunks = []
        if len(self.cache) > 0:
            pos = self.cache.find(b'#')
            if pos == -1:  # cache doesn't contain a complete message
                chunks.append(self.cache)
                self.recv_data_real(chunks)
            else:  # the message is short, just use cache data
                chunks.append(self.cache[:pos])
                self.cache = self.cache[pos + 1:]
        else:
            self.recv_data_real(chunks)
        # when disconnected, drop current chunks.
        if not self.is_connected:
            return None

        chunks = b''.join(chunks)
        chunks = base64.standard_b64decode(chunks)
        return chunks

    def recv_data_real(self, chunks):
        while self.is_connected:
            chunk = self.request.recv(self.buffer_size)
            # print(chunk)
            if chunk == b"":
                # The tcp socket connection is broken
                self.is_connected = False
                break
                # raise RuntimeError("tcp socket connection broken")
            pos = chunk.find(b'#')
            if pos == -1:
                chunks.append(chunk)
            else:
                chunks.append(chunk[:pos])
                self.cache = chunk[pos + 1:]
                break

    # send large block of data at once. (no deep copy)
    def send_data_large(self, data):
        view = memoryview(data).cast("B")
        while len(view):
            nsent = self.request.send(view)
            view = view[nsent:]

    # receive large block of data into a pre-allocated buffer.
    def recv_data_into_large(self, buffer):
        view = memoryview(buffer).cast("B")
        while len(view):
            nrecv = self.request.recv_into(view)
            view = view[nrecv:]

    # self.RequestHandlerClass(request, client_address, self)
    def process_request(self, request, client_address):
        print(request, client_address)
        self.request = request

        data1 = self.recv_data()
        data1 = data1.decode('utf-8')

        print(data1)
        if (data1.endswith("mp4")):
            # 输入路径
            input = data1
            # build detector
            detector = init_detector('demo/mmdetection_cfg/rtmdet_m_640-8xb32_coco-person.py',
                                     'https://download.openmmlab.com/mmpose/v1/projects/rtmpose/rtmdet_m_8xb32-100e_coco-obj365-person-235e8209.pth',
                                     'mps')
            detector.cfg = adapt_mmdet_pipeline(detector.cfg)
            # build pose estimator
            pose_estimator = init_pose_estimator(
                r"/Users/teresa/Program/gaoshunxiang/rowing-annotator/mmpose/td-hm_hrnet-w48_8xb32-210e_coco-256x192.py",
                r"/Users/teresa/Program/gaoshunxiang/rowing-annotator/mmpose/td-hm_hrnet-w48_8xb32-210e_coco-256x192-0e67c616_20220913.pth",
                device='cpu',
                cfg_options=dict(model=dict(test_cfg=dict(output_heatmaps=False))))
            # build visualizer
            pose_estimator.cfg.visualizer.radius = 3
            pose_estimator.cfg.visualizer.alpha = 0.8
            pose_estimator.cfg.visualizer.line_width = 1
            visualizer = VISUALIZERS.build(pose_estimator.cfg.visualizer)
            # the dataset_meta is loaded from the checkpoint and
            # then pass to the model in init_pose_estimator
            visualizer.set_dataset_meta(pose_estimator.dataset_meta, skeleton_style='mmpose')
            if input == 'webcam':
                input_type = 'webcam'
            else:
                input_type = mimetypes.guess_type(input)[0].split('/')[0]
            if input_type == 'image':
                # inference
                pred_instances = process_one_image(input, detector,
                                                   pose_estimator, visualizer)
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
                    pred_instances_list.append(pred_instances.keypoints.tolist())
                if video_writer:
                    video_writer.release()
                cap.release()
            else:
                raise ValueError(
                    f'file {os.path.basename(input)} has invalid format.')
            print(pred_instances_list)
            serialized_data = pickle.dumps(pred_instances_list)
            server.send_data(serialized_data)
            print('send data ok. over.')
        else:
            model = init_model(
                r"/Users/teresa/Program/gaoshunxiang/rowing-annotator/mmpose/td-hm_hrnet-w48_8xb32-210e_coco-256x192.py",
                r"/Users/teresa/Program/gaoshunxiang/rowing-annotator/mmpose/td-hm_hrnet-w48_8xb32-210e_coco-256x192-0e67c616_20220913.pth",
                device='cpu',
                cfg_options=None)
            model.cfg.visualizer.radius = 3
            model.cfg.visualizer.alpha = 0.8
            model.cfg.visualizer.line_width = 1
            visualizer = VISUALIZERS.build(model.cfg.visualizer)
            visualizer.set_dataset_meta(model.dataset_meta, skeleton_style='mmpose')
            # boxes
            data = self.recv_data()
            data_received = pickle.loads(data)
            data_received = np.array([data_received])
            print(data_received)

            batch_results = inference_topdown(model, data1, bboxes=data_received, bbox_format='xyxy')
            results = merge_data_samples(batch_results)
            indices = results.pred_instances.keypoints
            print(indices)
            serialized_data = pickle.dumps(indices[0])
            server.send_data(serialized_data)
            print('send data ok. over.')


if __name__ == '__main__':
    server = TcpNetworkServer('localhost', 9999, 8192)
    t = server.serve_forever(server.process_request)
