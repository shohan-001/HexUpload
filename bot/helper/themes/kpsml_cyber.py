#!/usr/bin/env python3
class KPSMLStyle:
    # ----------------------
    # async def start(client, message) ---> __main__.py
    ST_BN1_NAME = '🐨 Contact'
    ST_BN1_URL = 'https://telegram.me/Shohan_max'
    ST_BN2_NAME = '🐙 Github'
    ST_BN2_URL = 'https://github.com/shohan-001'
    ST_MSG = '''<b><i>🚀 Welcome to the HexUpload Bot! 🚀</i></b>

<b>✨ This bot can mirror all your links|files|torrents to:</b>
• 📁 Google Drive
• ☁️ Any RClone Cloud
• 📱 Telegram
• 🌐 DDL Servers

<b>Type {help_command} to get started! 🎯</b>'''
    ST_BOTPM = '''<b>🎉 Welcome to Bot PM! 🎉</b>

<i>🔥 All your files and links will appear here. Let's get started! 🚀</i>'''
    ST_UNAUTH = '''<b>🚫 Access Denied! 🚫</b>

<i>🔒 You are not authorized to use this bot.
Deploy your own KPSML-X Mirror-Leech bot! 🤖</i>'''
    OWN_TOKEN_GENERATE = '''<b>⚠️ Invalid Token! ⚠️</b>

<i>🔑 This temporary token doesn't belong to you.
Please generate your own token! ✨</i>'''
    USED_TOKEN = '''<b>❌ Token Expired! ❌</b>

<i>⏰ This temporary token has already been used.
Generate a fresh one to continue! 🔄</i>'''
    LOGGED_PASSWORD = '''<b>✅ Already Authenticated! ✅</b>

<i>🔐 Bot is logged in via password.
No need for temporary tokens! 🎯</i>'''
    ACTIVATE_BUTTON = '🔓 Activate Token'
    TOKEN_MSG = '''<b>🎫 Temporary Login Token Generated! 🎫</b>

<b>🔑 Token:</b> <code>{token}</code>
<b>⏳ Valid Until:</b> {validity}
<b>🚀 Ready to activate!</b>'''
    
    # ---------------------
    # async def token_callback(_, query): ---> __main__.py
    ACTIVATED = '✅ Token Activated! 🎉'
    
    # ---------------------
    # async def login(_, message): --> __main__.py
    LOGGED_IN = '<b>🔐 Already Logged In! 🔐</b>'
    INVALID_PASS = '''<b>❌ Wrong Password! ❌</b>

<i>🔑 Please enter the correct password to continue.</i>'''
    PASS_LOGGED = '<b>🎉 Login Successful! 🎉</b>'
    LOGIN_USED = '''<b>🔐 Login Instructions:</b>

<code>/cmd [your_password]</code>'''
    
    # ---------------------
    # async def log(_, message): ---> __main__.py
    LOG_DISPLAY_BT = '📋 View Logs'
    WEB_PASTE_BT = '🌐 Web Paste'
    
    # ---------------------
    # async def bot_help(client, message): ---> __main__.py
    BASIC_BT = '⚡ Basic'
    USER_BT = '👥 Users'
    MICS_BT = '🛠️ Tools'
    O_S_BT = '👑 Admin'
    CLOSE_BT = '❌ Close'
    HELP_HEADER = "🎯 <b><i>Command Center</i></b> 🎯\n\n<b>💡 Tip: <i>Click any button to explore commands!</i></b>"

    # async def stats(client, message):
    BOT_STATS = '''🤖 <b><i>BOT PERFORMANCE</i></b> 🤖
┖ <b>⏱️ Uptime:</b> {bot_uptime}

🧠 <b><i>MEMORY STATUS</i></b>
┃ {ram_bar} {ram}%
┖ <b>📊 Used:</b> {ram_u} | <b>🆓 Free:</b> {ram_f} | <b>📈 Total:</b> {ram_t}

💾 <b><i>SWAP MEMORY</i></b>
┃ {swap_bar} {swap}%
┖ <b>📊 Used:</b> {swap_u} | <b>🆓 Free:</b> {swap_f} | <b>📈 Total:</b> {swap_t}

💿 <b><i>STORAGE</i></b>
┃ {disk_bar} {disk}%
┃ <b>📖 Read:</b> {disk_read}
┃ <b>📝 Write:</b> {disk_write}
┖ <b>📊 Used:</b> {disk_u} | <b>🆓 Free:</b> {disk_f} | <b>📈 Total:</b> {disk_t}
    '''
    
    SYS_STATS = '''🖥️ <b><i>SYSTEM INFO</i></b>
┠ <b>⏰ OS Uptime:</b> {os_uptime}
┠ <b>🔧 Version:</b> {os_version}
┖ <b>🏗️ Architecture:</b> {os_arch}

🌐 <b><i>NETWORK STATS</i></b>
┠ <b>📤 Upload:</b> {up_data}
┠ <b>📥 Download:</b> {dl_data}
┠ <b>📦 Sent:</b> {pkt_sent}k packets
┠ <b>📨 Received:</b> {pkt_recv}k packets
┖ <b>🔄 Total I/O:</b> {tl_data}

⚡ <b><i>CPU STATUS</i></b>
┃ {cpu_bar} {cpu}%
┠ <b>🚄 Frequency:</b> {cpu_freq}
┠ <b>📊 Load Average:</b> {sys_load}
┠ <b>🔥 P-Cores:</b> {p_core} | <b>🧊 V-Cores:</b> {v_core}
┠ <b>🎯 Total Cores:</b> {total_core}
┖ <b>⚙️ Available CPUs:</b> {cpu_use}
    '''
    
    REPO_STATS = '''📦 <b><i>REPOSITORY INFO</i></b>
┠ <b>🔄 Last Update:</b> {last_commit}
┠ <b>🏷️ Current:</b> {bot_version}
┠ <b>✨ Latest:</b> {lat_version}
┖ <b>📝 Changes:</b> {commit_details}

💬 <b>Status:</b> <code>{remarks}</code>
    '''
    
    BOT_LIMITS = '''⚖️ <b><i>BOT LIMITATIONS</i></b>
┠ <b>🔗 Direct:</b> {DL} GB
┠ <b>🧲 Torrent:</b> {TL} GB
┠ <b>☁️ GDrive:</b> {GL} GB
┠ <b>🎥 YT-DLP:</b> {YL} GB
┠ <b>📋 Playlist:</b> {PL} items
┠ <b>🔥 Mega:</b> {ML} GB
┠ <b>📁 Clone:</b> {CL} GB
┖ <b>📱 Leech:</b> {LL} GB

🎫 <b><i>USAGE LIMITS</i></b>
┎ <b>⏳ Token Valid:</b> {TV}
┠ <b>👤 User Time:</b> {UTI} per task
┠ <b>👥 User Tasks:</b> {UT} parallel
┖ <b>🤖 Bot Tasks:</b> {BT} parallel
    '''
    
    # ---------------------
    # async def restart(client, message): ---> __main__.py
    RESTARTING = '<b>🔄 Restarting Bot...</b> <i>Please wait! ⏳</i>'
    
    # ---------------------
    # async def restart_notification(): ---> __main__.py
    RESTART_SUCCESS = '''🎉 <b><i>Restart Complete!</i></b> 🎉
┠ <b>📅 Date:</b> {date}
┠ <b>🕐 Time:</b> {time}
┠ <b>🌍 Zone:</b> {timz}
┖ <b>🏷️ Version:</b> {version}'''
    RESTARTED = '''✅ <b><i>Bot Successfully Restarted!</i></b> 🚀'''
    
    # ---------------------
    # async def ping(client, message): ---> __main__.py
    PING = '<i>🏓 Checking connection...</i>'
    PING_VALUE = '<b>🏓 Pong!</b>\n<code>⚡ {value} ms</code>'
    
    # ---------------------
    # async def onDownloadStart(self): --> tasks_listener.py
    LINKS_START = """🚀 <b><i>Task Initiated</i></b>
┠ <b>🎯 Mode:</b> {Mode}
┖ <b>👤 By:</b> {Tag}\n\n"""
    
    LINKS_SOURCE = """🔗 <b>Source Details:</b>
┖ <b>📅 Started:</b> {On}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{Source}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"""
    
    # async def __msg_to_reply(self): ---> pyrogramEngine.py
    PM_START = "🎬 <b><u>Task Started:</u></b>\n┃\n┖ <b>🔗 Link:</b> <a href='{msg_link}'>View Task</a>"
    L_LOG_START = "📥 <b><u>Leech Started:</u></b>\n┃\n┠ <b>👤 User:</b> {mention} ( #ID{uid} )\n┖ <b>📋 Source:</b> <a href='{msg_link}'>View Details</a>"

    # async def onUploadComplete(): ---> tasks_listener.py
    NAME = '<b><i>📁 {Name}</i></b>\n┃\n'
    SIZE = '┠ <b>📏 Size:</b> {Size}\n'
    ELAPSE = '┠ <b>⏱️ Duration:</b> {Time}\n'
    MODE = '┠ <b>🎯 Mode:</b> {Mode}\n'

    # ----- LEECH -------
    L_TOTAL_FILES = '┠ <b>📄 Files:</b> {Files}\n'
    L_CORRUPTED_FILES = '┠ <b>💥 Corrupted:</b> {Corrupt}\n'
    L_CC = '┖ <b>👤 By:</b> {Tag}\n\n'
    PM_BOT_MSG = '✅ <b><i>Files sent above! 📤</i></b>'
    L_BOT_MSG = '🤖 <b><i>Files sent to Bot PM! 📱</i></b>'
    L_LL_MSG = '🔗 <b><i>Files ready! Access via links... 🌐</i></b>\n'
    
    # ----- MIRROR -------
    M_TYPE = '┠ <b>📋 Type:</b> {Mimetype}\n'
    M_SUBFOLD = '┠ <b>📂 Folders:</b> {Folder}\n'
    TOTAL_FILES = '┠ <b>📄 Files:</b> {Files}\n'
    RCPATH = '┠ <b>📍 Path:</b> <code>{RCpath}</code>\n'
    M_CC = '┖ <b>👤 By:</b> {Tag}\n\n'
    M_BOT_MSG = '🤖 <b><i>Links sent to Bot PM! 📱</i></b>'
    
    # ----- BUTTONS -------
    CLOUD_LINK = '☁️ Cloud'
    SAVE_MSG = '💾 Save'
    RCLONE_LINK = '🔄 RClone'
    DDL_LINK = '🌐 {Serv}'
    SOURCE_URL = '🔐 Source'
    INDEX_LINK_F = '📂 Index'
    INDEX_LINK_D = '⚡ Index'
    VIEW_LINK = '👁️ Preview'
    CHECK_PM = '🤖 Bot PM'
    CHECK_LL = '🔗 Links Log'
    MEDIAINFO_LINK = '📊 Media Info'
    SCREENSHOTS = '🖼️ Screenshots'
    
    # ---------------------
    # def get_readable_message(): ---> bot_utilis.py
    ####--------OVERALL MSG HEADER----------
    STATUS_NAME = '<b><i>📁 {Name}</i></b>'

    #####---------PROGRESSIVE STATUS-------
    BAR = '\n┃ {Bar}'
    PROCESSED = '\n┠ <b>📊 Progress:</b> {Processed}'
    STATUS = '\n┠ <b>🎯 Status:</b> <a href="{Url}">{Status}</a>'
    ETA = ' | <b>⏳ ETA:</b> {Eta}'
    SPEED = '\n┠ <b>⚡ Speed:</b> {Speed}'
    ELAPSED = ' | <b>⏱️ Time:</b> {Elapsed}'
    ENGINE = '\n┠ <b>🔧 Engine:</b> {Engine}'
    STA_MODE = '\n┠ <b>🎯 Mode:</b> {Mode}'
    SEEDERS = '\n┠ <b>🌱 Seeds:</b> {Seeders} | '
    LEECHERS = '<b>📥 Peers:</b> {Leechers}'

    ####--------SEEDING----------
    SEED_SIZE = '\n┠ <b>📏 Size:</b> {Size}'
    SEED_SPEED = '\n┠ <b>⚡ Speed:</b> {Speed} | '
    UPLOADED = '<b>📤 Upload:</b> {Upload}'
    RATIO = '\n┠ <b>⚖️ Ratio:</b> {Ratio} | '
    TIME = '<b>⏰ Time:</b> {Time}'
    SEED_ENGINE = '\n┠ <b>🔧 Engine:</b> {Engine}'

    ####--------NON-PROGRESSIVE + NON SEEDING----------
    STATUS_SIZE = '\n┠ <b>📏 Size:</b> {Size}'
    NON_ENGINE = '\n┠ <b>🔧 Engine:</b> {Engine}'

    ####--------OVERALL MSG FOOTER----------
    USER = '\n┠ <b>👤 User:</b> <code>{User}</code> | '
    ID = '<b>🆔 ID:</b> <code>{Id}</code>'
    BTSEL = '\n┠ <b>✅ Select:</b> {Btsel}'
    CANCEL = '\n┖ {Cancel}\n\n'

    ####------FOOTER--------
    FOOTER = '🤖 <b><i>Bot Statistics</i></b>\n'
    TASKS = '┠ <b>📋 Tasks:</b> {Tasks}\n'
    BOT_TASKS = '┠ <b>📋 Tasks:</b> {Tasks}/{Ttask} | <b>🆓 Free:</b> {Free}\n'
    Cpu = '┠ <b>⚡ CPU:</b> {cpu}% | '
    FREE = '<b>💾 Free:</b> {free} [{free_p}%]'
    Ram = '\n┠ <b>🧠 RAM:</b> {ram}% | '
    uptime = '<b>⏰ UP:</b> {uptime}'
    DL = '\n┖ <b>📥 DL:</b> {DL}/s | '
    UL = '<b>📤 UL:</b> {UL}/s'

    ###--------BUTTONS-------
    PREVIOUS = '⬅️'
    REFRESH = '🔄\n{Page}'
    NEXT = '➡️'
    
    # ---------------------
    #STOP_DUPLICATE_MSG: ---> clone.py, aria2_listener.py, task_manager.py
    STOP_DUPLICATE = '⚠️ <b>Duplicate Found!</b>\n\nFile/Folder already exists in Drive.\n🔍 Here are {content} search results:'
    
    # ---------------------
    # async def countNode(_, message): ----> gd_count.py
    COUNT_MSG = '<b>🔍 Analyzing:</b> <code>{LINK}</code>'
    COUNT_NAME = '<b><i>📊 {COUNT_NAME}</i></b>\n┃\n'
    COUNT_SIZE = '┠ <b>📏 Size:</b> {COUNT_SIZE}\n'
    COUNT_TYPE = '┠ <b>📋 Type:</b> {COUNT_TYPE}\n'
    COUNT_SUB = '┠ <b>📂 Folders:</b> {COUNT_SUB}\n'
    COUNT_FILE = '┠ <b>📄 Files:</b> {COUNT_FILE}\n'
    COUNT_CC = '┖ <b>👤 By:</b> {COUNT_CC}\n'
    
    # ---------------------
    # LIST ---> gd_list.py
    LIST_SEARCHING = '<b>🔍 Searching for <i>{NAME}</i>...</b>'
    LIST_FOUND = '<b>✅ Found {NO} results for <i>{NAME}</i></b>'
    LIST_NOT_FOUND = '❌ <b>No results found for <i>{NAME}</i></b>'
    
    # ---------------------
    # async def mirror_status(_, message): ----> status.py
    NO_ACTIVE_DL = '''😴 <i>No active downloads</i>
    
🤖 <b><i>Current Stats</i></b>
┠ <b>⚡ CPU:</b> {cpu}% | <b>💾 Free:</b> {free} [{free_p}%]
┖ <b>🧠 RAM:</b> {ram} | <b>⏰ UP:</b> {uptime}
    '''
    
    # ---------------------
    # USER Setting --> user_setting.py 
    USER_SETTING = '''👤 <b><u>User Profile</u></b>
        
┎<b>📝 Name:</b> {NAME} ( <code>{ID}</code> )
┠<b>👤 Username:</b> {USERNAME}
┠<b>🌐 Telegram DC:</b> {DC}
┖<b>🗣️ Language:</b> {LANG}

💡 <u><b>Quick Setup:</b></u>
• Use <b>-s</b> or <b>-set</b> for direct configuration'''

    UNIVERSAL = '''⚙️ <b><u>Universal Settings: {NAME}</u></b>

┎<b>🎥 YT-DLP:</b> <code>{YT}</code>
┠<b>📅 Daily Limit:</b> <code>{DT}</code> tasks/day
┠<b>🕐 Last Used:</b> <code>{LAST_USED}</code>
┠<b>🔐 Session:</b> <code>{USESS}</code>
┠<b>📊 MediaInfo:</b> <code>{MEDIAINFO}</code>
┠<b>💾 Save Mode:</b> <code>{SAVE_MODE}</code>
┖<b>🤖 Bot PM:</b> <code>{BOT_PM}</code>'''

    MIRROR = '''☁️ <b><u>Mirror Settings: {NAME}</u></b>

┎<b>⚙️ RClone:</b> <i>{RCLONE}</i>
┠<b>📝 Prefix:</b> <code>{MPREFIX}</code>
┠<b>📝 Suffix:</b> <code>{MSUFFIX}</code>
┠<b>🏷️ Rename:</b> <code>{MREMNAME}</code>
┠<b>🌐 DDL Servers:</b> <i>{DDL_SERVER}</i>
┠<b>📁 TD Mode:</b> <i>{TMODE}</i>
┠<b>📊 Total TDs:</b> <i>{USERTD}</i>
┖<b>📅 Daily Mirror:</b> <code>{DM}</code>/day'''

    LEECH = '''📱 <b><u>Leech Settings: {NAME}</u></b>

┎<b>📅 Daily Limit:</b> <code>{DL}</code>/day
┠<b>📋 Type:</b> <i>{LTYPE}</i>
┠<b>🖼️ Thumbnail:</b> <i>{THUMB}</i>
┠<b>📏 Split Size:</b> <code>{SPLIT_SIZE}</code>
┠<b>⚖️ Equal Split:</b> <i>{EQUAL_SPLIT}</i>
┠<b>📱 Media Group:</b> <i>{MEDIA_GROUP}</i>
┠<b>📝 Caption:</b> <code>{LCAPTION}</code>
┠<b>📝 Prefix:</b> <code>{LPREFIX}</code>
┠<b>📝 Suffix:</b> <code>{LSUFFIX}</code>
┠<b>📂 Dumps:</b> <code>{LDUMP}</code>
┖<b>🏷️ Rename:</b> <code>{LREMNAME}</code>'''
