import aiohttp
import async_timeout
import os
from io import BytesIO
from PIL import Image as PImage

class Image:

	BRAZZERS_LOGO = 'blogo.png'
	DEFAULT_IMG_COMPRESSION = 'PNG'

	def __init__(self, bot):
		self.bot = bot
		self.assets_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'image_assets')

	def get_commands(self):
		commands = [
			{
				'name': 'brazzers',
				'description': 'The World\'s Best HD Porn Memes',
				'use': '?image brazzers [image_url]'
			}
		]
		return commands

	async def brazzers(self, message):
		image_url = message.content.split()[2]

		async with aiohttp.ClientSession() as session:
				with async_timeout.timeout(10):
					async with session.get(image_url) as response:
						try:
							raw_image = await response.read()
							byte_image_init = BytesIO(raw_image)
							image = PImage.open(byte_image_init)
							logo = PImage.open(os.path.join(self.assets_directory, self.BRAZZERS_LOGO))
							image_copy = image.copy()

							logo.thumbnail((image_copy.width/2, logo.height))
							position = ((image_copy.width - logo.width), (image_copy.height - logo.height))
							image_copy.paste(logo, position, logo)

							byte_image_final = BytesIO()
							image_copy.save(byte_image_final, self.DEFAULT_IMG_COMPRESSION)
							byte_image_final.seek(0)
							await self.bot.send_file(message.channel, byte_image_final, filename='img.png')
						except OSError as err:
							await self.bot.add_reaction(message, '❌')
							await self.bot.send_message(message.channel, 'Cannot identify image file')
						except Exception as err:
							raise(err)
						finally:
							if 'byte_image_init' in locals(): byte_image_init.close()
							if 'image'  in locals(): image.close()
							if 'logo'  in locals(): logo.close()
							if 'image_copy'  in locals(): image_copy.close()
							if 'byte_image_final'  in locals(): byte_image_final.close()