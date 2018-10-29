from Server import app
import webbrowser
from gevent.pywsgi import WSGIServer

PORT = 5000

def main(): 
    http_server = WSGIServer(('', PORT), app) #create wsgi server 
    
    url = "http://localhost:"+str(PORT)+"/"
    webbrowser.open(url, new=2) #Opens in new tab if possible
    http_server.serve_forever()

if __name__ == "__main__":
    main()