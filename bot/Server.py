import asyncio
import argparse
import os
import threading
import tornado.ioloop
import tornado.web

from HummingBot import HummingBot


parser = argparse.ArgumentParser(description='Starts up the HummingBot + Server.')
parser.add_argument('-t', '--token', dest='token', action='store', help='Your API Bot User token', required=False)
parser.add_argument('-s', '--sounds', dest='sound_directory', metavar='DIRECTORY', action='store', help='Directory containing sound files for the bot to play', required=False, default='sounds')

args = parser.parse_known_args()[0]

client = None

def start_bot(loop):
	asyncio.set_event_loop(loop)
	global client
	client = HummingBot(args.sound_directory)
	try:
		loop.run_until_complete(client.start(args.token or os.environ['HUMMINGBOT_TOKEN']))
	except KeyboardInterrupt:
		print('Logging out...')
		loop.run_until_complete(client.logout())
	finally:
		loop.close()

loop = asyncio.get_event_loop()
bot_thread = threading.Thread(target=start_bot,args=(loop,))
bot_thread.start()

class HealthHandler(tornado.web.RequestHandler):
	def get(self):
		status = 'DOWN'
		if bot_thread.is_alive and client.is_logged_in:
			status = 'UP'
		self.write({'status': status})

def make_app():
	return tornado.web.Application([
		(r"/api/health", HealthHandler),
		(r"/(.*)", tornado.web.StaticFileHandler, {'path': './static', 'default_filename': 'index.html'}),
	])

if __name__ == "__main__":
	app = make_app()
	app.listen(os.environ['PORT'] or 8888)
	tornado.ioloop.IOLoop.current().start()