import json
import logging
import socket
from threading import Thread, Lock
import numpy as np
import base64
import cv2


class TcpNetworkClient:
    def __init__(self, host, port, buffer_size):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.cache = []

        # create socket for connection
        self.request = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connect
        try:
            self.request.connect((self.host, self.port))
        except Exception:
            logging.error("Error: Failed to connect server at {}:{}!".format(self.host, self.port))

        # get a lock for data sending
        self.lock = Lock()

    # another constructor (implemented by classmethod)
    @classmethod
    def create_from_config(cls, config_filename="network_config.json"):
        # load config from file
        with open(config_filename, mode="r") as f:
            param = json.load(f)
            # print(param)
            return cls(param["host"], param["port"], param["buffer_size"])

    # send len(data) bytes data, returen number of bytes sent
    def send_data(self, data):
        data = base64.standard_b64encode(data)
        data += b'#'
        total_sent = 0
        if self.lock.acquire():
            try:
                while total_sent < len(data):
                    # print('in send_data while')
                    nsent = self.request.send(data[total_sent:])
                    # print('nsent={}'.format(nsent))
                    if nsent == 0:
                        raise RuntimeError("Send Error: tcp socket connection broken")
                    total_sent += nsent
            finally:
                self.lock.release()
        return total_sent

    def recv_data_real(self, chunks):
        while True:
            chunk = self.request.recv(self.buffer_size)
            # print(chunk)
            if chunk == b"":
                raise RuntimeError("Recv Error: tcp socket connection broken")
            pos = chunk.find(b'#')
            if pos == -1:
                chunks.append(chunk)
            else:
                chunks.append(chunk[:pos])
                self.cache = chunk[pos + 1:]
                break

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

        chunks = b''.join(chunks)
        chunks = base64.standard_b64decode(chunks)
        return chunks

    # receive count bytes data, return the data buffer
    def recv_data_stream(self, count):
        chunks = []
        total_recv = 0
        while total_recv < count:
            chunk = self.request.recv(min(self.buffer_size, count - total_recv))
            if chunk == b"":
                raise RuntimeError("Recv Error: tcp socket connection broken")
            chunks.append(chunk)
            total_recv += len(chunk)
        return b"".join(chunks)

    # send large block of data at once. (no deep copy)
    def send_data_large(self, data):
        data = base64.standard_b64encode(data)
        data += '#'
        view = memoryview(data).cast("B")
        while len(view):
            nsent = self.request.send(view)
            # print('nsent:', nsent)
            view = view[nsent:]

    # receive large block of data into a pre-allocated buffer.
    def recv_data_into_large(self, buffer):
        view = memoryview(buffer).cast("B")
        while len(view):
            nrecv = self.request.recv_into(view)
            view = view[nrecv:]


if __name__ == "__main__":
    client = TcpNetworkClient("localhost", 9999, 4096)
    image = cv2.imread('E:/SAM/segment-anything/notebooks/images/aaa.jpg')
    height, width, _ = image.shape
    client.send_data(image)

    height_str = str(height)  # 将整数转换为字符串
    encoded_height = height_str.encode('utf-8')  # 编码字符串为字节数据
    client.send_data(encoded_height)  # 发送字节数据给客户端

    width_str = str(width)  # 将整数转换为字符串
    encoded_width = width_str.encode('utf-8')  # 编码字符串为字节数据
    client.send_data(encoded_width)  # 发送字节数据给客户端

    point = np.array([[100, 175]])
    client.send_data(point)

    label = np.array([1])
    client.send_data(label)

    data = client.recv_data()
    mask = np.frombuffer(data, dtype=np.int32)

    print(mask)
