# HummingBot

General purpose discord bot written in Python 3.5.2, using [discord.py](https://github.com/Rapptz/discord.py). Currently with basic playlist and sound file playback functionality. Runs a [tornado server](http://www.tornadoweb.org/en/stable/) alongside the bot to serve a react based web application bootstrapped using [create-react-app](https://github.com/facebookincubator/create-react-app).

## Usage

1. Install [Python](https://www.python.org/)
2. Install [Node](https://nodejs.org/en/)
3. Run `pip install -r requirements.txt` on the root directory of this project
4. Inside the `client` directory
	- Run `npm install`
	- Run `npm run build`
	- `mv` the contents of the `build` directory to a `static` directory within the `bot` direcotry (Will be fixing this setup)
5. Get a bot token from the [Discord App Portal](https://discordapp.com/developers/applications/me)
6. Run the Bot+Server by running `python Server.py -t [HUMMINGBOT_TOKEN] -p [PORT] -m [MONGODB_URI] -d [MONGODB_DB]`
	- These can also be set through environment variables
		- HUMMINGBOT_TOKEN = your discord bot token
		- PORT = the port the web server hosting the client side will run on
		- YOUTUBE_API_KEY = youtube api key used for grabbing
		- MONGODB_URI = mongo uri to connect to your database
		- MONGODB_DB = mongo database that will contain hummingbot collections

## Tests

### Bot
TODO: Currently running tests using `nosetests` and written using standard 

### Client
TODO:
