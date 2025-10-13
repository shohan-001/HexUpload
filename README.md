<div align="center">

# 🚀 HexUploads 𝐃𝐞𝐩𝐥𝐨𝐲𝐦𝐞𝐧𝐭 𝐆𝐮𝐢𝐝𝐞

<p>
    <a href="https://github.com/shohan-001/HexUpload">
        <kbd>
            <img src="https://files.catbox.moe/2jpph5.png" width="550" alt="KPSML-X Logo">
        </kbd>
    </a>
</p>

[![Deploy on Heroku](https://www.herokucdn.com/deploy/button.svg)](https://dashboard.heroku.com/new?template=https://github.com/shohan-001/HexUpload)

### 🎯 Choose Your Deployment Method

<table>
<tr>
<td align="center"><b>🌐 Heroku</b><br/>Easy & Fast</td>
<td align="center"><b>🖥️ VPS</b><br/>Full Control</td>
<td align="center"><b>📓 Google Colab</b><br/>Free & Quick</td>
</tr>
</table>

<a href="https://colab.research.google.com/drive/1ntoqoj3jDq2FtU2-joizh0DO64uoec9q">
    <img src="https://graph.org/file/504ba776ef0724a4ae85b.png" width="20" alt="Colab">
    <b>Google Colab Deploy Link</b>
</a>

</div>

---

## 📑 Table of Contents

- [🚀 Quick Deploy (Heroku Button)](#-quick-deploy-heroku-button)
- [💻 VPS Deployment (Docker)](#-vps-deployment-docker)
- [⚙️ Heroku CLI Deployment](#️-heroku-cli-deployment)
- [📋 Configuration Variables](#-configuration-variables)
- [🔧 Branch Specifications](#-branch-specifications)

---

## 🚀 Quick Deploy (Heroku Button)

The fastest way to get started! Simply click the button below and fill in the required variables.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://dashboard.heroku.com/new?template=https://github.com/shohan-001/HexUpload)

> **Note:** After deployment, set your `BASE_URL` in config via bot settings `/bs`

---

## 💻 VPS Deployment (Docker)

Deploy KPSML-X on your own VPS with full control using Docker. Perfect for those who want maximum customization and reliability.

### 📋 Prerequisites

- A VPS running Ubuntu/Debian (recommended)
- SSH access to your VPS
- Basic command line knowledge

### 🎯 4-Step Deployment Process

<details open>
<summary><h3>Step 1: VPS Setup & Install Dependencies</h3></summary>

**SSH into your VPS** and run the following commands:

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Git and essential tools
sudo apt install git curl wget -y

# Install Docker using the official convenience script
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add your user to the docker group (avoid using sudo with docker)
sudo usermod -aG docker $USER

# Apply group changes (or logout and login again)
newgrp docker

# Verify Docker installation
docker --version
```

> ⚠️ **Important:** You may need to logout and login again for the docker group changes to take effect.

</details>

<details open>
<summary><h3>Step 2: Clone Repository & Setup Configuration</h3></summary>

**Clone the KPSML-X repository:**

```bash
# Clone the main repository
git clone https://github.com/Tamilupdates/KPSML-X
cd KPSML-X

# Or clone your forked repository
# git clone https://github.com/YOUR_USERNAME/KPSML-X
# cd KPSML-X
```

**Create and configure your `config.env` file:**

```bash
# Copy the sample configuration
cp config_sample.env config.env

# Edit with nano (or vim/vi)
nano config.env
```

**Minimum Required Configuration:**

```env
# ====== MANDATORY VARIABLES ======
BOT_TOKEN = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
OWNER_ID = "123456789"
TELEGRAM_API = "1234567"
TELEGRAM_HASH = "abcdef1234567890abcdef1234567890"
TORRENT_TIMEOUT = "0"
DATABASE_URL = "mongodb+srv://username:password@cluster.mongodb.net/dbname"

# ====== OPTIONAL BUT RECOMMENDED ======
UPSTREAM_REPO = "https://github.com/shohan-001/HexUpload"
UPSTREAM_BRANCH = "hk_kpsmlx"
SET_COMMANDS = "True"
```

> 🔥 **Critical:** Delete or comment out the line `_____REMOVE_THIS_LINE_____=True` to prevent the update script from exiting!

**Save and exit:**
- Press `CTRL + X`
- Press `Y` to confirm
- Press `Enter` to save

</details>

<details open>
<summary><h3>Step 3: Build Docker Image</h3></summary>

**Build your bot's Docker image:**

```bash
# Build the image (this may take a few minutes)
docker build -t kpsmlx-bot .

# Verify the image was created
docker images | grep kpsmlx-bot
```

</details>

<details open>
<summary><h3>Step 4: Run the Bot Container</h3></summary>

**Start your bot in a Docker container:**

```bash
# Run the bot in detached mode with auto-restart
docker run -d \
  --name kpsmlx_bot \
  --restart=always \
  --env-file config.env \
  kpsmlx-bot
```

**Verify deployment and check logs:**

```bash
# View real-time logs
docker logs -f kpsmlx_bot

# Check if container is running
docker ps | grep kpsmlx_bot

# Exit logs view with CTRL + C
```

**Look for success messages like:**
```
✅ Successfully updated with latest commits !!
🤖 Bot started successfully!
```

</details>

### 🔧 Useful Docker Commands

```bash
# Stop the bot
docker stop kpsmlx_bot

# Start the bot
docker start kpsmlx_bot

# Restart the bot
docker restart kpsmlx_bot

# Remove the container
docker rm -f kpsmlx_bot

# View logs (last 100 lines)
docker logs --tail 100 kpsmlx_bot

# Execute commands inside the container
docker exec -it kpsmlx_bot bash

# Update and redeploy
git pull
docker build -t kpsmlx-bot .
docker rm -f kpsmlx_bot
docker run -d --name kpsmlx_bot --restart=always --env-file config.env kpsmlx-bot
```

### 🛡️ Security Best Practices for VPS

1. **Firewall Configuration:**
   ```bash
   sudo ufw allow ssh
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw enable
   ```

2. **Keep your system updated:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

3. **Never share your `config.env` file** - it contains sensitive credentials!

4. **Use SSH keys** instead of passwords for VPS access

---

## ⚙️ Heroku CLI Deployment

<details>
<summary><h3>Click to expand Heroku CLI guide</h3></summary>

### Step 1: Clone Repository

```bash
# Install prerequisites
apt-get install git pip curl -y

# Clone the repository
git clone https://github.com/Tamilupdates/KPSML-X
cd KPSML-X 
```

### Step 2: Install Heroku CLI

**For Linux/Ubuntu/Debian:**
```bash
curl https://cli-assets.heroku.com/install-ubuntu.sh | sh
```

**For other systems (requires sudo):**
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

**Via npm (not recommended):**
```bash
npm install -g heroku
```

📚 **Official Installation Guide:** [Heroku CLI Docs](https://devcenter.heroku.com/articles/heroku-cli#install-the-heroku-cli)

### Step 3: Login to Heroku

**With browser:**
```bash
heroku login
```

**Without browser (headless):**
```bash
heroku login -i
```

- **Email:** Your Heroku account email
- **Password:** Your Heroku API Key from [Account Settings](https://dashboard.heroku.com/account)

### Step 4: Create Heroku App

```bash
# Create app with container stack
heroku create --region us --stack container APP_NAME
```

**Options:**
- `--region us` → US servers
- `--region eu` → European servers
- `APP_NAME` → Your unique app name (optional)
- `--stack container` → Required for Docker deployment

> 📝 **Important:** Copy the `BASE_URL` shown after app creation (e.g., `https://app-name-12345.herokuapp.com/`) and add it to your `config.env`

### Step 5: Configure Environment

**Edit config.env:**
```bash
nano config.env
```

**Minimum configuration:**
```env
BOT_TOKEN = ""
TELEGRAM_API = ""
TELEGRAM_HASH = ""
OWNER_ID = ""
DATABASE_URL = ""
BASE_URL = ""
SET_COMMANDS = "True"
UPSTREAM_REPO = "https://github.com/shohan-001/HexUpload"
UPSTREAM_BRANCH = "hk_kpsmlx"
```

**Save:** `CTRL + X` → `Y` → `Enter`

### Step 6: Setup Git Remote

```bash
git add . -f
git commit -m "Initial Heroku Setup"
heroku git:remote -a APP_NAME
```

### Step 7: Deploy to Heroku

```bash
# Force push to deploy
git push heroku main -f
```

### Step 8: Monitor Logs

```bash
# View logs
heroku logs -a APP_NAME

# Live stream logs (CTRL + C to exit)
heroku logs -a APP_NAME -t
```

### 📚 Additional Resources

- **All Heroku CLI Commands:** [Official Documentation](https://devcenter.heroku.com/articles/heroku-cli-commands)
- **Heroku Config Management:** Use `heroku config:set VAR=value -a APP_NAME`

</details>

---

## 📋 Configuration Variables

<details>
<summary><h3>Click to view all variables</h3></summary>

### 🔴 Mandatory Variables

| Variable | Description | Type |
|----------|-------------|------|
| `BOT_TOKEN` | Telegram Bot Token from [@BotFather](https://t.me/BotFather) | String |
| `OWNER_ID` | Your Telegram User ID (not username) | Integer |
| `TELEGRAM_API` | API ID from [my.telegram.org](https://my.telegram.org) | Integer |
| `TELEGRAM_HASH` | API Hash from [my.telegram.org](https://my.telegram.org) | String |
| `TORRENT_TIMEOUT` | Timeout for dead torrents (set to `0` if not using) | Integer |
| `DATABASE_URL` | MongoDB connection URL for storing data | String |

### 🟡 Important Variables

| Variable | Description | Type | Default |
|----------|-------------|------|---------|
| `UPSTREAM_REPO` | GitHub repository URL for updates | String | - |
| `UPSTREAM_BRANCH` | Branch for updates | String | `hk_kpsmlx` |
| `BASE_URL` | Your deployment URL (for Heroku) | String | - |
| `SET_COMMANDS` | Auto-set bot commands | Boolean | `True` |

### 📝 Notes

- For **private repositories**, use format: `https://username:token@github.com/username/repo`
- **BASE_URL** format: `https://app-name-12345.herokuapp.com/` (must end with `/`)
- Any Docker changes require rebuild to take effect
- All configuration can be updated via bot settings command `/bs`

</details>

---

## 🔧 Branch Specifications

- **Upload Branch:** `main` - All files must be uploaded here
- **Upstream Branch:** `hk_kpsmlx` - Set this as your upstream for updates
- **Configuration:** Ensure `UPSTREAM_BRANCH = "hk_kpsmlx"` in your config

---

## 🆘 Troubleshooting

<details>
<summary><h3>Common Issues & Solutions</h3></summary>

### Bot won't start

**Solution:** Check logs for errors
```bash
# VPS
docker logs kpsmlx_bot

# Heroku
heroku logs -a APP_NAME -t
```

### Update script exits immediately

**Solution:** Remove the line `_____REMOVE_THIS_LINE_____=True` from `config.env`

### MongoDB connection failed

**Solution:** 
- Verify your `DATABASE_URL` is correct
- Ensure your MongoDB cluster allows connections from your IP
- Check MongoDB Atlas whitelist settings

### Docker build fails

**Solution:**
```bash
# Clear Docker cache and rebuild
docker system prune -a
docker build --no-cache -t kpsmlx-bot .
```

### Bot crashes after startup

**Solution:** 
- Ensure `TORRENT_TIMEOUT` is set (even if just `0`)
- Verify all mandatory variables are filled
- Check if all required private files are present

</details>

---

## 🤝 Support & Community

<div align="center">

**Need help?** Join our community!

[📢 Updates Channel](https://t.me/Tamilupdates) • [💬 Support Group](https://t.me/TamilupdatesGroup)

**Found a bug?** [Report it here](]https://github.com/shohan-001/HexUpload/issues)

---

### ⭐ Star this repo if you found it helpful!

**Made with ❤️ by the HexUploads Team**

</div>
