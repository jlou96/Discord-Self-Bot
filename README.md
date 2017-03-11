# Discord-Self-Bot
This is a small fork of DiNitride's Discord-Self-Bot. In this fork, I aim to introduce functionality that logs and downloads image files shared between you and a friend via DM. As with the original, [Discord.py](https://github.com/Rapptz/discord.py) is required.

The command syntax is `self.dl_images n fchan=False`.
`n` is the number of most recent messages that you want to log (may or may not include image files).
`fchan` is an optional parameter. By default it will ignore links that are hosted on 4chan.org or 4cdn.org, but you may choose to turn it on by setting `fchan=True`.