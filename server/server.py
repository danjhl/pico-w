import network
import socket
import machine
from time import sleep

ssid = 'WIFI_ID_HERE'
password = 'WIFI_PW_HERE'

pin = machine.Pin('LED', machine.Pin.OUT)

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    # Disable power saving mode for better connection
    wlan.config(pm = 0xa11140)
    wlan.connect(ssid, password)

    while wlan.isconnected() == False:
        print('Waiting for connection... status', wlan.status())
        sleep(1)

    ip = wlan.ifconfig()[0]
    print(wlan.ifconfig())
    print(f'Connected on {ip}')
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
        <input type="submit" value="Light on" />
        </form>
        <form action="./lightoff">
        <input type="submit" value="Light off" />
        </form>
        <p>LED is {state}</p>
        </body>
        </html>
    """
    return str(html)


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
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()