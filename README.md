<div align=center>🚀 KPSML-X Bot: The Ultimate Deployable Mirror Leech Bot 🚀<p><a href="https://github.com/Tamilupdates/KPSML-X"><kbd><img src="https://graph.org/file/879239eb830dd6c00b07e.jpg" width="550" alt="KPSML-X Logo"></kbd></a></p>This repository contains the KPSML-X Bot, a feature-rich Telegram bot designed for efficient mirroring, leeching, and file management, deployable on multiple platforms, including Heroku and any Virtual Private Server (VPS) via Docker.🛠️ Deployment Options1. VPS Deployment (Recommended for Stability & Performance)Deploying via Docker on your own VPS ensures the most stable performance, persistent storage, and full control over resources.2. Heroku DeploymentThe traditional quick-start method for easy, fast deployment.3. Google Colab (Temporary Testing)A convenient way to test the bot without a persistent server.<img src="https://graph.org/file/504ba776ef0724a4ae85b.png" width="25" alt="Google Colab Logo"> Google Colab : Deploy Link</div><details><summary><h2>1. 🐳 VPS Deployment Guide (Using Docker)</h2></summary>This guide provides the robust, Docker-based method for self-hosting on any Linux VPS (Ubuntu/Debian recommended).PrerequisitesA running VPS with root access.Git and Docker Engine installed on the VPS.Step-by-Step InstructionsPhase 1: Setup and ConfigurationSSH into your VPS and Clone the Repository:# Install Git and Docker dependencies (if not already installed)
sudo apt update && sudo apt install git curl -y

# Clone the bot repository
git clone [https://github.com/Tamilupdates/KPSML-X](https://github.com/Tamilupdates/KPSML-X)
cd KPSML-X

Create and Configure config.env:The file config.env holds all your bot's essential variables. Ensure there are NO spaces around the = sign (i.e., use KEY=VALUE, not KEY = VALUE).# Copy sample file to create config.env
cp config_sample.env config.env

# Open the file for editing
nano config.env 

Critical variables to set:BOT_TOKEN="<Your Bot Token>"OWNER_ID="<Your Telegram User ID>"TELEGRAM_API="<Your API ID>"TELEGRAM_HASH="<Your API Hash>"DATABASE_URL="<Your MongoDB URL>"TORRENT_TIMEOUT="0" (Required to prevent crashes)BASE_URL (Set to your VPS's public IP or domain for web features like file selection):# Example if using default port 80:
BASE_URL="[http://123.45.67.89/](http://123.45.67.89/)"

CRITICAL FIX: REMOVE THE SAMPLE LINEIf the file contains _____REMOVE_THIS_LINE_____=True, this must be deleted or commented out (e.g., # _____REMOVE_THIS_LINE_____=True) to prevent the bot from exiting.Phase 2: Docker Build and RunBuild the Docker Image:This process compiles the entire environment, including necessary system dependencies like ffmpeg.docker build -t kpsmlx-bot .

Run the Container and Expose the Web Port (Mandatory for File Selection):We must publish the container's internal web port (which is assumed to be 80) to the host's public port (80) to enable features like torrent file selection (/qms command).# IMPORTANT: The '-e CONFIG_FILE_URL=""' prevents the bot from overwriting 
# your local config.env with old cloud configurations.
docker run -d \
  --name kpsmlx_bot \
  --restart=always \
  --env-file config.env \
  -e CONFIG_FILE_URL="" \
  -p 80:80 \
  kpsmlx-bot

Verify Deployment and Troubleshoot:Check the logs immediately after running to ensure no errors occurred.docker logs -f kpsmlx_bot

If you see the ffmpeg not installed error, repeat the build/run process.If file selection still shows a Heroku URL, ensure you added -e CONFIG_FILE_URL="" and corrected the BASE_URL in config.env.</details><details><summary><h2>2. ☁️ Heroku CLI Deployment Guide</h2></summary>The original guide is included here for Heroku CLI deployment.Step 1 : Git clone this Repo and change directoryMake sure git is Installed in your system or quick run apt-get install git pip curl -ygit clone [https://github.com/Tamilupdates/KPSML-X](https://github.com/Tamilupdates/KPSML-X) && cd KPSML-X 

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

</details><details><summary><h2>3. ⚙️ Variables Configuration Reference</h2></summary>Mandatory VariablesVariableDescriptionTypeNotesBOT_TOKENTelegram Bot Token from BotFather.StrRequired for bot operation.OWNER_IDTelegram User ID of the Owner (integer).IntUse /id bot command to get your ID.TELEGRAM_APIAPI ID from .IntUsed for account authentication.TELEGRAM_HASHAPI Hash from .StrUsed for account authentication.DATABASE_URLMongoDB Database URL.StrHighly Recommended for persistent settings and data.TORRENT_TIMEOUTTimeout for dead torrents in seconds.IntMUST BE SET (e.g., to "0") to prevent bot crashes.BASE_URLPublic URL where the bot's web features (torrent select) are accessible.StrMUST be http(s)://your-ip-or-domain/ (VPS) or https://app-name.herokuapp.com/ (Heroku).Update VariablesVariableDescriptionTypeUPSTREAM_REPOGitHub repository URL for self-update checks.StrUPSTREAM_BRANCHUpstream branch for updates. Default is hk_kpsmlx.Str</details>
