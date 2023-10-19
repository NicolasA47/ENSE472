from twisted.internet import reactor, protocol

class Client(protocol.DatagramProtocol):
    def startProtocol(self):
        self.transport.connect("127.0.0.1", 1234)
        self.sendName()

    def sendName(self):
        name = input("Enter your name: ")
        self.transport.write(name.encode("utf-8"))

    def datagramReceived(self, datagram, addr):
        print(datagram.decode("utf-8"))

    def startChat(self):
        reactor.callInThread(self.sendMessage)

    def sendMessage(self):
        while True:
            message = input()
            if message == "!Q":
                self.transport.write(message.encode("utf-8"))
                reactor.stop()
                break
            else:
                self.transport.write(message.encode("utf-8"))

if __name__ == "__main__":
    client = Client()
    reactor.listenUDP(0, client)  # Port 0 means to allocate any available port
    client.startChat()
    reactor.run()
