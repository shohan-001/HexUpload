from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.filters import command, regex
from html import escape
from traceback import format_exc
from base64 import b64encode
from re import match as re_match
from asyncio import sleep, wrap_future
from aiofiles import open as aiopen
from aiofiles.os import path as aiopath
from cloudscraper import create_scraper
import os
import re
from pathlib import Path
from shutil import rmtree

from bot import bot, DOWNLOAD_DIR, LOGGER, config_dict, bot_name, categories_dict, user_data
from bot.helper.mirror_utils.download_utils.direct_downloader import add_direct_download
from bot.helper.ext_utils.bot_utils import is_url, is_magnet, is_mega_link, is_gdrive_link, get_content_type, new_task, sync_to_async, is_rclone_path, is_telegram_link, arg_parser, fetch_user_tds, fetch_user_dumps, get_stats
from bot.helper.ext_utils.exceptions import DirectDownloadLinkException
from bot.helper.ext_utils.task_manager import task_utils
from bot.helper.mirror_utils.download_utils.aria2_download import add_aria2c_download
from bot.helper.mirror_utils.download_utils.gd_download import add_gd_download
from bot.helper.mirror_utils.download_utils.qbit_download import add_qb_torrent
from bot.helper.mirror_utils.download_utils.mega_download import add_mega_download
from bot.helper.mirror_utils.download_utils.rclone_download import add_rclone_download
from bot.helper.mirror_utils.rclone_utils.list import RcloneList
from bot.helper.mirror_utils.upload_utils.gdriveTools import GoogleDriveHelper
from bot.helper.mirror_utils.download_utils.direct_link_generator import direct_link_generator
from bot.helper.mirror_utils.download_utils.telegram_download import TelegramDownloadHelper
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.button_build import ButtonMaker
from bot.helper.telegram_helper.message_utils import sendMessage, editMessage, editReplyMarkup, deleteMessage, get_tg_link_content, delete_links, auto_delete_message, open_category_btns, open_dump_btns
from bot.helper.listeners.tasks_listener import MirrorLeechListener
from bot.helper.ext_utils.help_messages import MIRROR_HELP_MESSAGE, CLONE_HELP_MESSAGE, YT_HELP_MESSAGE, help_string
from bot.helper.ext_utils.bulk_links import extract_bulk_links
from bot.modules.gen_pyro_sess import get_decrypt_key

