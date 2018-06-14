# coding=utf-8
from sys import argv
import time
import datetime
import dateutil.parser as timeparser

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import Series

from scraping import live_chat_replay_scraper as chat_scraper


chat_list = None

def plot(video_id=None):
	title = video_id
	s_time = time.time()

	global chat_list
	chat_list = chat_scraper.make_chat_list(video_id)
	
	d = time.time() - s_time
	print("s-w:"+str(d))

	chat_freq_data = count_chats_by_time(chat_list=chat_list)

	d = time.time() - s_time
	print("s-e:"+str(d))

	display_graph(chat_freq_data, video_id, "bar")


def display_graph(data=None, title="No Name", kind="bar"):
	if data is None :
		global chat_list
		if chat_list is None: return None
		data = count_chats_by_time(chat_list)

	data.plot(title=title, kind=kind)
	plt.show(block=False)

	print(kind)

	return True


def count_chats_by_time(chat_list=None):
	if chat_list is None: return None

	freq_series = Series()

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
