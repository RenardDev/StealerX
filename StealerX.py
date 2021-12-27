import ctypes
import sys
import platform
import os
import socket
import math
import time
from pathlib import Path
from threading import Thread

HOST_IP = '127.0.0.1'
HOST_PORT = 5005
CLIENT_TIMEOUT = 3.0
CLIENT_NAME = 'Anonymous'
#OUTPUT_DIR = Path(__file__).parent.joinpath('Tests').__str__()
OUTPUT_DIR = 'Tests'

SOCKET_BUFFER_SIZE = 1024 * 16

def main(argc, argv:list) -> int:
	print('MyTestX Stealer [1.0.0.2] by RenardDev (zeze839@gmail.com)')
	global HOST_IP
	global HOST_PORT
	global CLIENT_TIMEOUT
	global CLIENT_NAME
	global OUTPUT_DIR
	if argc > 0:
		OUTPUT_DIR = Path(argv[0]).parent.joinpath('Tests').__str__()
	if argc == 1:
		#print(f'[*] Usage: {Path(argv[0]).name} -h=<IP> -p=<PORT> -t=<TIMEOUT> -u=<USERNAME> -d=<DIR>')
		good_result = False
		while good_result != True:
			L_HOST_IP = input('[?] IP (Default = {}): '.format(HOST_IP))
			if len(L_HOST_IP) == 0:
				good_result = True
				break
			if len(L_HOST_IP) > 7:
				try:
					socket.inet_aton(L_HOST_IP)
					HOST_IP = L_HOST_IP
					good_result = True
					break
				except socket.error:
					print('[!] Invalid server IP address.')
		good_result = False
		while good_result != True:
			L_HOST_PORT = input('[?] PORT (Default = {}): '.format(HOST_PORT))
			if len(L_HOST_PORT) == 0:
				good_result = True
				break
			try:
				L_HOST_PORT = int(L_HOST_PORT)
				if (L_HOST_PORT >= 0) & (L_HOST_PORT <= 65535):
					HOST_PORT = L_HOST_PORT
					good_result = True
					break
				else:
					print('[!] Invalid server port.')
			except:
				print('[!] Invalid server port.')
		good_result = False
		while good_result != True:
			L_CLIENT_TIMEOUT = input('[?] TIMEOUT (Default = {}): '.format(CLIENT_TIMEOUT))
			if len(L_CLIENT_TIMEOUT) == 0:
				good_result = True
				break
			try:
				L_CLIENT_TIMEOUT = float(L_CLIENT_TIMEOUT)
				if L_CLIENT_TIMEOUT > 30.0:
					print('[!] Invalid client timeout interval.')
					continue
				CLIENT_TIMEOUT = L_CLIENT_TIMEOUT
				good_result = True
				break
			except:
				print('[!] Invalid client timeout interval.')
		good_result = False
		while good_result != True:
			L_CLIENT_NAME = input('[?] USERNAME (Default = {}): '.format(CLIENT_NAME))
			if len(L_CLIENT_NAME) == 0:
				good_result = True
				break
			if len(L_CLIENT_NAME) > 0:
				CLIENT_NAME = L_CLIENT_NAME
				good_result = True
				break
		good_result = False
		while good_result != True:
			L_OUTPUT_DIR = input('[?] DIR (Default = {}): '.format(OUTPUT_DIR))
			if len(L_OUTPUT_DIR) == 0:
				good_result = True
				break
			if len(L_OUTPUT_DIR) > 0:
				LL_OUTPUT_DIR = Path(L_OUTPUT_DIR)
				if LL_OUTPUT_DIR.exists():
					if LL_OUTPUT_DIR.is_dir() != True:
						print('[!] The save directory is not available.')
						continue
					else:
						OUTPUT_DIR = L_OUTPUT_DIR
						good_result = True
						break
				else:
					OUTPUT_DIR = L_OUTPUT_DIR
					good_result = True
					break
	for i in range(1, argc):
		arg = argv[i]
		if arg == '--help':
			print('[*] Usage: {} -h=<IP> -p=<PORT> -t=<TIMEOUT> -u=<USERNAME> -d=<DIR>'.format(Path(argv[0]).name))
			return -1
		if arg[0:3] == '-h=':
			L_HOST_IP = arg[3:18]
			try:
				socket.inet_aton(L_HOST_IP)
				HOST_IP = L_HOST_IP
			except socket.error:
				print('[!] Invalid server IP address.')
				return -1
		if arg[0:3] == '-p=':
			L_HOST_PORT = arg[3:8]
			try:
				L_HOST_PORT = int(L_HOST_PORT)
				if (L_HOST_PORT >= 0) & (L_HOST_PORT <= 65535):
					HOST_PORT = L_HOST_PORT
				else:
					print('[!] Invalid server port.')
					return -1
			except:
				print('[!] Invalid server port.')
				return -1
		if arg[0:3] == '-t=':
			L_CLIENT_TIMEOUT = arg[3:]
			try:
				L_CLIENT_TIMEOUT = float(L_CLIENT_TIMEOUT)
				if L_CLIENT_TIMEOUT > 30.0:
					print('[!] Invalid client timeout interval.')
					return -1
				CLIENT_TIMEOUT = L_CLIENT_TIMEOUT
			except:
				print('[!] Invalid client timeout interval.')
				return -1
		if arg[0:3] == '-u=':
			L_CLIENT_NAME = arg[3:]
			if len(L_CLIENT_NAME) > 0:
				CLIENT_NAME = L_CLIENT_NAME
		if arg[0:3] == '-d=':
			L_OUTPUT_DIR = arg[3:]
			if len(L_OUTPUT_DIR) > 0:
				LL_OUTPUT_DIR = Path(L_OUTPUT_DIR)
				if LL_OUTPUT_DIR.exists():
					if LL_OUTPUT_DIR.is_dir() != True:
						print('[!] The save directory is not available.')
						return -1
					else:
						OUTPUT_DIR = L_OUTPUT_DIR
				else:
					OUTPUT_DIR = L_OUTPUT_DIR

	print('[*] Starting with {}@{}:{} connection...'.format(CLIENT_NAME, HOST_IP, HOST_PORT), end=' ')
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(CLIENT_TIMEOUT)
	try:
		sock.connect((HOST_IP, HOST_PORT))
	except socket.timeout:
		print('[ FAIL ] (Reason: TIMEOUT)')
		sock.close()
		return -1
	except:
		print('[ FAIL ] (Reason: UNKNOWN)')
		return -1
	print('[  OK  ]')
	print('[*] Sending handshake...', end=' ')
	try:
		sock.send('GETLIST\r\n{}\r\n'.format(CLIENT_NAME).encode('utf-8'))
	except socket.timeout:
		print('[ FAIL ] (Reason: TIMEOUT)')
		sock.close()
		return -1
	except:
		print('[ FAIL ] (Reason: UNKNOWN)')
		return -1
	print('[  OK  ]')
	print('[*] Getting a list of tests...', end=' ')
	response = bytearray()
	while True:
		try:
			response.extend(sock.recv(SOCKET_BUFFER_SIZE))
		except socket.timeout:
			break
		except:
			print('[ FAIL ] (Reason: UNKNOWN)')
			return -1
	data = response.decode('utf-8').split('\r\n')
	if len(data) < 2:
		print('[ FAIL ] (Reason: CORRUPTED)')
		return -1
	if (data[0] == 'NO') | (data[1] == ''):
		print('[ FAIL ] (Reason: NOACCESS)')
		return -1
	num_tests = 0
	try:
		num_tests = int(data[1])
	except:
		print('[ FAIL ] (Reason: UNKNOWN)')
		return -1
	data = data[2:-1]
	print('[  OK  ]')
	print('[i] Found {} tests!'.format(num_tests))
	print('[*] Closing a connection...', end=' ')
	try:
		sock.send(b'QUIT\r\n')
	except socket.timeout:
		print('[ FAIL ] (Reason: TIMEOUT)')
		sock.close()
		return -1
	except:
		print('[ FAIL ] (Reason: UNKNOWN)')
		return -1
	sock.close()
	print('[  OK  ]')
	print('[+] Tests:')
	tests = list()
	for i in range(0, num_tests):
		tests.append((data[i:][i], data[i:][i + 1]))
	index = 1
	for test in tests:
		print('[  {}  ]'.format(index))
		print('  > Title: `{}`'.format(test[1]))
		print('   > File: `{}`'.format(Path(test[0]).name))
		index += 1
	print('[+] Threads:')
	num_threads = os.cpu_count() * 2
	num_tests_for_thread = int(math.ceil(num_tests / num_threads))
	threads_input_data = list()
	for thread in range(0, num_threads):
		thread_tests = list()
		for test in tests[num_tests_for_thread * thread: num_tests_for_thread * thread + num_tests_for_thread]:
			thread_tests.append(test)
		threads_input_data.append((thread, thread_tests))
	remainder = tests[num_tests_for_thread * num_threads: num_tests_for_thread * num_threads + num_tests_for_thread]
	if len(remainder):
		thread_tests = list()
		for test in remainder:
			thread_tests.append(test)
		threads_input_data.append((num_threads, thread_tests))
		num_threads += 1
	for thread in threads_input_data:
		print('[  {}  ]'.format(thread[0] + 1))
		for test in thread[1]:
			print('  > Title: `{}`'.format(test[1]))
			print('   > File: `{}`'.format(Path(test[0]).name))
	print('[*] Setup threads...', end=' ')
	threads_status_data = [ None ] * num_threads
	threads_output_data = [ None ] * num_threads
	def _ProcessThread(thread_index:int) -> None:
		nonlocal threads_input_data
		nonlocal threads_status_data
		nonlocal threads_output_data
		threads_status_data[thread_index] = 'Started'
		threads_output_data[thread_index] = list()
		max_tests = len(threads_input_data[thread_index][1])
		total_tests = 0
		for test in threads_input_data[thread_index][1]:
			threads_status_data[thread_index] = 'Downloading ({}/{}) `{}`'.format(total_tests, max_tests, Path(test[1]).name)
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.settimeout(CLIENT_TIMEOUT)
			try:
				sock.connect((HOST_IP, HOST_PORT))
			except socket.timeout:
				threads_status_data[thread_index] = 'Restarting'
				sock.close()
				return
			except:
				threads_status_data[thread_index] = 'Error #1'
				return
			try:
				sock.send('GETTEST\r\n{}\r\n{}\r\n'.format(CLIENT_NAME, test[0]).encode('utf-8'))
			except socket.timeout:
				threads_status_data[thread_index] = 'Restarting'
				sock.close()
				return
			except:
				threads_status_data[thread_index] = 'Error #2'
				return
			data = bytearray()
			while True:
				try:
					data.extend(sock.recv(SOCKET_BUFFER_SIZE))
				except socket.timeout:
					break
				except:
					threads_status_data[thread_index] = 'Error #3'
					return
			threads_output_data[thread_index].append((thread_index, Path(test[0].replace('\\',  '/')).name, data))
			try:
				sock.send(b'QUIT\r\n')
			except socket.timeout:
				threads_status_data[thread_index] = 'Restarting'
				sock.close()
				return
			except:
				threads_status_data[thread_index] = 'Error #4'
				return
			sock.close()
			total_tests += 1
		threads_status_data[thread_index] = 'Finished'
	print('[  OK  ]')
	threads_handles = list()
	for thread_index in range(0, num_threads):
		t = Thread(target=_ProcessThread, args=(thread_index,))
		threads_handles.append(t)
	print('[*] Starting threads...', end=' ')
	for thread_index in range(0, num_threads):
		threads_handles[thread_index].start()
	print('[  OK  ]')
	threads_finished = False
	while threads_finished != True:
		threads_finished = True
		for thread_index in range(0, num_threads):
			if threads_status_data[thread_index] == 'Restarting':
				threads_handles[thread_index] = Thread(target=_ProcessThread, args=(thread_index,))
				threads_handles[thread_index].start()
			if threads_status_data[thread_index] != 'Finished':
				threads_finished = False
			print('[*] {}> Thread-{} {}(Status: {})'.format(" " * thread_index, thread_index + 1, " " * (num_threads - thread_index), threads_status_data[thread_index]))
		if threads_finished != True:
			time.sleep(5)
	print('[*] Saving tests...')
	if Path(OUTPUT_DIR).exists():
		if Path(OUTPUT_DIR).is_dir() != True:
			print('[!] The save directory is not available.')
			return -1
	else:
		Path(OUTPUT_DIR).mkdir()
	index = 1
	for thread_index in range(0, num_threads):
		for thread_data in threads_output_data[thread_index]:
			save_path = Path(OUTPUT_DIR).joinpath(thread_data[1])
			if save_path.exists():
				if save_path.is_file() != True:
					print('[!] File `{}` could not be created.'.format(thread_data[1]))
					index += 1
					continue
				if save_path.stat().st_size < len(thread_data[2]):
					f = open(save_path.__str__(), 'wb+')
					f.write(thread_data[2])
					f.close()
					print('[+] ReSaved (#{}): `{}`` (Reason: Size difference)'.format(index, thread_data[1]))
					index += 1
					continue
				#if save_path.stat().st_size == len(thread_data[2]):
				#	fs = open(save_path.__str__(), 'rb')
				#	fsd = fs.read()
				#	fs.close()
				#	if hashlib.sha1(fsd).hexdigest() != hashlib.sha1(thread_data[2]).hexdigest():
				#		f = open(save_path.__str__(), 'wb+')
				#		f.write(thread_data[2])
				#		f.close()
				#		print(f'ReSaved: {thread_data[1]}  (Reason: Corrupted file)')
				#		continue
				print('[!] File `{}` has already been created.'.format(thread_data[1]))
				continue
			if len(thread_data[2]) != 0:
				f = open(save_path.__str__(), 'wb+')
				f.write(thread_data[2])
				f.close()
				print('[+] Saved (#{}): `{}`'.format(index, thread_data[1]))
			else:
				print('[!] Test (#{}) `{}` not found.'.format(index, thread_data[1]))
			index += 1
	print('[ DONE ]')
	input('Press <Enter> to exit...')
	return 0

if __name__ == '__main__':
	encoding = None
	encoding_output = None
	if platform.system() == 'Windows':
		encoding = ctypes.windll.kernel32.GetConsoleCP()
		encoding_output = ctypes.windll.kernel32.GetConsoleOutputCP()
		ctypes.windll.kernel32.SetConsoleCP(65001)
		ctypes.windll.kernel32.SetConsoleOutputCP(65001)
		ctypes.windll.kernel32.SetConsoleTitleA(b'StylerX')
		sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)
	exit_code = main(len(sys.argv), sys.argv)
	if platform.system() == 'Windows':
		ctypes.windll.kernel32.SetConsoleCP(encoding)
		ctypes.windll.kernel32.SetConsoleOutputCP(encoding_output)
	sys.exit(exit_code)
