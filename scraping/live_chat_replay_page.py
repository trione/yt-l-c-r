#coding=utf8
import httplib2
import json
import re

from scraping.item import live_chat


def open_by_continuation(continuation=None):
	if continuation is None : 
		return None

	h = httplib2.Http()
	headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
	base_url = 'https://www.youtube.com/live_chat_replay'
	uri = base_url + '?continuation=' + continuation

	response, context = h.request(uri=uri, headers=headers)
	context = context.decode(encoding='utf-8')

	return context


# find responseContext json 
def find_context_json(context=None):
	""" 
		Returns:
			dict: response context json as dict
	"""
	if context is None :
		return None

	pattern = r'({"responseContext".+});'
	p = re.compile(pattern)
	m = p.search(context)

	if m is None: return None

	json_str = m.group(1)
	
	json_data = json.loads(json_str)

	
	return json_data


# return nextContinuation, live_chat_items 
#                          liveChatTextMessageRenderers
def pick_live_chat_items_from_continuation_json(json_data=None):
	if json_data is None:
		return None, None

	if "continuationContents" not in json_data:
		return None, None


	liveChatCont = json_data["continuationContents"]["liveChatContinuation"]
	
	# liveChatContinuation > continuations
	# find next continuation in continuations json dict
	cont_dict = liveChatCont["continuations"]
	
	next_continuation = None
	for cont in cont_dict:
		if "liveChatReplayContinuationData" in cont:
			next_continuation = cont["liveChatReplayContinuationData"]["continuation"]
			break
	
	# liveChatContinuation > actions
	# find chat data in actions json dict
	actions = liveChatCont["actions"]

	chat_items = []

	check = actions[0]["replayChatItemAction"]["actions"][0]["addChatItemAction"]["item"]
	if "liveChatViewerEngagementMessageRenderer" in check:
		print("pop")
		actions.pop(0)


	# JSON :dict to LiveChat :object
	for act in actions:
		replay_item_act = act["replayChatItemAction"]["actions"][0]
		add_item_act_item = replay_item_act["addChatItemAction"]["item"]

		if "liveChatTextMessageRenderer" in add_item_act_item:
			chat_item = add_item_act_item["liveChatTextMessageRenderer"]
			chat_items.append(live_chat.LiveChat(chat_item))
	

	return next_continuation, chat_items


def get_contents(continuation=None):
	"""	https://www.youtube.com/live_chat_replay contents
		
		Args:
			continuation (str): query param string for live_chat_replay

		Returns:
			str: next continuation
			array: dict of chat_data

		chat_data has keys:
					message, authorName, authorPhoto, contextMenuEndpoint,
					id, timestampUsec, authorExternalChannelId, contextMenuAccessibility,
					timestampText
	"""

	cont = open_by_continuation(continuation=continuation)
	json_data = find_context_json(context=cont)
	nxt, chats = pick_live_chat_items_from_continuation_json(json_data=json_data)

	return nxt, chats
