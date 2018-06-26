# coding=utf-8
import time
import concurrent.futures as futures

from scraping import video_page
from scraping import live_chat_replay_page as chat_page


def scraping_video_details(video_id=None):
	if video_id is None: return None
	p = video_page.open_by_id(video_id=video_id)
	details = video_page.get_video_details(p)

	if details is not None:
		current_video_id = details.video_id

	return details


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
	ftrs = []
	executor = futures.ThreadPoolExecutor()
	while(start_sec < rear_sec):
		ftr = executor.submit(run_making_chat_list_worker, video_id, start_sec, end_sec)
		ftrs.append(ftr)
		start_sec = end_sec
		end_sec = end_sec + d_sec
		if end_sec > seconds:
			end_sec = rear_sec

	# wait done worker
	done_num = 0
	ftrs_num = len(ftrs)
	while ftrs_num != done_num:
		done_num = 0
		time.sleep(5)
		for ftr in ftrs:
			if ftr.done():
				done_num = done_num + 1

		print("done:"+str(done_num)+"/"+str(ftrs_num))

	# get result of working
	chat_list = []
	for ftr in ftrs:
		chats = ftr.result()
		chat_list.extend(chats)

	return chat_list


def run_making_chat_list_worker(video_id=None, start_second=None, end_second=None):
	rtn_chats = []
	start_minute = int(start_second / 60)
	end_minute = int(end_second / 60)
	current_rear_second = start_second

	page = video_page.open_by_id_minutes(video_id, start_minute)
	continuation = video_page.pick_out_chat_continuation(page)
	while(continuation is not None and current_rear_second < end_second-1):
		next_continuation, chats = chat_page.get_contents(continuation=continuation)

		is_empty_contents = next_continuation is None and chats is None
		if is_empty_contents and end_second >= current_rear_second:
			time.sleep(3)
			continue
		continuation = next_continuation

		current_rear_second = int(chats[-1].seconds())
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
