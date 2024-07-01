# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl
from io import BytesIO


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        body = self.rfile.read(content_length)
        print("\n\n")
        print(f"body: {body}")
        print("\n\n")
        self.send_response(200)
        self.end_headers()


def main():
    context = ssl.SSLContext()
    context.load_cert_chain("localhost.crt", "localhost.key")

    httpd = HTTPServer(("localhost", 8000), SimpleHTTPRequestHandler)
    httpd.socket = context.wrap_socket(
        httpd.socket,
        server_side=True,
    )
    httpd.serve_forever()


if __name__ == "__main__":
    main()
