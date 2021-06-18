#import library yang diperlukan
import os
import socket
import pickle

#cek apakah client sudah memiliki aplikasi  yang terinstall
if (not os.path.isfile('./client_log.pkl')): #jika tidak, buat dictionary kosong
    client_ver = dict()
else: #jika iya, ambil data aplikasi dari log dan simpan di dictionary
    client_log = open("client_log.pkl", "rb")
    client_ver = pickle.load(client_log)

# untuk koneksi ke server, client masukkan alamat ip server
print("Enter hostname:")
host = input("> ")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# cek apakah alamat yang dimasukan benar atau tidak
try:
    sock.connect((host, 22222))
    print("Connected Successfully")
except:
    print("Unable to connect")
    exit(0)

# untuk mengecek perbedaan versi aplikasi di server dan client
def check_ver(app_ver):
    count = 0
    if (not os.path.isfile('./client_log.pkl')): #jika tidak ada aplikasi yang terinstall, anggap seluruh aplikasi perlu di download / upgrade
        return 4

    for key in client_ver:
        if (app_ver[key] > client_ver[key]): # untuk setiap aplikasi yang ada, cek perbedaan versi
            count+= 1

    return count

# persiapan untuk membandingkan jumlah aplikasi yang ada
app_count = 0
app_ver = dict()
while True:
    command = input("> ")
    if (command.casefold() == "update"): #jika client memasukan perintah update, client mengirim pesan ke server untuk meminta data aplikasi
        sock.send(command.casefold().encode())

        data = sock.recv(1024) #client menerima data aplikasi dan melakukan de-serialisasi menjadi dictionary
        app_ver = pickle.loads(data)

        app_count = check_ver(app_ver)
        if (app_count > 0): #jika ada aplikasi yang perlu diupdate
            print("Ada", app_count,"aplikasi yang bisa di-upgrade")
        else: #jika tidak ada aplikasi yang perlu di-update
            print("Tidak ada aplikasi yang perlu di-update")
    elif (command.casefold() == "list"): #untuk mengecek aplikasi yang terinstall di client
        if (not os.path.isfile('./client_log.pkl')):
            print("Tidak ada aplikasi yang terinstall")
        else:
            for key in client_ver:
                print(key, client_ver[key])
    elif (command.casefold() == "upgrade"):
        if (app_count == 0): #client belum atau tidak ada aplikasi yang diupdate
            print("Tidak ada yang perlu di-upgrade")
        else:
            if (not os.path.isfile('./client_log.pkl')): #jika client fresh install (belum ada aplikasi)
                client_log = open("client_log.pkl", "wb")
                pickle.dump(app_ver, client_log)
                client_log.close()
                print("4 aplikasi berhasil di-upgrade")
            else:
                for key in client_ver:
                    if (app_ver[key] > client_ver[key]): #cek aplikasi yang perlu diupgrade
                        client_ver[key] = app_ver[key]
                client_log = open("client_log.pkl", "wb")
                pickle.dump(client_ver, client_log)
                client_log.close()
                print(app_count, "aplikasi berhasil di-upgrade")

sock.close()
