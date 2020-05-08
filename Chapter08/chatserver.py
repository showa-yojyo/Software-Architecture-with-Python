#!/usr/bin/env python
# Code Listing #2
"""

Chat server using select based I/O multiplexing

"""

# I/O multiplexing というのは単一のチャンネルによる複数送受信のことか？

# chatserver.py

import socket
import select
import signal
import sys
from communication import send, receive # ユーザーモジュール


class ChatServer:
    """ Simple chat server using select """

    def __init__(self, port=3490, backlog=5):
        self.clients = 0
        # Client map
        self.clientmap = {}
        # Output socket list
        self.potential_writers = []
        # サーバーソケットを作成する。だいたいこのコードになるようだ。
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # ここはわからないので後回し。
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # bind() を呼び出すのはサーバーソケット。
        self.server.bind(('', port))
        print('Listening to port', port, '...')
        # このサーバーソケットは backlog 個までの接続を許す。
        self.server.listen(backlog)
        # Trap keyboard interrupts
        signal.signal(signal.SIGINT, self.sighandler)

    def sighandler(self, signum, frame):
        # Close the server
        print('Shutting down server...')
        # Close existing client sockets
        for o in self.potential_writers:
            o.close()

        # ソケットプログラミングでは close() は特に重要
        self.server.close()

    def get_name(self, client):

        # Return the printable name of the
        # client, given its socket...
        info = self.clientmap[client]
        host, name = info[0][0], info[1]
        return '@'.join((name, host))

    def serve(self):
        # Windows では sys.stdin をソケットとして扱えないことに注意
        # (WinError 10038)
        potential_readers = [self.server, sys.stdin]
        self.potential_writers = []

        running = 1
        # サーバーソケットなので無限ループの形を取る。
        while running:

            try:
                # select は blocking 呼び出し
                ready_to_read, ready_to_write, in_error = select.select(
                    potential_readers,
                    self.potential_writers,
                    []) # potential_errors だが通常は空リストを渡す
            except select.error:
                break
            except socket.error:
                break

            # 実際に読めるソケットをループで回していく
            for s in ready_to_read:
                # サーバーソケットが読める場合
                if s == self.server:
                    # handle the server socket
                    # 外部からの接続を受け付ける。
                    client, address = self.server.accept()
                    print('chatserver: got connection %d from %s' %
                          (client.fileno(), address))
                    # Read the login name
                    # この receive() は信頼できる。
                    cname = receive(client).split('NAME: ')[1]

                    # Compute client name and send back
                    self.clients += 1
                    send(client, 'CLIENT: ' + str(address[0]))
                    # client を potential_readers に入れておくのか？
                    potential_readers.append(client)

                    self.clientmap[client] = (address, cname)
                    # Send joining information to other clients
                    msg = '\n(Connected: New client (%d) from %s)' % (
                        self.clients, self.get_name(client))

                    # 書き込みたいソケットに送信する。
                    for o in self.potential_writers:
                        # o.send(msg)
                        send(o, msg)

                    # 接続するためのクライアントソケットを
                    # porential_writers に入れておく
                    self.potential_writers.append(client)
                # 標準入力が読み込める場合
                elif s == sys.stdin:
                    # 一行読み込んでループフラグをリセットする
                    # handle standard input
                    sys.stdin.readline()
                    running = 0
                # 一般の読み込み可能なソケット s に対して
                else:
                    # handle all other sockets
                    try:
                        # この receive() は信頼できる。
                        if data := receive(s):
                            # Send as new client's message...
                            msg = '\n#[' + self.get_name(s) + ']>> ' + data
                            # Send data to all except ourselves
                            for o in self.potential_writers:
                                if o != s:
                                    send(o, msg)
                        else:
                            # 受信なしは接続終了を意味する。
                            print('chatserver: %d hung up' % s.fileno())
                            self.clients -= 1
                            # ソケットプログラミングでは close() は特に重要
                            s.close()
                            potential_readers.remove(s)
                            self.potential_writers.remove(s)

                            # Send client leaving information to others
                            msg = '\n(Hung up: Client from %s)' % self.get_name(
                                s)
                            for o in self.potential_writers:
                                # o.send(msg)
                                send(o, msg)

                    except socket.error:
                        # Remove
                        potential_readers.remove(s)
                        self.potential_writers.remove(s)
        # data = receive(s)
        # ソケットプログラミングでは close() は特に重要
        self.server.close()


if __name__ == "__main__":
    ChatServer().serve()
