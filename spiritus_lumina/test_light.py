import phue
import time
import random

from caduceussocket import connection


class LightPainter(connection.Client):
    def __init__(self):
        super().__init__()
        self.bridge = phue.Bridge('192.168.1.211')
        self.bridge.connect()

        self.white_list_functions += [
            "draw"
        ]

        state = False
        for i in range(100):
            state = not state
            command = {
                'transitiontime': 1,
    #            'on': state,
    #            'bri': 255,
                'hue':random.randint(0, 255)
            }
            self.bridge.set_light('cal', command)
            time.sleep(0.1)


    def connect(self):
        super().connect()
        self.send_data({
            "type": "register",
            "args": [
                "graph",
                2077
            ]
        })

    def draw(self, frame_rate, graph, graph1, sample, hsv, peaks, troughs):
        command = {
            'transitiontime': 1,
            'on': True,
            'hue': int(hsv[0] * 65535),
            'sat': int(hsv[1] * 254),
            'bri': int(hsv[2] * 254)
        }
        self.bridge.set_light('cal', command)



if __name__ == "__main__":
    lp = LightPainter()
    lp.run()