# ====== ADD THIS NEW CLASS FOR SPLIT FILE COMBINING ======
class SplitFileCombiner:
    def __init__(self, client, message):
        self.client = client
        self.message = message
        self.user_id = message.from_user.id
        self.chat_id = message.chat.id
        self.temp_dir = f"{DOWNLOAD_DIR}{self.message.id}_combine/"
        self.split_files = []
        self.combined_file_path = ""
        
    async def combine_split_files(self, file_messages, output_filename=None, upload_to_drive=True):
        """Combine multiple split files from Telegram messages"""
        try:
            await aiopath.makedirs(self.temp_dir, exist_ok=True)
            
            # Download all split files
            progress_msg = await sendMessage(self.message, "📥 <b>Downloading split files...</b>")
            
            downloaded_files = []
            for i, msg in enumerate(file_messages, 1):
                if msg.document:
                    file_path = await msg.download(file_name=f"{self.temp_dir}{i:03d}_{msg.document.file_name}")
                    downloaded_files.append(file_path)
                    await editMessage(progress_msg, f"📥 <b>Downloaded:</b> {i}/{len(file_messages)} files")
            
            if not downloaded_files:
                await editMessage(progress_msg, "❌ <b>Error:</b> No files downloaded!")
                return False
            
            # Sort files naturally
            downloaded_files.sort(key=self._natural_sort_key)
            
            # Determine output filename
            if not output_filename:
                first_file = Path(downloaded_files[0]).name
                output_filename = re.sub(r'\.\d+$|\.part\d*$|\.z\d+$', '', first_file)
                if not output_filename or output_filename == first_file:
                    output_filename = f"combined_{self.message.id}"
            
            self.combined_file_path = f"{self.temp_dir}{output_filename}"
            
            # Combine files
            await editMessage(progress_msg, "🔄 <b>Combining files...</b>")
            await self._combine_files(downloaded_files, self.combined_file_path)
            
            # Check if combined file exists
            if not await aiopath.exists(self.combined_file_path):
                await editMessage(progress_msg, "❌ <b>Error:</b> Failed to create combined file!")
                return False
            
            file_size = await aiopath.getsize(self.combined_file_path)
            await editMessage(progress_msg, f"✅ <b>Files combined successfully!</b>\n"
                                         f"📁 <b>Filename:</b> {output_filename}\n"
                                         f"📏 <b>Size:</b> {self._format_size(file_size)}")
            
            # Upload to Google Drive
            if upload_to_drive:
                await self._upload_to_drive(progress_msg, output_filename)
            
            return True
            
        except Exception as e:
            LOGGER.error(f"Error combining files: {e}")
            await sendMessage(self.message, f"❌ <b>Error:</b> {str(e)}")
            return False
        finally:
            await self._cleanup()
    
    async def _combine_files(self, file_paths, output_path):
        """Combine multiple files into one"""
        async with aiopen(output_path, 'wb') as outfile:
            for file_path in file_paths:
                async with aiopen(file_path, 'rb') as infile:
                    while True:
                        chunk = await infile.read(1024 * 1024)  # 1MB chunks
                        if not chunk:
                            break
                        await outfile.write(chunk)
    
    async def _upload_to_drive(self, progress_msg, filename):
        """Upload combined file to Google Drive"""
        try:
            await editMessage(progress_msg, "☁️ <b>Uploading to Google Drive...</b>")
            
            user_tds = await fetch_user_tds(self.user_id)
            drive_id = ""
            index_link = ""
            
            if user_tds and len(user_tds) == 1:
                drive_data = next(iter(user_tds.values()))
                drive_id = drive_data.get('drive_id', '')
                index_link = drive_data.get('index_link', '')
            elif config_dict.get('GDRIVE_ID'):
                drive_id = config_dict['GDRIVE_ID']
                index_link = config_dict.get('INDEX_URL', '')
            
            if not drive_id:
                await editMessage(progress_msg, "❌ <b>Error:</b> No Google Drive ID configured!")
                return
            
            tag = f"@{self.message.from_user.username}" if self.message.from_user.username else self.message.from_user.mention
            
            # Create mock listener for upload
            class CombineUploadListener:
                def __init__(self, message, tag, drive_id, index_link):
                    self.message = message
                    self.tag = tag
                    self.drive_id = drive_id
                    self.index_link = index_link
                    self.isLeech = False
                    self.compress = False
                    self.extract = False
                    self.isQbit = False
                    self.select = False
                    self.seed = False
                    self.newDir = ""
                    self.dir = f"{DOWNLOAD_DIR}{message.id}_combine/"
                    self.isClone = False
                    self.upPath = "gd"
                    self.user_dict = user_data.get(message.from_user.id, {})
            
            listener = CombineUploadListener(self.message, tag, drive_id, index_link)
            gd_helper = GoogleDriveHelper(drive_id, "", listener)
            result = await sync_to_async(gd_helper.upload, filename, self.combined_file_path, self.combined_file_path)
            
            if result:
                link = f"https://drive.google.com/file/d/{result}/view"
                if index_link:
                    index_url = f"{index_link.rstrip('/')}/{filename}"
                else:
                    index_url = link
                
                msg = f"✅ <b>File uploaded successfully to Google Drive!</b>\n\n"
                msg += f"📁 <b>Filename:</b> <code>{filename}</code>\n"
                msg += f"📏 <b>Size:</b> {self._format_size(await aiopath.getsize(self.combined_file_path))}\n"
                msg += f"🔗 <b>Drive Link:</b> <a href='{link}'>Click Here</a>\n"
                if index_url != link:
                    msg += f"🌐 <b>Index Link:</b> <a href='{index_url}'>Click Here</a>"
                
                await editMessage(progress_msg, msg)
            else:
                await editMessage(progress_msg, "❌ <b>Error:</b> Failed to upload to Google Drive!")
                
        except Exception as e:
            LOGGER.error(f"Error uploading to drive: {e}")
            await editMessage(progress_msg, f"❌ <b>Upload Error:</b> {str(e)}")
    
    def _natural_sort_key(self, text):
        """Natural sorting key for filenames with numbers"""
        return [int(x) if x.isdigit() else x.lower() for x in re.split('([0-9]+)', str(text))]
    
    def _format_size(self, size_bytes):
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0B"
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        return f"{size_bytes:.2f} {size_names[i]}"
    
    async def _cleanup(self):
        """Clean up temporary files"""
        try:
            if await aiopath.exists(self.temp_dir):
                await sync_to_async(rmtree, self.temp_dir)
        except Exception as e:
            LOGGER.error(f"Error during cleanup: {e}")


