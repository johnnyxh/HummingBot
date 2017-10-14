import asyncio
import argparse
import os
import tornado.ioloop
import tornado.web

from tornado.platform.asyncio import AsyncIOMainLoop
from HummingBot import HummingBot

args = None

class HealthHandler(tornado.web.RequestHandler):
	def initialize(self, bot):
		self.bot = bot

	def get(self):
		status = 'DOWN'
		servers = []
		if self.bot.is_logged_in and not self.bot.is_closed:
			status = self.bot.health
			for server in self.bot.servers:
				servers.append(server.name)
		self.write({'status': status, 'servers': servers, 'uptime': self.bot.uptime()})

class RestartHandler(tornado.web.RequestHandler):
	def initialize(self, bot):
		self.bot = bot

	async def get(self):
		try:
			loop = asyncio.get_event_loop()
			await self.bot.logout()
			self.bot.__init__(args.sound_directory)
			loop.create_task(bot.start(args.token or os.environ['HUMMINGBOT_TOKEN']))
			await bot.wait_until_ready()
			self.write({'status': 'success'})
		except Exception as err:
			print(err)
			self.write({'status': 'failure'})

def make_server(bot):
	return tornado.web.Application([
		(r"/api/health", HealthHandler, dict(bot=bot)),
		(r"/api/restart", RestartHandler, dict(bot=bot)),
		(r"/(.*)", tornado.web.StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'static'), 'default_filename': 'index.html'}),
	])

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Starts up the HummingBot + Server.')
	parser.add_argument('-t', '--token', dest='token', action='store', help='Your API Bot User token', required=False)
	parser.add_argument('-s', '--sounds', dest='sound_directory', metavar='DIRECTORY', action='store', help='Directory containing sound files for the bot to play', required=False, default='sounds')
	parser.add_argument('-p', '--port', dest='port', action='store', help='Port to run the webserver on', required=False)

	args = parser.parse_known_args()[0]

	loop = asyncio.get_event_loop()

	bot = HummingBot(args.sound_directory)
	loop.create_task(bot.start(args.token or os.environ['HUMMINGBOT_TOKEN']))

	AsyncIOMainLoop().install()

	app = make_server(bot)
	app.listen(args.port or os.environ['PORT'])

	loop.run_forever()