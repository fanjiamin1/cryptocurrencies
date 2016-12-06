from chat import Peer
from chat.crypto import RSA


message = "The default message"
message_1 = "Another message that can be useful"
message_2 = "A more contrived 2016 @ RU message"


def test_send_receive():
    public, private = RSA.generate_key_pair()

    receiver_port = 8000
    receiver_address = ("127.0.0.1", receiver_port)

    receiver = Peer(port=receiver_port)
    receiver.set_private_key(private)

    sender = Peer()
    sender.set_public_key(public)

    sender.send(receiver_address, message)

    assert receiver.receive() == message

def test_send_receive_2():
    public, private = RSA.generate_key_pair()

    receiver_port = 8000
    receiver_address = ("127.0.0.1", receiver_port)

    receiver = Peer(port=receiver_port)
    receiver.set_private_key(private)

    sender_1 = Peer()
    sender_1.set_public_key(public)
    sender_2 = Peer()
    sender_2.set_public_key(public)

    sender_1.send(receiver_address, message_1)
    sender_2.send(receiver_address, message_2)

    assert receiver.receive() == message_1
    assert receiver.receive() == message_2
