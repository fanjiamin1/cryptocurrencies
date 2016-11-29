import netifaces


def get_local_ip():
    for interface_name in netifaces.interfaces():
        try:
            addresses = netifaces.ifaddresses(interface_name)[netifaces.AF_INET]
            for address in addresses:
                ip = address["addr"]
                if ip != "127.0.0.1":
                    return ip
        except:
            # TODO: Do something smart
            raise
    raise RuntimeError("Local IP not found")


def get_broadcast_ip():
    for interface_name in netifaces.interfaces():
        try:
            addresses = netifaces.ifaddresses(interface_name)[netifaces.AF_INET]
            for address in addresses:
                try:
                    return address["broadcast"]
                except KeyError:
                    pass  # ignore
        except:
            # TODO: Do something smart
            raise
    raise RuntimeError("Broadcast IP not found")
