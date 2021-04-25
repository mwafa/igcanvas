from http.server import BaseHTTPRequestHandler


class handler(BaseHTTPRequestHandler):

  def do_GET(self):
    self.send_response(200, "it's work")
    return