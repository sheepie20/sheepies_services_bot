# Sheepie's Services Discord Bot

A feature-rich Discord bot for managing support tickets, built with discord.py. This bot allows users to create, manage, and close tickets, with persistent button support and transcript logging.

## Features
- **Ticket System**: Users can open tickets via buttons and modals.
- **Admin Panel**: Admins can set up, reset, and manage ticket settings.
- **Persistent Buttons**: UI buttons remain functional after bot restarts.
- **Transcripts**: Ticket transcripts are exported and logged.
- **Role-based Permissions**: Only staff/admins can manage tickets.
- **Database-backed Settings**: Uses SQLite for server-specific configuration.

## Setup

### Prerequisites
- Python 3.8+
- Discord bot token

### Installation
1. Clone the repository or copy the files to your project directory.
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set up your Discord bot and invite it to your server.

### Configuration
- The bot uses a SQLite database (`ticket_system.db`) to store server settings.
- Run `/tickets setup [admin-role]` in your server to initialize the ticket system.

### Running the Bot
Edit `main.py` to include your bot token and register persistent views:

```python
from discord.ext import commands
from cogs.tickets import CreateButton, CloseButton, TrashButton

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# Register persistent views
bot.add_view(CreateButton(bot))
bot.add_view(CloseButton(bot))
bot.add_view(TrashButton())

# Load cogs and run
bot.load_extension('cogs.tickets')
bot.run('YOUR_BOT_TOKEN')
```

## Usage
- `/tickets setup [admin-role]`: Set up the ticket system.
- `/tickets panel`: Send the ticket creation panel.
- `/tickets reset-settings`: Reset the ticket system configuration.
- `/tickets help`: Show help and setup instructions.

### Ticket Workflow
1. User clicks the "Create Ticket" button.
2. User enters a product code or project details via modal.
3. A private ticket channel is created for the user and staff.
4. Staff can close or delete the ticket using buttons.
5. Ticket transcripts are exported and logged.

## File Structure
- `main.py` — Bot entry point
- `cogs/tickets.py` — Ticket system logic and UI
- `settings/` — Utility modules
- `ticket_system.db` — SQLite database
- `requirements.txt` — Python dependencies

## Dependencies
- `discord.py`
- `asqlite`
- `chat_exporter`
- `aiohttp`

Install all dependencies with `pip install -r requirements.txt`.

## Contributing
Pull requests and suggestions are welcome!

## License
MIT License
