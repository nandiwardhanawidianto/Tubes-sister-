import os
import socket
import pickle

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((socket.gethostname(), 22222))
sock.listen(5)
print("Host Name: ", sock.getsockname())

client, addr = sock.accept()

# server baca file isi versi aplikasi (aplikasi apa saja yang udah terinstall) (di server)
# simpan di variabel
server_log = open("server_log.pkl", "rb")
server_app = pickle.load(server_log)

while True:
    data = client.recv(1024)
    if (data.decode() == "update"):
        s_server_app = pickle.dumps(server_app)
        client.send(s_server_app)
        print("sent information requested by client")

# client cek apakah ada aplikasi yang harus diinstal / diupdate (di client)
# if yes->update (di client)

sock.close()
#case 1: client belum install apapun
#case 2: client sudah terinstall aplikasi, tapi ada yang belum update
#case 3: clinet sudah terinstall aplikasi, dan sudah terupdate
#case 4: versi di client >= versi di server