# ====== ADD NEW COMBINE COMMAND FUNCTION ======
@new_task
async def combine_command(client, message):
    """Command handler for combining split files"""
    try:
        if not message.reply_to_message:
            help_msg = (
                "📋 <b>How to use Split File Combiner:</b>\n\n"
                "1️⃣ Forward/send all split files to this chat\n"
                "2️⃣ Reply to the first split file with <code>/combine [optional_filename]</code>\n"
                "3️⃣ Select all split files when prompted\n\n"
                "💡 <b>Tips:</b>\n"
                "• Files will be combined in the order you select them\n"
                "• Use a descriptive filename to avoid confusion\n"
                "• Large files will be automatically uploaded to Google Drive\n\n"
                "📝 <b>Example:</b> <code>/combine my_video.mp4</code>"
            )
            await sendMessage(message, help_msg)
            return
        
        # Parse command arguments
        args = message.text.split()[1:] if len(message.text.split()) > 1 else []
        custom_filename = " ".join(args) if args else None
        
        # Get recent messages to find split files
        recent_messages = []
        async for msg in client.get_chat_history(message.chat.id, limit=50):
            if msg.document and msg.date >= message.reply_to_message.date:
                recent_messages.append(msg)
            if len(recent_messages) >= 20:
                break
        
        if not recent_messages:
            await sendMessage(message, "❌ <b>No files found in recent messages!</b>")
            return
        
        # Create file selection interface
        buttons = ButtonMaker()
        for i, msg in enumerate(recent_messages[:10]):
            filename = msg.document.file_name[:30] + "..." if len(msg.document.file_name) > 30 else msg.document.file_name
            file_size = msg.document.file_size
            buttons.ibutton(
                f"📄 {filename} ({file_size // (1024*1024)}MB)",
                f"select_file_{msg.id}"
            )
        
        buttons.ibutton("✅ Combine Selected Files", "start_combine")
        buttons.ibutton("❌ Cancel", "cancel_combine")
        
        selection_msg = await sendMessage(
            message,
            "📋 <b>Select split files to combine:</b>\n\n"
            "🔸 Click on files to select/deselect them\n"
            "🔸 Selected files will be marked with ✅\n"
            "🔸 Click 'Combine Selected Files' when ready",
            buttons.build_menu(1)
        )
        
        # Store selection data
        user_data[message.from_user.id] = user_data.get(message.from_user.id, {})
        user_data[message.from_user.id]['combine_selection'] = {
            'messages': {msg.id: msg for msg in recent_messages[:10]},
            'selected': [],
            'filename': custom_filename,
            'selection_msg_id': selection_msg.id
        }
        
    except Exception as e:
        LOGGER.error(f"Error in combine command: {e}")
        await sendMessage(message, f"❌ <b>Error:</b> {str(e)}")


# ====== ADD COMBINE CALLBACK HANDLER ======
async def combine_callback(client, query):
    """Handle callback queries for file combination"""
    try:
        user_id = query.from_user.id
        data = query.data.split('_', 2)
        
        if user_id not in user_data or 'combine_selection' not in user_data[user_id]:
            await query.answer("❌ Selection expired. Please run /combine again.", show_alert=True)
            return
        
        selection_data = user_data[user_id]['combine_selection']
        
        if data[1] == "file":
            # Toggle file selection
            msg_id = int(data[2])
            if msg_id in selection_data['selected']:
                selection_data['selected'].remove(msg_id)
            else:
                selection_data['selected'].append(msg_id)
            
            # Update buttons
            buttons = ButtonMaker()
            for msg_id, msg in selection_data['messages'].items():
                filename = msg.document.file_name[:25] + "..." if len(msg.document.file_name) > 25 else msg.document.file_name
                file_size = msg.document.file_size
                prefix = "✅" if msg_id in selection_data['selected'] else "📄"
                buttons.ibutton(
                    f"{prefix} {filename} ({file_size // (1024*1024)}MB)",
                    f"select_file_{msg_id}"
                )
            
            buttons.ibutton("🔄 Combine Selected Files", "start_combine")
            buttons.ibutton("❌ Cancel", "cancel_combine")
            
            await query.edit_message_reply_markup(buttons.build_menu(1))
            await query.answer()
            
        elif query.data == "start_combine":
            if not selection_data['selected']:
                await query.answer("❌ Please select at least one file!", show_alert=True)
                return
            
            selected_messages = [selection_data['messages'][msg_id] for msg_id in selection_data['selected']]
            selected_messages.sort(key=lambda x: selection_data['selected'].index(x.id))
            
            await query.edit_message_text("🔄 <b>Starting file combination process...</b>")
            
            combiner = SplitFileCombiner(client, query.message)
            await combiner.combine_split_files(
                selected_messages, 
                selection_data['filename'], 
                upload_to_drive=True
            )
            
            if user_id in user_data and 'combine_selection' in user_data[user_id]:
                del user_data[user_id]['combine_selection']
            
        elif query.data == "cancel_combine":
            await query.edit_message_text("❌ <b>File combination cancelled.</b>")
            if user_id in user_data and 'combine_selection' in user_data[user_id]:
                del user_data[user_id]['combine_selection']
            
    except Exception as e:
        LOGGER.error(f"Error in combine callback: {e}")
        await query.answer(f"❌ Error: {str(e)}", show_alert=True)


