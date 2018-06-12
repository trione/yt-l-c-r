# coding=utf-8
import httplib2
import re

# return str type html page 
def open_by_id(video_id=None):
	if video_id is None :
		return None

	uri = 'https://www.youtube.com/watch?v=' + video_id
	h = httplib2.Http()
	
	try:
		resp, content = h.request(uri)
		return content
	
	except Exception as e:
		raise e


#return str type OF live_chat_replay's continuation
def pick_out_chat_continuation(video_id=None):
	page = open_by_id(video_id=video_id)
	if page is None: return None

	page = page.decode(encoding='utf-8')

	pattern = r'continuation=([a-zA-Z0-9_%]+)'
	p = re.compile(pattern)
	m = p.search(page)

	if m is not None:
		# print(m.group(1))
		conti = m.group(1)
		return conti
	else :
		# print("No Match")
		return None