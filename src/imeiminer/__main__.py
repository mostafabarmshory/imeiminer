from imeiminer.server import PythonServer
import logging
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

root = logging.getLogger()

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.WARN)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

HOST_NAME = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8080"))

def start_imeiminer():
    server = HTTPServer((HOST_NAME, PORT), PythonServer)
    logging.info(f"Server started http://{HOST_NAME}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        logging.info("Server stopped successfully")
        sys.exit(0)

if __name__ == "__main__":
    start_imeiminer()