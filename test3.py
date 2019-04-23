import connection

if __name__ == '__main__':
    client = connection.Client('192.168.1.233', 8089)
    client.start()

    while True:
        msg = input(">")
        client.send_msg(bytearray(msg, 'utf-8'))
