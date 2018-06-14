# coding=utf-8
import time

from scraping import video_page
from scraping import live_chat_replay_page as chat_page


def make_chat_list(video_id=None):
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
		
		tsp = chats[-1]
		print("time:"+tsp.timestamp_text+", list_len:"+str(len(chat_list)))
		# break

		time.sleep(0.01)

	return chat_list

