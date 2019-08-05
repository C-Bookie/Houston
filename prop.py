import threading

import pygame
import connection
import session

class Screen():
    def __init__(s, client):
        s.client = client
        s.height = 300
        s.width = 400

        pygame.init()
        s.screen = pygame.display.set_mode((s.width, s.height))  # , pygame.FULLSCREEN)
        pygame.display.set_caption('jazZy')

        s.background = pygame.Surface(s.screen.get_size())
        s.background = s.background.convert()


    def run(s):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    s.client.send_state(True)
                if event.type == pygame.KEYUP:
                    s.client.send_state(False)
                if event.type == pygame.QUIT:
                    return

            if s.client.state:
                s.background.fill((0, 0, 0))
            else:
                s.background.fill((250, 250, 250))

            s.screen.blit(s.background, (0, 0))
            pygame.display.flip()


class Prop(connection.Client):
    def __init__(s):
        super().__init__()
        s.state = False

        data = connection.encode({
            "type": "move_session",
            "args": [
                2077
            ]
        })
        s.send_msg(data)

    def callback(s, data):
        response = connection.decode(data)
        if response["type"] == "state_change":
            s.state = response["content"]["state"]

    def send_state(s, state):
        data = connection.encode({
            "type": "broadcast",
            "args": [{
                "type": "state_change",
                "content": {
                    "state": state
                }
            }]
        })
        s.send_msg(data)


if __name__ == "__main__":
    prop1 = Prop()
    screen = Screen(prop1)
    prop1.start()
    screen.run()