# ====== YOUR EXISTING CODE CONTINUES HERE ======
@new_task
async def _mirror_leech(client, message, isQbit=False, isLeech=False, sameDir=None, bulk=[]):
    # ... (all your existing _mirror_leech code remains the same) ...
    text = message.text.split('\n')
    input_list = text[0].split(' ')

    arg_base = {'link': '',
                '-i': '0',
                '-m': '', '-sd': '', '-samedir': '',
                '-d': False, '-seed': False,
                '-j': False, '-join': False,
                '-s': False, '-select': False,
                '-b': False, '-bulk': False,
                '-n': '', '-name': '',
                '-e': False, '-extract': False,
                '-uz': False, '-unzip': False,
                '-z': False, '-zip': False,
                '-up': '', '-upload': '',
                '-rcf': '', 
                '-u': '', '-user': '',
                '-p': '', '-pass': '',
                '-id': '',
                '-index': '',
                '-c': '', '-category': '',
                '-ud': '', '-dump': '',
                '-h': '', '-headers': '',
                '-ss': '0', '-screenshots': '',
                '-t': '', '-thumb': '',
    }

    args = arg_parser(input_list[1:], arg_base)
    cmd = input_list[0].split('@')[0]

    multi = int(args['-i']) if args['-i'].isdigit() else 0

    link          = args['link']
    folder_name   = args['-m'] or args['-sd'] or args['-samedir']
    seed          = args['-d'] or args['-seed']
    join          = args['-j'] or args['-join']
    select        = args['-s'] or args['-select']
    isBulk        = args['-b'] or args['-bulk']
    name          = args['-n'] or args['-name']
    extract       = args['-e'] or args['-extract'] or args['-uz'] or args['-unzip'] or 'uz' in cmd or 'unzip' in cmd
    compress      = args['-z'] or args['-zip'] or (not extract and ('z' in cmd or 'zip' in cmd))
    up            = args['-up'] or args['-upload']
    rcf           = args['-rcf']
    drive_id      = args['-id']
    index_link    = args['-index']
    gd_cat        = args['-c'] or args['-category']
    user_dump     = args['-ud'] or args['-dump']
    headers       = args['-h'] or args['-headers']
    ussr          = args['-u'] or args['-user']
    pssw          = args['-p'] or args['-pass']
    thumb         = args['-t'] or args['-thumb']
    sshots        = int(ss) if (ss := (args['-ss'] or args['-screenshots'])).isdigit() else 0
    bulk_start    = 0
    bulk_end      = 0
    ratio         = None
    seed_time     = None
    reply_to      = None
    file_         = None
    session       = ''
    
    if not isinstance(seed, bool):
        dargs = seed.split(':')
        ratio = dargs[0] or None
        if len(dargs) == 2:
            seed_time = dargs[1] or None
        seed = True

    if not isinstance(isBulk, bool):
        dargs = isBulk.split(':')
        bulk_start = dargs[0] or None
        if len(dargs) == 2:
            bulk_end = dargs[1] or None
        isBulk = True
        
    if drive_id and is_gdrive_link(drive_id):
        drive_id = GoogleDriveHelper.getIdFromUrl(drive_id)

    if folder_name and not isBulk:
        seed = False
        ratio = None
        seed_time = None
        folder_name = f'/{folder_name}'
        if sameDir is None:
            sameDir = {'total': multi, 'tasks': set(), 'name': folder_name}
        sameDir['tasks'].add(message.id)

    if isBulk:
        try:
            bulk = await extract_bulk_links(message, bulk_start, bulk_end)
            if len(bulk) == 0:
                raise ValueError('Bulk Empty!')
        except:
            await sendMessage(message, 'Reply to text file or tg message that have links seperated by new line!')
            return
        b_msg = input_list[:1]
        b_msg.append(f'{bulk[0]} -i {len(bulk)}')
        nextmsg = await sendMessage(message, " ".join(b_msg))
        nextmsg = await client.get_messages(chat_id=message.chat.id, message_ids=nextmsg.id)
        nextmsg.from_user = message.from_user
        _mirror_leech(client, nextmsg, isQbit, isLeech, sameDir, bulk)
        return

    if len(bulk) != 0:
        del bulk[0]

    @new_task
    async def __run_multi():
        if multi <= 1:
            return
        await sleep(5)
        if len(bulk) != 0:
            msg = input_list[:1]
            msg.append(f'{bulk[0]} -i {multi - 1}')
            nextmsg = await sendMessage(message, " ".join(msg))
        else:
            msg = [s.strip() for s in input_list]
            index = msg.index('-i')
            msg[index+1] = f"{multi - 1}"
            nextmsg = await client.get_messages(chat_id=message.chat.id, message_ids=message.reply_to_message_id + 1)
            nextmsg = await sendMessage(nextmsg, " ".join(msg))
        nextmsg = await client.get_messages(chat_id=message.chat.id, message_ids=nextmsg.id)
        if folder_name:
            sameDir['tasks'].add(nextmsg.id)
        nextmsg.from_user = message.from_user
        await sleep(5)
        _mirror_leech(client, nextmsg, isQbit, isLeech, sameDir, bulk)

    __run_multi()

    path = f'{DOWNLOAD_DIR}{message.id}{folder_name}'

    if len(text) > 1 and text[1].startswith('Tag: '):
        tag, id_ = text[1].split('Tag: ')[1].split()
        message.from_user = await client.get_users(id_)
        try:
            await message.unpin()
        except:
            pass
    elif sender_chat := message.sender_chat:
        tag = sender_chat.title
    if username := message.from_user.username:
        tag = f"@{username}"
    else:
        tag = message.from_user.mention
        
    decrypter = None
    if not link and (reply_to := message.reply_to_message):
        if reply_to.text:
            link = reply_to.text.split('\n', 1)[0].strip()
    if link and is_telegram_link(link):
        try:
            reply_to, session = await get_tg_link_content(link, message.from_user.id)
            if reply_to is None and session == "":
                decrypter, is_cancelled = await wrap_future(get_decrypt_key(client, message))
                if is_cancelled:
                    return
                reply_to, session = await get_tg_link_content(link, message.from_user.id, decrypter)
        except Exception as e:
            LOGGER.info(format_exc())
            await sendMessage(message, f'<b>ERROR:</b> <i>{e}</i>')
            await delete_links(message)
            return

    if reply_to:
        file_ = getattr(reply_to, reply_to.media.value) if reply_to.media else None
        if file_ is None and reply_to.text:
            reply_text = reply_to.text.split('\n', 1)[0].strip()
            if is_url(reply_text) or is_magnet(reply_text):
                link = reply_text
        elif reply_to.document and (file_.mime_type == 'application/x-bittorrent' or file_.file_name.endswith('.torrent')):
            link = await reply_to.download()
            file_ = None

    if not is_url(link) and not is_magnet(link) and not await aiopath.exists(link) and not is_rclone_path(link) and file_ is None:
        btn = ButtonMaker()
        btn.ibutton('Cʟɪᴄᴋ Hᴇʀᴇ Tᴏ Rᴇᴀᴅ Mᴏʀᴇ ...', f'kpsmlx {message.from_user.id} help MIRROR')
        await sendMessage(message, MIRROR_HELP_MESSAGE[0], btn.build_menu(1))
        await delete_links(message)
        return

    error_msg = []
    error_button = None
    task_utilis_msg, error_button = await task_utils(message)
    if task_utilis_msg:
        error_msg.extend(task_utilis_msg)

    if error_msg:
        final_msg = f'<b><i>User:</i> {tag}</b>,\n'
        for __i, __msg in enumerate(error_msg, 1):
            final_msg += f'\n<b>{__i}</b>: {__msg}\n'
        if error_button is not None:
            error_button = error_button.build_menu(2)
        await sendMessage(message, final_msg, error_button)
        await delete_links(message)
        return

    org_link = None
    if link:
        LOGGER.info(link)
        org_link = link

    if (not is_mega_link(link) or (is_mega_link(link) and not config_dict['MEGA_EMAIL'] and config_dict['DEBRID_LINK_API'])) \
        and (not is_magnet(link) or (config_dict['REAL_DEBRID_API'] and is_magnet(link))) \
        and (not isQbit or (config_dict['REAL_DEBRID_API'] and is_magnet(link))) \
        and not is_rclone_path(link) and not is_gdrive_link(link) and not link.endswith('.torrent') and file_ is None:
        content_type = await get_content_type(link)
        if content_type is None or re_match(r'text/html|text/plain', content_type):
            process_msg = await sendMessage(message, f"<i><b>Processing:</b></i> <code>{link}</code>")
            try:
                if not is_magnet(link) and (ussr or pssw):
                    link = (link, (ussr, pssw))
                link = await sync_to_async(direct_link_generator, link)
                if isinstance(link, tuple):
                    link, headers = link
                elif isinstance(link, str):
                    LOGGER.info(f"Generated link: {link}")
                    await editMessage(process_msg, f"<i><b>Generated link:</b></i> <code>{link}</code>")
            except DirectDownloadLinkException as e:
                e = str(e)
                if 'This link requires a password!' not in e:
                    LOGGER.info(e)
                if str(e).startswith('ERROR:'):
                    await editMessage(process_msg, str(e))
                    await delete_links(message)
                    return
            await deleteMessage(process_msg)

    if not isLeech:
        if config_dict['DEFAULT_UPLOAD'] == 'rc' and not up or up == 'rc':
            up = config_dict['RCLONE_PATH']
        elif config_dict['DEFAULT_UPLOAD'] == 'ddl' and not up or up == 'ddl':
            up = 'ddl'
        if not up and config_dict['DEFAULT_UPLOAD'] == 'gd':
            up = 'gd'
            user_tds = await fetch_user_tds(message.from_user.id)
            if not drive_id and gd_cat:
                merged_dict = {**categories_dict, **user_tds}
                drive_id, index_link = next(((drive_dict['drive_id'], drive_dict['index_link']) for drive_name, drive_dict in merged_dict.items() if drive_name.casefold() == gd_cat.replace('_', ' ').casefold()), ('', ''))
            if not drive_id and len(user_tds) == 1:
                drive_id, index_link = next(iter(user_tds.values())).values()
            elif not drive_id and (len(categories_dict) > 1 and len(user_tds) == 0 or len(categories_dict) >= 1 and len(user_tds) > 1):
                drive_id, index_link, is_cancelled = await open_category_btns(message)
                if is_cancelled:
                    await delete_links(message)
                    return
            if drive_id and not await sync_to_async(GoogleDriveHelper().getFolderData, drive_id):
                return await sendMessage(message, "Google Drive ID validation failed!!")
        if up == 'gd' and not config_dict['GDRIVE_ID'] and not drive_id:
            await sendMessage(message, 'GDRIVE_ID not Provided!')
            return
        elif not up:
            await sendMessage(message, 'No RClone Destination!')
            await delete_links(message)
            return
        elif up not in ['rcl', 'gd', 'ddl']:
            if up.startswith('mrcc:'):
                config_path = f'wcl/{message.from_user.id}.conf'
            else:
                config_path = 'wcl.conf'
            if not await aiopath.exists(config_path):
                await sendMessage(message, f"RClone Config: {config_path} not Exists!")
                await delete_links(message)
                return
        if up != 'gd' and up != 'ddl' and not is_rclone_path(up):
            await sendMessage(message, 'Wrong Rclone Upload Destination!')
            await delete_links(message)
            return
    else:
        if user_dump and (user_dump.isdigit() or user_dump.startswith('-')):
            up = int(user_dump)
        elif user_dump and user_dump.startswith('@'):
            up = user_dump
        elif (ldumps := await fetch_user_dumps(message.from_user.id)):
            if user_dump and user_dump.casefold() == "all":
                up = [dump_id for dump_id in ldumps.values()]
            elif user_dump:
                up = next((dump_id for name_, dump_id in ldumps.items() if user_dump.casefold() == name_.casefold()), '')
            if not up and len(ldumps) == 1:
                up = next(iter(ldumps.values()))
            elif not up:
                up, is_cancelled = await open_dump_btns(message)
                if is_cancelled:
                    await delete_links(message)
                    return

    if link == 'rcl':
        link = await RcloneList(client, message).get_rclone_path('rcd')
        if not is_rclone_path(link):
            await sendMessage(message, link)
            await delete_links(message)
            return

    if up == 'rcl' and not isLeech:
        up = await RcloneList(client, message).get_rclone_path('rcu')
        if not is_rclone_path(up):
            await sendMessage(message, up)
            await delete_links(message)
            return

    listener = MirrorLeechListener(message, compress, extract, isQbit, isLeech, tag, select, seed,
                                    sameDir, rcf, up, join, drive_id=drive_id, index_link=index_link, 
                                    source_url=org_link or link, leech_utils={'screenshots': sshots, 'thumb': thumb})

    if file_ is not None:
        await delete_links(message)
        await TelegramDownloadHelper(listener).add_download(reply_to, f'{path}/', name, session, decrypter)
    elif isinstance(link, dict):
        await add_direct_download(link, path, listener, name)
    elif is_rclone_path(link):
        if link.startswith('mrcc:'):
            link = link.split('mrcc:', 1)[1]
            config_path = f'wcl/{message.from_user.id}.conf'
        else:
            config_path = 'wcl.conf'
        if not await aiopath.exists(config_path):
            await sendMessage(message, f"<b>RClone Config:</b> {config_path} not Exists!")
            await delete_links(message)
            return
        await add_rclone_download(link, config_path, f'{path}/', name, listener)
    elif is_gdrive_link(link):
        await delete_links(message)
        await add_gd_download(link, path, listener, name, org_link)
    elif is_mega_link(link):
        await delete_links(message)
        await add_mega_download(link, f'{path}/', listener, name)
    elif isQbit and 'real-debrid' not in link:
        await add_qb_torrent(link, path, listener, ratio, seed_time)
    elif not is_telegram_link(link):
        if ussr or pssw:
            auth = f"{ussr}:{pssw}"
            headers += f" authorization: Basic {b64encode(auth.encode()).decode('ascii')}"
        await add_aria2c_download(link, path, listener, name, headers, ratio, seed_time)
    await delete_links(message)


