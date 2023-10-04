from twisted.internet import protocol, reactor, endpoints

class Echo(protocol.Protocol): # The brackets means we are extending their class
    def dataReceived(self, data): # This callback will run when we recieve data
        print(f"received {data!r}") #print it out
        self.transport.write(data) # Write that data back to our transport

class EchoFactory(protocol.Factory): # Rather than use a constructor, we will use a Factory
    def buildProtocol(self, addr):
        return Echo()

# Creates a server endpoint. Starts the EchoFactory, listening to new tcp connections on port 1234
reactor.listenTCP(1234, EchoFactory())
reactor.run() 
