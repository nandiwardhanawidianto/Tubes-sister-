import os
import socket
import pickle

if (not os.path.isfile('./client_log.pkl')):
    client_ver = dict()
else:
    client_log = open("client_log.pkl", "rb")
    client_ver = pickle.load(client_log)

print("Enter hostname:")
host = input("> ")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect((host, 22222))
    print("Connected Successfully")
except:
    print("Unable to connect")
    exit(0)

def check_ver(app_ver):
    count = 0
    if (not os.path.isfile('./client_log.pkl')):
        return 4

    for key in client_ver:
        if (app_ver[key] > client_ver[key]):
            count+= 1

    return count

app_count = 0
app_ver = dict()
while True:
    command = input("> ")
    if (command.casefold() == "update"):
        sock.send(command.casefold().encode())

        data = sock.recv(1024)
        app_ver = pickle.loads(data)

        app_count = check_ver(app_ver)
        if (app_count > 0):
            print("Ada", app_count,"aplikasi yang bisa di-upgrade")
        else:
            print("Tidak ada aplikasi yang perlu di-update")
    elif (command.casefold() == "list"):
        if (not os.path.isfile('./client_log.pkl')):
            print("Tidak ada aplikasi yang terinstall")
        else:
            for key in client_ver:
                print(key, client_ver[key])
    elif (command.casefold() == "upgrade"):
        if (app_count == 0): #belum update
            print("Tidak ada yang perlu di-upgrade")
        else:
            if (not os.path.isfile('./client_log.pkl')):
                client_log = open("client_log.pkl", "wb")
                pickle.dump(app_ver, client_log)
                client_log.close()
                print("4 aplikasi berhasil di-upgrade")
            else:
                for key in client_ver:
                    if (app_ver[key] > client_ver[key]):
                        client_ver[key] = app_ver[key]
                client_log = open("client_log.pkl", "wb")
                pickle.dump(client_ver, client_log)
                client_log.close()
                print(app_count, "aplikasi berhasil di-upgrade")

sock.close()