# ====== MODIFIED CALLBACK HANDLER TO INCLUDE COMBINE FUNCTIONALITY ======
@new_task
async def kpsmlxcb(_, query):
    message = query.message
    user_id = query.from_user.id
    data = query.data.split()
    
    if user_id != int(data[1]):
        return await query.answer(text="Not Yours!", show_alert=True)
    
    # ====== ADD THIS: Handle combine-related callbacks ======
    if query.data.startswith('select_file_') or query.data in ['start_combine', 'cancel_combine']:
        return await combine_callback(_, query)
    
    elif data[2] == "logdisplay":
        await query.answer()
        async with aiopen('log.txt', 'r') as f:
            logFileLines = (await f.read()).splitlines()
        def parseline(line):
            try:
                return "[" + line.split('] [', 1)[1]
            except IndexError:
                return line
        ind, Loglines = 1, ''
        try:
            while len(Loglines) <= 3500:
                Loglines = parseline(logFileLines[-ind]) + '\n' + Loglines
                if ind == len(logFileLines): 
                    break
                ind += 1
            startLine = f"<b>Showing Last {ind} Lines from log.txt:</b> \n\n----------<b>START LOG</b>----------\n\n"
            endLine = "\n----------<b>END LOG</b>----------"
            btn = ButtonMaker()
            btn.ibutton('Cʟᴏsᴇ', f'kpsmlx {user_id} close')
            await sendMessage(message, startLine + escape(Loglines) + endLine, btn.build_menu(1))
            await editReplyMarkup(message, None)
        except Exception as err:
            LOGGER.error(f"TG Log Display : {str(err)}")
    elif data[2] == "webpaste":
        await query.answer()
        async with aiopen('log.txt', 'r') as f:
            logFile = await f.read()
        cget = create_scraper().request
        resp = cget('POST', 'https://spaceb.in/api/v1/documents', data={'content': logFile, 'extension': 'None'}).json()
        if resp['status'] == 201:
            btn = ButtonMaker()
            btn.ubutton('📨 Web Paste (SB)', f"https://spaceb.in/{resp['payload']['id']}")
            await editReplyMarkup(message, btn.build_menu(1))
        else:
            LOGGER.error(f"Web Paste Failed : {str(err)}")
    elif data[2] == "botpm":
        await query.answer(url=f"https://t.me/{bot_name}?start=kpsmlx")
    elif data[2] == "help":
        await query.answer()
        btn = ButtonMaker()
        btn.ibutton('Cʟᴏsᴇ', f'kpsmlx {user_id} close')
        if data[3] == "CLONE":
            await editMessage(message, CLONE_HELP_MESSAGE[1], btn.build_menu(1))
        elif data[3] == "MIRROR":
            if len(data) == 4:
                msg = MIRROR_HELP_MESSAGE[1][:4000]
                btn.ibutton('Nᴇxᴛ Pᴀɢᴇ', f'kpsmlx {user_id} help MIRROR readmore')
            else:
                msg = MIRROR_HELP_MESSAGE[1][4000:]
                btn.ibutton('Pʀᴇ Pᴀɢᴇ', f'kpsmlx {user_id} help MIRROR')
            await editMessage(message, msg, btn.build_menu(2))
        if data[3] == "YT":
            await editMessage(message, YT_HELP_MESSAGE[1], btn.build_menu(1))
    elif data[2] == "guide":
        btn = ButtonMaker()
        btn.ibutton('Bᴀᴄᴋ', f'kpsmlx {user_id} guide home')
        btn.ibutton('Cʟᴏsᴇ', f'kpsmlx {user_id} close')
        if data[3] == "basic":
            await editMessage(message, help_string[0], btn.build_menu(2))
        elif data[3] == "users":
            await editMessage(message, help_string[1], btn.build_menu(2))
        elif data[3] == "miscs":
            await editMessage(message, help_string[3], btn.build_menu(2))
        elif data[3] == "admin":
            if not await CustomFilters.sudo('', query):
                return await query.answer('Not Sudo or Owner!', show_alert=True)
            await editMessage(message, help_string[2], btn.build_menu(2))
        else:
            buttons = ButtonMaker()
            buttons.ibutton('Basic', f'kpsmlx {user_id} guide basic')
            buttons.ibutton('Users', f'kpsmlx {user_id} guide users')
            buttons.ibutton('Mics', f'kpsmlx {user_id} guide miscs')
            buttons.ibutton('Owner & Sudos', f'kpsmlx {user_id} guide admin')
            buttons.ibutton('Close', f'kpsmlx {user_id} close')
            await editMessage(message, "㊂ <b><i>Help Guide Menu!</i></b>\n\n<b>NOTE: <i>Click on any CMD to see more minor detalis.</i></b>", buttons.build_menu(2))
        await query.answer()
    elif data[2] == "stats":
        msg, btn = await get_stats(query, data[3])
        await editMessage(message, msg, btn, 'IMAGES')
    else:
        await query.answer()
        await deleteMessage(message)
        if message.reply_to_message:
            await deleteMessage(message.reply_to_message)
            if message.reply_to_message.reply_to_message:
                await deleteMessage(message.reply_to_message.reply_to_message)


