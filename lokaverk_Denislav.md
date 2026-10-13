```python
from mfrc522 import MFRC522
from machine import Pin, SoftSPI
from servo import Servo
from time import sleep_ms
import network
import socket

SSID = "TskoliVESM"
PASSWORD = "Fallegurhestur"
KORT = [1044135024563]

motor = Servo(Pin(15))
opid = False
motor.write_angle(15)

spi = SoftSPI(baudrate=100000, polarity=0, phase=0, sck=Pin(3), mosi=Pin(7), miso=Pin(5))
lesari = MFRC522(spi=spi, gpioRst=4, gpioCs=9)

def opna():
    global opid
    if not opid:
        for i in range(15, 165):
            motor.write_angle(i)
            sleep_ms(10)
        opid = True

def loka():
    global opid
    if opid:
        for i in range(165, 15, -1):
            motor.write_angle(i)
            sleep_ms(10)
        opid = False

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)
while not wlan.isconnected():
    sleep_ms(200)
print("IP:", wlan.ifconfig()[0])

server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("0.0.0.0", 80))
server.listen(1)
server.setblocking(False)

def vefsida():
    if opid:
        stada = "OPID"
    else:
        stada = "LOKAD"
    return ("<html><head><meta http-equiv='refresh' content='2'>"
            "<meta name='viewport' content='width=device-width, initial-scale=1'></head>"
            "<body style='text-align:center;font-family:sans-serif'>"
            "<h1>Kassinn er: " + stada + "</h1>"
            "<a href='/opna'><button style='font-size:28px;padding:20px'>Opna</button></a> "
            "<a href='/loka'><button style='font-size:28px;padding:20px'>Loka</button></a>"
            "</body></html>")

def vefur():
    try:
        cl, addr = server.accept()
    except OSError:
        return
    try:
        cl.settimeout(1)
        beidni = cl.recv(1024).decode()
        if "GET /opna" in beidni:
            opna()
        elif "GET /loka" in beidni:
            loka()
        cl.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
        cl.send(vefsida())
    except OSError:
        pass
    cl.close()

print("Skannadu kort!")

while True:
    vefur()

    stada, tegund = lesari.request(lesari.REQIDL)
    if stada == lesari.OK:
        stada, uid = lesari.anticoll()
        if stada == lesari.OK:
            numer = int.from_bytes(uid, "big")
            print("Kort:", numer)
            if numer in KORT:
                print("Rett kort, opid =", opid)
                if opid:
                    print("Loka")
                    loka()
                else:
                    print("Opna")
                    opna()
            else:
                print("Rangt kort, a ad vera:", KORT)
```
            sleep_ms(3000)
    sleep_ms(50)
