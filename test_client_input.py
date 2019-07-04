import connection

if __name__ == '__main__':
    client = connection.Client()
    client.start()

    while True:
        msg = input(">")
        if client.closed.is_set():
            break
        client.send_msg(msg)
