import network
import socket
import machine

# CHANGE TO SECURE PW!
essid='pico'
password='WAP_PW_HERE'

def create_wap():
    wap = network.WLAN(network.AP_IF)
    wap.config(essid=essid, password=password)
    wap.active(True)
    netConfig = wap.ifconfig()
    ip = netConfig[0]
    print('IPv4 adress:', ip, '/', netConfig[1])
    print('Standard-Gateway:', netConfig[2])
    print('DNS-Server:', netConfig[3])
    return ip

def open_socket(ip):
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection


def webpage(state):
    html = f"""
        <!DOCTYPE html>
        <html>
        <form action="./lighton">
        <input type="submit" value="Light on" style="height:50px; width:100px;"/>
        </form>
        <br>
        <form action="./lightoff">
        <input type="submit" value="Light off" style="height:50px; width:100px;"/>
        </form>
        <p>LED is {state}</p>
        </body>
        </html>
    """
    return str(html)


pin = machine.Pin('LED', machine.Pin.OUT)

def serve(connection):
    state = 'OFF'
    pin.off()
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == '/lighton?':
            pin.on()
            state = 'ON'
        elif request == '/lightoff?':
            pin.off()
            state = 'OFF'
        html = webpage(state)
        client.send(html)
        client.close()
        

try:
    ip = create_wap()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()
