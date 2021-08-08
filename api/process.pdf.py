from http.server import BaseHTTPRequestHandler
import cgi, igcanvas, time
import os
from PyPDF2 import PdfFileReader, PdfFileWriter
from pdf2image import convert_from_path
from PIL import ImageFilter, Image


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open('pdf.html', 'r') as index:
            self.wfile.write(index.read().encode())
        return

    def wm(self, img):
        wm = Image.open("wmk.png")
        x1, y1 = wm.size
        x2, y2 = img.size
        offset = ((x2 - x1) // 2, (y2 - y1) // 2)
        img.paste(wm, offset)
        return img

    def blur(self, src, out, start=8):
        if (os.path.exists('/tmp')):
            tmp = '/tmp/__tmp__.pdf'
        pdf_reader = PdfFileReader(src)
        pdf_writer = PdfFileWriter()
        imgs = convert_from_path(src, size=610)

        for i in range(pdf_reader.getNumPages()):
            if (i >= start - 1):
                img = imgs[i].copy()
                img = img.filter(ImageFilter.GaussianBlur(4))
                img = self.wm(img)
                img.save(tmp)
                p = PdfFileReader(tmp)
                page = p.getPage(0)
                pdf_writer.addPage(page)
            else:
                page = pdf_reader.getPage(i)
                pdf_writer.addPage(page)
        with open(out, "wb") as output:
            pdf_writer.write(output)

    def do_POST(self):
        form = cgi.FieldStorage(fp=self.rfile,
                                headers=self.headers,
                                environ={
                                    'REQUEST_METHOD': 'POST',
                                    'CONTENT_TYPE':
                                    self.headers['Content-Type'],
                                })
        filename = form['file'].filename
        data = form['file'].file.read()
        filepath = "%s-%s" % (time.time(), filename)
        if (os.path.exists('/tmp')):
            filepath = '/tmp/' + filepath
        with open(filepath, 'wb') as f:
            f.write(data)

        self.blur(
            filepath,
            filepath,
        )

        self.send_response(200)
        self.send_header('Content-type', 'application/pdf')
        self.end_headers()
        with open(filepath, 'rb') as content:
            self.wfile.write(content.read())
        os.remove(filepath)
        return

    def respond(self, s: str):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(str(s).encode())
