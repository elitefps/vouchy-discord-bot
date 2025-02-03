
<h1 align="center">
  <samp>🤖 Vouchy</samp>
</h1>

> A multi-purpose **Discord Vouch Bot** that allows users to leave vouches with star ratings, product details, and descriptions. Built with **Python** and **discord.py**, this bot ensures an organized vouching system and includes a **timeout feature** for incorrect usage.

---

## 🚀 **Features**
- **Slash Command `/vouch`** – Users can submit vouches with ratings (1-5 stars), product names, descriptions, and optional images.
- **Automatic Timeout** – Users who post in the vouch channel without using `/vouch` are timed out for **60 seconds**.
---

## 🛠️ **Installation & Setup**
### 1️⃣ Clone the Repository
```sh
git clone https://github.com/elitefps/discord-vouch-bot.git
cd discord-vouch-bot
```

### 2️⃣ Install Dependencies
Make sure you have **Python 3.8+** installed, then run:
```sh
pip install -r requirements.txt
```

### 3️⃣ Configure the Bot  
Edit the `config.json` file and fill in the required values:
```json
{
    "guild_id": "YOUR_GUILD_ID",
    "bot_token": "YOUR_BOT_TOKEN",
    "presence_activity": "Made by Overtimexo",
    "watermark": "YOUR_WATERMARK_HERE",
    "watermark_imagelink": "YOUR_IMAGE_URL",
    "total_vouches": 0
}
```

### 4️⃣ Run the Bot  
Start the bot with:
```sh
python bot.py
```

---

## 🧩 **Commands**
| Command           | Description |
|------------------|-------------|
| `/vouch <stars> <product> <description> [image]` | Adds a vouch with a rating (1-5 stars), product, description, and optional image. |
| `/restore_vouches` | Restores all vouches from storage (Requires specific role). |

---

## 🔐 **Security & Moderation**
- **Timeout System**: Users who post in the wrong channel are automatically **timed out for 60 seconds**.
- **Error Handling**: Corrupted vouch entries are skipped to prevent crashes.
- **Permissions Check**: `/restore_vouches` is restricted to users with a specific role.

---

## 🌟 **Developer**
- **Elite (Overtimexo)**  
  - [![YouTube](https://img.shields.io/badge/-YouTube-0D1117?style=for-the-badge&logo=youtube&logoColor=FF0000)](https://www.youtube.com/elitefpss)
  - [![X](https://img.shields.io/badge/-X-0D1117?style=for-the-badge&logo=x&logoColor=1DA1F2)](https://www.x.com/elitewtw)
  - [![Website](https://img.shields.io/badge/-Website-0D1117?style=for-the-badge&logo=google-chrome&logoColor=white)](https://www.elite.dev)
  - [![LinkedIn](https://img.shields.io/badge/-LinkedIn-0D1117?style=for-the-badge&logo=linkedin&logoColor=0A66C2)](https://www.linkedin.com/in/elitefps)
  - [![Discord Presence](https://lanyard.cnrad.dev/api/1109047212069093386)](https://discord.com/users/1109047212069093386)


