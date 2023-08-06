from __future__ import annotations

import grp
import os
import socket
import traceback
from logger import logger
from typing import Optional
from _thread import *

logger = logger.getChild('server')

class Server:
    def __init__(self, socket_file: str, buffer_size: int = 128, encoding: Optional[str] = 'utf-8'):
        self._last_client_id = 0
        self.buffer_size = buffer_size
        self.socket_file = socket_file
        self.encoding = encoding

    def start(self):
        # Create a Unix socket
        if os.path.exists(self.socket_file):
            os.unlink(self.socket_file)
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

        # Bind the socket to socket_file
        sock.bind(self.socket_file)
        os.chown(self.socket_file, os.getuid(), grp.getgrnam('gpio').gr_gid)
        os.chmod(self.socket_file, 0o770)

        # Listen for incoming connections
        sock.listen()

        logger.info(f'Listening at: {self.socket_file}')

        while True:
            if not self.accept_connection(sock):
                break

        sock.close()
        logger.info(f'Server shutdown')

    def accept_connection(self, sock: socket) -> bool:
        try:
            client, address = sock.accept()
            self._last_client_id = self._last_client_id + 1
            client_id = self._last_client_id
            start_new_thread(self.handle_connection, (client, client_id))
        except KeyboardInterrupt:
            print('\r', end='')
            return False

        return True

    def handle_connection(self, connection: socket, client_id):
        logger.info(f'Connected {client_id}')
        connection.send('HELLO\n'.encode(self.encoding))
        try:
            while True:
                data: str = connection.recv(self.buffer_size).decode(self.encoding)
                try:
                    if not self.handle_data(connection, data, client_id=client_id):
                        break
                except BrokenPipeError:
                    break
                except Exception as err:
                    connection.sendall('ERROR!\n'.encode(self.encoding))
                    logger.error("".join(traceback.format_exception(type(err), err, err.__traceback__)))
                    pass

            connection.close()
        except OSError as e:
            if e.errno != 9:
                raise e
        finally:
            logger.info(f'Disconnected {client_id}')

    def handle_data(self, connection, data: str, client_id: int) -> bool:
        pass
