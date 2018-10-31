# coding=utf-8
import datetime
import dateutil.parser as timeparser

class LiveChat:
	ID = "id"
	TSU = "timestampUsec"
	TST = "timestampText"
	MSG = "message"
	ANAME = "authorName"
	APHOTO = "authorPhoto"
	AECI = "authorExternalChannelId"
	STXT = "simpleText"
	THMBS = "thumbnails"

	def __init__(self, data, video_id=""):
		d = {}
		self.video_id = video_id

		self.id = d[self.ID] = data[self.ID]
		self.timestamp_usec = d[self.TSU] = data[self.TSU]
		self.timestamp_text = d[self.TST] = data[self.TST][self.STXT]
		self.message = d[self.MSG] = ""
		self.author_name = d[self.ANAME] = None
		self.author_photo = d[self.APHOTO] = None
		self.author_external_channel_id = d[self.AECI] = ""
		if self.MSG in data and self.STXT in data[self.MSG]:
			self.message = d[self.MSG]= data[self.MSG][self.STXT]
		if self.ANAME in data and self.STXT in data[self.ANAME]:
			self.author_name = d[self.ANAME] = data[self.ANAME][self.STXT]
		if self.APHOTO in data and self.THMBS in data[self.APHOTO]:
			self.author_photo = d[self.APHOTO] = data[self.APHOTO][self.THMBS]
		if self.AECI in data:
			self.author_external_channel_id = d[self.AECI] = data[self.AECI]

		self.data = d

	def datetime(self):
		timestamp_text = self.timestamp_text
		if '-' in timestamp_text:
			timestamp_text = "00:00"
		if len(timestamp_text) <= 5:
			return datetime.datetime.strptime(timestamp_text, "%M:%S")
		else :
			return timeparser.parse(timestamp_text)

	def seconds(self):
		dt = self.datetime()
		tt = dt.timetuple()
		return tt[3] * 3600 + tt[4] * 60 + tt[5]

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
