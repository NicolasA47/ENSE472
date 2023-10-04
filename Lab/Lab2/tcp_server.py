from twisted.internet import reactor, protocol, endpoints

class Server(protocol.Protocol):
    def __init__ (self, users):
        self.users = users
        self.name = None
    
    def connectionMade(self):
        print ("New Connection")
        self.users.append(self)
        print ("A new connection has been made. Geting name...")
        self.transport.write("Welcome to the Server, what is your name?".encode("utf-8"))

    def dataReceived (self, data):
        message = data.decode("utf-8") 
        if self.name:
            if message == "!Q":
                print (f"<{self.name}> left the chat.")
                for user in self.users:
                    if user != self:
                        user.transport.write(f"<{self.name}> has left the chat!".encode("utf-8"))
                self.users.remove(self)
            else:
                print (f"<{self.name}>: " + message)
                for user in self.users:
                    if user != self:
                        user.transport.write(f"<{self.name}>: ".encode("utf-8") + data)
        else:
            if message == "!Q":
                print ("Unnamed user left")
            else:
                self.name = data.decode()
                print (f"A new connection is now known as <{self.name}>")
                for user in self.users:
                    if user != self:
                        user.transport.write(f"<{self.name}> has entered the chat".encode("utf-8"))
                    else:
                        user.transport.write(f"Welcome to the chat <{self.name}>. Please type !Q to quit.".encode("utf-8"))

class ServerFactory (protocol.ServerFactory):
    def __init__(self):
        self.users = []

    def buildProtocol(self, addr):
        return Server(self.users)

if __name__ == "__main__":
    reactor.listenTCP(1234, ServerFactory())
    reactor.run()
