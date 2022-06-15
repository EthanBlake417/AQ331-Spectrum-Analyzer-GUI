from multiprocessing import Pool
import pyvisa
from pywatlow.watlow import Watlow


def check_connected_ports_pool():
    """ Uses a pool to check all the ports more quickly
    Edit this program to include more Devices
    """
    rm = pyvisa.ResourceManager()
    items = rm.list_resources()
    with Pool(len(items)) as p:
        results = p.map(pool_helper, [item for item in items])
    return results


def pool_helper(port):
    """ checks the connected ports and displays them in a copyable Text box """
    message2 = None
    rm = pyvisa.ResourceManager()
    # try Easy Connection
    try:
        resource = rm.open_resource(port)
        try:
            IDN = resource.query("*IDN?")  # .split(',')[0]
        # for Multimeters
        except Exception:
            resource.read_termination = '\n'
            resource.write_termination = '\n'
            IDN = resource.query("ID?")
        message = f"{port} {IDN}"
        resource.close()
    # If not Easy Connection, try Oven
    except Exception:
        try:
            message2 = f"{port} Not Recognized"
            resource.close()
            resource = [char for char in str(port) if 48 <= ord(char) <= 57]
            com = "COM"
            for num in resource:
                com += num
            resource = Watlow(port=com, address=1)
            if resource.read()['error'] is None:
                message = f"{com} EzZoneOven"
            else:
                message = f"{com} Not Recognized"
            resource.close()
        # If neither of those connections, print not recognized
        except Exception:
            message = "Not Recognized"
    if message2:
        message = [message, message2]
    return message


if __name__ == '__main__':
    check_connected_ports_pool()
