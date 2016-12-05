from chat import Peer
from chat.crypto import RSA


message = "The default message"


def test_send_receive(self):
    private, public = RSA.generate_key_pair()

    sender_address = ("127.0.0.1", 9999)
    receiver_address = ("127.0.0.1", 8000)

    with Peer(sender_address) as sender:
        sender.set_public_key(public)
        sender.send_to(receiver_address, message)

    with Peer(receiver_address) as receiver:
        receiver.set_private_key(private)
        assert receiver.receive() == message
