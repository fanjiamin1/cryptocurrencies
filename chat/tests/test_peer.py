from chat import Peer
from chat.crypto import RSA


message = "The default message"


def test_send_receive():
    public, private = RSA.generate_key_pair()

    receiver_port = 8000
    receiver_address = ("127.0.0.1", receiver_port)

    # Set up receiving end
    receiver = Peer(port=receiver_port)
    receiver.set_private_key(private)

    # Set up sending end
    sender = Peer()
    sender.set_public_key(public)

    sender.send(receiver_address, message)

    assert receiver.receive() == message
