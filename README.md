## HLDS Notifier
Simple TG Bot written on Python with usage of Aiogram and asyncio's UDP server.

### Features
* Event log receiving (obvious)
* Posting events filtered with templates to channel
* Ability to filter events between public/closed and chat channel

### Available Commands
1. /start - shows greeting message
2. /info - shows version, url to this repo, game and server ip:port
3. /channels - shows available channels. Private one is available only for users specified in `Configurations.admin_ids`

### Setting up
1. Create and acquire bot token from `@botfather`
2. Create 1 up to 3 channels (for public/private posts and one for chat events), acquire it/their id's in BotAPI format
3. Clone this repo: `git clone https://github.com/crossfireTeam/HLDS-Notifier.git` and `cd HLDS-Notifier`
4. Install dependencies: `pip install -r requirements.txt`
5. Set up `configurations.py`
6. You're ready to rock!

### TODO:
* Improve `EventParser`
* Parse whole log data (including timestamp and etc)
* Add banners for some events
* Maybe something more

### Note
Support is only for HL, any other game you should implement by yourself