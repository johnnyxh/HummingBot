import aiohttp
import asyncio
import discord
import functools
import math
import os
import time

import youtube_dl

class SongEntry:
	YOUTUBE_OPTS = {
		'format': 'webm[abr>0]/bestaudio/best',
		'prefer_ffmpeg': True,
		'verbose': True,
		'playlistrandom': True,
		'ignoreerrors': True
	}

	def __init__(self, requester, request_url):
		self.requester = requester.display_name
		self.request_url = request_url

	async def create(self, info = None):
		info = info or await self._get_video_info(self.request_url)
		self.url = info.get('url')
		self.uploader = info.get('uploader')
		self.title = info.get('title')
		self.id = info.get('id')
		self.duration = info.get('duration')
		self.start_time = info.get('start_time') or 0
		self.is_live = info.get('is_live')

	def get_embed_info(self, description):
		song_embed = discord.Embed(title=self.title, description=description, colour=0xDEADBF)
		song_embed.set_thumbnail(url='https://img.youtube.com/vi/{}/0.jpg'.format(self.id))
		return song_embed

	def to_rest_dict(self):
		return {'videoId': self.id, 'uploader': self.uploader, 'title': self.title, 'requester': self.requester, 'duration': self.duration, 'isLive': self.is_live}

	async def get_recommendations(self, requester, recommendation_amount=5,):
		recommendations = []
		async with aiohttp.ClientSession() as session:
			async with session.get('https://www.googleapis.com/youtube/v3/search?type=video&relatedToVideoId={}&part=snippet&maxResults={}&key={}'.format(self.id, recommendation_amount, os.environ['YOUTUBE_API_KEY'])) as response:
				json_body = await response.json()
				for entry in json_body['items']:
					url = 'https://www.youtube.com/watch?v={}'.format(entry['id']['videoId']) 
					new_song = SongEntry(requester, url)
					await new_song.create()
					recommendations.append(new_song)
		return recommendations

	async def _get_video_info(self, youtube_url):
		with youtube_dl.YoutubeDL(self.YOUTUBE_OPTS) as ydl:
			func = functools.partial(ydl.extract_info, youtube_url, download=False)
			return await asyncio.get_event_loop().run_in_executor(None, func)