from twisted.internet import reactor, protocol, endpoints

# We'll use the Datagram Protocol now
class Echo(protocol.DatagramProtocol):
    # datagram Protocols need to identify who we are!
    def datagramReceived(self, data, addr):
        print(f"received {data!r} from {addr}")
        self.transport.write(data, addr)

# UDP does not use streams, instead we register callbacks to handle as they come in
reactor.listenUDP(1234, Echo())
reactor.run()
