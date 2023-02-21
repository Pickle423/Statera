# Statera
Discord bot meant as an easy-to-use version of Katalam's AutoSlot discord bot, as well as providing some other basic functionality.

## Features
- Autoslot for Arma 3 and other slot-based mission games.
- Provides moderation commands for admins
- Supports YouTube video to audio/music streaming
- Provides miscellaneous commands for users
- Will soon support the option to send a Reaction Roles message (hopefully).
- Shiba...

## Commands
`?version`<br />
Post the latest changes to the bot.

`?ping`<br />
Pings the bot. Bot will pong back with latency.

`?play ?P ?p <YouTube URL>`<br />
Converts a YouTube video to audio then plays it in the user's voice channel.

`?skip`<br />
Skips the current video.

`?leave`<br />
Removes the bot from the current channel.

`?pause`<br />
Pauses the current playing video.

`?resume`<br />
Resumes the current playing video.

`?stop`<br />
Indefinitely stops the current video from playing. Unlike `?pause`, you cannot continue playing the current song. You can still use `?skip` and `?play` to continue with the rest of the queue.

`?queue`<br />
Display a queue of all videos to be played.

`?clear ?Clear ?Empty`<br />
Clear the queue of videos.

`/clean <integer>` **Admin**<br />
Removes a certain amount of messages.

`(NOT RELEASED) ?roleReactMessage`<br />
Set up a role selector message in the current channel

`/shibe or ?dog ?doge?!doggeg ?shiba ?shibainu`<br />
Posts a random Shiba Inu picture, courtesy of http://shibe.online/

`(NOT RELEASED) ?help`<br/>
provides the User with the purpose of different commands

`?8ball`<br/>
Magic 8ball

`?calculate`<br/>
Simple calculator

`?dice`<br/>
Rolls a die

##FAQ (We're lying no one's asked us anything):
Why is the slot functionality done with slash-commands, I hate slash-commands.:

I hate them too, but I felt like it.

Your code sucks:
Yeah. We're both novice python ""developers.""

I hate this Fletch guy:
So do I.

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
