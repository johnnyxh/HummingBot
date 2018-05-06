import motor.motor_asyncio

class Datastore:
	def __init__(self, connection_uri = 'mongodb://localhost:27017', db = 'hummingbot'):
		self.client = motor.motor_asyncio.AsyncIOMotorClient(connection_uri)
		self.db = self.client[db]

	async def insert_song(self, song, label = None):
		song_query = {'videoId': song.id}
		update_operations = {'$inc': { 'play_count': 1 } }

		song_entry = await self.db.songs.find_one_and_update(song_query, update_operations)
		
		if song_entry is None:
			song_entry = song.to_rest_dict()
			song_entry['play_count'] = 1
			song_entry['skip_count'] = 0
			song_entry['song_label'] = label
			await self.db.songs.insert_one(song_entry)

	async def update_song_skipped(self, song):
		song_query = {'videoId': song.id}
		update_operations = {'$inc': { 'skip_count': 1 } }

		song_entry = await self.db.songs.find_one_and_update(song_query, update_operations)
