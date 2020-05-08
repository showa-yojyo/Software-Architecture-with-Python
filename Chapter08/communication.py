# Code Listing #4

"""

Communication module for serializing and de-serializing messages from
chat client <-> server

"""

# communication.py
import pickle
import socket
import struct


def send(channel, *args):
    """ Send a message to a channel """

    # ある意味急所。ソケットプログラミングに独特のコード。
    buf = pickle.dumps(args)
    # send なのでホスト形式からネットワーク形式にコンバートする
    value = socket.htonl(len(buf)) # 整数の変換 h: host n: network l: long
    size = struct.pack("L", value)
    channel.send(size)
    channel.send(buf)


def receive(channel):
    """ Receive a message from a channel """

    size = struct.calcsize("L")
    size = channel.recv(size)
    try:
        # receive はその逆にコンバートする
        size = socket.ntohl(struct.unpack("L", size)[0])
    except struct.error:
        return ''

    buf = ""
    while (lenbuf := len(buf)) < size:
        buf += channel.recv(size - lenbuf)

    return pickle.loads(buf)[0]
