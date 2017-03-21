import numpy as np
import cv2
import threading
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import StringIO
from time import sleep
import PIL as pillow
from PIL import Image

cap = None
class Cam(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith('.mjpg'):
            self.send_response(200)
            self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=--jpgboundary')
            self.end_headers()
            while(True):
                try:
                    rc, img = cap.read()
                    if not rc:
                        continue
                    InColour=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    jpg = Image.fromarray(InColour)
                    tmpStr = StringIO.StringIO()
                    jpg.save(tmpStr, 'JPEG')
                    self.wfile.write("--jpgboundary")
                    self.send_header('Content-type', 'image/jpeg')
                    self.send_header('Content-length',str(tmpStr.len))
                    self.end_headers()
                    jpg.save(self.wfile, 'JPEG')
                    sleep(0.05)
                except KeyboardInterrupt:
                    break

            return
        if self.path.endswith('.html'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write('<html><head></head><body>')
            self.wfile.write('<img src="http://127.0.0.1:8080/cam.mjpg"/>')
            self.wfile.write('</body></html>')
            return

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """.."""

def main():
    global cap
    cap = cv2.VideoCapture(0)
    global img
    try:
        server = ThreadedHTTPServer(('0.0.0.0', 8080), Cam)
        print "Server Started"
        server.serve_forever()
    except KeyboardInterrupt:
        cap.release()
        server.socket.close()
        
if __name__ == '__main__':
    main()
    