async def mirror(client, message):
    _mirror_leech(client, message)


async def qb_mirror(client, message):
    _mirror_leech(client, message, isQbit=True)


async def leech(client, message):
    _mirror_leech(client, message, isLeech=True)


async def qb_leech(client, message):
    _mirror_leech(client, message, isQbit=True, isLeech=True)


# ====== ADD NEW COMBINE COMMAND HANDLER AT THE END ======
bot.add_handler(MessageHandler(mirror, filters=command(
    BotCommands.MirrorCommand) & CustomFilters.authorized & ~CustomFilters.blacklisted))
bot.add_handler(MessageHandler(qb_mirror, filters=command(
    BotCommands.QbMirrorCommand) & CustomFilters.authorized & ~CustomFilters.blacklisted))
bot.add_handler(MessageHandler(leech, filters=command(
    BotCommands.LeechCommand) & CustomFilters.authorized & ~CustomFilters.blacklisted))
bot.add_handler(MessageHandler(qb_leech, filters=command(
    BotCommands.QbLeechCommand) & CustomFilters.authorized & ~CustomFilters.blacklisted))

# ====== ADD THIS NEW HANDLER FOR COMBINE COMMAND ======
bot.add_handler(MessageHandler(
    combine_command, 
    filters=command(BotCommands.CombineCommand) & CustomFilters.authorized & ~CustomFilters.blacklisted
))

bot.add_handler(CallbackQueryHandler(kpsmlxcb, filters=regex(r'^kpsml')))
