import asyncio
import argparse
import os
import tornado.ioloop
import tornado.web

from tornado.platform.asyncio import AsyncIOMainLoop
from HummingBot import HummingBot

from handlers.AuthorizationHandler import AuthorizationHandler
from handlers.UserHandler import UserHandler
from handlers.HealthHandler import HealthHandler
from handlers.RestartHandler import RestartHandler
from handlers.PlaylistHandler import PlaylistHandler

args = None

def make_server(bot):
	return tornado.web.Application([
		(r"/api/health", HealthHandler, dict(bot=bot)),
		(r"/api/playlist", PlaylistHandler, dict(bot=bot)),
		(r"/api/restart", RestartHandler, dict(bot=bot, start_args=args)),
		(r"/api/user", UserHandler),
		(r"/api/auth", AuthorizationHandler, dict(client_id=args.client_id or os.environ['CLIENT_ID'], client_secret=args.client_secret or os.environ['CLIENT_SECRET'])),
		(r"/(.*)", tornado.web.StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'static'), 'default_filename': 'index.html'}),
	], compress_response=True, cookie_secret = args.cookie_secret or os.environ['COOKIE_SECRET'], xsrf_cookies = True, login_url = '/api/authorize')

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Starts up the HummingBot + Server.')
	parser.add_argument('-t', '--token', dest='token', action='store', help='Your API Bot User token', required=False)
	parser.add_argument('-p', '--port', dest='port', action='store', help='Port to run the webserver on', required=False)
	parser.add_argument('--mongodb-uri', dest='mongodb_uri', action='store', help='Mongodb connection uri to store user submitted songs', required=False)
	parser.add_argument('--mongodb-db', dest='mongodb_db', action='store', help='Mongodb database that will contain hummingbot collections', required=False)
	parser.add_argument('--cookie-secret', dest='cookie_secret', action='store', help='Cookie secret used to sign secure cookies on the client', required=False)
	parser.add_argument('--client-id', dest='client_id', action='store', help='Discord bot client id', required=False)
	parser.add_argument('--client-secret', dest='client_secret', action='store', help='Discord bot client secret', required=False)

	args = parser.parse_known_args()[0]

	loop = asyncio.get_event_loop()

	bot = HummingBot(connection_uri=args.mongodb_uri or os.environ['MONGODB_URI'], db=args.mongodb_db or os.environ['MONGODB_DB'])
	loop.create_task(bot.start(args.token or os.environ['HUMMINGBOT_TOKEN']))

	AsyncIOMainLoop().install()

	app = make_server(bot)
	app.listen(args.port or os.environ['PORT'])

	loop.run_forever()