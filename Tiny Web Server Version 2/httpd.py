'''
    Disclaimer
    tiny httpd is a web server program for instructional purposes only
    It is not intended to be used as a production quality web server
    as it does not fully in compliance with the 
    HTTP RFC https://tools.ietf.org/html/rfc2616

    This task is designed by Praveen Garimella and is to be used
    as part of the Learning by Doing, Project Based Course on Operating Systems
    Write to pg@fju.us for any questions or comments
'''

'''
    == Task 2 ==
    This file has the solution for M1 and the description for M2.
    Review this solution before you start implementing the M2.
    If you don't like our solution for M1 then
    tell us why so that we can improve it.

    In the M2 you have to write code to handle http requests for static content.
    Web servers maintain static content in a directory called document root.
    We have provided you with a directory with the name www.
    This directory has some html files and images.
    A web server may receive a request to access one of these files.

    When such a request is received you have to parse the HTTP request
    and extract the name of the file in the request aka Uniform Resourse Indicator    
    Learn the format of the http requests from the tutorial given below.
    https://www.tutorialspoint.com/http/http_requests.htm

    After extracting the URI,
    check if the file exists in the document root directory i.e., www

    If it exists, you have to read the file contents as the response data.
    If not you have to send a 404 file not found response.

    Construct the http response by invoking response_headers method
    This method is provided in the HTTPServer class
    Passing the appropriate response code, content type and length to the method
    
    A tricky part to the response construction is to identify the content type.
    Set the content type text/html for files that end with the extension .html
    
    What would be the content type for images? Review the link below.
    https://www.iana.org/assignments/media-types/media-types.xhtml#image

    How do we figure out the content subtype of an image?
    Explore the use of the library mimetype in python.
    https://www.tutorialspoint.com/How-to-find-the-mime-type-of-a-file-in-Python
'''

import socket
import mimetypes
import os
import sys

class HTTPServer:
    def __init__(self, IP, port):
        super().__init__()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP) as self.s:
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.bind((IP, port))
            self.s.listen()
            while True:
                conn, addr = self.s.accept()
                with conn:
                    print('Connected by', addr)
                    # TODO read the request and extract the URI
                    text = conn.recv(1024).decode('utf-8')
                    requrl = text.split(" ")
                    # TODO update the parameter with the request URI
                    uri = ""
                    if len(requrl) > 1 :
                        uri = requrl[1]
                    else :
                        uri = "/"
                    result2 = self.get_data(uri)
                    if result2 is None :
                        continue
                    else :
                        code, c_type, c_length, data = result2
                    response = self.response_headers(code, c_type, c_length).encode() + data
                    conn.sendall(response)
                    conn.close()

    
    def get_data(self, uri):
        '''
            TODO: This function has to be updated for M2
        '''
        docroot = "/home/prem/Documents/IOS/M4/"
        if uri == "/bin/":
            data = "Can not access bin directory"
            return 404, "text/plain", len(data), data.encode()
        elif uri.startswith("/bin") :
            stdin  = sys.stdin.fileno() # usually 0
            stdout = sys.stdout.fileno() # usually 1
            pr, cw  = os.pipe()
            pid = os.fork()
            if pid > 0:
              os.close(cw)
              os.dup2(pr,  stdin)
              res = ""
              for line in sys.stdin:
                res = res + line + "<br>"
              return 200, "text/html", len(res), res.encode()
            else:
              os.close(pr)
              os.dup2(cw, stdout)
              args = [docroot[:-1] + uri]        
              if uri.find(".py") != -1 :
                    cmd = "python3"
                    args = [cmd, docroot[:-1] + uri]
                    os.execvp(args[0], args)
              else :
                os.execvp(args[0], args)
        else :

            if uri == "/" :
                text = os.listdir("./www/")
                data = ""
                for i in text :
                    if not i.startswith(".") :
                        data = data + '''<a href = '''+"/"+i+'''>'''+i+'''</a><br>'''
                return 200,"text/html", len(data), data.encode()
            elif os.path.isfile("./www"+uri) :
                mime = mimetypes.MimeTypes().guess_type("./www"+uri)[0]
                file_pointer = open("./www"+uri, 'rb')
                data = file_pointer.read()
                return 200,mime,len(data),data
            elif os.path.isdir("./www"+uri):
                text = os.listdir("./www"+uri)
                data = ""
                for i in text :
                    if not i.startswith(".") :
                        data = data + '''<a href = '''+uri+"/"+i+'''>'''+i+'''</a><br>'''
                return 200,"text/html", len(data), data.encode()
            else :
                data = "<h1>File Not Found</h1>"
                return 404, "text/html", len(data), data.encode()
    
    def response_headers(self, status_code, content_type, length):
        line = "\n"
        # TODO update this dictionary for 404 status codes
        response_code = {200: "200 OK", 404: "404 File not found!"}
        headers = ""
        headers += "HTTP/1.1 " + response_code[status_code] + line
        headers += "Content-Type: " + content_type + line
        headers += "Content-Length: " + str(length) + line
        headers += "Connection: close" + line
        headers += line
        return headers

def main():
    # test harness checks for your web server on the localhost and on port 8888
    # do not change the host and port
    # you can change  the HTTPServer object if you are not following OOP
    HTTPServer('127.0.0.1', 8888)

if __name__ == "__main__":
    main()                   
