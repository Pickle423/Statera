# Statera
Discord bot meant as an easy-to-use version of Katalam's AutoSlot Discordbot, as well as providing some other basic functionality.

## Features
- Autoslot for Arma 3 and other slot-based mission games.
- Provides moderation commands for admins
- Supports YouTube video to audio/music streaming
- Provides miscellaneous commands for the users
- Will soon support the option to send a Reaction Roles message.
- Shiba...

## Commands
`!load <cogs name without .py from folder /cogs>`<br />
Load cog.

`!unload <cogs name without .py from folder /cogs>`<br />
Unload cog.

`!reload`<br />
Reloads all cogs

`!reload <cogs name without .py from folder /cogs>`<br />
Reloads a specific cog

`!version`<br />
Post the latest changes to the bot.

`!kill` **Debug**<br />
Kills the bot process. Useful for debugging.

`!ping`<br />
Pings the bot. Bot will pong back with latency.

`!play !P !p <YouTube URL>`<br />
Converts a YouTube video to audio then plays it in the user's voice channel.

`!skip`<br />
Skips the current video.

`!leave`<br />
Removes the bot from the current channel.

`!pause`<br />
Pauses the current playing video.

`!resume`<br />
Resumes the current playing video.

`!stop`<br />
Indefinitely stops the current video from playing. Unlike `!pause`, you cannot continue playing the current song. You can still use `!skip` and `!play` to continue with the rest of the queue.

`!queue`<br />
Display a queue of all videos to be played.

`!clear !Clear !Empty`<br />
Clear the queue of videos.

`!clean <integer>` **Admin**<br />
Removes a certain amount of messages.

`!ban @user` **Admin**<br />
Bans a user from the guild.

`!unban @user` **Admin**<br />
Unbans a user.

`!mute @user` **Admin**<br />
Mutes a user. This is persistent even if the user leaves and returns to the guild.

`!unmute @user` **Admin**<br />
Unmutes a user.

`!roleReactMessage`<br />
Set up a role selector message in the current channel

`!dog !doge !doggeg !shiba !shibainu`<br />
Posts a random Shiba Inu picture, courtesy of http://shibe.online/
Idea by Dallkori#3909

`!limit`<br/>
Limits the amount of people who can join the Voice Channel

`!lock`<br/>
Locks the current Voice Channel

`!unlock`<br/>
Unlocks the current Voice Channel

`!help`<br/>
provides the User with the purpose of different commands

`!ping`<br/>
Gives the user the Latency of the bot.

`!8ball`<br/>
Magic 8ball

`!calculate`<br/>
Simple calculator

`!dice`<br/>
Rolls a die

## Installation
To install it, your system needs the following dependencies on your project. Most of them can be installed with `pip` or the Python package manager of choice.

### Dependencies
- Python 3.8
- `nextcord`
- `PyNaCl`
- `python-dotenv`
- `youtube-search-python`
- `yt-dlp`

### Setup
Clone the project into a folder of your choice, enter it. In Unix it would be:

```shell
user@hostname:~ $ git clone https://github.com/Pickle423/Statera.git
user@hostname:~ $ cd Statera
```

### Tokens
Tokens are sourced from `.env`. Create `.env` in the project folder.

```shell
user@hostname:~ $ nano .env
```

Paste the following tokens into your .env file. Feel free to change "example" to something else. Make sure you keep the quotation marks.

```
discord_token = "example"
```

Press `CTRL+O` then `CNTRL+X` to save the file.

### Execution
Running the bot is as simple as `python3 bot.py` inside the project folder. If that fails, make sure the tokens in .env are correct. If you want the bot to run in the background, install a package like `screen` or `termux` so there can be a terminal running in the background. Refer to those packages on how to set it up.
