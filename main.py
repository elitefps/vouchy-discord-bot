import discord
from discord import app_commands
import json
import os
from datetime import datetime, timedelta

CONFIG_PATH = "config.json"
VOUCHES_DIR = "vouches"

DEFAULT_CONFIG = {
    "guild_id": ",
    "bot_token": "",
    "presence_activity": "",
    "watermark": "",
    "watermark_imagelink": "",
    "total_vouches": 0
}

def load_config():
    """Load or create the configuration file."""
    if not os.path.exists(CONFIG_PATH) or os.stat(CONFIG_PATH).st_size == 0:
        with open(CONFIG_PATH, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        print("config.json has been created. Please update it with your bot token and guild ID.")
        return DEFAULT_CONFIG
    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        with open(CONFIG_PATH, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        print("Corrupted config.json detected. Replaced with default values.")
        return DEFAULT_CONFIG

def save_config(data):
    """Save the configuration to the file."""
    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f, indent=4)

def ensure_vouches_dir():
    """Ensure the vouches directory exists."""
    if not os.path.exists(VOUCHES_DIR):
        os.makedirs(VOUCHES_DIR)

def save_vouch(vouch_data):
    """Save a vouch to a JSON file."""
    ensure_vouches_dir()
    file_index = config["total_vouches"] // 200
    file_path = os.path.join(VOUCHES_DIR, f"vouches_{file_index}.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            vouches = json.load(f)
    else:
        vouches = []
    vouches.append(vouch_data)
    with open(file_path, "w") as f:
        json.dump(vouches, f, indent=4)

def load_vouches():
    """Load all vouches from the JSON files."""
    ensure_vouches_dir()
    all_vouches = []
    for file_name in os.listdir(VOUCHES_DIR):
        if file_name.endswith(".json"):
            with open(os.path.join(VOUCHES_DIR, file_name), "r") as f:
                all_vouches.extend(json.load(f))
    return all_vouches


config = load_config()


GUILD_ID = config["guild_id"]
BOT_TOKEN = config["bot_token"]
PRESENCE_ACTIVITY = config["presence_activity"]
WATERMARK = config["watermark"]
WATERMARK_IMAGE = config["watermark_imagelink"]


if not BOT_TOKEN:
    print("BOT: The bot token is not configured in config.json. Please update the file and restart the bot.")
    exit(1)


intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True


client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Store
RESTORE_ROLE_ID = 1331219355748401224 # You have to have a role that can do this
VOUCH_CHANNEL_ID = 1331219538154360853

@tree.command(
    name="vouch",
    description="Add a vouch with stars, a product, a description, and an optional image.",
    guild=discord.Object(id=int(GUILD_ID)),
)
async def vouch(
    interaction: discord.Interaction,
    stars: int,
    product: str,
    description: str,
    image: discord.Attachment = None,
):
    if stars < 1 or stars > 5:
        await interaction.response.send_message("Stars must be between 1 and 5.", ephemeral=True)
        return

    total_vouches = increment_vouch()
    vouch_id = config["total_vouches"]
    vouch_data = {
        "id": vouch_id,
        "stars": stars,
        "product": product,
        "description": description,
        "user_id": interaction.user.id,
        "user_name": interaction.user.name,
        "created_at": interaction.created_at.isoformat(),
        "image_url": image.url if image else None,
    }
    save_vouch(vouch_data)

    colors = {1: 0xFF0000, 2: 0xFF4500, 3: 0xFFA500, 4: 0xFFD700, 5: 0x00FF00}
    embed_color = colors.get(stars, 0xFFFFFF)

    stars_str = "\u2b50" * stars
    embed = discord.Embed(
        title=f"Vouch #{vouch_id} - {product}",
        description=f"\n{description}",
        color=embed_color,
    )
    embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
    embed.add_field(name="Client", value=f"{interaction.user.mention}", inline=True)
    embed.add_field(name="Product", value=product, inline=True)
    embed.add_field(name="Stars", value=stars_str, inline=True)
    embed.add_field(
        name="Vouched At",
        value=f"{discord.utils.format_dt(interaction.created_at, style='f')}",
        inline=True,
    )
    embed.set_footer(
        text=f"{WATERMARK} • {interaction.created_at.strftime('%Y-%m-%d %H:%M:%S')}",
        icon_url=WATERMARK_IMAGE,
    )

    if image:
        embed.set_thumbnail(url=image.url)

    await interaction.response.send_message(embed=embed)
    await interaction.followup.send(f"> Vouch **#{vouch_id}** for **{product}** has been added. Thank you! <:heart:1331701352480510106>")

@tree.command(
    name="restore_vouches",
    description="Restore all vouches from storage.",
    guild=discord.Object(id=int(GUILD_ID)),
)
async def restore_vouches(interaction: discord.Interaction):
    # Check if the user has the required role
    if not any(role.id == RESTORE_ROLE_ID for role in interaction.user.roles):
        await interaction.response.send_message(
            "You do not have permission to use this command.", ephemeral=True
        )
        return

    vouches = load_vouches()
    if not vouches:
        await interaction.response.send_message("No vouches found to restore.", ephemeral=True)
        return

    await interaction.response.send_message(f"Restoring {len(vouches)} vouches...", ephemeral=True)

    for vouch in vouches:
       
        if "id" not in vouch or "stars" not in vouch or "product" not in vouch or "description" not in vouch:
            print(f"Skipping corrupted vouch entry: {vouch}")  
            continue  

        stars_str = "\u2b50" * vouch["stars"]
        colors = {1: 0xFF0000, 2: 0xFF4500, 3: 0xFFA500, 4: 0xFFD700, 5: 0x00FF00}
        embed_color = colors.get(vouch["stars"], 0xFFFFFF)

        embed = discord.Embed(
            title=f"Vouch #{vouch['id']} - {vouch['product']}",
            description=f"**{stars_str}**\n{vouch['description']}",
            color=embed_color,
        )

        try:
            user = await client.fetch_user(vouch["user_id"])
            embed.set_author(name=user.name, icon_url=user.avatar.url)
        except discord.NotFound:
            embed.set_author(name=f"User ID: {vouch.get('user_id', 'Unknown')}")

        embed.add_field(name="Client", value=f"<@{vouch['user_id']}>", inline=True)
        embed.add_field(name="Product", value=vouch["product"], inline=True)
        embed.add_field(name="Stars", value=stars_str, inline=True)

        try:
            vouched_at = datetime.fromisoformat(vouch["created_at"])
            embed.add_field(name="Vouched At", value=f"{discord.utils.format_dt(vouched_at, style='f')}", inline=True)
            embed.set_footer(
                text=f"{WATERMARK} • {vouched_at.strftime('%Y-%m-%d %H:%M:%S')}",
                icon_url=WATERMARK_IMAGE,
            )
        except (KeyError, ValueError):
            embed.set_footer(text=f"{WATERMARK} • Unknown", icon_url=WATERMARK_IMAGE)

        if "image_url" in vouch and vouch["image_url"]:
            embed.set_thumbnail(url=vouch["image_url"])

        await interaction.channel.send(embed=embed)


def increment_vouch():
    config["total_vouches"] += 1
    save_config(config)
    return config["total_vouches"]

@client.event
async def on_ready():
    print(f"[ output ]Bot is starting...")
    guild = client.get_guild(int(GUILD_ID))
    if not guild:
        print(f"Error: Guild with ID {GUILD_ID} not found. Please verify the ID in config.json.")
        return

    await tree.sync(guild=guild)
    print("[ output ] Bot is ready and commands are synced!")
    await client.change_presence(activity=discord.Game(name=PRESENCE_ACTIVITY))

# Timeout for incorrect usage (Remove to disable)
@client.event
async def on_message(message):
    # Check if the message is in the specified channel and is not a command
    if message.channel.id == VOUCH_CHANNEL_ID and not message.content.startswith('/'):
        # Time out the user for 60 seconds
        timeout_duration = timedelta(seconds=60) # Set this to duration of choice.
        await message.author.timeout(timeout_duration, reason="Used the wrong channel for vouching.")
        
        # The message *
        embed = discord.Embed(
            title="⚠️ You have been timed out!",
            description=(
                "You were timed out for **60 seconds** because you did not use the `/vouch` command in the "
                f"<#{VOUCH_CHANNEL_ID}> channel.\n\n"
                "**Please use the `/vouch` command to submit your vouch.**\n"
                "This helps keep the channel organized and ensures your vouch is recorded properly."
            ),
            color=0xFF0000,  # Red color for warning
        )
        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/123456789012345678.png")  # warning emoji
        embed.set_footer(
            text=f"{WATERMARK} • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            icon_url=WATERMARK_IMAGE,
        )

        # Send the embed as a DM
        try:
            await message.author.send(embed=embed)
        except discord.Forbidden:
            # If the user has DMs disabled, send the embed in the channel instead
            embed.set_footer(
                text=f"{WATERMARK} • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Could not DM you.",
                icon_url=WATERMARK_IMAGE,
            )
            await message.channel.send(f"{message.author.mention}", embed=embed)
        
        # Delete the message that triggered the timeout
        await message.delete()

client.run(BOT_TOKEN)
