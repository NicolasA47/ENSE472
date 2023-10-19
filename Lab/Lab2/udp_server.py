from twisted.internet import reactor, protocol

class Server(protocol.DatagramProtocol):
    def __init__(self):
        self.users = {}  # Now, we need to track users by their addresses

    def datagramReceived(self, datagram, addr):
        message = datagram.decode("utf-8")

        # If the address is known, it's either a chat message or a disconnect command
        if addr in self.users:
            if message == "!Q":
                print(f"<{self.users[addr]}> left the chat.")
                del self.users[addr]
            else:
                print(f"<{self.users[addr]}>: {message}")
                for user_addr, user_name in self.users.items():
                    if user_addr != addr:
                        self.transport.write(f"<{self.users[addr]}>: {message}".encode("utf-8"), user_addr)
        else:
            # If it's a new address, set the user's name
            self.users[addr] = message
            print(f"A new user <{message}> joined the chat from {addr}")

if __name__ == "__main__":
    reactor.listenUDP(1234, Server())
    reactor.run()
