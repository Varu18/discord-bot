# Discord Bot

A Discord bot built with Python using discord.py.

This project is part of my programming learning process. I am using it to practice Python, object-oriented programming, asynchronous programming, working with APIs, and Git/GitHub.

## Features

### General

- Responds to messages starting with `salut` in a specific `general-chat` Discord channel
- `/salut` sends a greeting message
- `/ping` displays the bot's latency
- Sends a welcome message when a new member joins the server
- Sends a message when a member leaves the server


### Moderation

- `/clear` deletes a specified number of messages
- `/kick` removes a member from the server
- `/ban` bans a member from the server
- `/unban` unbans a member using their Discord ID
- `/mute` temporarily mutes a member
- `/unmute` removes a member's mute
- `/warn` gives a warning to a member
- `/unwarn` removes the latest warning from a member
- `/warnings` displays a member's warnings
- Automatically kicks a member after 3 warnings
- Moderation commands are restricted to a custom Moderator role
- Permission checks for moderation commands
- Moderation responses use Discord embeds
- Sends moderation logs to a private moderation channel


### Fun commands

- `/fortune` "predicts" your future
- `/rate` bot rates an user using score
- `/coinflip` clasic
- `/roast` bot roasts a server member

### Security

- Uses environment variables to securely store the Discord bot token
- `.env` is excluded from the Git repository using `.gitignore`
- Uses Discord permission checks for moderation commands


### Warning System

Warnings are stored in a local SQLite database and persist when the bot restarts.


The warning system includes:

- Adding warnings
- Viewing warnings
- Removing the latest warning
- Automatic kick after 3 warnings

### Moderation Logs

The bot records moderation actions in a dedicated Discord channel using embeds.

Logged actions include:

- Clear
- Kick
- Ban
- Unban
- Warn
- Warning removal
- Mute
- Unmute

Each log contains information such as the action, affected user, moderator, reason, and additional details when applicable. Also fun commands are included in logs.


### Technologies

- Python
- discord.py
- python-dotenv
- Git
- GitHub
- SQLite

### Project Structure

Discord Bot/
├── docs/
│   ├── privacy.md
│   └── terms.md
├── .gitignore
├── database.py
├── main.py
└── README.md

## Legal

- [Terms of Service](docs/terms.md)
- [Privacy Policy](docs/privacy.md)
