
import connection

class Prop():
    def __init__(self):
        pass
    client = connection.Client()
    client.start()

    while True:
        msg = input(">")
        if client.closed.is_set():
            break
        client.send_msg(msg)


