# coding=utf-8
import datetime
import dateutil.parser as timeparser

class LiveChat:

	def __init__(self, data, video_id=""):
		self.data = data
		self.video_id = video_id
		self.message = data["message"]["simpleText"]
		self.author_name = data["authorName"]["simpleText"]
		self.author_photo = data["authorPhoto"]["thumbnails"]
		self.id = data["id"]
		self.timestamp_usec = data["timestampUsec"]
		self.author_external_channel_id = data["authorExternalChannelId"]
		self.timestamp_text = data["timestampText"]["simpleText"]


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
