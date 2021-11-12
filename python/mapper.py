import contextlib
import os
import queue
import requests
import sys
import threading
import time

FILTERED = [".jpg", ".gif", ".png", ".css"]
TARGET = "https://www.imep.pro/wordpress"
THREADS = 10

answers = queue.Queue()
web_paths = queue.Queue()

def gather_paths():
	for root, _, files in os.walk('.'):
		for fname in files:
			if os.path.splitext(fname)[1] in FILTERED:
				continue
			path = os.path.join(root, fname)
			if path.startswith('.'):
				path = path[1:]
			print(path)
			web_paths.put(path)

@contextlib.contextmanager
def chdir(path):
	"""
	on enter, change directory to specified path.
	on exite, change directory back to original.
	"""
	this_dir = os.getcwd()
	os.chdir(path)
	try:
		yield
	finally:
		os.chdir(this_dir)

def test_remote():		# testing live target
	while not web_paths.empty():
		path = web_paths.get()
		url = f'{TARGET}{path}'
		time.sleep(2)	#your target my have throttling/lockout
		r = requests.get(url)
		if r.status_code == 200:
			answers.put(url)
			sys.stdout.write('+')
		else:
			sys.stdout.write('x')
		sys.stdout.flush()

def run():				#function orchestrates the mapping process
	mythreads = list()
	for i in range(THREADS):
		print(f'Spawnin thread {i}')
		t = threading.Thread(target=test_remote)
		mythreads.append(t)
		t.start()
	for thread in mythreads:
		thread.join()

if __name__ == '__main__':
	with chdir("/home/kali/Downloads/wordpress"): 			#Download wordpress from : https://wordpress.org/download/
		gather_paths()
	input('Press return to continue.')

	run()

	with open('mythreads.txt', 'w') as f:
		while not answers.empty():
			f.write(f'{answers.get()}\n')
		print('\ndone')


"""
Example Output:
└─$ python3 mapper.py        
/wp-admin/network/update-core.php
/wp-admin/network/plugins.php
/wp-admin/network/site-info.php
/wp-admin/network/edit.php
/wp-admin/network/sites.php
/wp-admin/network/about.php
/wp-admin/network/plugin-editor.php
/wp-admin/network/setup.php
/wp-admin/network/theme-editor.php
/wp-admin/network/admin.php
/wp-admin/network/freedoms.php
/wp-admin/network/upgrade.php
/wp-admin/network/users.php
/wp-admin/network/theme-install.php
Press return to continue.
Spawnin thread 0
Spawnin thread 1
Spawnin thread 2
Spawnin thread 3
Spawnin thread 4
Spawnin thread 5
Spawnin thread 6
Spawnin thread 7
Spawnin thread 8
Spawnin thread 9
+xxxx++x++x+xx+x++x+x+x+xx+x++xxx+x+x+xx+x+++++++++++xxx+++x+++xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx+xxx+++x+xx++++xxxxxxxxxxxx++++xx++xxx++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++x+x+++++++xxx+xxxxxxxxxxxxxxxxxxxxxxxx+++++++++x+++++++++++++x+xx+xx+++x+x+x++x+xx+x++xxx++x++++x++++++x+x+++++xxxx+++x+++++x++x++++xx+x++xx+++++++++xx++++++x++xxxx++xxx++xx++++xx++++x++++xx+x+++++++x+xx++++++x+xx++++xx+++x++++++x++x+++++++++x+++++++x+++++++x++++x+++++xx+xxxxxxxxxxx++++xxxx+++++++xxx+xxxxxxxxxx++xxxx+++++++xxxxxxxxxxxxxxxxxxxxxxxxxx+xxxxxxxxxxxxxxxxxxxxxxxxxxxxx++x+++++++++++++++++++++x++xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx+++xxxxx++++++++++++x++++++++++++++xxxx+xxxxxxx+xx+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++x+xxxxxxx+xxxxxx+xxxxxxxxxxxxxxxxxxx++++++x+xx+++++++++xx++++++xxxxxxxxxxxxxxxxxxxxxxxx+xxxxxxxx+x+x+++++++++++xx+xxxx+xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++x+++++++++++++x+++++++++++++x++++++++++xx++++++++++++++++++x+++x+++++++x++++++++x+++++x+++++++++++++++x+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++x+xxx+xx+++++xxx+xxx++x+xxx++xxxx+++xx+x+x+xxxx+x+x+++++x+++xx++x++xxx+xx++x+xxx+++xx+x++++xxx+x+x+xx+xxx+++++++++++x++++++++++++++++++++++++++++
done
└─$ head mythreads.txt                                                                                                                                                                  1 ⚙
https://www.imep.pro/wordpress/license.txt
https://www.imep.pro/wordpress/wp-cron.php
https://www.imep.pro/wordpress/wp-login.php
https://www.imep.pro/wordpress/wp-activate.php
https://www.imep.pro/wordpress/wp-content/index.php
https://www.imep.pro/wordpress/wp-load.php
https://www.imep.pro/wordpress/wp-links-opml.php
https://www.imep.pro/wordpress/wp-signup.php
https://www.imep.pro/wordpress/wp-content/themes/index.php
https://www.imep.pro/wordpress/wp-content/themes/twentytwenty/header.php
"""
