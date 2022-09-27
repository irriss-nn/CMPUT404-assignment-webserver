#  coding: utf-8 
import socketserver



# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

######## check security

class MyWebServer(socketserver.BaseRequestHandler):
 
    def handle(self):
        ### self.request is the TCP socket connected to the client which is the method + URL
        #### what is request method  file url
        self.data = self.request.recv(1024).decode("utf-8").strip()
        print ("Got a request of: %s\n" % self.data)
        ### sendall --- either all data has been sent or an error occured 
        
        ########## 
        firstline= self.data.split('\n')[0]#
        print('firstline '+firstline)
        method = firstline.split(' ')[0]
        fileUrl = firstline.split(' ')[1]
        print('fileUrl '+fileUrl)
        
        #no css, html or '/', ------> redirect

        if method != "GET":
            self.request.sendall(bytearray("HTTP/1.0 405 Method Not Allowed\n\n405 Method Not Allowed",'utf-8'))
            return 
        else:
           
            if fileUrl[-1] == '/': #test if end with '/'
                try: 
                    file = open("www/" + fileUrl + "index.html")
                    self.request.sendall(bytearray("HTTP/1.1 200 OK\nContent-Type: text/html\n\n" + file.read(),'utf-8'))
                except:
                     self.request.sendall(bytearray("HTTP/1.1 404 Not Found\n\n404 Not Found",'utf-8'))
                return
            
            if '../' in fileUrl:
                self.request.sendall(bytearray("HTTP/1.1 404 Not Found\n\n404 Not Found",'utf-8'))
            
            urlSplit = fileUrl.split('.')

            if len(urlSplit) ==2:
                print("urlsplit") 
                print(urlSplit)
                if urlSplit[-1] not in ["css","html"]:
                    self.request.sendall(bytearray("HTTP/1.1 404 Not Found\n\n404 Not Found",'utf-8'))
                    return 
                elif urlSplit[-1]  == "css":
                    try:
                        file = open("www" + fileUrl)#ope
                        self.request.sendall(bytearray("HTTP/1.1 200 OK\nContent-Type: text/css\n\n" + file.read(),'utf-8'))
                    except:
                        self.request.sendall(bytearray("HTTP/1.1 404 Not Found\n\n404 Not Found",'utf-8'))
                        return
                else:
                    try:
                        file = open("www" + fileUrl)#ope
                        self.request.sendall(bytearray("HTTP/1.1 200 OK\nContent-Type: text/html\n\n" + file.read(),'utf-8'))
                    except:
                        self.request.sendall(bytearray("HTTP/1.1 404 Not Found\n\n404 Not Found",'utf-8'))
                        return

            #redirect
            else:
                if len(urlSplit) == 1:
                    print("urlSplitttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt")
                    print(urlSplit[-1])
                    ###check whether in the www directory
                    if "deep" in urlSplit[-1]:
                        new = "www/" + fileUrl + "/index.html"
                        self.request.sendall(bytearray(f"HTTP/1.1 301 Moved Permanently\r\nLocation: {fileUrl}/\r\n", 'utf-8'))
                        #try:
                        #    file = open(new)#ope
                        #    self.request.sendall(bytearray("HTTP/1.1 301 Moved Permanently\nContent-Type: text/html\n\n" + file.read(),'utf-8'))
                        #except:
                        #    self.request.sendall(bytearray("HTTP/1.1 404 Not Found\n\n404 Not Found",'utf-8'))
                        #    return
                        self.request.sendall(bytearray("HTTP/1.1 301 Moved Permanently\n\n",'utf-8'))#fix content
                        self.request.sendall(bytearray("Location: " + new + "\r\n",'utf-8'))
                    else:
                        self.request.sendall(bytearray("HTTP/1.1 404 Not Found\n\n404 Not Found",'utf-8'))
                       


                


            
            
        #try:
            #fileURL = self.data.split('\n')[0] 

            #file = open("www" + fileUrl)#ope
            #self.request.sendall(bytearray("HTTP/1.1 200 OK\nContent-Type: text/html\n\n" + file.read(),'utf-8'))
        #except:
            #self.request.sendall(bytearray("HTTP/1.1 404 Not Found\n\n",'utf-8'))
            #return


        

       
        ##########  is it necessary to add "/www"
        #absPath = os.path.abspath(fileURL) + "/www" 
        #dirName = os.path.dirname(absPath)
        #### check get necessary????
        ####send sth
        #self.request.sendall(bytearray("HTTP/1.1 200 OK\nContent-Type: text/html\n\n" + file.read(),'utf-8'))
        file.close()
        ### what does the formal filepath look like
    





















        #self.request,sendall(status)

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080

    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
