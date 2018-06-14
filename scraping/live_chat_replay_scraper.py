# coding=utf-8
import time

from scraping import video_page
from scraping import live_chat_replay_page as chat_page

current_video_id = None


def scraping_video_details(video_id=None):
	if video_id is None: return None
	global current_video_id
	if video_id != current_video_id:
		video_page.open_by_id(video_id=video_id)
	
	details = video_page.get_video_details()
	
	if details is not None:
		current_video_id = details.video_id

	return details


def make_chat_list(video_id=None):
	if video_id is None: return None
	scraping_video_details(video_id=video_id)

	chat_list = []
	continuation = video_page.pick_out_chat_continuation()

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

