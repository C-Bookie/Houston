import connection

if __name__ == '__main__':
    client = connection.Client()
    client.start()

    while True:
        msg = input(">")
        print("Sending: ", msg)
        client.send_msg(bytearray(msg, 'utf-8'))
