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
	print(video_details)
	seconds = int(video_details.length_seconds)
	minutes = int(seconds / 60)
	
	chat_list = []
	
	start_min = 0
	d = 10
	end_min = start_min + d
	rear_min = minutes + 1
	
	# run worker
	ftrs = []
	executor = futures.ThreadPoolExecutor()
	while(start_min < rear_min):
		ftr = executor.submit(run_making_chat_list_worker, video_id, start_min, end_min)
		ftrs.append(ftr)
		start_min = end_min
		end_min = end_min + d
		if end_min > minutes:
			end_min = rear_min

	print("Future Appended")

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
	for ftr in ftrs:
		chats = ftr.result()
		chat_list.extend(chats)

	return chat_list


def run_making_chat_list_worker(video_id=None, start_minute=None, end_minute=None):
	rtn_chats = []

	page = video_page.open_by_id_minutes(video_id, start_minute)
	continuation = video_page.pick_out_chat_continuation(page)

	while(continuation is not None):
		continuation, chats = chat_page.get_contents(continuation=continuation)
		
		if continuation is None:
			print("continuation is Invalid or This is End")
			break
		if chats is None or len(chats) == 0:
			print("chat is End")
			break

		current_rear_chat = chats[-1]
		current_minute = int(current_rear_chat.minutes())

		if current_minute == int(end_minute):
			front_chat = chats[0]
			f_min = int(front_chat.minutes())
			if f_min == end_minute:
				chats = []
			else :
				chats = remove_surplus_from_chats(chats, end_minute)
			
			continuation = None

		rtn_chats.extend(chats)

		tsp = chats[-1]
		print("end:"+str(end_minute)+", time:"+tsp.timestamp_text+", list_len:"+str(len(rtn_chats)))
		# break
		time.sleep(0.01)
	print("start:"+str(start_minute)+", Worker END")
	return rtn_chats


def remove_surplus_from_chats(chats=None, end_minute=None):
	print("end_min:"+str(end_minute)+", Remove Surplus start")
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

		ri = chats[right]
		rim = int(ri.minutes())
		le = chats[left]
		lem = int(le.minutes())
		print("end_min:"+str(end_minute)+", index:"+str(index)+", m:"+str(m)+", l:r="+str(left)+":"+str(right)+", lm:rm="+str(rim)+":"+str(lem))
		# just end_minute
		if m == end_minute and s == 0:
			print("Find Just End Min")
			break
		elif m >= end_minute and s > 0:
			right = index
		elif m < end_minute:
			left = index
		if right - left == 1:
			break
	

	# find boundary between end_minute-1 and end_minute
	for i in reversed(range(index)):
		chat = chats[index]
		m = int(chat.minutes())
		if m < end_minute:
			index = i
			break

	length = len(chats) 
	del chats[index:length]

	print("end_min:"+str(end_minute)+", Remove Surplus end")
	return chats