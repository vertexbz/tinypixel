from __future__ import annotations
from server import Server
from logger import logger
from command import from_line as command_from_line, UnknownCommandError, Controller

logger = logger.getChild('controller-server')


class ControllerAwareServer(Server):
    def __init__(self, socket_file: str, controller: Controller):
        super().__init__(socket_file)
        self.controller = controller

    def handle_data(self, connection, data: str, client_id: int):
        try:
            result = self.controller.handle(command_from_line(data))
            if isinstance(result, bool):
                return result
            if isinstance(result, str):
                connection.sendall(f'{result}\n'.encode(self.encoding))
                return True
            if isinstance(result, tuple) and len(result) == 2 and isinstance(result[0], str) and isinstance(result[1], bool):
                connection.sendall(f'{result[0]}\n'.encode(self.encoding))
                return result[1]
            raise ValueError('Invalid response from controller')
        except UnknownCommandError:
            connection.sendall(f'INVALID COMMAND: {data.strip()}\n'.encode(self.encoding))
            logger.warning(f'Client {client_id}: invalid command: {data.strip()}')

        return True
