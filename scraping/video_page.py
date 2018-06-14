# coding=utf-8
import httplib2
import re
import json

from scraping.item import video_details

page = None

def open_by_id(video_id=None):
	if video_id is None : return None

	h = httplib2.Http()
	uri = 'https://www.youtube.com/watch?v=' + video_id
	headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}

	global page
	resp, page = h.request(uri=uri, headers=headers)
	page = page.decode(encoding='utf-8')

	return page

#return str type OF live_chat_replay's continuation
def pick_out_chat_continuation():
	global page
	if page is None: return None

	pattern = r'"continuation":"(op2w0w[a-zA-Z0-9_%]+)"'
	p = re.compile(pattern)
	m = p.search(page)

	if m is None: return None
	
	conti = m.group(1)
	return conti


def get_video_details():
	global page
	if page is None: return None

	pattern = r'({"responseContext":.+})\);'
	p = re.compile(pattern)
	m = p.search(page)

	if m is None: return None

	json_str = m.group(1)
	json_data = json.loads(json_str)

	if "videoDetails" in json_data:
		details_json = json_data["videoDetails"]
		microformat_json = None
		if "microformat" in json_data: 
			microformat_json = json_data["microformat"]
		vd = video_details.VideoDetails(details_json, microformat_json)
		return vd

	else:
		return None
