import os
import signal
from multiprocessing import Process, Queue
from queue import Empty
from time import time
from typing import cast
from waitress import serve

from flask import Flask, request

class Server:
    def __init__(self) -> None:
        self.message: Queue[str] = Queue()
        self.webserver_host = "127.0.0.1"
        self.webserver_port = 8080

    def _run_server(self):
        app = Flask(__name__)
        app.route("/", methods=["PUT"]) (
            self._message_endpoint
        )
        serve(app, host=self.webserver_host, port=self.webserver_port)


    def _message_endpoint(self) -> str:
        received = request.json
        if not received.get("message", ""):
            raise ValueError("No message received")

        self.message.put(received.get("message"))
        return "Thanks for your message!"


    def get_message(self, timeout: int = 60) -> str:
        server_process = Process(target=self._run_server)
        server_process.start()
        print("Server started, waiting for message")

        end_time = time() + timeout
        message = None
        while time() < end_time:
            try:
                message = self.message.get(timeout=1)
                if message:
                    break
            except Empty:
                print("...waiting for message")
                continue

        if message is None:
            raise ValueError("No message received")

        print("\nMessage received!")
        os.kill(cast(int, server_process.pid), signal.SIGINT)
        return message

def main():
    server = Server()
    message = server.get_message()
    print(f"Received {message=}")


if __name__ == '__main__':
    main()