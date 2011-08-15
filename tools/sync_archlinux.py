#!/usr/bin/env python
# autor: Ni Qingliang
# NOTE: this script can be used to sync arch repository which is accessed through
#       http

import urllib.request, urllib.parse, urllib.error
import sys
import time
import datetime
import re
import os
import queue
import threading
import http.client
import tempfile



g_host = "mirrors.163.com"
g_loc_base_dir = "/srv/http/archlinux/"
g_blk_size = 256 * 1024
g_progress_bar_size = 25

def my_print(fmt):
#	print(fmt, end='')
	sys.stdout.write(fmt)
	sys.stdout.flush()

def report_hook(count, block_size, total_size, url, loc):
	nb_total = int((total_size + block_size) / block_size)
	if int(25 * count / nb_total) > int(25 * (count - 1) / nb_total):
#		sys.stdout.write("#")
		my_print("#")
#		sys.stdout.write("%02d%%" %((100.0 * count / nb_total)))
#	sys.stdout.write('%02d%% %010d %010d %010d %s %s' %((100.0 * count * block_size/ total_size), count, block_size, total_size, url, loc))

#urllib.urlretrieve("http://sports.sina.com.cn/", reporthook= report_hook)

def g_download(rem_file, loc_file):
	file_name = os.path.basename(loc_file)
	starttime =  datetime.datetime.now()
#	print('download start time is %s'% starttime)
#	urllib.request.urlretrieve(url,'test.html', reporthook= report_hook)  #开始下载，test.exe为下载后保存的文件名
	my_print("%-50s[" % (file_name))

	rem_fp = urllib.request.urlopen(rem_file)
	headers = rem_fp.info()
	real_size = -1
	if "content-length" in headers:
		real_size = int(headers["Content-Length"])
	loc_fp = open(loc_file, 'wb')

	read_size = 0
	block_size = g_blk_size
	real_block_num = int((real_size + block_size - 1) / block_size)
	block_num = 0
	prg_bar_total = g_progress_bar_size
	prg_bar = 0
	while 1:
		block = rem_fp.read(block_size)
		if not block:
			break
		read_size += len(block)
		loc_fp.write(block)
		block_num += 1
		new_bar = int(prg_bar_total * block_num / real_block_num)
		for i in range(new_bar - prg_bar):
			my_print("-")
		prg_bar = new_bar
	loc_fp.close()
	rem_fp.close()
#	urllib.request.urlretrieve(rem_file, loc_file, lambda nb, bs, fs, remote_file = rem_file, locale_file = loc_file:report_hook(nb, bs, fs, rem_file, loc_file))
	endtime =  datetime.datetime.now()
	my_print("]\n")
#	print('download end time is %s'% endtime)
#	print('you download the file use time %s s' % (endtime - starttime).seconds)

class crep_block:
	def __init__(self, nbr, size, rep_file):
		self._block = None
#		self._isDownloading = False
		self._nbr = nbr
		self._size = size
		self._start = nbr * size
		self._end = self._start + self._size - 1
		self._rep_file = rep_file
		return

	def download(self, conn):
		my_print("%2d" % (self._nbr))
		headers = {
			'Range':'bytes=%s-%s' % ( self._start, self._end )
		};
		conn.request('GET', self._rep_file.rem_path(), None, headers)
		resp = conn.getresponse()
		self._block = resp.read()

		my_print("#")
#		my_print(" %d %d\n" % (self._nbr, len(self._block)))
		return

	def correct(self, size):
		self._end = size
		self._size = self._end - self._start + 1
		return

class crep_file:
	def __init__(self, name, timestamp, size, sub_rep):
		self._name = name
#		self._timestamp = datetime.datetime.strptime(timestamp, "%d-%b-%Y %H:%M")
		self._timestamp = time.strptime(timestamp, "%d-%b-%Y %H:%M")
		self._size = int(size)
		self._blk_size = g_blk_size
		self._nBlk = int((self._size + self._blk_size - 1) / self._blk_size)
		self._sub_rep = sub_rep
#		my_print("block num: %d\n" %(nblock))
		self._blocks = []
		self._blocks_null = []
		self._blocks_dling = []

	def need_dl(self):
		file_path = self._sub_rep.loc_dir() + self._name
		if os.path.exists(file_path) and (os.path.getsize(file_path) == self._size):
			stat_info = os.stat(file_path)
#			dt_tmp = datetime.datetime.fromtimestamp(stat_info.st_mtime)
#			my_print(" mtime is %s\n" % (dt_tmp.strftime("%d-%b-%Y %H:%M")))
			if stat_info.st_mtime > time.mktime(self._timestamp):
				return False
		return True
	def download(self):
		if self.need_dl():
			g_download("http://" + g_host + self._sub_rep.main_page() + self._name, self._sub_rep.loc_dir() + self._name)
		else:
			my_print("%-50s skip\n" % (self._name) )
		return

	def _gen_blks(self, queue):
		# donot need to download files
		file_path = self._sub_rep.loc_dir() + self._name
		if os.path.exists(file_path) and (os.path.getsize(file_path) == self._size):
			return

		# block		
		for index in range(self._nBlk):
			blk_info_tmp = crep_block(index, self._blk_size, self)
			self._blocks.append(blk_info_tmp)
			self._blocks_null.append(blk_info_tmp)
			queue.put(blk_info_tmp)

		self._blocks[self._nBlk - 1].correct(self._size)

		return
	def write_to_file(self):
		file_path = self._sub_rep._loc_dir + self._name
		if len(self._blocks) == 0:
			return

		fp = open(file_path, "wb")
		for i in self._blocks:
			fp.write(i._block)
		fp.close()

	def tostr(self):
		return self._name + self._timestamp.strftime("%d-%b-%Y %H:%M") + str(self._size)

	def name(self):
		return self._name

	def rem_path(self):
		return self._sub_rep.main_page() + self._name

	def blk_num(self):
		return self._nBlk

	def size(self):
		return self._size


class csub_rep:
	def __init__(self, conn, main_page, loc_dir):
		self._main_page = main_page
		self._file_list = []
		self._loc_dir = loc_dir
		file_info = None
		if (0 < 1):
			tmp = urllib.request.urlopen("http://" + g_host + self._main_page)
			file_info = tmp.read()
		else:
			conn.request('GET', main_page)
			file_info = conn.getresponse().read()
		fp = tempfile.TemporaryFile()
		fp.write(file_info)
		fp.seek(0)
		for line in fp:
			str_line = str(line)
			#过滤无用行
			if not re.match("^b\'\<a", str_line):
				continue
			str_arr = re.split('b\'\<a href=\"|\"\>|\</a\> +|  +|\\\\r\\\\n\'', str_line)

			if str_arr[4] == "-":
				continue
			# fix 163's bug
			if int(str_arr[4]) < 100:
				continue

			#my_print("  add %s\n" % (str_arr[2]))
			#如果链接以./开头，则去除
			str_arr[1] = re.sub("^\./", "", str_arr[1])
			self._file_list.append(crep_file(str_arr[1], str_arr[3], str_arr[4], self))

		fp.close()

		# create locale directory
		if not os.path.exists(self._loc_dir):
			os.makedirs(self._loc_dir)
#		for single_file in self._file_list:
#			print(single_file.tostr())

	def main_page(self):
		return self._main_page

	def loc_dir(self):
		return self._loc_dir

	def download(self):
		for i in self._file_list:
			my_print("%-50s %-6d " % (i.name(), i.blk_num()))
			i._gen_blks(g_q)
			g_q.join()
			i.write_to_file()
			my_print("\n")
		return
	def dl_urllib(self):
		for i in self._file_list:
			i.download()

		return

	def rm_old_files(self):
		cur_files = os.listdir(self._loc_dir)
		set_cur = set()
		#my_print("curfiles:")
		for i in cur_files:
			#my_print("  %s\n" % (i))
			set_cur.add(i)
		set_repo = set()
		#my_print("\nrepofiles:")
		for i in self._file_list:
			#my_print("  %s\n" % (i.name()))
			set_repo.add(i.name())

		set_del = set_cur - set_repo
		for i in set_del:
			my_print("rming %s\n" % (self._loc_dir + i))
			os.remove(self._loc_dir + i)
		#my_print("\n")

		return

g_q = queue.Queue()

def g_worker():
	conn = http.client.HTTPConnection(g_host, 80)
	while True:
		item = g_q.get()
		item.download(conn)
		g_q.task_done()

	conn.close()

'''
def prc_file(file_name):
	net_page = open(file_name)
	for line in net_page:
		str_line = str(line)
		if not re.match("^\<a", str_line):
			continue
		print(re.split('\<a href=\"|\"\>|\</a\> +|  +|\r|\n', str_line))
#		print(str_line)
'''

if __name__ == '__main__':
	main_conn = http.client.HTTPConnection(g_host, 80)
	repos = ["core",
		"extra",
		"community",
		"multilib",
#		"testing",
#		"multilib-testing",
#		"community-testing"
		]
	for repo in repos:
		my_print("dling repo %s:\n" % (repo))
		test = csub_rep(main_conn, '/archlinux/' + repo + '/os/x86_64/', g_loc_base_dir + repo + "/os/x86_64/")

		if (1 < 0):
			for i in range(0):
				t = threading.Thread(target=g_worker)
				t.daemon = True
				t.start()

			test.download()
		else:
			test.dl_urllib()

		test.rm_old_files()

	main_conn.close()
#	prc_file("test.html")
#	download('http://mirrors.163.com/archlinux/core/os/x86_64/', 'test.html')
#	file_time = datetime.datetime.strptime("14-Feb-2011 22:00", "%d-%b-%Y %H:%M")
#	print(file_time.strftime("%d-%b-%Y %H:%M"))


