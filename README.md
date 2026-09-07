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
- `/warn` gives a warning to a member
- `/warnings` displays a member's warnings
- Automatically kicks a member after 3 warnings
- Moderation commands are restricted to a custom Moderator role
- Permission checks for moderation commands

### Security

- Uses environment variables to securely store the Discord bot token
- `.env` is excluded from the Git repository using `.gitignore`

## Technologies

- Python
- discord.py
- python-dotenv
- Git
- GitHub

## Project Structure

```text
Discord Bot/
├── .gitignore
├── main.py
└── README.md