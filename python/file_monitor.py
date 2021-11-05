import os
import tempfile
import threading
import win32con
import win32file

FILE_CREATED = 1
FILE_DELETED = 2
FILE_MODIFIED = 3
FILE_RENAMED_FROM = 4
FILE_RENAMED_TO = 5

FILE_LIST_DIRECTORY = 0x0001
PATHS = ['c:\\WINDOWS\\Temp', tempfile.gettempdir()]

def monitor(path_to_watch):
	h_directory = win32file.CreateFile(
		path_to_watch,
		FILE_LIST_DIRECTORY,
		win32con.FILE_SHARE_READ |
		win32con.FILE_SHARE_WRITE |
		win32con.FILE_SHARE_DELETE,
		None,
		win32con.OPEN_EXISTING,
		win32con.FILE_FLAG_BACKUP_SEMANTICS,
		None
		)
	while True:
		try:
			results = win32file.ReadDirectoryChangesW(
			h_directory,	
			1024,
			True,
			win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
			win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
			win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
			win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
			win32con.FILE_NOTIFY_CHANGE_SECURITY |
			win32con.FILE_NOTIFY_CHANGE_SIZE,
			None,
			None
			)

			for action, file_name in results:
				full_filename = os.path.join(path_to_watch, file_name)
				if action == FILE_CREATED:
					print(f'[+] Created {full_filename}')
				elif action == FILE_DELETED:
					print(f'[-] Deleted {full_filename}')
				elif action == FILE_MODIFIED:
					print(f'[*] Modified {full_filename}')
					try:
						print('[vvv] Dumping contents ...')

						with open(full_filename) as f:
							contents = f.read()
						print(contents)
						print('[^^^] Dump complete.')
				except Exception as e:
					print(f'[!!!] Dump failed. {e}')

				elif action == FILE_RENAMED_FROM:
					print(f'[>] Renamed from {full_filename}')
				elif action == FILE_RENAMED_TO: 
					print(f'[<] Renamed to {full_filename}')
				else:
					print(f'[?] Unknown action on {full_filename}')
		except Exception:
			pass 

if __name__ == '__main__':
	for path in PATHS:
		monitor_thread = threading.Thread(target=monitor,args=(path,))
		monitor_thread.start()


"""
C:\Users\tim\work> python.exe file_monitor.py
Open a second cmd.exe shell and execute the following commands:
C:\Users\tim\work> cd C:\Windows\temp
C:\Windows\Temp> echo hello > filetest.batC:\Windows\Temp> rename filetest.bat file2test
C:\Windows\Temp> del file2test
You should see output that looks like the following:
[+] Created c:\WINDOWS\Temp\filetest.bat
[*] Modified c:\WINDOWS\Temp\filetest.bat
[vvv] Dumping contents ...
hello
[^^^] Dump complete.
[>] Renamed from c:\WINDOWS\Temp\filetest.bat
[<] Renamed to c:\WINDOWS\Temp\file2test
[-] Deleted c:\WINDOWS\Temp\file2test
"""