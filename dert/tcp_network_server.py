import base64
import json
import socket
from threading import Thread
from segment_anything import build_sam_vit_h,SamPredictor
import numpy as np
from tcp_network_client import TcpNetworkClient
from PIL import Image
import requests
import matplotlib.pyplot as plt
import pickle
#import ipywidgets as widgets
#from IPython.display import display, clear_output

import torch
from torch import nn
from torchvision.models import resnet50
import torchvision.transforms as T
from hubconf import*
from util.misc import nested_tensor_from_tensor_list
torch.set_grad_enabled(False)

# COCO classes
CLASSES = [
    'background','person'
]

# colors for visualization
COLORS = [[0.000, 0.447, 0.741], [0.850, 0.325, 0.098]]

# standard PyTorch mean-std input image normalization
transform = T.Compose([
    T.Resize(800),
    T.ToTensor(),
    T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# for output bounding box post-processing
def box_cxcywh_to_xyxy(x):
    x_c, y_c, w, h = x.unbind(1)
    b = [(x_c - 0.5 * w), (y_c - 0.5 * h),
         (x_c + 0.5 * w), (y_c + 0.5 * h)]
    return torch.stack(b, dim=1)

def rescale_bboxes(out_bbox, size):
    img_w, img_h = size
    b = box_cxcywh_to_xyxy(out_bbox)
    b = b * torch.tensor([img_w, img_h, img_w, img_h], dtype=torch.float32)
    return b

def plot_results(pil_img, prob, boxes):
    plt.figure(figsize=(16,10))
    plt.imshow(pil_img)
    ax = plt.gca()
    colors = COLORS * 100
    print(boxes.tolist())
    for p, (xmin, ymin, xmax, ymax), c in zip(prob, boxes.tolist(), colors):
        ax.add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                                   fill=False, color=c, linewidth=3))
        cl = p.argmax()
        text = f'{CLASSES[cl]}: {p[cl]:0.2f}'
        ax.text(xmin, ymin, text, fontsize=15,
                bbox=dict(facecolor='yellow', alpha=0.5))
    plt.axis('off')
    plt.show()


def detect(im, model, transform):
    # mean-std normalize the input image (batch-size: 1)
    img = transform(im).unsqueeze(0)

    # propagate through the model
    outputs = model(img)

    # keep only predictions with 0.7+ confidence
    probas = outputs['pred_logits'].softmax(-1)[0, :, :-1]
    keep = probas.max(-1).values > 0.00001

    # convert boxes from [0; 1] to image scales
    bboxes_scaled = rescale_bboxes(outputs['pred_boxes'][0, keep], im.size)
    return probas[keep], bboxes_scaled

def predict(im, model, transform):
    # mean-std normalize the input image (batch-size: 1)
    anImg = transform(im)
    data = nested_tensor_from_tensor_list([anImg])

    # propagate through the model
    outputs = model(data)

    # keep only predictions with 0.7+ confidence
    probas = outputs['pred_logits'].softmax(-1)[0, :, :-1]
    
    keep = probas.max(-1).values > 0.7
    #print(probas[keep])

    # convert boxes from [0; 1] to image scales
    bboxes_scaled = rescale_bboxes(outputs['pred_boxes'][0, keep], im.size)
    return probas[keep], bboxes_scaled

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

        model=detr_resnet50(False,2)
        state_dict = torch.load("outputs/checkpoint.pth",map_location='cpu')
        model.load_state_dict(state_dict["model"])
        model.eval()

        data = self.recv_data()

        im = Image.open(data.decode())
        im = im.convert("RGB")
        scores, boxes = predict(im, model, transform)
        
        # plot_results(im, scores, boxes)
        

        list_data = boxes.tolist()
        new_array = []
        for listimage in list_data:
            print(listimage)
            client = TcpNetworkClient("localhost", 9999, 4096)
            client.send_data(data)

            serialized_data = pickle.dumps(listimage)  
            client.send_data(serialized_data)

            imagedata = client.recv_data()
            data_received = pickle.loads(imagedata)

            new_array.append(data_received)
            
        new_array = np.array(new_array)
        # new_array = new_array.reshape(1,17,2)
        print(new_array)
        serialized_data = pickle.dumps(new_array)  
        server.send_data(serialized_data)
        print('dert send data ok. over.')


if __name__ == '__main__':
    server = TcpNetworkServer('localhost', 9998, 8191)
    t = server.serve_forever(server.process_request)
   # data = server.recv_data()
