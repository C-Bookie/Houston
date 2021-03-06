import pygame

from caduceussocket import connection


class Screen:
    def __init__(self, client):
        self.client = client
        self.height = 300
        self.width = 400

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))  # , pygame.FULLSCREEN)
        pygame.display.set_caption('jazZy')

        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()

    def run(self):
        try:
            while True:
                self.loop()
        finally:
            self.client.close()

    def loop(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.client.send_state(True)
            if event.type == pygame.KEYUP:
                self.client.send_state(False)
            if event.type == pygame.QUIT:
                return

        if self.client.state:
            self.background.fill((0, 0, 0))
        else:
            self.background.fill((250, 250, 250))

        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()


class Prop(connection.Client):
    def __init__(self):
        super().__init__()
        self.state = False

        data = connection.encode({
            "type": "move_session",
            "args": [
                2077
            ]
        })
        self.send_msg(data)

    def callback(self, data):
        response = connection.decode(data)
        if response["type"] == "state_change":
            self.state = response["content"]["state"]

    def send_state(self, state):
        data = connection.encode({
            "type": "broadcast",
            "args": [{
                "type": "state_change",
                "content": {
                    "state": state
                }
            }]
        })
        self.send_msg(data)


if __name__ == "__main__":
    prop = Prop()
    screen = Screen(prop)
    prop.start()
    screen.run()

