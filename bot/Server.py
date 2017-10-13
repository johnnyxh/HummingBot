import asyncio
import argparse
import os
import tornado.ioloop
import tornado.web

from tornado.platform.asyncio import AsyncIOMainLoop
from HummingBot import HummingBot

client = None
args = None

class HealthHandler(tornado.web.RequestHandler):
	def get(self):
		status = 'DOWN'
		if client.is_logged_in:
			status = 'UP'
		self.write({'status': status})

class RestartHandler(tornado.web.RequestHandler):
	async def get(self):
		global client
		global args
		loop = asyncio.get_event_loop()
		await client.logout()
		client = HummingBot('sounds')
		loop.create_task(client.start(args.token or os.environ['HUMMINGBOT_TOKEN']))


def make_server():
	return tornado.web.Application([
		(r"/api/health", HealthHandler),
		(r"/api/restart", RestartHandler),
		(r"/(.*)", tornado.web.StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'static'), 'default_filename': 'index.html'}),
	])

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Starts up the HummingBot + Server.')
	parser.add_argument('-t', '--token', dest='token', action='store', help='Your API Bot User token', required=False)
	parser.add_argument('-s', '--sounds', dest='sound_directory', metavar='DIRECTORY', action='store', help='Directory containing sound files for the bot to play', required=False, default='sounds')
	parser.add_argument('-p', '--port', dest='port', action='store', help='Port to run the webserver on', required=False, default=8888)

	args = parser.parse_known_args()[0]

	loop = asyncio.get_event_loop()

	AsyncIOMainLoop().install()

	client = HummingBot(args.sound_directory)
	loop.create_task(client.start(args.token or os.environ['HUMMINGBOT_TOKEN']))

	app = make_server()
	app.listen(args.port or os.environ['PORT'])

	asyncio.get_event_loop().run_forever()