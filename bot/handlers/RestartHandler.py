import asyncio
import json
import os
import tornado.web

from tornado import httpclient

from handlers.BaseHandler import BaseHandler

class RestartHandler(BaseHandler):

	def initialize(self, bot, start_args):
		self.bot = bot
		self.start_args = start_args

	async def post(self):
		try:
			body = tornado.escape.json_decode(self.request.body)

			if await self.isUserInServer(body['server']):
				loop = asyncio.get_event_loop()
				await self.bot.logout()
				self.bot.__init__(connection_uri=self.start_args.mongodb_uri or os.environ['MONGODB_URI'], db=self.start_args.mongodb_db or os.environ['MONGODB_DB'])
				loop.create_task(self.bot.start(self.start_args.token or os.environ['HUMMINGBOT_TOKEN']))
				await self.bot.wait_until_ready()
				self.write({'status': 'success'})
				return
			self.set_status(403)
			self.write({'message': 'User does not have permission to restart the bot in this channel'})
		except json.decoder.JSONDecodeError as err:
			self.set_status(400)
			self.write({'message': 'Unable to decode POST body'})
		except KeyError as err:
			self.set_status(400)
			self.write({'message': 'Missing POST attribute: {}'.format(str(err))})
		except Exception as err:
			print(err)
			self.set_status(500)
			self.write({'message': 'Internal Server Error'})

	async def isUserInServer(self, restart_server):
		http_client = httpclient.AsyncHTTPClient()
		response = await http_client.fetch('https://discordapp.com/api/users/@me/guilds', headers={'Authorization': 'Bearer {}'.format(self.get_current_user().decode('utf-8'))}, method='GET')

		server_list = tornado.escape.json_decode(response.body)

		for server in server_list:
			if server['name'] == restart_server:
				return True
		return False
