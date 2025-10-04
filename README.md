<div align="center">🚀 KPSML-X Bot: Feature-Rich Mirror Leech Telegram Bot 🚀<p><a href="https://github.com/Tamilupdates/KPSML-X"><kbd><img src="https://graph.org/file/879239eb830dd6c00b07e.jpg" width="550" alt="KPSML-X Logo"></kbd></a></p>This repository hosts the KPSML-X Bot, a powerful Telegram bot designed for high-speed file mirroring, torrent leeching, and versatile file management across various cloud platforms.🛠️ Deployment OptionsDeployment MethodRecommended Use CaseStatus1. VPS + DockerSelf-hosting, Stability, & High Performance.✅ Recommended2. Heroku CLIQuick setup and basic cloud deployment.✅ Supported3. Google ColabTemporary testing/demonstration only.✅ Supported☁️ Heroku One-Click Deploy🧪 Google Colab Deploy<img src="https://graph.org/file/504ba776ef0724a4ae85b.png" width="25" alt="Google Colab Logo"> Google Colab : Deploy Link</div><details> <summary><h2>1. 🐳 VPS Deployment Guide (Using Docker)</h2></summary>This guide provides the robust, Docker-based method for self-hosting on any Linux VPS (Ubuntu/Debian recommended) for maximum performance and stability.PrerequisitesA running VPS (Linux) with git and docker installed.Required credentials: Bot Token, API ID, API Hash, and a MongoDB URI.Step-by-Step InstructionsPhase 1: Setup and ConfigurationSSH into your VPS and Clone the Repository:# Install Git and Docker dependencies (if not already installed)
sudo apt update && sudo apt install git curl -y

# Clone the bot repository
git clone [https://github.com/Tamilupdates/KPSML-X](https://github.com/Tamilupdates/KPSML-X)
cd KPSML-X
Create and Configure config.env: Edit the environment file to hold all your sensitive configuration. NOTE: Ensure there are NO spaces around the = sign (use KEY=VALUE).# Copy sample file to create config.env
cp config_sample.env config.env

# Open the file for editing
nano config.env 
Critical Configuration:Set all mandatory variables (BOT_TOKEN, OWNER_ID, DATABASE_URL, etc.).Set TORRENT_TIMEOUT="0".Set BASE_URL to your VPS's public IP or domain. This is mandatory for web-based features like torrent file selection (/qms).# Example if using default HTTP port 80:
BASE_URL="[http://123.45.67.89/](http://123.45.67.89/)"
CRITICAL FIX: Ensure the line _____REMOVE_THIS_LINE_____=True is deleted or commented out (e.g., # _____REMOVE_THIS_LINE_____=True).Phase 2: Docker Build and RunBuild the Docker Image: This process compiles the entire bot environment.docker build -t kpsmlx-bot .
Run the Container and Expose the Web Port (Mandatory): You must publish the container's internal web port (assumed to be 80) to the host's public port (80) using -p 80:80. The -e CONFIG_FILE_URL="" flag is essential to prevent configuration overwrites from older deployments.docker run -d \
  --name kpsmlx_bot \
  --restart=always \
  --env-file config.env \
  -e CONFIG_FILE_URL="" \
  -p 80:80 \
  kpsmlx-bot
Verify Deployment and Troubleshoot: Check the logs immediately after running to ensure the bot initialized without errors.docker logs -f kpsmlx_bot
</details><details> <summary><h2>2. ☁️ Heroku CLI Deployment Guide</h2></summary>Use this guide for deploying directly via the Heroku Command Line Interface.Step 1 : Git clone this Repo and change directoryMake sure git is Installed in your system or quick run apt-get install git pip curl -ygit clone [https://github.com/Tamilupdates/KPSML-X](https://github.com/Tamilupdates/KPSML-X) && cd KPSML-X 
Step 2 : Install Heroku CLIcurl [https://cli-assets.heroku.com/install.sh](https://cli-assets.heroku.com/install.sh) | sh
# OR use apt-get/npm as described in the official Heroku docs.
Step 3 : Login into Herokuheroku login
# OR
heroku login -i 
Step 4 : Create Heroku App and specify stackheroku create --region us --stack container APP_NAME
To Be Noted: Copy the BASE_URL displayed after creation for use in config.env.Step 5 : Configure config.env Locallynano config.env
# ... Edit the mandatory variables including the BASE_URL copied from above ...
Step 6 : Set Local git remote for Heroku.git add . -f
git commit -m "HK Setup"
heroku git:remote -a APP_NAME
Step 7 : Now push to Heroku via git forcefully to build.git push heroku main -f
</details><details> <summary><h2>3. ⚙️ Variables Configuration Reference</h2></summary>Mandatory VariablesVariableDescriptionTypeNotesBOT_TOKENTelegram Bot Token from BotFather.StrRequired for bot operation.OWNER_IDTelegram User ID of the Owner (integer).IntUse /id bot command to get your ID.TELEGRAM_APIAPI ID from $$ my.telegram.org $$.IntUsed for account authentication.TELEGRAM_HASHAPI Hash from $$ my.telegram.org $$.StrUsed for account authentication.DATABASE_URLMongoDB Database URL.StrHighly Recommended for persistent settings and data.TORRENT_TIMEOUTTimeout for dead torrents in seconds.IntMUST BE SET (e.g., to "0") to prevent bot crashes.BASE_URLPublic URL where the bot's web features (torrent select) are accessible.StrMUST be http(s)://your-ip-or-domain/ (VPS) or https://app-name.herokuapp.com/ (Heroku).Update VariablesVariableDescriptionTypeUPSTREAM_REPOGitHub repository URL for self-update checks.StrUPSTREAM_BRANCHUpstream branch for updates. Default is hk_kpsmlx.Str</details>
