# coding=utf-8
import datetime
import dateutil.parser as timeparser

class LiveChat:

	def __init__(self, data, video_id=""):
		self.data = data
		self.video_id = video_id

		self.id = data["id"]
		self.timestamp_usec = data["timestampUsec"]
		self.timestamp_text = data["timestampText"]["simpleText"]

		self.message = ""
		self.author_name = None
		self.author_photo = None
		self.author_external_channel_id = ""
		if "message" in data:
			self.message = data["message"]["simpleText"]
		if "authorName" in data:
			self.author_name = data["authorName"]["simpleText"]
		if "authorPhoto" in data:
			self.author_photo = data["authorPhoto"]["thumbnails"]
		if "authorExternalChannelId" in data:
			self.author_external_channel_id = data["authorExternalChannelId"]
			

	def datetime(self):
		timestamp_text = self.timestamp_text
		if len(timestamp_text) <= 5:
			return datetime.datetime.strptime(timestamp_text, "%M:%S")
		else :
			return timeparser.parse(timestamp_text)


	def minutes(self):
		dt = self.datetime()
		tt = dt.timetuple()
		return tt[3] * 60 + tt[4] + tt[5] / 60




class SuperLiveChat(LiveChat):

	def __init__(self, data, video_id=""):
		chat_data = data["showItemEndpoint"]["showLiveChatItemEndpoint"]["renderer"].pop("liveChatPaidMessageRenderer")
		super().__init__(chat_data, video_id)
		data.update(chat_data)
		self.data = data
		self.amount_text = data["amount"]["simpleText"]
		self.duration_sec = data["durationSec"]
