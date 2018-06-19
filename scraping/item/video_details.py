# coding=utf-8

class VideoDetails:

	def __init__(self, details_json, microformat_json):
		try:
			d = details_json
			self.video_id = d["videoId"]
			self.title = d["title"]
			self.length_seconds = d["lengthSeconds"]
			self.channel_id = d["channelId"]
			self.description = d["shortDescription"]
			self.thumbnail = d["thumbnail"]
			self.view_count = d["viewCount"]
			self.author = d["author"]
			self.publish_date = ""
			self.category = ""

			if microformat_json is not None:
				m = microformat_json["microformatDataRenderer"]
				self.publish_date = m["publishDate"]
				self.category = m["category"]

		except Exception as e:
			raise e
