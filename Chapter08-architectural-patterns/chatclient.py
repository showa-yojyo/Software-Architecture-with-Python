#!/usr/bin/env python
# Code Listing #3
"""

Chat client using select based I/O multiplexing

"""

import socket
import select
import sys
from communication import send, receive


class ChatClient:
    """ A simple command line chat client using select """

    def __init__(self, name, host='127.0.0.1', port=3490):
        self.name = name
        # Quit flag
        self.flag = False
        self.port = int(port)
        self.host = host
        # Initial prompt
        self.prompt = '[' + \
            '@'.join((name, socket.gethostname().split('.')[0])) + ']> '
        # Connect to server at port
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # 即 connect() はクライアントソケット。
            self.sock.connect((host, self.port))
            print('Connected to chat server@%d' % self.port)
            # Send my name...
            send(self.sock, 'NAME: ' + self.name)
            data = receive(self.sock)
            # Contains client address, set it
            addr = data.split('CLIENT: ')[1]
            self.prompt = '[' + '@'.join((self.name, addr)) + ']> '
        except socket.error:
            print('Could not connect to chat server @%d' % self.port)
            sys.exit(1)

    def chat(self):
        """ Main chat method """

        while not self.flag:
            try:
                sys.stdout.write(self.prompt)
                sys.stdout.flush()

                # Wait for input from stdin & socket
                ready_to_read, ready_to_write, in_error = select.select(
                    [0, self.sock], # potential readers
                    [], # potential writers
                    []) # empty

                # 実際に読めるソケットをすべて処理する
                for i in ready_to_read:
                    if i == 0 and (data := sys.stdin.readline().strip()):
                        send(self.sock, data)
                    elif i == self.sock:
                        data = receive(self.sock)
                        # 0 バイト受信は接続終了を常に意味する。
                        if not data:
                            print('Shutting down.')
                            self.flag = True
                            break

                        sys.stdout.write(data + '\n')
                        sys.stdout.flush()

            except KeyboardInterrupt:
                print('Interrupted.')
                # ソケットプログラミングでは close() は特に重要
                self.sock.close()
                break


if __name__ == "__main__":

    if len(sys.argv) < 3:
        sys.exit('Usage: %s chatid host portno' % sys.argv[0])

    client = ChatClient(sys.argv[1], sys.argv[2], int(sys.argv[3]))
    client.chat()
