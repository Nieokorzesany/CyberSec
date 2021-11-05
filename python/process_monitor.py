import os
import sys
import win32api
import win32con
import win32security
import wmi

def get_process_privileges(pid):
	try:
		hproc = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION, False,pid)
		htok = win32security.OpenProcessToken(hproc,win32con.TOKEN_QUERY)
		privs = win32security.GetTokenInformation(htok,win32security.TokenPrivileges)
		privileges = ''
		for priv_id, flags in privs:
			if flags == (win32security.SE_PRIVILEGE_ENABLED | win32security.SE_PRIVILEGE_ENABLED_BY_DEFAULT):
				privileges += f'{win32security.LookupPrivilegeName(None, priv_id)}|'
	except Exception:
		#privileges = 'N/A'
		privileges = get_process_privileges(pid)
	return privileges


def log_to_file(message):
	with open('process_monitor_log.csv', 'a') as fd:
		fd.write(f'{message}\r\n')

def monitor():
	head = 'CommandLine, Time, Executable, Parent PID,PID, User, Privileges'
	log_to_file(head)
	c = wmi.WMI()
	process_watcher = c.Win32_Process.watch_for('creation')
	while True:
		try:
			new_process = process_watcher()
			cmdline = new_process.CommandLine
 			create_date = new_process.CreationDate
 			executable = new_process.ExecutablePath
			parent_pid = new_process.ParentProcessId
			pid = new_process.ProcessId
			proc_owner = new_process.GetOwner()
			privileges = 'N/A'
			process_log_message = (f'{cmdline} , {create_date} ,{executable},'
								   f'{parent_pid} , {pid} , {proc_owner} ,{privileges}')
			print(process_log_message)
			print()
			log_to_file(process_log_message)
		except Exception:
			pass 

if __name__ == '__main__':
	monitor()


"""
C:\Users\tim\work> python.exe process_monitor.py
"Calculator.exe",
20200624084445.120519-240 ,
C:\Program
Files\WindowsApps\Microsoft.WindowsCalculator\Calculator.exe,
1204 ,
13116 ,
('DESKTOP-CC91N7I', 0, 'tim') ,
SeChangeNotifyPrivilege|
notepad ,
20200624084436.727998-240 ,
C:\Windows\system32\notepad.exe,
10720 ,
2732 ,
('DESKTOP-CC91N7I', 0, 'tim') ,SeChangeNotifyPrivilege|SeImpersonatePrivilege|SeCreateGlobalPrivilege|
"""
