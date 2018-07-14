import tornado.web
import tornado.auth
import tornado.escape

import urllib.parse as urllib_parse

from handlers.BaseHandler import BaseHandler

class AuthorizationHandler(BaseHandler, tornado.auth.OAuth2Mixin):
	_OAUTH_AUTHORIZE_URL = 'https://discordapp.com/api/oauth2/authorize'
	_OAUTH_ACCESS_TOKEN_URL = 'https://discordapp.com/api/oauth2/token'

	def initialize(self, client_id, client_secret):
		self.client_id = client_id
		self.client_secret = client_secret

	async def get(self):
		redirect_uri = "{}://{}/api/auth".format(self.request.protocol, self.request.host)

		if self.get_argument('code', False):
			state = self.get_argument('state')

			xsrf_token = self.get_cookie('_xsrf')

			if state != xsrf_token:
				return

			access = await self.get_authenticated_user(redirect_uri=redirect_uri, code=self.get_argument('code'))
			self.set_secure_cookie('DiscordId', tornado.escape.json_decode(access.body)['access_token'], httpOnly=True, expires_days=7)
			self.redirect('/')
			return
		else:
			self.set_cookie('_xsrf', self.xsrf_token)
			await self.authorize_redirect(redirect_uri=redirect_uri, client_id=self.client_id, client_secret=self.client_secret, extra_params={ 'state': self.xsrf_token }, scope=['identify', 'guilds'])
			return

	async def get_authenticated_user(self, redirect_uri, code):
		http = self.get_auth_http_client()
		body = urllib_parse.urlencode({
        	'redirect_uri': redirect_uri,
			'code': code,
			'client_id': self.client_id,
			'client_secret': self.client_secret,
			'grant_type': 'authorization_code',
		})

		return await http.fetch(self._OAUTH_ACCESS_TOKEN_URL,
			method='POST', headers={'Content-Type': 'application/x-www-form-urlencoded'}, body=body)