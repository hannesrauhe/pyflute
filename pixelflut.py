import socket,os,time
from PIL import Image

HOST = os.environ['HOST'] if 'HOST' in os.environ else 'pixelflut'
PORT = 1234
IMAGE = os.environ['IMAGE'] if 'IMAGE' in os.environ else 'wtf.png'
STARTX= int(os.environ['STARTX']) if 'STARTX' in os.environ else 0
STARTY= int(os.environ['STARTY']) if 'STARTY' in os.environ else 0
SIZEX= int(os.environ['SIZEX']) if 'SIZEX' in os.environ else 200
SIZEY= int(os.environ['SIZEY']) if 'SIZEY' in os.environ else 200
TRANSPARENT= 'TRANSPARENT' in os.environ
SLEEP = int(os.environ['SLEEP']) if 'SLEEP' in os.environ else 0

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
linecache=""
size_of_cache=0
flushed=0
cache_capacity=1000

def flush():
  global linecache
  global size_of_cache
  global flushed
  sock.send(bytes(linecache,"utf-8"))
  linecache=""
  size_of_cache=0
  flushed=flushed+1
  print("{0}".format(flushed),end="\r")


def send(strtosend):
  global linecache
  global size_of_cache
  linecache = linecache+strtosend
  size_of_cache=size_of_cache+1
  if size_of_cache>=cache_capacity:
    flush()

def pixel(x,y,r,g,b,a=255):
  x = STARTX+x
  y = STARTY+y
  if TRANSPARENT and r+g+b==0:
    return

  strtosend=''
  if a == 255:
    send('PX %d %d %02x%02x%02x\n' % (x,y,r,g,b))
  else:
    send('PX %d %d %02x%02x%02x%02x\n' % (x,y,r,g,b,a))


im = Image.open(IMAGE).convert('RGB')
im.thumbnail((SIZEX,SIZEY), Image.ANTIALIAS)
_,_,w,h = im.getbbox()

while True:
  for x in range(w):
    for y in range(h):
      r,g,b = im.getpixel((x,y))
      pixel(x,y,r,g,b)
  flush()
  time.sleep(SLEEP)
