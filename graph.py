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
	s_time = time.time()
	video_details = chat_scraper.scraping_video_details(video_id=video_id)
	title = video_id

	global chat_list
	chat_list = chat_scraper.make_chat_list(video_id)

	chat_freq_data = count_chats_by_minutes(chat_list=chat_list)

	d = time.time() - s_time
	print("s-e:"+str(d))


def display_graph(data=None, title="No Name", kind="bar"):
	if data is None :
		global chat_list
		if chat_list is None: return None
		data = count_chats_by_minutes(chat_list)
	num = len(data)

	data.plot(title=title, kind=kind)
	plt.show(block=False)

	print(kind)
	return True


def count_chats_by_minutes(chat_list=None):
	if chat_list is None: return None
	d = {}
	for chat in chat_list:
		m = int(chat.minutes())
		if m not in d.keys():
			print("new Key:"+str(m))
			d[m] = 0
		d[m] += 1

	df = pd.DataFrame(list(d.values()), columns=['numbers'])

	return df

# input video_id from command line
# $ python graph.py [youtube video_id]
if __name__ == '__main__':
	if len(argv) > 1 :
		for v in range(1, len(argv)):
			print(argv[v])
			val = argv[v]
			if len(val) == 11:
				plot(video_id=val)
