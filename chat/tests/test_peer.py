from chat import Peer


message = "The default message"


def test_send_receive(self):
    sender_address = ("127.0.0.1", 9999)
    receiver_address = ("127.0.0.1", 8000)
    with Peer(sender_address) as client:
        client.send_to(receiver_address, message)
    with Peer(receiver_address) as client:
        assert client.receive() == message
