<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Discord Vouch Bot</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 20px auto;
            padding: 20px;
        }
        h1, h2 {
            color: #333;
        }
        code {
            background: #f4f4f4;
            padding: 3px 6px;
            border-radius: 5px;
        }
        pre {
            background: #f4f4f4;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
        }
    </style>
</head>
<body>

    <h1>Discord Vouch Bot</h1>

    <h2>Description</h2>
    <p>This is a Discord bot that manages a vouch system, allowing users to submit vouches for products and services. The bot logs vouches, ensures correct usage, and maintains order in designated channels.</p>

    <h2>Features</h2>
    <ul>
        <li><code>/vouch</code> command: Users can submit vouches with a star rating, product name, description, and optional image.</li>
        <li><code>/restore_vouches</code> command: Admins with the required role can restore previous vouches.</li>
        <li>Automatic vouch logging in structured JSON files.</li>
        <li>Restricts vouching to a specific channel.</li>
        <li>Automatically times out users who do not use the <code>/vouch</code> command.</li>
        <li>Sends a DM explaining the timeout reason.</li>
        <li>Dynamically generated embed messages for vouches with colors based on star rating.</li>
    </ul>

    <h2>Setup Instructions</h2>

    <h3>Prerequisites</h3>
    <ul>
        <li>Python 3.8+</li>
        <li><code>discord.py</code> library (install with <code>pip install discord</code>)</li>
    </ul>

    <h3>Configuration</h3>
    <p>Create a <code>config.json</code> file in the root directory with the following format:</p>
    
    <pre>
{
    "guild_id": "YOUR_GUILD_ID",
    "bot_token": "YOUR_BOT_TOKEN",
    "presence_activity": "Made by ProtiDEV",
    "watermark": "ProtiDEV",
    "watermark_imagelink": "https://cdn.discordapp.com/attachments/1190998549744341117/1320876112057995264/logo.jpeg",
    "total_vouches": 0
}
    </pre>
    
    <p>Replace <code>YOUR_GUILD_ID</code> with your Discord server ID.</p>
    <p>Replace <code>YOUR_BOT_TOKEN</code> with your bot’s token.</p>
    <p>Save the file.</p>

    <h3>Running the Bot</h3>
    <p>Run the bot using:</p>
    <pre><code>python bot.py</code></pre>

    <h2>Commands</h2>

    <h3>/vouch</h3>
    <p><strong>Description:</strong> Submit a vouch.</p>
    <p><strong>Usage:</strong> <code>/vouch &lt;stars&gt; &lt;product&gt; &lt;description&gt; [image]</code></p>
    <ul>
        <li><code>stars</code>: A rating from 1 to 5.</li>
        <li><code>product</code>: Name of the product/service.</li>
        <li><code>description</code>: A short review.</li>
        <li><code>image</code>: (Optional) An attached image.</li>
    </ul>

    <h3>/restore_vouches</h3>
    <p><strong>Description:</strong> Restore all stored vouches.</p>
    <p><strong>Usage:</strong> <code>/restore_vouches</code></p>
    <p>Only available to users with the restore role.</p>

    <h2>Channel Restriction & Auto Timeout</h2>
    <p>The bot ensures that vouches are only submitted in the designated channel.</p>
    <p>Messages in the wrong channel result in a <strong>60-second timeout</strong> and an explanatory DM.</p>

    <h2>Logging System</h2>
    <p>Vouches are stored in the <code>vouches/</code> directory as JSON files, with each file containing up to 200 vouches.</p>

    <h2>License</h2>
    <p>This bot is created by <strong>ProtiDEV</strong>. Feel free to modify and use it for your Discord server.</p>

</body>
</html>
