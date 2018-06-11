# coding=utf8
from sys import argv
import time

# import channels_list
from scraping import video_page
from scraping import live_chat_replay_page as chat_page


def start_live_chat_replay_by_video_id(video_id=None):
	continuation = video_page.pick_out_chat_continuation(video_id=video_id)
	if continuation is None:
		return None
	continue_live_chat_replay(continuation=continuation)


def continue_live_chat_replay(continuation=None):
	chat_list = []
	while(True):
		if continuation is None:
			print("continuation is Invalid or This is End")
			break

		continuation, chats = chat_page.get_contents(continuation=continuation)

		chat_list.extend(chats)
		break


		if chats is None or len(chats) == 0:
			print("chat is End")
			break
		
		time.sleep(0.5)

	liveChats = []

	for c in chat_list:
		print(c.timestamp_text+":"+c.message)



def save_text(name=None, text=None):
	f = open(name, 'wt')
	f.write(text)
	f.close()


# input video_id from command line
if len(argv) > 1 :
	for v in range(1, len(argv)):
		print(argv[v])
		val = argv[v]
		if len(val) == 11:
			start_live_chat_replay_by_video_id(video_id=val)
		elif len(val) >= 11 and val[0:6] == 'op2w0w':
			continue_live_chat_replay(continuation=val)
