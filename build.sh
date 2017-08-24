cd ./client
npm install
npm run build
mv ./build ../bot/static
cd ../bot
gunicorn --workers 1 HummingBot:app