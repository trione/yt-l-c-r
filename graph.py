# coding=utf-8
from sys import argv
import time
import datetime
import dateutil.parser as timeparser

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import Series

from scraping import video_page
from scraping import live_chat_replay_page as chat_page


chat_list = None

def plot(video_id=None):
	s_time = time.time()
	make_chat_list(video_id)
	d = time.time() - s_time
	print("s-e:"+str(d))


def make_chat_list(video_id=None):
	title = video_id

	global chat_list
	chat_list = []

	continuation = video_page.pick_out_chat_continuation(video_id=video_id)

	while(True):
		if continuation is None:
			print("continuation is Invalid or This is End")
			break

		continuation, chats = chat_page.get_contents(continuation=continuation)

		if chats is None or len(chats) == 0:
			print("chat is End")
			break

		chat_list.extend(chats)
		# break

		tsp = chats[-1]
		print("time:"+tsp.timestamp_text+", list_len:"+str(len(chat_list)))

		time.sleep(0.01)


def display_graph(data=None, title="No Name", kind="bar"):
	if data is None :
		global chat_list
		if chat_list is None: return None
		data = count_chats_by_time(chat_list)

	data.plot(title=title, kind=kind)
	plt.show()
	plt.close()

	print(kind)

	return True


def count_chats_by_time(chat_list=None):
	freq_series = Series()

	if chat_list is None: return None

	for chat in chat_list:

		# date_time = chat.datetime()
		# t_tuple = date_time.timetuple()

		# h = t_tuple[3]
		# m = t_tuple[4]
		# s = t_tuple[5]

		mins = chat.minutes()
		m = int(mins)

		if m not in freq_series.index:
			print("new Series:"+str(m))
			freq_series = freq_series.append(Series(index=[m]))
			freq_series[m] = 0

		freq_series[m] += 1

	return freq_series


# input video_id from command line
# $ python graph.py [youtube video_id]
if __name__ == '__main__':
	if len(argv) > 1 :
		for v in range(1, len(argv)):
			print(argv[v])
			val = argv[v]
			if len(val) == 11:
				plot(video_id=val)
