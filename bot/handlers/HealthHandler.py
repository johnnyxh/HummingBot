import tornado.web

from handlers.BaseHandler import BaseHandler

class HealthHandler(BaseHandler):
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