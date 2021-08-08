from http.server import HTTPServer
from api import process

if __name__ == "__main__":
    port = 3000
    hostname = 'localhost'
    webServer = HTTPServer((hostname, port), process.handler)
    print("Server started http://%s:%s" % (hostname, port))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")