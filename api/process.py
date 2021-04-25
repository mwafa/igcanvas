from http.server import BaseHTTPRequestHandler
import cgi, igcanvas, time
import os

class handler(BaseHTTPRequestHandler):

  def do_GET(self):
    self.send_response(200)
    self.send_header('Content-type','text/plain')
    self.end_headers()
    self.wfile.write(
      str("it's work!").encode()
    )
    return
  
  def do_POST(self):
    form = cgi.FieldStorage(
        fp=self.rfile,
        headers=self.headers,
        environ={'REQUEST_METHOD':'POST',
                  'CONTENT_TYPE':self.headers['Content-Type'],
                  })
    filename = form['file'].filename
    data = form['file'].file.read()
    filepath = "%s-%s" % (time.time(), filename)
    with open(filepath, 'wb') as f:
      f.write(data)
    igcanvas.genImage(filepath).save(filepath)
    self.send_response(200)
    self.send_header('Content-type', 'image/jpeg')
    self.end_headers()
    with open(filepath, 'rb') as content:
      self.wfile.write(content.read())
    os.remove(filepath)
    return
  
  def respond(self, s: str):
    self.send_response(200)
    self.send_header('Content-type','text/plain')
    self.end_headers()
    self.wfile.write(
      str(s).encode()
    )