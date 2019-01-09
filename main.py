
#title: Show Host
#aurthor: Callum B-C

import yaml

def run():
    shows = []

    #adding a show
    with yaml.load(open("shows.yaml", 'r')) as showList :
        shows.append(Show(showList["room1"]))

class Show():
    def __init__(self, showScript):
        self.script = showScript

        self.reset()

    # reset all IOs and states
    def reset(self):
        for node in self.script["panels"]:
            for finger in self.script["panels"][node]["out"]:
                if "default" in self.script["panels"]:
                    pass # todo send MQTT command, topic: "show/node", finger, self.script["panels"][node][finger]["default"]

    # reload a shows state from an SQL database that the show host will auto save to periodically
    def reload(self):
        pass

    # begin timer
    def start(self):
        pass



if __name__ == "__main__":
    run()