import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(("0.0.0.0", 80))
s.listen(3)

while True:

    client, addr = s.accept()
    print("Connected by {}".format(addr))

    while True:
        content = client.recv(32)

        if len(content) == 0:
            break

        else:
            print(content)

    print("Closing connection")
    client.close()
