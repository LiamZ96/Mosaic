from gevent import monkey
#monkey.patch_all() this breaks Multiprocessing.Queue. 
from Server import app
import webbrowser
from gevent.pywsgi import WSGIServer
from gevent.pool import Pool as gPool

PORT = 5000

def main(): 
    pool = gPool(1000) #create thread pool with a limit of 1000
    http_server = WSGIServer(('', PORT), app, spawn=pool) #create wsgi server 
    
    url = "http://localhost:"+str(PORT)+"/"
    webbrowser.open(url, new=2) #Opens in new tab if possible
    http_server.serve_forever()

if __name__ == "__main__":    
    main()