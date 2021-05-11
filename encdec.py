from cryptography.fernet import Fernet
import os

print('encdecpy easy directory encryption/decryption!')

op = input('\nEncrypt or Decrypt? ')
op = True if op.lower() == 'encrypt' else False

print(f'Mode: {"Encrypt" if op else "Decrypt"}...')
if op:
	key = Fernet.generate_key()
	print('\nUsing secret key (SAVE THIS KEY IN A SAFE PLACE): '+key.decode('utf-8'))
else:
	key = input('\nSecret Key: ').encode('utf-8')

try:
	f = Fernet(key)
except:
	print('Invalid key! Provide a valid Fernet 32 byte key.')
	exit()

if op: 
	print('\nWARNING! Once you encrypt this directory, all of its contents will be INACCESSIBLE UNLESS YOU HAVE THE KEY!')
else:
	print('\nWARNING! Decrypting an unencrypted directory will cause file corruption!')
folder = input(f'Directory to {"encrypt" if op else "decrypt"} (all files and subfolders in this directory will be {"encrypt" if op else "decrypt"}ed): ')

if not os.path.exists(folder):
	print('Invalid path provided.')
	exit()

def encrypt(file):
	with open(file, 'rb') as working_file:
		encrypted = f.encrypt(working_file.read())
	with open(file, 'wb') as working_file:
		working_file.write(encrypted)

def decrypt(file):
	with open(file, 'rb') as working_file:
		decrypted = f.decrypt(working_file.read())
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

while dirqueue:
	for folder in dirqueue:
		dirqueue.extend(traverse(folder, op))
		dirqueue.remove(folder)