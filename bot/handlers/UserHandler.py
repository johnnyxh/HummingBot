import tornado.web

from tornado import httpclient

from handlers.BaseHandler import BaseHandler

class UserHandler(BaseHandler):
	async def get(self):
		user = self.get_current_user()
		if user is None:
			self.set_status(401)
			self.write({ 'message': 'User is not logged in' })
			return
		http_client = httpclient.AsyncHTTPClient()
		response = await http_client.fetch('https://discordapp.com/api/users/@me', headers={'Authorization': 'Bearer {}'.format(self.get_current_user().decode('utf-8'))}, method='GET')

		user_response = tornado.escape.json_decode(response.body)
		self.write({ 'username': user_response['username'], 'discriminator': user_response['discriminator'], 'avatarUrl': 'https://discordapp.com/api/users/{}/avatars/{}.jpg'.format(user_response['id'], user_response['avatar']) })
