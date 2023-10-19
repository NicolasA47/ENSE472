from twisted.internet import reactor, protocol, endpoints, ssl

class Client(protocol.Protocol):
    def __init__(self):
       reactor.callInThread(self.send_data)

    def dataReceived(self, data):
        data = data.decode("utf-8")
        print (data)
        
    def send_data(self):
        while True:
            message = input()
            self.transport.write(message.encode("utf-8"))
            if message == "!Q":
                reactor.stop()
                break
            
class ClientFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return Client()

if __name__ == "__main__":
    factory = ClientFactory()
    reactor.connectSSL("localhost", 1234, factory, ssl.ClientContextFactory())
    reactor.run()


