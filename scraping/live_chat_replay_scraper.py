# coding=utf-8
import time
import concurrent.futures as futures

from scraping import video_page
from scraping import live_chat_replay_page as chat_page

CHAT_WORKERS = []
IS_FINISHED = False
FINISH_COUNTER = 0
def scraping_video_details(video_id=None):
	if video_id is None: return None
	p = video_page.open_by_id(video_id=video_id)
	details = video_page.get_video_details(p)

	if details is not None:
		current_video_id = details.video_id

	return details

def worker_finish_callback(future):
	global FINISH_COUNTER
	global CHAT_WORKERS
	global IS_FINISHED
	FINISH_COUNTER += 1
	IS_FINISHED = (FINISH_COUNTER == len(CHAT_WORKERS))
	print("fin_cnt:"+str(FINISH_COUNTER)+"/"+str(len(CHAT_WORKERS)))

def make_chat_list(video_id=None):
	if video_id is None: return None

	# make continuation list from starting minutes
	video_details = scraping_video_details(video_id=video_id)
	print(video_details.title)
	seconds = int(video_details.length_seconds)
	start_sec = 0
	d_sec = 10 * 60 # 10 minutes
	end_sec = start_sec + d_sec
	rear_sec = seconds

	# make running worker
	global CHAT_WORKERS
	CHAT_WORKERS = []
	executor = futures.ThreadPoolExecutor()
	while(start_sec < rear_sec):
		chat_worker = executor.submit(run_making_chat_list_worker, video_id, start_sec, end_sec)
		chat_worker.add_done_callback(worker_finish_callback)
		CHAT_WORKERS.append(chat_worker)
		start_sec = end_sec
		end_sec = end_sec + d_sec
		if end_sec > seconds:
			end_sec = rear_sec

	# wait done worker
	global IS_FINISHED
	global FINISH_COUNTER
	IS_FINISHED = False
	FINISH_COUNTER = 0
	while not IS_FINISHED:
		pass

	# get result of working
	chat_list = []
	for chat_worker in CHAT_WORKERS:
		chats = chat_worker.result()
		chat_list.extend(chats)

	return chat_list


def run_making_chat_list_worker(video_id=None, start_second=None, end_second=None):
	rtn_chats = []
	start_minute = int(start_second / 60)
	end_minute = int(end_second / 60)
	current_rear_second = start_second

	page = video_page.open_by_id_minutes(video_id, start_minute)
	continuation = video_page.pick_out_chat_continuation(page)
	cntn_cnt = 0
	while(continuation is not None and current_rear_second < end_second-1):
		next_continuation, chats = chat_page.get_contents(continuation=continuation)

		is_empty_contents = next_continuation is None and chats is None
		if is_empty_contents and end_second >= current_rear_second:
			cntn_cnt += 1
			if cntn_cnt >= 5:
				break
			time.sleep(3)
			continue
		cntn_cnt = 0
		continuation = next_continuation

		if chats is not None:
			current_rear_second = int(chats[-1].seconds())
		else:
			current_rear_second = end_second
			chats = []

		if current_rear_second >= end_second and continuation is not None:
			chats = remove_surplus_from_chats(chats, end_minute)
			continuation = None

		rtn_chats.extend(chats)
		if len(chats) > 0:
			tsp = chats[-1]
			print("end:"+str(end_minute)+", time:"+tsp.timestamp_text+", list_len:"+str(len(rtn_chats)))
		# break
		time.sleep(0.01)

	print("start:"+str(start_minute)+", Worker END")
	return rtn_chats


def remove_surplus_from_chats(chats=None, end_minute=None):
	if chats is None or len(chats) == 0:
		return []

	left = 0
	right = len(chats)-1
	index = None

	# find just end_minute
	while(True):
		index = int((left+right)/2)

		chat = chats[index]
		m = int(chat.minutes())
		dt = chat.datetime()
		tt = dt.timetuple()
		s = tt[5]

		# just end_minute
		if m == end_minute and s == 0:
			break
		elif m >= end_minute and s > 0:
			right = index
		elif m < end_minute:
			left = index
		if right - left == 1:
			break


	# find boundary between end_minute-1 and end_minute
	while index > 0:
		chat = chats[index]
		m = int(chat.minutes())
		if m < end_minute:
			index += 1
			break
		index -= 1

	length = len(chats)
	del chats[index:length]

	return chats
