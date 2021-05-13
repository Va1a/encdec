from cryptography.fernet import Fernet
import os

from halo import Halo
from colorama import Fore, init

spinner = Halo(text='Initializing...', spinner='dots')
init(autoreset=True)

print(Fore.BLUE+'encdec fernet symmetric encryption')

op = input('\nEncrypt or Decrypt? '+Fore.CYAN)
op = True if op.lower() == 'encrypt' else False

print(f'{Fore.MAGENTA}Mode: {"Encrypt" if op else "Decrypt"}...')
if op:
	key = Fernet.generate_key()
	print('\nUsing secret key (SAVE THIS KEY IN A SAFE PLACE): '+Fore.YELLOW+key.decode('utf-8'))
else:
	print(Fore.RED+'\n[!] Providing an invalid key may result in data corruption.')
	key = input('Secret Key: '+Fore.YELLOW).encode('utf-8')

try:
	f = Fernet(key)
except:
	print(Fore.RED+'Invalid key! Provide a valid Fernet 32 byte key.')
	exit()

if op: 
	print(Fore.RED+'\n[!] Once you encrypt this directory, all of its contents will be INACCESSIBLE UNLESS YOU HAVE THE KEY!')
else:
	print(Fore.RED+'\n[!] Decrypting an unencrypted directory will cause file corruption!')
folder = input(f'Directory to {"encrypt" if op else "decrypt"} (all files and subfolders in this directory will be {"encrypt" if op else "decrypt"}ed): {Fore.CYAN}')

if not os.path.exists(folder):
	print(Fore.RED+'Invalid path provided.')
	exit()

def encrypt(file):
	spinner.text = f'{Fore.MAGENTA}Encrypting {Fore.WHITE}{file} ...'
	with open(file, 'rb') as working_file:
		encrypted = f.encrypt(working_file.read())
	with open(file, 'wb') as working_file:
		working_file.write(encrypted)

def decrypt(file):
	spinner.text = f'{Fore.MAGENTA}Decrypting {Fore.WHITE}{file} ...'
	with open(file, 'rb') as working_file:
		try:
			decrypted = f.decrypt(working_file.read())
		except:
			spinner.fail(Fore.RED+'Invalid decryption key!')
			exit()
	with open(file, 'wb') as working_file:
		working_file.write(decrypted)

def traverse(folder: str, op: bool):
	for root, dirs, files in os.walk(folder):
		for file in files:
			if op:
				encrypt(f'{root}/'+file)
			else:
				decrypt(f'{root}/'+file)

	return [root+'/'+dir for dir in dirs]

dirqueue = [folder]

spinner.start()
while dirqueue:
	for folder in dirqueue:
		dirqueue.extend(traverse(folder, op))
		dirqueue.remove(folder)

spinner.succeed(f'{Fore.GREEN}Done! Fully {"encrypt" if op else "decrypt"}ed...')