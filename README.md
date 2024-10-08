# Statera
Discord bot meant as an easy-to-use version of Katalam's AutoSlot discord bot, as well as providing some other basic functionality.

## Features
- Autoslot for Arma 3 and other slot-based mission games.
- Automatic temporary voice channels.
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

`(IN PROGRESS, JOIN SUPPORT SERVER FOR READMES) ?help`<br/>
provides the User with the purpose of different commands

`?8ball`<br/>
Magic 8ball

`?calculate`<br/>
Simple calculator

`?dice`<br/>
Rolls a die

##FAQ (We're lying no one's asked us anything):<br/>
Why is the prefix ?:<br/>
I don't know any bots that use it, a selection option will be coming in the future. Or the bot will transition entirely to slash commands, remains to be seen.

Why is the slot functionality done with slash-commands, while others not?:<br/>
Slash commands are 'encouraged' by discord, and eventually I'd like all of our commands to be slash commands. They're easier to understand if you're using a new bot.

## Invite link:
https://discord.com/api/oauth2/authorize?client_id=1044392710695551058&permissions=8&scope=bot

It needs admin to create the channels, if you just want it for the music system, do NOT grant it these permissions.
If you do grant it these permissions, keep any roles it has below any secured roles, such as admin roles. This would prevent it from assigning critical roles in the event it was compromised. Follow this advice for all bots you use.
