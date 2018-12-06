'''
MIT License

Copyright (c) 2018 LiamZ96

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
'''Authors: Jacob Wakefield'''

from gevent import monkey
from Server import app
import webbrowser
from gevent.pywsgi import WSGIServer
from gevent.pool import Pool as gPool

PORT = 5000

def main(): 
    pool = gPool(1000) #create thread pool with a limit of 1000
    http_server = WSGIServer(('0.0.0.0', PORT), app, spawn=pool) #create wsgi server 
    
    url = "http://localhost:"+str(PORT)+"/"
    webbrowser.open(url, new=2) #Opens in new tab if possible
    http_server.serve_forever()

if __name__ == "__main__":    
    main()
