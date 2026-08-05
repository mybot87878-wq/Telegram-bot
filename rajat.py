import os
import asyncio
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())
import requests
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, \
    InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, \
    ChatMemberUpdated
from pyrogram.enums import ChatMemberStatus
import yt_dlp
from motor.motor_asyncio import AsyncIOMotorClient
import shlex
import csv
import io
import json
# ==================== CONFIGURATIONS ====================
API_ID = 31937622
API_HASH = "1d9b89edeccb63cc3936876054953698"
BOT_TOKEN = "8603916772:AAFMmMQvfuU2gZ_XILHDtekj-VJdBxkyfAI"
OWNER_USERNAME = "Kya_bacche"
OWNER_ID = 8714260394
# Sudo/Owner IDs (Add authorized user IDs here)
SUDO_USERS = {123456789, OWNER_ID}
START_GIF_URL = \
"https://giffiles.alphacoders.com/221/thumb-440-221968.mp4"
MINI_APP_URL = "https://powermusic.vercel.app/"
BOT_USERNAME = "test_hain_bot"
# MongoDB Configuration
MONGO_URL = \
"mongodb+srv://Mew:Rajat@cluster0.vpteszc.mongodb.net/?appName=Cluster0"
mongo_client = AsyncIOMotorClient(MONGO_URL)
db = mongo_client["tanjiro_music_bot"]
# Collections
locks_collection = db["group_locks"]
allowlist_collection = db["group_allowlist"]
WELCOMES_DB = db["group_welcomes"]
GOODBYES_DB = db["group_goodbyes"]
CLEAN_WELCOME_DB = db["group_clean_welcome"]
FILTERS_DB = db["group_filters"]
GBAN_DB = db["global_bans"]
GMUTE_DB = db["global_mutes"]
GWARN_DB = db["global_warns"]
BADWORDS_DB = db["group_badwords"]
GLOBALIST_DB = db["global_list"]
CHAT_FILTERS_DB = db["chat_filters"] # For custom chat filters & stickers
LOCKWARNS_DB = db["group_lockwarns"] # For lockwarns status
# Federation Collections
FEDS_DB = db["federations"]
FED_ADMINS_DB = db["federation_admins"]
FED_BANS_DB = db["federation_bans"]
FED_SETTINGS_DB = db["federation_settings"]
FED_LOGS_DB = db["federation_logs"]
FED_SUBS_DB = db["federation_subscriptions"]
CHAT_FED_DB = db["chat_federations"]
FED_PENDING_ADMINS_DB = db["federation_pending_admins"]
# =========================================================
SONG_CACHE = {}
USER_PLAYLISTS = {}
WAITING_FOR_PLAYLIST_NAME = set()
ALL_USERS = set()
print("Initializing Lightning-Fast Pyrogram Client...")
app = Client(
    "simple_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)
hindi_artists = ["Arijit Singh", "Jubin Nautiyal", "Shreya Ghoshal",
"Darshan Raval", "Atif Aslam", "Armaan Malik", "B Praak", "Neha Kakkar", "Vishal Mishra", "Sonu Nigam"]
hindi_song_titles = ["Kesariya", "Apna Bana Le", "Raataan Lambiyan",
"Tum Hi Ho", "Chaleya", "Heeriye", "Dil Jhoom", "O Mahi", "Sajni",
"Humnava Mere", "Pehle Bhi Main", "Tera Ghata", "Baarish",
"Khairiyat", "Naino Ne Baandhi", "Channa Mereya", "Ae Dil Hai Mushkil", "Tum Se Hi", "Kabira", "Ilahi"]
english_artists = ["Ed Sheeran", "The Weeknd", "Taylor Swift", "Justin Bieber", "Billie Eilish", "Dua Lipa", "Harry Styles", "Shawn Mendes", "Ariana Grande", "Post Malone"]
english_song_titles = ["Shape of You", "Blinding Lights", "As It Was", "Believer", "Watermelon Sugar", "Stay", "Anti-Hero", "Levitating",
"Peaches", "Bad Guy", "Flowers", "Starboy", "Save Your Tears",
"Mockingbird", "Despacito", "Senorita", "One Dance", "Someone You Loved", "Let Her Go", "Counting Stars"]
punjabi_artists = ["AP Dhillon", "Diljit Dosanjh", "Karan Aujla",
"Sidhu Moose Wala", "Shubh", "Karan Aujla", "Guru Randhawa", "Ammy Virk", "Jass Manak", "Parmish Verma"]
punjabi_song_titles = ["With You", "Obsessed", "Born to Shine",
"Excuses", "So High", "Brown Munde", "GOAT", "Softly", "Winning Speech", "IDGAF", "Elevated", "Levels", "Check It Out", "Tauba Tauba", "Lover", "Case", "Tera Mera Rishta", "Prada", "Lahore", "Illegal Weapon"]
haryanvi_artists = ["Sanju Rathod", "DG Immortal", "Raju Punjabi",
"Sapna Choudhary", "Masoom Sharma", "Renuka Panwar", "Ankit Baliyan",
"Gulzaar Chhaniwala", "Kavita Shibu", "Vikas Kumar"]
haryanvi_song_titles = ["Gulabi Sharara", "5 Foota 9 Inch", "Desi", "Solid Body", "Kabootar", "Bahu Kale Ki", "Jale 2", "Kabza",
"Salwar Suit", "Kade Aaja", "Billo", "Haryanvi Mashup", "Chora Haryane Ka", "Bhabhi", "Laad Piya Ke", "Khatola", "Gypsy", "Balam Ji", "Thada Bhartar", "Goli"]
HINDI_SONGS = [f"{title} {i} - {artist}" for i, (title, artist) in
enumerate(zip(hindi_song_titles * 10, hindi_artists * 10), 1)]
ENGLISH_SONGS = [f"{title} {i} - {artist}" for i, (title, artist) in
enumerate(zip(english_song_titles * 10, english_artists * 10), 1)]
PUNJABI_SONGS = [f"{title} {i} - {artist}" for i, (title, artist) in
enumerate(zip(punjabi_song_titles * 10, punjabi_artists * 10), 1)]
HARYANVI_SONGS = [f"{title} {i} - {artist}" for i, (title, artist) in
enumerate(zip(haryanvi_song_titles * 10, haryanvi_artists * 10), 1)]
SONGS_DB = {
"hindi": HINDI_SONGS,
"english": ENGLISH_SONGS,
"punjabi": PUNJABI_SONGS,
"haryanvi": HARYANVI_SONGS
}
TOP_SONGS = [f"Top Song {i} - Mega Artist" for i in range(1, 201)]
TOP_SONGS[0] = "Kesariya - Arijit Singh"
TOP_SONGS[1] = "Shape of You - Ed Sheeran"
TOP_SONGS[2] = "With You - AP Dhillon"
TOP_SONGS[3] = "Gulabi Sharara - Sanju Rathod"
TOP_SONGS[4] = "Blinding Lights - The Weeknd"
TOP_SONGS[5] = "As It Was - Harry Styles"
TOP_SONGS[6] = "Flowers - Miley Cyrus"
TOP_SONGS[7] = "Levitating - Dua Lipa" 
TOP_SONGS[8] = "Apna Bana Le - Arijit Singh"
TOP_SONGS[9] = "Heeriye - Jasleen Royal ft. Arijit Singh"
COLLECTIONS_SONGS = [
"Espresso - Sabrina Carpenter", "Beautiful Things - Benson Boone",
"Too Sweet - Hozier",
"BIRDS OF A FEATHER - Billie Eilish", "Gata Only - FloyMenor & Cris Mj", "I Had Some Help - Post Malone ft. Morgan Wallen",
"Lose Control - Teddy Swims", "We Can't Be Friends - Ariana Grande", "Texas Hold 'Em - Beyoncé",
"Greedy - Tate McRae", "Water - Tyla", "Paint The Town Red - Doja Cat", "Cruel Summer - Taylor Swift",
"Vampire - Olivia Rodrigo", "Fast Car - Luke Combs", "Houdini - Dua Lipa", "Is It Over Now? - Taylor Swift",
"Agora Hills - Doja Cat", "Standing Next to You - Jung Kook",
"Think U The Shit (Fuk U) - Ice Spice"
]
PERFORMER_TRACKS = [f"Performer Hit Track {i} - Star Artist" for i in
range(1, 1051)]
ARTIST_TRACKS = [f"Artist Trending Hit {i} - Super Star" for i in
range(1, 1051)]
SIMILAR_TRACKS = [f"Similar Track {i} - Matching Vibe" for i in
range(1, 1051)]
ALBUM_TRACKS = [f"Album Collection {i} - Studio Release" for i in
range(1, 1051)]
EXCLUSIVE_SHAYARI = [
"Khamoshi se pyaar karne ka maza hi kuch aur hai, yahan dard bhi apna aur humdard bhi apna hota hai.",
"Waqt ki rait par naam likhne se kya fayda, hawaayein tez ho toh sab mit jata hai.",
"Kitna bhi chaho kisi ko roye bina, yaadein aankhon mein nami chhod hi jaati hain."
]
for i in range(4, 501):
    EXCLUSIVE_SHAYARI.append(f"Zindagi ke safar ka yeh panna bhi khaas hai, jismein yaad hai teri aur dil ke paas hai (Shayari #{i}).")
# Rose Lock Types
VALID_LOCK_TYPES = [
"all", "album", "anonchannel", "audio", "bot", "botlink",
"button", "cashtag", "checklist",
"cjk", "collage", "command", "comment", "contact", "cyrillic",
"document", "email", "emoji",
"emojicustom", "emojigame", "emojionly", "externalreply",
"forward", "forwardbot", "forwardchannel",
"forwardstory", "forwarduser", "game", "gif", "guestbot", "inline", "invitelink", "location",
"outsidereaction", "phone", "photo", "poll", "reaction",
"richmessage", "rtl", "slideshow",
"spoiler", "sticker", "stickeranimate", "stickerpremium", "text",
"url", "video", "videonote",
"voice", "zalgo"
]
DEFAULT_WELCOME = "Hey {first}, welcome to {chat}!"
DEFAULT_GOODBYE = "Goodbye {first}, thanks for staying!"
async def send_custom_reply(message: Message, custom_text: str,
reply_markup=None, delay: int = 5):
    sent = await message.reply_text(custom_text,
    reply_markup=reply_markup)
    asyncio.create_task(delete_messages_after_delay(message, sent,
    delay))
    return sent
async def delete_messages_after_delay(user_msg: Message, bot_msg:
Message, delay: int):
    await asyncio.sleep(delay)
    try:
        await bot_msg.delete()
    except Exception:
        pass
    try:
        await user_msg.delete()
    except Exception:
        pass
def get_main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("NEW TRACKS",
        callback_data="new_tracks"), InlineKeyboardButton("TOP",
        callback_data="top_tracks_0")],
        [InlineKeyboardButton("COLLECTIONS",
        callback_data="collections_0"), InlineKeyboardButton("PRO",
        callback_data="pro_mode"), InlineKeyboardButton("PLAYLISTS",
        callback_data="playlists")],
        [InlineKeyboardButton("ADD TO YOUR GROUPS",
        url=f"https://t.me/{BOT_USERNAME}?startgroup=true"),
        InlineKeyboardButton("DEVELOPER",
        url=f"https://t.me/{OWNER_USERNAME}"), InlineKeyboardButton("⚡ FEATURES", callback_data="exciting")],
        [InlineKeyboardButton("🔴 START STREAM",
        web_app=WebAppInfo(url=MINI_APP_URL))]
    ]) 
def get_playlists_menu(user_id):
    user_playlists = USER_PLAYLISTS.get(user_id, {})
    keyboard_buttons = [[InlineKeyboardButton(f"📁 {pl}",
    callback_data=f"view_pl_{pl}")] for pl in user_playlists.keys()]
    keyboard_buttons.append([InlineKeyboardButton("➕ Create Playlist", callback_data="create_playlist_prompt")])
    keyboard_buttons.append([InlineKeyboardButton("« Menu",
    callback_data="back_to_menu")])
    return InlineKeyboardMarkup(keyboard_buttons)
def get_song_keyboard(song_query):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎧 Press to find any song",
        callback_data="open_dashboard_new")],
        [InlineKeyboardButton("•••",
        callback_data=f"opt1_{song_query}"), InlineKeyboardButton("🔴 Delete",
        callback_data="opt2_delete")]
    ])
def get_three_dots_menu(song_query):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("By performer",
        callback_data=f"opt_performer_{song_query}0")],
        [InlineKeyboardButton("Artist",
        callback_data=f"opt_artist{song_query}0")],
        [InlineKeyboardButton("Similar",
        callback_data=f"opt_similar{song_query}0")],
        [InlineKeyboardButton("Albums",
        callback_data=f"opt_albums{song_query}0")],
        [InlineKeyboardButton("🔓",
        callback_data=f"opt_dlt{song_query}")]
    ])
# ==================== HELPER FUNCTIONS FOR MODERATION ====================
async def is_sudo(user_id: int) -> bool:
    if user_id in SUDO_USERS:
        return True
    try:
        user_info = await app.get_users(user_id)
        if user_info.username and user_info.username.lower() == OWNER_USERNAME.lower():
            return True
    except Exception:
        pass
    return False 
async def is_admin(chat, user_id: int) -> bool:
    if await is_sudo(user_id):
        return True
    try:
        member = await chat.get_member(user_id)
        if member.status in [ChatMemberStatus.ADMINISTRATOR,
        ChatMemberStatus.OWNER]:
            return True
    except Exception:
        pass
    return False
async def extract_user(client: Client, message: Message):
    user_id = None
    user_name = "User"
    if message.reply_to_message and message.reply_to_message.from_user:
        target_user = message.reply_to_message.from_user
        return target_user.id, target_user.first_name
    if len(message.command) > 1:
        query = message.command[1].strip()
        if query.isdigit():
            user_id = int(query)
            try:
                user_info = await client.get_users(user_id)
                user_name = user_info.first_name
            except Exception:
                pass
            return user_id, user_name
        elif query.startswith("@"):
            try:
                user_info = await client.get_users(query)
                return user_info.id, user_info.first_name
            except Exception:
                return query, query
    return None, None
@app.on_message(filters.command("start", prefixes=["/", "\\!", "."]) &
filters.private)
async def start_cmd(client: Client, message: Message):
    user_id = message.from_user.id
    ALL_USERS.add(user_id)
    try:
        await message.reply_animation(animation=START_GIF_URL,
        caption="🎵 Welcome to Power Music Bot!", reply_markup=get_main_menu_keyboard())
    except Exception:
        await message.reply_text(text="🎵 Welcome to Power Music Bot!", reply_markup=get_main_menu_keyboard())
# --- ENFORCEMENT DECORATOR / HANDLER FOR NEW MESSAGES & LOCKS ---
@app.on_message(~filters.private & ~filters.bot, group=1)
async def enforcement_handler(client: Client, message: Message):
    if not message.from_user:
        return
    user_id = message.from_user.id
    chat = message.chat
    # 1. GBAN & Globalist & Federation Ban Check
    is_gbanned = await GBAN_DB.find_one({"user_id": user_id})
    is_globalisted = await GLOBALIST_DB.find_one({"user_id": user_id})
    fed_banned = False
    chat_fed = await CHAT_FED_DB.find_one({"chat_id": chat.id})
    if chat_fed:
        fed_id = chat_fed["fed_id"]
        # Check sub feds too
        fed_ids_to_check = [fed_id]
        async for sub in FED_SUBS_DB.find({"fed_id": fed_id}):
            fed_ids_to_check.append(sub["sub_fed_id"])
        for fid in fed_ids_to_check:
            fb = await FED_BANS_DB.find_one({"fed_id": fid, "user_id": user_id})
            if fb:
                fed_banned = True
                break
    if is_gbanned or is_globalisted or fed_banned:
        try:
            await chat.ban_member(user_id)
            await message.delete()
            # Check quietfed setting
            if chat_fed:
                s_doc = await FED_SETTINGS_DB.find_one({"fed_id": chat_fed["fed_id"]})
                if s_doc and s_doc.get("quietfed", False):
                    pass # Don't send notification
                else:
                    try:
                        await chat.send_message(f"⚠️ Fed-banned user {message.from_user.mention} tried to join/speak and was banned.") 
                    except Exception:
                        pass
            return
        except Exception:
            pass
    # 2. Skip checks if user is chat admin or sudo
    if await is_admin(chat, user_id):
        pass
    else:
        # Check active locks for this chat
        locks_doc = await locks_collection.find_one({"chat_id": chat.id})
        locked_items = locks_doc.get("locks", []) if locks_doc else []
        if locked_items:
            should_delete = False
            is_all = "all" in locked_items
            is_text = "text" in locked_items or is_all
            is_url = "url" in locked_items or ("url" in [l.lower() for l in locked_items]) or is_all
            is_sticker = "sticker" in locked_items or is_all
            is_photo = "photo" in locked_items or is_all
            is_video = "video" in locked_items or is_all
            is_audio = "audio" in locked_items or is_all
            is_voice = "voice" in locked_items or is_all
            is_document = "document" in locked_items or is_all
            is_gif = "gif" in locked_items or is_all
            is_forward = "forward" in locked_items or is_all
            is_game = "game" in locked_items or is_all
            is_poll = "poll" in locked_items or is_all
            is_contact = "contact" in locked_items or is_all
            is_inline = "inline" in locked_items or is_all
            is_invitelink = "invitelink" in locked_items or is_all
            is_command = "command" in locked_items or is_all
            if message.text:
                if is_text:
                    if message.text.startswith("/") and is_command:
                        should_delete = True
                    elif not message.text.startswith("/"):
                        should_delete = True
                if not should_delete and is_url:
                    if "http://" in message.text or "https://" in message.text or "t.me/" in message.text or "@" in message.text:
                        should_delete = True 
            if message.sticker and is_sticker:
                should_delete = True
            if message.photo and is_photo:
                should_delete = True
            if message.video and is_video:
                should_delete = True
            if message.audio and is_audio:
                should_delete = True
            if message.voice and is_voice:
                should_delete = True
            if message.document and is_document:
                should_delete = True
            if message.animation and is_gif:
                should_delete = True
            if (message.forward_from or message.forward_from_chat) and is_forward:
                should_delete = True
            if message.game and is_game:
                should_delete = True
            if message.poll and is_poll:
                should_delete = True
            if message.contact and is_contact:
                should_delete = True
            if message.via_bot and is_inline:
                should_delete = True
            if message.text and ("t.me/joinchat/" in message.text or "https://t.me/+" in message.text) and is_invitelink:
                should_delete = True
            if should_delete:
                try:
                    await message.delete()
                    lw_doc = await LOCKWARNS_DB.find_one({"chat_id": chat.id})
                    if lw_doc and lw_doc.get("status", True):
                        warn_msg = await chat.send_message(f"⚠️ Hey {message.from_user.mention}, that item is locked in this chat!")
                        asyncio.create_task(delete_messages_after_delay(message, warn_msg, 5))
                    return
                except Exception:
                    pass
    # 3. Custom Chat Filters Check
    if message.text or message.caption:
        text_content = message.text or message.caption
        words = [w.lower() for w in text_content.strip().split()] 
        filters_cursor = CHAT_FILTERS_DB.find({"chat_id": chat.id})
        async for filt in filters_cursor:
            trigger = filt["trigger"].lower()
            if trigger in words:
                reply_type = filt.get("reply_type", "text")
                if reply_type == "text":
                    await message.reply_text(filt["reply_content"])
                elif reply_type == "sticker":
                    await message.reply_sticker(filt["reply_content"])
                elif reply_type == "photo":
                    await message.reply_photo(filt["reply_content"], caption=filt.get("reply_caption"))
                elif reply_type == "animation":
                    await message.reply_animation(filt["reply_content"], caption=filt.get("reply_caption"))
                elif reply_type == "document":
                    await message.reply_document(filt["reply_content"], caption=filt.get("reply_caption"))
                elif reply_type == "audio":
                    await message.reply_audio(filt["reply_content"], caption=filt.get("reply_caption"))
                elif reply_type == "video":
                    await message.reply_video(filt["reply_content"], caption=filt.get("reply_caption"))
                break
# ==================== GREETINGS & GOODBYES HANDLER ====================
def parse_welcome_goodbye_template(template: str, user, chat):
    """
    Parses fillings: {first}, {last}, {fullname}, {username}, {id}, {chat}
    Supports inline buttons formatted like [Button Text](buttonurl:https://...)
    """
    first = user.first_name or "User"
    last = user.last_name or ""
    fullname = f"{first} {last}".strip()
    username = f"@{user.username}" if user.username else f"[@{first}](tg://user?id={user.id})"
    uid = str(user.id)
    chat_title = chat.title or "this chat"
    text = template.replace("{first}", first) 
    text = text.replace("{last}", last)
    text = text.replace("{fullname}", fullname)
    text = text.replace("{username}", username)
    text = text.replace("{id}", uid)
    text = text.replace("{chat}", chat_title)
    # Parse inline buttons if present in markdown format: [Text](buttonurl:URL)
    import re
    buttons = []
    button_pattern = r'\[([^\]]+)\]\(buttonurl:([^\)]+)\)'
    def replace_btn(match):
        btn_text = match.group(1)
        btn_url = match.group(2)
        buttons.append(InlineKeyboardButton(btn_text, url=btn_url))
        return ""
    text = re.sub(button_pattern, replace_btn, text)
    reply_markup = None
    if buttons:
        # Arrange in rows of 2 buttons max
        keyboard_rows = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]
        reply_markup = InlineKeyboardMarkup(keyboard_rows)
    return text.strip(), reply_markup
@app.on_chat_member_updated()
async def greetings_chat_member_updated(client: Client, member_update: ChatMemberUpdated):
    chat = member_update.chat
    # Check if someone joined or left
    old_status = member_update.old_chat_member.status if member_update.old_chat_member else ChatMemberStatus.UNKNOWN
    new_status = member_update.new_chat_member.status if member_update.new_chat_member else ChatMemberStatus.UNKNOWN
    user = member_update.new_chat_member.user if member_update.new_chat_member else None
    if not user:
        return
    # User joined the chat
    is_joined = old_status in [ChatMemberStatus.LEFT, ChatMemberStatus.BANNED, ChatMemberStatus.RESTRICTED] and new_status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
    # User left the chat
    is_left = old_status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER] and new_status in [ChatMemberStatus.LEFT, ChatMemberStatus.BANNED]
    if is_joined:
        # Federation ban check on join
        chat_fed = await CHAT_FED_DB.find_one({"chat_id": chat.id})
        if chat_fed:
            fed_id = chat_fed["fed_id"]
            fed_ids_to_check = [fed_id]
            async for sub in FED_SUBS_DB.find({"fed_id": fed_id}):
                fed_ids_to_check.append(sub["sub_fed_id"])
            for fid in fed_ids_to_check:
                fb = await FED_BANS_DB.find_one({"fed_id": fid, "user_id": user.id})
                if fb:
                    try:
                        await chat.ban_member(user.id)
                        s_doc = await FED_SETTINGS_DB.find_one({"fed_id": fed_id})
                        if not (s_doc and s_doc.get("quietfed", False)):
                            await chat.send_message(f"⚠️ Fed-banned user {user.mention} tried to join and was banned.")
                        return
                    except Exception:
                        pass
        # Check if welcome is enabled (Default: True)
        w_doc = await WELCOMES_DB.find_one({"chat_id": chat.id})
        is_welcome_enabled = w_doc.get("status", True) if w_doc else True
        if is_welcome_enabled:
            # Check cleanwelcome previous message deletion if enabled
            cw_doc = await CLEAN_WELCOME_DB.find_one({"chat_id": chat.id})
            if cw_doc and cw_doc.get("status", False):
                old_msg_id = cw_doc.get("last_welcome_msg_id")
                if old_msg_id:
                    try:
                        await client.delete_messages(chat.id, old_msg_id)
                    except Exception: 
                        pass
            template = w_doc.get("template", DEFAULT_WELCOME) if w_doc else DEFAULT_WELCOME
            parsed_text, reply_markup = parse_welcome_goodbye_template(template, user, chat)
            try:
                sent_msg = await chat.send_message(parsed_text, reply_markup=reply_markup)
                # If cleanwelcome is enabled, save message ID for deletion on next join or after 5 mins
                if cw_doc and cw_doc.get("status", False):
                    await CLEAN_WELCOME_DB.update_one(
                        {"chat_id": chat.id},
                        {"$set": {"last_welcome_msg_id": sent_msg.id}},
                        upsert=True
                    )
                # Also schedule deletion after 5 minutes
                async def delayed_clean():
                    await asyncio.sleep(300)
                    try:
                        await sent_msg.delete()
                    except Exception:
                        pass
                asyncio.create_task(delayed_clean())
            except Exception as e:
                print(f"Failed to send welcome message: {e}")
    elif is_left:
        # Check if goodbye is enabled (Default: False or True, let's keep default False unless enabled by admin)
        g_doc = await GOODBYES_DB.find_one({"chat_id": chat.id})
        if g_doc and g_doc.get("status", False):
            template = g_doc.get("template", DEFAULT_GOODBYE)
            parsed_text, reply_markup = parse_welcome_goodbye_template(template, user, chat)
            try:
                await chat.send_message(parsed_text, reply_markup=reply_markup)
            except Exception as e:
                print(f"Failed to send goodbye message: {e}")
# ==================== GREETINGS ADMIN COMMANDS ====================
@app.on_message(filters.command("welcome", prefixes=["/", "\\!", "."]) & ~filters.private)
async def welcome_toggle_command(client: Client, message: Message):
    chat = message.chat
    if not await is_admin(chat, message.from_user.id):
        await message.reply_text("❌ You must be an admin to use this command!")
        return
    if len(message.command) < 2:
        doc = await WELCOMES_DB.find_one({"chat_id": chat.id})
        status = "enabled" if (not doc or doc.get("status", True)) else "disabled"
        await message.reply_text(f"ℹ️ Welcome messages status: **{status}**\nUsage: `/welcome (yes/no/on/off)`")
        return
    val = message.command[1].lower()
    if val in ["yes", "on", "true"]:
        status = True
        text = "✅ Welcome messages have been **enabled**."
    elif val in ["no", "off", "false"]:
        status = False
        text = "❌ Welcome messages have been **disabled**."
    else:
        await message.reply_text("⚠️ Invalid option! Use `/welcome on` or `/welcome off`.")
        return
    await WELCOMES_DB.update_one(
        {"chat_id": chat.id},
        {"$set": {"status": status}},
        upsert=True
    )
    await message.reply_text(text)
@app.on_message(filters.command("goodbye", prefixes=["/", "\\!", "."]) & ~filters.private)
async def goodbye_toggle_command(client: Client, message: Message):
    chat = message.chat
    if not await is_admin(chat, message.from_user.id):
        await message.reply_text("❌ You must be an admin to use this command!")
        return
    if len(message.command) < 2:
        doc = await GOODBYES_DB.find_one({"chat_id": chat.id})
        status = "enabled" if (doc and doc.get("status", False)) else "disabled"
        await message.reply_text(f"ℹ️ Goodbye messages status: **{status}**\nUsage: `/goodbye (yes/no/on/off)`")
        return
    val = message.command[1].lower()
    if val in ["yes", "on", "true"]:
        status = True
        text = "✅ Goodbye messages have been **enabled**."
    elif val in ["no", "off", "false"]:
        status = False
        text = "❌ Goodbye messages have been **disabled**."
    else:
        await message.reply_text("⚠️ Invalid option! Use `/goodbye on` or `/goodbye off`.")
        return
    await GOODBYES_DB.update_one(
        {"chat_id": chat.id},
        {"$set": {"status": status}},
        upsert=True
    )
    await message.reply_text(text)
@app.on_message(filters.command("setwelcome", prefixes=["/", "\\!", "."]) & ~filters.private)
async def setwelcome_command(client: Client, message: Message):
    chat = message.chat
    if not await is_admin(chat, message.from_user.id):
        await message.reply_text("❌ You must be an admin to use this command!")
        return
    if len(message.command) < 2 and not message.reply_to_message:
        await message.reply_text("⚠️ Usage: `/setwelcome <text>` or reply to a message with `/setwelcome`.\nFillings: `{first}`, `{last}`, `{fullname}`, `{username}`, `{id}`, `{chat}`\nButtons format: `[Button Text](buttonurl:https://...)`")
        return
    template = ""
    if message.reply_to_message and message.reply_to_message.text:
        template = message.reply_to_message.text.markdown
    else:
        try:
            template = message.text.markdown.split(None, 1)[1]
        except Exception: 
            template = ""
    if not template:
        await message.reply_text("❌ Please provide a valid welcome message template.")
        return
    await WELCOMES_DB.update_one(
        {"chat_id": chat.id},
        {"$set": {"template": template, "status": True}},
        upsert=True
    )
    await message.reply_text("✅ Successfully updated the custom welcome message!")
@app.on_message(filters.command("resetwelcome", prefixes=["/", "\\!", "."]) & ~filters.private)
async def resetwelcome_command(client: Client, message: Message):
    chat = message.chat
    if not await is_admin(chat, message.from_user.id):
        await message.reply_text("❌ You must be an admin to use this command!")
        return
    await WELCOMES_DB.update_one(
        {"chat_id": chat.id},
        {"$set": {"template": DEFAULT_WELCOME, "status": True}},
        upsert=True
    )
    await message.reply_text("🔄 Welcome message has been reset to default.")
@app.on_message(filters.command("setgoodbye", prefixes=["/", "\\!", "."]) & ~filters.private)
async def setgoodbye_command(client: Client, message: Message):
    chat = message.chat
    if not await is_admin(chat, message.from_user.id):
        await message.reply_text("❌ You must be an admin to use this command!")
        return
    if len(message.command) < 2 and not message.reply_to_message:
        await message.reply_text("⚠️ Usage: `/setgoodbye <text>` or reply to a message with `/setgoodbye`.\nFillings: `{first}`, `{last}`, `{fullname}`, `{username}`, `{id}`, `{chat}`\nButtons format: `[Button Text](buttonurl:https://...)`") 
        return
    template = ""
    if message.reply_to_message and message.reply_to_message.text:
        template = message.reply_to_message.text.markdown
    else:
        try:
            template = message.text.markdown.split(None, 1)[1]
        except Exception:
            template = ""
    if not template:
        await message.reply_text("❌ Please provide a valid goodbye message template.")
        return
    await GOODBYES_DB.update_one(
        {"chat_id": chat.id},
        {"$set": {"template": template, "status": True}},
        upsert=True
    )
    await message.reply_text("✅ Successfully updated the custom goodbye message!")
@app.on_message(filters.command("resetgoodbye", prefixes=["/", "\\!", "."]) & ~filters.private)
async def resetgoodbye_command(client: Client, message: Message):
    chat = message.chat
    if not await is_admin(chat, message.from_user.id):
        await message.reply_text("❌ You must be an admin to use this command!")
        return
    await GOODBYES_DB.update_one(
        {"chat_id": chat.id},
        {"$set": {"template": DEFAULT_GOODBYE, "status": False}},
        upsert=True
    )
    await message.reply_text("🔄 Goodbye message has been reset to default and disabled.")
@app.on_message(filters.command("cleanwelcome", prefixes=["/", "\\!", "."]) & ~filters.private)
async def cleanwelcome_command(client: Client, message: Message):
    chat = message.chat
    if not await is_admin(chat, message.from_user.id): 
        await message.reply_text("❌ You must be an admin to use this command!")
        return
    if len(message.command) < 2:
        doc = await CLEAN_WELCOME_DB.find_one({"chat_id": chat.id})
        status = "enabled" if (doc and doc.get("status", False)) else "disabled"
        await message.reply_text(f"ℹ️ Cleanwelcome status: **{status}**\nUsage: `/cleanwelcome (yes/no/on/off)`")
        return
    val = message.command[1].lower()
    if val in ["yes", "on", "true"]:
        status = True
        text = "✅ Cleanwelcome has been **enabled**. Old welcome messages will now be deleted after 5 minutes or when a new person joins."
    elif val in ["no", "off", "false"]:
        status = False
        text = "❌ Cleanwelcome has been **disabled**."
    else:
        await message.reply_text("⚠️ Invalid option! Use `/cleanwelcome on` or `/cleanwelcome off`.")
        return
    await CLEAN_WELCOME_DB.update_one(
        {"chat_id": chat.id},
        {"$set": {"status": status}},
        upsert=True
    )
    await message.reply_text(text)
# ==================== LOCK COMMANDS ====================
@app.on_message(filters.command("lock", prefixes=["/", "\\!", "."]) & ~filters.private)
async def lock_items_command(client: Client, message: Message):
    chat = message.chat
    if not await is_admin(chat, message.from_user.id):
        await message.reply_text("❌ You must be an admin to use this command!")
        return
    if len(message.command) < 2:
        await message.reply_text("⚠️ Usage: `/lock <item(s)>`\nUse `/locktypes` to see all lockable items.")
        return 
    items_to_lock = [arg.lower() for arg in message.command[1:]]
    invalid_items = [item for item in items_to_lock if item not in VALID_LOCK_TYPES]
    if invalid_items:
        await message.reply_text(f"❌ Invalid lock type(s): `{'`, `'.join(invalid_items)}`\nUse `/locktypes` to view valid items.")
        return
    doc = await locks_collection.find_one({"chat_id": chat.id})
    current_locks = doc.get("locks", []) if doc else []
    added = []
    for item in items_to_lock:
        if item == "all":
            current_locks = list(VALID_LOCK_TYPES)
            added = ["all"]
            break
        elif item not in current_locks:
            current_locks.append(item)
            added.append(item)
    await locks_collection.update_one(
        {"chat_id": chat.id},
        {"$set": {"locks": current_locks}},
        upsert=True
    )
    if added:
        await message.reply_text(f"🔒 Locked successfully: `{'`, `'.join(added)}`")
    else:
        await message.reply_text("ℹ️ Specified item(s) are already locked!")
@app.on_message(filters.command("unlock", prefixes=["/", "\\!", "."]) & ~filters.private)
async def unlock_items_command(client: Client, message: Message):
    chat = message.chat
    if not await is_admin(chat, message.from_user.id):
        await message.reply_text("❌ You must be an admin to use this command!")
        return
    if len(message.command) < 2:
        await message.reply_text("⚠️ Usage: `/unlock <item(s)>`") 
        return
    items_to_unlock = [arg.lower() for arg in message.command[1:]]
    doc = await locks_collection.find_one({"chat_id": chat.id})
    if not doc or not doc.get("locks"):
        await message.reply_text("📭 No items are currently locked in this chat.")
        return
    current_locks = doc["locks"]
    removed = []
    for item in items_to_unlock:
        if item == "all":
            current_locks = []
            removed = ["all"]
            break
        elif item in current_locks:
            current_locks.remove(item)
            removed.append(item)
    await locks_collection.update_one(
        {"chat_id": chat.id},
        {"$set": {"locks": current_locks}},
        upsert=True
    )
    if removed:
        await message.reply_text(f"🔓 Unlocked successfully: `{'`, `'.join(removed)}`")
    else:
        await message.reply_text("❌ Specified item(s) were not locked.")
@app.on_message(filters.command("locks", prefixes=["/", "\\!", "."]) & ~filters.private)
async def list_locks_command(client: Client, message: Message):
    chat = message.chat
    doc = await locks_collection.find_one({"chat_id": chat.id})
    current_locks = doc.get("locks", []) if doc else []
    if not current_locks:
        await message.reply_text("🔓 No items are currently locked in this chat.")
        return 
    text = f"🔒 **Currently Locked Items ({len(current_locks)}):**\n\n"
    for item in current_locks:
        text += f"• `{item}`\n"
    await message.reply_text(text)
@app.on_message(filters.command("lockwarns", prefixes=["/", "\\!", "."]) & ~filters.private)
async def lockwarns_command(client: Client, message: Message):
    chat = message.chat
    if not await is_admin(chat, message.from_user.id):
        await message.reply_text("❌ You must be an admin to use this command!")
        return
    if len(message.command) < 2:
        doc = await LOCKWARNS_DB.find_one({"chat_id": chat.id})
        status = "enabled" if (not doc or doc.get("status", True)) else "disabled"
        await message.reply_text(f"ℹ️ Lockwarns status: **{status}**\nUsage: `/lockwarns <yes/no/on/off>`")
        return
    val = message.command[1].lower()
    if val in ["yes", "on", "true"]:
        status = True
        text = "✅ Lockwarns has been **enabled**."
    elif val in ["no", "off", "false"]:
        status = False
        text = "❌ Lockwarns has been **disabled**."
    else:
        await message.reply_text("⚠️ Invalid option! Use `/lockwarns on` or `/lockwarns off`.")
        return
    await LOCKWARNS_DB.update_one(
        {"chat_id": chat.id},
        {"$set": {"status": status}},
        upsert=True
    )
    await message.reply_text(text)
@app.on_message(filters.command("locktypes", prefixes=["/", "\\!", "."]) & ~filters.private)
async def locktypes_command(client: Client, message: Message):
    text = "📋 **All Lockable Items (Rose Style):**\n\n" 
    chunked = [", ".join(VALID_LOCK_TYPES[i:i+3]) for i in range(0, len(VALID_LOCK_TYPES), 3)]
    text += "\n".join([f"• `{chunk}`" for chunk in chunked])
    await message.reply_text(text)
# ==================== FEDERATION COMMANDS ====================
async def log_fed_event(client: Client, fed_id: str, text: str):
    s_doc = await FED_SETTINGS_DB.find_one({"fed_id": fed_id})
    if s_doc and s_doc.get("log_chat_id"):
        try:
            await client.send_message(s_doc["log_chat_id"], f"ℹ️ [FedLog]: {text}")
        except Exception:
            pass
    # Also check fed owner PM notification
    fed_doc = await FEDS_DB.find_one({"fed_id": fed_id})
    if fed_doc:
        owner_id = fed_doc["owner_id"]
        if s_doc and s_doc.get("fednotif", True):
            try:
                await client.send_message(owner_id, f"🔔 [Fed Notification - {fed_doc['name']}]: {text}")
            except Exception:
                pass
@app.on_message(filters.command("newfed", prefixes=["/", "\\!", "."]))
async def newfed_cmd(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("⚠️ Usage: <code>/newfed &lt;fedname&gt;</code>", parse_mode=enums.ParseMode.HTML)
        return
    fedname = message.command[1].strip()
    user_id = message.from_user.id
    existing_fed = await FEDS_DB.find_one({"owner_id": user_id})
    if existing_fed:
        await message.reply_text("❌ You already own a federation! Only one federation per user is allowed.")
        return
    import uuid
    fed_id = str(uuid.uuid4())
    await FEDS_DB.insert_one({"fed_id": fed_id, "name": fedname, "owner_id": user_id})
    await FED_ADMINS_DB.insert_one({"fed_id": fed_id, "user_id": user_id})
    await FED_SETTINGS_DB.insert_one({"fed_id": fed_id, "fednotif": True, "fedreason": True, "quietfed": False}) 
    await message.reply_text(f"🎉 Successfully created federation **{fedname}**!\nFederation ID: `{fed_id}`")
@app.on_message(filters.command("renamefed", prefixes=["/", "\\!", "."]))
async def renamefed_cmd(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("⚠️ Usage: `/renamefed <fedname>`")
        return
    fedname = message.command[1].strip()
    user_id = message.from_user.id
    fed = await FEDS_DB.find_one({"owner_id": user_id})
    if not fed:
        await message.reply_text("❌ You do not own any federation!")
        return
    await FEDS_DB.update_one({"fed_id": fed["fed_id"]}, {"$set": {"name": fedname}})
    await message.reply_text(f"✅ Successfully renamed federation to **{fedname}**.")
@app.on_message(filters.command("delfed", prefixes=["/", "\\!", "."]))
async def delfed_cmd(client: Client, message: Message):
    user_id = message.from_user.id
    fed = await FEDS_DB.find_one({"owner_id": user_id})
    if not fed:
        await message.reply_text("❌ You do not own any federation!")
        return
    fed_id = fed["fed_id"]
    await FEDS_DB.delete_one({"fed_id": fed_id})
    await FED_ADMINS_DB.delete_many({"fed_id": fed_id})
    await FED_BANS_DB.delete_many({"fed_id": fed_id})
    await FED_SETTINGS_DB.delete_many({"fed_id": fed_id})
    await FED_SUBS_DB.delete_many({"fed_id": fed_id})
    await CHAT_FED_DB.delete_many({"fed_id": fed_id})
    await message.reply_text("🗑️ Your federation has been deleted successfully along with all related info.")
@app.on_message(filters.command("fedtransfer", prefixes=["/", "\\!", "."]))
async def fedtransfer_cmd(client: Client, message: Message):
    user_id = message.from_user.id
    fed = await FEDS_DB.find_one({"owner_id": user_id})
    if not fed: 
        await message.reply_text("❌ You do not own any federation!")
        return
    target_id, target_name = await extract_user(client, message)
    if not target_id:
        await message.reply_text("⚠️ Please reply to a user or provide a valid User ID/Username to transfer your federation.")
        return
    fed_id = fed["fed_id"]
    await FEDS_DB.update_one({"fed_id": fed_id}, {"$set": {"owner_id": target_id}})
    await FED_ADMINS_DB.update_one({"fed_id": fed_id, "user_id": user_id}, {"$set": {"user_id": target_id}}, upsert=True)
    await message.reply_text(f"✅ Successfully transferred federation ownership to **{target_name}** (`{target_id}`).")
@app.on_message(filters.command("fedpromote", prefixes=["/", "\\!", "."]))
async def fedpromote_cmd(client: Client, message: Message):
    user_id = message.from_user.id
    fed = await FEDS_DB.find_one({"owner_id": user_id})
    if not fed:
        await message.reply_text("❌ You do not own any federation!")
        return
    target_id, target_name = await extract_user(client, message)
    if not target_id:
        await message.reply_text("⚠️ Please reply to a user or provide a valid User ID/Username to promote.")
        return
    fed_id = fed["fed_id"]
    existing = await FED_ADMINS_DB.find_one({"fed_id": fed_id, "user_id": target_id})
    if existing:
        await message.reply_text(f"ℹ️ User {target_name} is already a federation admin.")
        return
    # Send confirmation message to user PM or reply
    await FED_PENDING_ADMINS_DB.update_one({"fed_id": fed_id, "user_id": target_id}, {"$set": {"status": "pending"}}, upsert=True)
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Accept FedAdmin", callback_data=f"accept_fedadmin_{fed_id}"), InlineKeyboardButton("❌ Decline", callback_data=f"decline_fedadmin_{fed_id}")]
    ]) 
    try:
        await client.send_message(target_id, f"📬 You have been invited to become a federation admin for **{fed['name']}**. Do you accept?", reply_markup=keyboard)
        await message.reply_text(f"✅ Sent confirmation request to **{target_name}** for federation admin role.")
    except Exception:
        # Fallback if bot can't PM user
        await FED_ADMINS_DB.insert_one({"fed_id": fed_id, "user_id": target_id})
        await message.reply_text(f"✅ Promoted **{target_name}** to federation admin successfully (Could not send PM).")
@app.on_message(filters.command("feddemote", prefixes=["/", "\\!", "."]))
async def feddemote_cmd(client: Client, message: Message):
    user_id = message.from_user.id
    fed = await FEDS_DB.find_one({"owner_id": user_id})
    if not fed:
        await message.reply_text("❌ You do not own any federation!")
        return
    target_id, target_name = await extract_user(client, message)
    if not target_id:
        await message.reply_text("⚠️ Please reply to a user or provide a valid User ID/Username to demote.")
        return
    fed_id = fed["fed_id"]
    if target_id == user_id:
        await message.reply_text("❌ You cannot demote yourself as owner! Use `/feddemoteme` instead.")
        return
    res = await FED_ADMINS_DB.delete_one({"fed_id": fed_id, "user_id": target_id})
    if res.deleted_count > 0:
        await message.reply_text(f"✅ Successfully demoted **{target_name}** from federation admin.")
    else:
        await message.reply_text("❌ User is not an admin in your federation.")
@app.on_message(filters.command("feddemoteme", prefixes=["/", "\\!", "."]))
async def feddemoteme_cmd(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("⚠️ Usage: /feddemoteme <fedID>")

        return
    fed_id = message.command[1].strip()
    user_id = message.from_user.id
    fed = await FEDS_DB.find_one({"fed_id": fed_id})
    if not fed:
        await message.reply_text("❌ Federation not found.")
        return
    if fed["owner_id"] == user_id:
        await message.reply_text("❌ You are the owner of this federation! You cannot demote yourself.")
        return
    res = await FED_ADMINS_DB.delete_one({"fed_id": fed_id, "user_id": user_id})
    if res.deleted_count > 0:
        await message.reply_text("✅ You have successfully demoted yourself from this federation.")
    else:
        await message.reply_text("❌ You are not an admin in this federation.")
@app.on_message(filters.command("myfeds", prefixes=["/", "\\!", "."]))
async def myfeds_cmd(client: Client, message: Message):
    user_id = message.from_user.id
    feds_list = []
    async for admin_doc in FED_ADMINS_DB.find({"user_id": user_id}):
        fed_doc = await FEDS_DB.find_one({"fed_id": admin_doc["fed_id"]})
        if fed_doc:
            role = "Owner" if fed_doc["owner_id"] == user_id else "Admin"
            feds_list.append(f"• **{fed_doc['name']}** (`{fed_doc['fed_id']}`) - *{role}*")
    if not feds_list:
        await message.reply_text("📭 You are not an admin in any federation.")
        return
    await message.reply_text(f"📋 **Your Federations:**\n\n" + "\n".join(feds_list))
@app.on_message(filters.command("fban", prefixes=["/", "\\!", "."]))
async def fban_cmd(client: Client, message: Message):
    chat = message.chat
    chat_fed = await CHAT_FED_DB.find_one({"chat_id": chat.id}) 
    if not chat_fed:
        await message.reply_text("❌ This chat is not in any federation!")
        return
    fed_id = chat_fed["fed_id"]
    user_id = message.from_user.id
    is_fed_admin = await FED_ADMINS_DB.find_one({"fed_id": fed_id, "user_id": user_id})
    fed_doc = await FEDS_DB.find_one({"fed_id": fed_id})
    is_owner = fed_doc and fed_doc["owner_id"] == user_id
    if not (is_fed_admin or is_owner or await is_sudo(user_id)):
        await message.reply_text("❌ You must be a federation admin to use `/fban`.")
        return
    # Check reason setting
    s_doc = await FED_SETTINGS_DB.find_one({"fed_id": fed_id})
    requires_reason = s_doc.get("fedreason", True) if s_doc else True
    target_id, target_name = await extract_user(client, message)
    if not target_id:
        await message.reply_text("⚠️ Please reply to a user or provide a valid User ID/Username to fban.")
        return
    # Extract reason if any
    reason = "No reason provided."
    if len(message.command) > 2:
        reason = " ".join(message.command[2:])
    elif message.reply_to_message and len(message.command) > 1:
        reason = " ".join(message.command[1:])
    if requires_reason and reason == "No reason provided.":
        await message.reply_text("⚠️ This federation requires a reason for fbans. Please provide a reason.")
        return
    await FED_BANS_DB.update_one(
        {"fed_id": fed_id, "user_id": target_id},
        {"$set": {"name": str(target_name), "reason": reason, "admin_id": user_id}},
        upsert=True
    )
    try: 
        await chat.ban_member(target_id)
    except Exception:
        pass
    await message.reply_text(f"🎉 Successfully Fed-banned **{target_name}** (`{target_id}`).\nReason: `{reason}`")
    await log_fed_event(client, fed_id, f"User {target_name} (`{target_id}`) was fbanned by admin. Reason: {reason}")
@app.on_message(filters.command("unfban", prefixes=["/", "\\!", "."]))
async def unfban_cmd(client: Client, message: Message):
    chat = message.chat
    chat_fed = await CHAT_FED_DB.find_one({"chat_id": chat.id})
    if not chat_fed:
        await message.reply_text("❌ This chat is not in any federation!")
        return
    fed_id = chat_fed["fed_id"]
    user_id = message.from_user.id
    is_fed_admin = await FED_ADMINS_DB.find_one({"fed_id": fed_id, "user_id": user_id})
    fed_doc = await FEDS_DB.find_one({"fed_id": fed_id})
    is_owner = fed_doc and fed_doc["owner_id"] == user_id
    if not (is_fed_admin or is_owner or await is_sudo(user_id)):
        await message.reply_text("❌ You must be a federation admin to use `/unfban`.")
        return
    target_id, target_name = await extract_user(client, message)
    if not target_id:
        await message.reply_text("⚠️ Please reply to a user or provide a valid User ID/Username to unfban.")
        return
    res = await FED_BANS_DB.delete_one({"fed_id": fed_id, "user_id": target_id})
    if res.deleted_count > 0:
        try:
            await chat.unban_member(target_id)
        except Exception:
            pass
        await message.reply_text(f"✅ Successfully un-fbanned user (`{target_id}`).")
        await log_fed_event(client, fed_id, f"User (`{target_id}`) was un-fbanned.") 
    else:
        await message.reply_text("❌ User is not banned in this federation.")
@app.on_message(filters.command("fednotif", prefixes=["/", "\\!", "."]))
async def fednotif_cmd(client: Client, message: Message):
    user_id = message.from_user.id
    fed = await FEDS_DB.find_one({"owner_id": user_id})
    if not fed:
        await message.reply_text("❌ You do not own any federation!")
        return
    if len(message.command) < 2:
        s_doc = await FED_SETTINGS_DB.find_one({"fed_id": fed["fed_id"]})
        status = "enabled" if (s_doc and s_doc.get("fednotif", True)) else "disabled"
        await message.reply_text(f"ℹ️ Fednotif status: **{status}**\nUsage: `/fednotif <yes/no/on/off>`")
        return
    val = message.command[1].lower()
    status = val in ["yes", "on", "true"]
    await FED_SETTINGS_DB.update_one({"fed_id": fed["fed_id"]}, {"$set": {"fednotif": status}}, upsert=True)
    await message.reply_text(f"✅ Federation notifications set to: **{status}**")
@app.on_message(filters.command("fedreason", prefixes=["/", "\\!", "."]))
async def fedreason_cmd(client: Client, message: Message):
    user_id = message.from_user.id
    fed = await FEDS_DB.find_one({"owner_id": user_id})
    if not fed:
        await message.reply_text("❌ You do not own any federation!")
        return
    if len(message.command) < 2:
        s_doc = await FED_SETTINGS_DB.find_one({"fed_id": fed["fed_id"]})
        status = "enabled" if (s_doc and s_doc.get("fedreason", True)) else "disabled"
        await message.reply_text(f"ℹ️ Fedreason status: **{status}**\nUsage: `/fedreason <yes/no/on/off>`")
        return
    val = message.command[1].lower() 
    status = val in ["yes", "on", "true"]
    await FED_SETTINGS_DB.update_one({"fed_id": fed["fed_id"]}, {"$set": {"fedreason": status}}, upsert=True)
    await message.reply_text(f"✅ Federation reason requirement set to: **{status}**")
@app.on_message(filters.command("subfed", prefixes=["/", "\\!", "."]))
async def subfed_cmd(client: Client, message: Message):
    user_id = message.from_user.id
    fed = await FEDS_DB.find_one({"owner_id": user_id})
    if not fed:
        await message.reply_text("❌ You do not own any federation!")
        return
    if len(message.command) < 2:
        await message.reply_text("⚠️ Usage: `/subfed <FedId>`")
        return
    sub_fed_id = message.command[1].strip()
    target_fed = await FEDS_DB.find_one({"fed_id": sub_fed_id})
    if not target_fed:
        await message.reply_text("❌ Target federation not found.")
        return
    if sub_fed_id == fed["fed_id"]:
        await message.reply_text("❌ You cannot subscribe to your own federation.")
        return
    await FED_SUBS_DB.update_one(
        {"fed_id": fed["fed_id"], "sub_fed_id": sub_fed_id},
        {"$set": {"name": target_fed["name"]}},
        upsert=True
    )
    await message.reply_text(f"✅ Successfully subscribed to federation **{target_fed['name']}**.")
@app.on_message(filters.command("unsubfed", prefixes=["/", "\\!", "."]))
async def unsubfed_cmd(client: Client, message: Message):
    user_id = message.from_user.id
    fed = await FEDS_DB.find_one({"owner_id": user_id})
    if not fed:
        await message.reply_text("❌ You do not own any federation!")
        return
    if len(message.command) < 2:
        await message.reply_text("⚠️ Usage: `/unsubfed <FedId>`") 
        return
    sub_fed_id = message.command[1].strip()
    res = await FED_SUBS_DB.delete_one({"fed_id": fed["fed_id"], "sub_fed_id": sub_fed_id})
    if res.deleted_count > 0:
        await message.reply_text("✅ Successfully unsubscribed from the federation.")
    else:
        await message.reply_text("❌ You were not subscribed to this federation.")
@app.on_message(filters.command("fedexport", prefixes=["/", "\\!", "."]))
async def fedexport_cmd(client: Client, message: Message):
    user_id = message.from_user.id
    fed = await FEDS_DB.find_one({"owner_id": user_id})
    if not fed:
        await message.reply_text("❌ You do not own any federation!")
        return
    fed_id = fed["fed_id"]
    export_type = "csv"
    if len(message.command) > 1:
        export_type = message.command[1].lower()
    bans = []
    async for b in FED_BANS_DB.find({"fed_id": fed_id}):
        bans.append(b)
    if not bans:
        await message.reply_text("📭 No banned users in your federation to export.")
        return
    if export_type == "json":
        data = [{"user_id": b["user_id"], "name": b.get("name"), "reason": b.get("reason")} for b in bans]
        file_content = json.dumps(data, indent=4)
        file_obj = io.BytesIO(file_content.encode("utf-8"))
        file_obj.name = f"fed_bans_{fed_id}.json"
        await message.reply_document(file_obj, caption="📁 Here is your federation banlist in JSON format.")
    else:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["user_id", "name", "reason"])
        for b in bans: 
            writer.writerow([b["user_id"], b.get("name", ""), b.get("reason", "")])
        file_content = output.getvalue()
        file_obj = io.BytesIO(file_content.encode("utf-8"))
        file_obj.name = f"fed_bans_{fed_id}.csv"
        await message.reply_document(file_obj, caption="📁 Here is your federation banlist in CSV format.")
@app.on_message(filters.command("fedimport", prefixes=["/", "\\!", "."]))
async def fedimport_cmd(client: Client, message: Message):
    user_id = message.from_user.id
    fed = await FEDS_DB.find_one({"owner_id": user_id})
    if not fed:
        await message.reply_text("❌ You do not own any federation!")
        return
    if not message.reply_to_message or not message.reply_to_message.document:
        await message.reply_text("⚠️ Please reply to a exported banlist document with `/fedimport <overwrite/keep> <csv/json>`")
        return
    mode = "keep"
    if len(message.command) > 1 and message.command[1].lower() in ["overwrite", "keep"]:
        mode = message.command[1].lower()
    if mode == "overwrite":
        await FED_BANS_DB.delete_many({"fed_id": fed["fed_id"]})
    file_path = await client.download_media(message.reply_to_message)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            if file_path.endswith(".json"):
                data = json.loads(content)
                for item in data:
                    await FED_BANS_DB.update_one(
                        {"fed_id": fed["fed_id"], "user_id": item["user_id"]},
                        {"$set": {"name": item.get("name", "Unknown"), "reason": item.get("reason", "Imported")}},
                        upsert=True
                    )
            else:
                reader = csv.reader(content.splitlines())
                next(reader, None) # skip header 
                for row in reader:
                    if len(row) >= 1:
                        uid = int(row[0])
                        name = row[1] if len(row) > 1 else "Unknown"
                        reason = row[2] if len(row) > 2 else "Imported"
                        await FED_BANS_DB.update_one(
                            {"fed_id": fed["fed_id"], "user_id": uid},
                            {"$set": {"name": name, "reason": reason}},
                            upsert=True
                        )
        await message.reply_text("✅ Successfully imported federation banlist!")
    except Exception as e:
        await message.reply_text(f"❌ Failed to import file: {e}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
@app.on_message(filters.command("setfedlog", prefixes=["/", "\\!", "."]) & ~filters.private)
async def setfedlog_cmd(client: Client, message: Message):
    chat = message.chat
    if not await is_admin(chat, message.from_user.id):
        await message.reply_text("❌ You must be an admin to use this command!")
        return
    chat_fed = await CHAT_FED_DB.find_one({"chat_id": chat.id})
    if not chat_fed:
        await message.reply_text("❌ This chat is not in any federation!")
        return
    fed_id = chat_fed["fed_id"]
    fed = await FEDS_DB.find_one({"fed_id": fed_id})
    if not fed or fed["owner_id"] != message.from_user.id:
        await message.reply_text("❌ You must be the owner of the federation to set the log channel.")
        return
    await FED_SETTINGS_DB.update_one({"fed_id": fed_id}, {"$set": {"log_chat_id": chat.id}}, upsert=True)
    await message.reply_text("✅ Successfully set this chat as the federation log channel.")
@app.on_message(filters.command("unsetfedlog", prefixes=["/", "\\!", "."]) & ~filters.private)
async def unsetfedlog_cmd(client: Client, message: Message):
    chat = message.chat
    if not await is_admin(chat, message.from_user.id):
        await message.reply_text("❌ You must be an admin to use this command!")
        return
    chat_fed = await CHAT_FED_DB.find_one({"chat_id": chat.id})
    if not chat_fed:
        await message.reply_text("❌ This chat is not in any federation!")
        return
    fed_id = chat_fed["fed_id"]
    fed = await FEDS_DB.find_one({"fed_id": fed_id})
    if not fed or fed["owner_id"] != message.from_user.id:
        await message.reply_text("❌ You must be the owner of the federation.")
        return
    await FED_SETTINGS_DB.update_one({"fed_id": fed_id}, {"$unset": {"log_chat_id": ""}}, upsert=True)
    await message.reply_text("✅ Successfully unset the federation log channel.")
@app.on_message(filters.command("setfedlang", prefixes=["/", "\\!", "."]) & ~filters.private)
async def setfedlang_cmd(client: Client, message: Message):
    await message.reply_text("ℹ️ Federation log language feature is available.")
# User / General Fed Commands
@app.on_message(filters.command("fedinfo", prefixes=["/", "\\!", "."]))
async def fedinfo_cmd(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("⚠️ Usage: `/fedinfo <FedID>`")
        return
    fed_id = message.command[1].strip()
    fed = await FEDS_DB.find_one({"fed_id": fed_id})
    if not fed:
        await message.reply_text("❌ Federation not found.")
        return
    owner = await client.get_users(fed["owner_id"])
    owner_name = owner.first_name if owner else "Unknown" 
    admin_count = await FED_ADMINS_DB.count_documents({"fed_id": fed_id})
    ban_count = await FED_BANS_DB.count_documents({"fed_id": fed_id})
    chats_count = await CHAT_FED_DB.count_documents({"fed_id": fed_id})
    text = f"📋 **Federation Information:**\n\n" \
           f"• **Name:** {fed['name']}\n" \
           f"• **ID:** `{fed_id}`\n" \
           f"• **Owner:** {owner_name} (`{fed['owner_id']}`)\n" \
           f"• **Admins:** {admin_count}\n" \
           f"• **Banned Users:** {ban_count}\n" \
           f"• **Connected Chats:** {chats_count}"
    await message.reply_text(text)
@app.on_message(filters.command("fedadmins", prefixes=["/", "\\!", "."]))
async def fedadmins_cmd(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("⚠️ Usage: `/fedadmins <FedID>`")
        return
    fed_id = message.command[1].strip()
    fed = await FEDS_DB.find_one({"fed_id": fed_id})
    if not fed:
        await message.reply_text("❌ Federation not found.")
        return
    admins = []
    async for a in FED_ADMINS_DB.find({"fed_id": fed_id}):
        try:
            u = await client.get_users(a["user_id"])
            name = u.first_name if u else "Unknown"
        except Exception:
            name = "Unknown"
        role = "Owner" if a["user_id"] == fed["owner_id"] else "Admin"
        admins.append(f"• {name} (`{a['user_id']}`) - *{role}*")
    await message.reply_text(f"📋 **Federation Admins for {fed['name']}:**\n\n" + "\n".join(admins))
@app.on_message(filters.command("fedsubs", prefixes=["/", "\\!", "."]))
async def fedsubs_cmd(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("⚠️ Usage: `/fedsubs <FedID>`")
        return
    fed_id = message.command[1].strip()
    fed = await FEDS_DB.find_one({"fed_id": fed_id}) 
    if not fed:
        await message.reply_text("❌ Federation not found.")
        return
    subs = []
    async for s in FED_SUBS_DB.find({"fed_id": fed_id}):
        subs.append(f"• **{s['name']}** (`{s['sub_fed_id']}`)")
    if not subs:
        await message.reply_text("📭 This federation is not subscribed to any other federations.")
        return
    await message.reply_text(f"📋 **Subscribed Federations:**\n\n" + "\n".join(subs))
@app.on_message(filters.command("joinfed", prefixes=["/", "\\!", "."]) & ~filters.private)
async def joinfed_cmd(client: Client, message: Message):
    chat = message.chat
    chat_member = await chat.get_member(message.from_user.id)
    if chat_member.status != ChatMemberStatus.OWNER and not await is_sudo(message.from_user.id):
        await message.reply_text("❌ Only chat owners can join a chat to a federation!")
        return
    if len(message.command) < 2:
        await message.reply_text("⚠️ Usage: `/joinfed <FedID>`")
        return
    fed_id = message.command[1].strip()
    fed = await FEDS_DB.find_one({"fed_id": fed_id})
    if not fed:
        await message.reply_text("❌ Federation not found.")
        return
    await CHAT_FED_DB.update_one(
        {"chat_id": chat.id},
        {"$set": {"fed_id": fed_id, "fed_name": fed["name"]}},
        upsert=True
    )
    await message.reply_text(f"✅ Successfully joined this chat to federation **{fed['name']}**.")
@app.on_message(filters.command("leavefed", prefixes=["/", "\\!", "."]) & ~filters.private)
async def leavefed_cmd(client: Client, message: Message): 
    chat = message.chat
    chat_member = await chat.get_member(message.from_user.id)
    if chat_member.status != ChatMemberStatus.OWNER and not await is_sudo(message.from_user.id):
        await message.reply_text("❌ Only chat owners can make the chat leave a federation!")
        return
    res = await CHAT_FED_DB.delete_one({"chat_id": chat.id})
    if res.deleted_count > 0:
        await message.reply_text("✅ Successfully left the federation.")
    else:
        await message.reply_text("❌ This chat is not in any federation.")
@app.on_message(filters.command("fedstat", prefixes=["/", "\\!", "."]))
async def fedstat_cmd(client: Client, message: Message):
    target_id = message.from_user.id
    fed_id = None
    if len(message.command) > 1:
        arg1 = message.command[1].strip()
        if arg1.isdigit() or arg1.startswith("@"):
            uid, _ = await extract_user(client, message)
            if uid:
                target_id = uid
            if len(message.command) > 2:
                fed_id = message.command[2].strip()
        else:
            fed_id = arg1
    if not fed_id and not message.chat.private:
        chat_fed = await CHAT_FED_DB.find_one({"chat_id": message.chat.id})
        if chat_fed:
            fed_id = chat_fed["fed_id"]
    if fed_id:
        fed = await FEDS_DB.find_one({"fed_id": fed_id})
        if not fed:
            await message.reply_text("❌ Federation not found.")
            return
        fb = await FED_BANS_DB.find_one({"fed_id": fed_id, "user_id": target_id})
        if fb:
            await message.reply_text(f"🔴 User is **banned** in federation **{fed['name']}**.\nReason: `{fb.get('reason', 'N/A')}`")
        else:
            await message.reply_text(f"🟢 User is **not banned** in federation **{fed['name']}**.")
    else:
        feds_banned = []
        async for fb in FED_BANS_DB.find({"user_id": target_id}):
            fed = await FEDS_DB.find_one({"fed_id": fb["fed_id"]})
            if fed:
                feds_banned.append(f"• **{fed['name']}** (Reason: `{fb.get('reason', 'N/A')}`)")
        if not feds_banned:
            await message.reply_text("🟢 User has not been banned in any federation.")
        else:
            await message.reply_text(f"📋 **Federations where user is banned:**\n\n" + "\n".join(feds_banned))
@app.on_message(filters.command("chatfed", prefixes=["/", "\\!", "."]) & ~filters.private)
async def chatfed_cmd(client: Client, message: Message):
    chat_fed = await CHAT_FED_DB.find_one({"chat_id": message.chat.id})
    if not chat_fed:
        await message.reply_text("❌ This chat is not in any federation.")
        return
    fed = await FEDS_DB.find_one({"fed_id": chat_fed["fed_id"]})
    if not fed:
        await message.reply_text("❌ Federation information not found.")
        return
    await message.reply_text(f"ℹ️ This chat is part of federation **{fed['name']}** (`{fed['fed_id']}`).")
@app.on_message(filters.command("quietfed", prefixes=["/", "\\!", "."]) & ~filters.private)
async def quietfed_cmd(client: Client, message: Message):
    chat = message.chat
    if not await is_admin(chat, message.from_user.id):
        await message.reply_text("❌ You must be an admin to use this command!")
        return
    chat_fed = await CHAT_FED_DB.find_one({"chat_id": chat.id})
    if not chat_fed: 
        await message.reply_text("❌ This chat is not in any federation!")
        return
    fed_id = chat_fed["fed_id"]
    fed = await FEDS_DB.find_one({"fed_id": fed_id})
    if not fed or fed["owner_id"] != message.from_user.id:
        await message.reply_text("❌ You must be the owner of the federation.")
        return
    if len(message.command) < 2:
        s_doc = await FED_SETTINGS_DB.find_one({"fed_id": fed_id})
        status = "enabled" if (s_doc and s_doc.get("quietfed", False)) else "disabled"
        await message.reply_text(f"ℹ️ Quietfed status: **{status}**\nUsage: `/quietfed <yes/no/on/off>`")
        return
    val = message.command[1].lower()
    status = val in ["yes", "on", "true"]
    await FED_SETTINGS_DB.update_one({"fed_id": fed_id}, {"$set": {"quietfed": status}}, upsert=True)
    await message.reply_text(f"✅ Quietfed set to: **{status}**")
# ==================== GBAN / GLOBALIST COMMANDS ====================
@app.on_message(filters.command("gban", prefixes=["/", "\\!", "."]))
async def gban_command(client: Client, message: Message):
    if not await is_sudo(message.from_user.id):
        await message.reply_text("😜𝗬𝗼𝘂 𝗮𝗿𝗲 𝗻𝗼𝘁 𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 𝘁𝗼 𝘂𝘀𝗲 𝘁𝗵𝗶𝘀 𝗰𝗼𝗺𝗺𝗮𝗻𝗱!")
        return
    user_id, user_name = await extract_user(client, message)
    if not user_id:
        await message.reply_text("🌝𝗣𝗹𝗲𝗮𝘀𝗲 𝗿𝗲𝗽𝗹𝘆 𝘁𝗼 𝗮 𝘂𝘀𝗲𝗿 𝗼𝗿 𝗽𝗿𝗼𝘃𝗶𝗱𝗲 𝗮 𝘃𝗮𝗹𝗶𝗱 𝗨𝘀𝗲𝗿 𝗜𝗗/𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲 𝘁𝗼 𝗴𝗯𝗮𝗻🔪.")
        return
    if user_id == OWNER_ID or user_id in SUDO_USERS:
        await message.reply_text("😵‍💫𝗬𝗼𝘂 𝗰𝗮𝗻𝗻𝗼𝘁 𝗴𝗯𝗮𝗻 𝗮 𝗦𝘂𝗱𝗼 𝗨𝘀𝗲𝗿 𝗼𝗿 𝗢𝘄𝗻𝗲𝗿!")
        return
    existing = await GBAN_DB.find_one({"user_id": user_id})
    if existing:
        await message.reply_text(f"🖕 𝗨𝘀𝗲𝗿 {user_name} (`{user_id}`) 𝗶𝘀 𝗮𝗹𝗿𝗲𝗮𝗱𝘆 𝗴𝗹𝗼𝗯𝗮𝗹𝗹𝘆 𝗯𝗮𝗻𝗻𝗲𝗱.")
        return
    await GBAN_DB.insert_one({"user_id": user_id, "name": str(user_name)})
    try:
        await message.chat.ban_member(user_id)
        await message.reply_text(f"🎉 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 𝗚𝗹𝗼𝗯𝗮𝗹𝗹𝘆 𝗕𝗮𝗻𝗻𝗲𝗱 **{user_name}** (`{user_id}`).")
    except Exception as e:
        await message.reply_text(f"✅ Added to GBAN database, but failed to ban in this specific chat: {e}")
@app.on_message(filters.command("ungban", prefixes=["/", "\\!", "."]))
async def ungban_command(client: Client, message: Message):
    if not await is_sudo(message.from_user.id):
        await message.reply_text("👺 𝗬𝗼𝘂 𝗮𝗿𝗲 𝗻𝗼𝘁 𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 𝘁𝗼 𝘂𝘀𝗲 𝘁𝗵𝗶𝘀 𝗰𝗼𝗺𝗺𝗮𝗻𝗱!")
        return
    user_id, user_name = await extract_user(client, message)
    if not user_id:
        await message.reply_text("🙂‍↔️ 𝗣𝗹𝗲𝗮𝘀𝗲 𝗿𝗲𝗽𝗹𝘆 𝘁𝗼 𝗮 𝘂𝘀𝗲𝗿 𝗼𝗿 𝗽𝗿𝗼𝘃𝗶𝗱𝗲 𝗮 𝘃𝗮𝗹𝗶𝗱 𝗨𝘀𝗲𝗿 𝗜𝗗/𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲 𝘁𝗼 𝘂𝗻𝗴𝗯𝗮𝗻.")
        return
    existing = await GBAN_DB.find_one({"user_id": user_id})
    if not existing:
        await message.reply_text(f"🖕 𝗨𝘀𝗲𝗿 (`{user_id}`) 𝗶𝘀 𝗻𝗼𝘁 𝗴𝗹𝗼𝗯𝗮𝗹𝗹𝘆 𝗯𝗮𝗻𝗻𝗲𝗱.")
        return
    await GBAN_DB.delete_one({"user_id": user_id})
    try:
        await message.chat.unban_member(user_id)
    except Exception:
        pass
    await message.reply_text(f"🖕🏿 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 𝗚𝗹𝗼𝗯𝗮𝗹𝗹𝘆 𝗨nbanned (`{user_id}`).")
@app.on_message(filters.command("globalist", prefixes=["/", "\\!", "."]))
async def globalist_command(client: Client, message: Message):
    if not await is_sudo(message.from_user.id):
        await message.reply_text("😜𝗬𝗼𝘂 𝗮𝗿𝗲 𝗻𝗼𝘁 𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 𝘁𝗼 𝘂𝘀𝗲 𝘁𝗵𝗶𝘀 𝗰𝗼𝗺𝗺𝗮𝗻𝗱!")
        return
    user_id, user_name = await extract_user(client, message)
    if not user_id:
        await message.reply_text("🌝𝗣𝗹𝗲𝗮𝘀𝗲 𝗿𝗲𝗽𝗹𝘆 𝘁𝗼 𝗮 𝘂𝘀𝗲𝗿 or provide a valid User ID/Username to add to globalist.")
        return
    if user_id == OWNER_ID or user_id in SUDO_USERS:
        await message.reply_text("😵‍💫𝗬𝗼𝘂 𝗰𝗮𝗻𝗻𝗼𝘁 𝗮𝗱𝗱 𝗮 𝗦𝘂𝗱𝗼 𝗨𝘀𝗲𝗿 𝗼𝗿 𝗢𝘄𝗻𝗲𝗿 𝘁𝗼 𝗴𝗹𝗼𝗯𝗮𝗹𝗶𝘀𝘁!")
        return
    existing = await GLOBALIST_DB.find_one({"user_id": user_id})
    if existing:
        await message.reply_text(f"🖕 𝗨𝘀𝗲𝗿 {user_name} (`{user_id}`) 𝗶𝘀 𝗮𝗹𝗿𝗲𝗮𝗱𝘆 𝗶𝗻 𝘁𝗵𝗲 𝗴𝗹𝗼𝗯𝗮𝗹𝗶𝘀𝘁.")
        return
    await GLOBALIST_DB.insert_one({"user_id": user_id, "name": str(user_name)})
    try:
        await message.chat.ban_member(user_id)
        await message.reply_text(f"🎉 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 𝗔𝗱𝗱𝗲𝗱 **{user_name}** (`{user_id}`) 𝘁𝗼 𝗚𝗹𝗼𝗯𝗮𝗹𝗶𝘀𝘁 𝗮𝗻𝗱 𝗯𝗮𝗻𝗻𝗲𝗱.")
    except Exception as e:
        await message.reply_text(f"✅ Added to Globalist database, but failed to ban in this specific chat: {e}")
@app.on_message(filters.command("unglobalist", prefixes=["/", "\\!", "."]))
async def unglobalist_command(client: Client, message: Message):
    if not await is_sudo(message.from_user.id):
        await message.reply_text("👺 𝗬𝗼𝘂 𝗮𝗿𝗲 𝗻𝗼𝘁 𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 𝘁𝗼 𝘂𝘀𝗲 𝘁𝗵𝗶𝘀 𝗰𝗼𝗺𝗺𝗮𝗻𝗱!")
        return
    user_id, user_name = await extract_user(client, message)
    if not user_id:
        await message.reply_text("🙂‍↔️ 𝗣𝗹𝗲𝗮𝘀𝗲 𝗿𝗲𝗽𝗹𝘆 𝘁𝗼 𝗮 𝘂𝘀𝗲𝗿 𝗼𝗿 𝗽𝗿𝗼𝘃𝗶𝗱𝗲 𝗮 𝘃𝗮𝗹𝗶𝗱 𝗨𝘀𝗲𝗿 𝗜𝗗/𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲 𝘁𝗼 𝗿𝗲𝗺𝗼𝘃𝗲 𝗳𝗿𝗼𝗺 𝗴𝗹𝗼𝗯𝗮𝗹𝗶𝘀𝘁.")
        return
    existing = await GLOBALIST_DB.find_one({"user_id": user_id})
    if not existing:
        await message.reply_text(f"🖕 𝗨𝘀𝗲𝗿 (`{user_id}`) 𝗶𝘀 𝗻𝗼𝘁 𝗶𝗻 𝘁𝗵𝗲 𝗴𝗹𝗼𝗯𝗮𝗹𝗶𝘀𝘁.")
        return
    await GLOBALIST_DB.delete_one({"user_id": user_id})
    try:
        await message.chat.unban_member(user_id)
    except Exception:
        pass
    await message.reply_text(f"🖕🏿 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 𝗥𝗲𝗺𝗼𝘃𝗲𝗱 𝗨𝘀𝗲𝗿 (`{user_id}`) 𝗳𝗿𝗼𝗺 𝗚𝗹𝗼𝗯𝗮𝗹𝗶𝘀𝘁.")
@app.on_message(filters.command(["gbannedlist", "gbanlist"], prefixes=["/", "\\!", "."]))
async def gbanned_list_command(client: Client, message: Message):
    if not await is_sudo(message.from_user.id):
        await message.reply_text("😜𝗬𝗼𝘂 𝗮𝗿𝗲 𝗻𝗼𝘁 𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 𝘁𝗼 𝘂𝘀𝗲 𝘁𝗵𝗶𝘀 𝗰𝗼𝗺𝗺𝗮𝗻𝗱!")
        return
    count = await GBAN_DB.count_documents({})
    if count == 0:
        await message.reply_text("📭 No users are globally banned yet.")
        return
    text = f"📋 **Globally Banned Users List ({count}):**\n\n"
    async for user in GBAN_DB.find({}):
        name = user.get("name", "Unknown")
        uid = user.get("user_id")
        text += f"• {name} (`{uid}`)\n"
    if len(text) > 4096:
        await message.reply_text("⚠️ List is too long to display.")
    else:
        await message.reply_text(text)
@app.on_message(filters.command(["globalistlist", "glist"], prefixes=["/", "\\!", "."]))
async def globalist_list_command(client: Client, message: Message):
    if not await is_sudo(message.from_user.id):
        await message.reply_text("😜𝗬𝗼𝘂 𝗮𝗿𝗲 𝗻𝗼𝘁 𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 𝘁𝗼 𝘂𝘀𝗲 𝘁𝗵𝗶𝘀 𝗰𝗼𝗺𝗺𝗮𝗻𝗱!")
        return
    count = await GLOBALIST_DB.count_documents({})
    if count == 0: 
        await message.reply_text("📭 No users are in the Globalist list yet.")
        return
    text = f"📋 **Globalist Users List ({count}):**\n\n"
    async for user in GLOBALIST_DB.find({}):
        name = user.get("name", "Unknown")
        uid = user.get("user_id")
        text += f"• {name} (`{uid}`)\n"
    if len(text) > 4096:
        await message.reply_text("⚠️ List is too long to display.")
    else:
        await message.reply_text(text)
# ==================== CHAT FILTER COMMANDS ====================
@app.on_message(filters.command("filter", prefixes=["/", "\\!", "."]) & ~filters.private)
async def save_filter(client: Client, message: Message):
    try:
        text = message.text.markdown if message.text else message.caption.markdown
    except Exception:
        return
    args = text.split(None, 1)
    if len(args) < 2:
        await message.reply_text("⚠️ Usage: `/filter <trigger> <reply>` (or reply to a sticker/media with `/filter trigger`)")
        return
    remaining = args[1]
    if remaining.startswith('"') or remaining.startswith("'"):
        quote_char = remaining[0]
        parts = remaining[1:].split(quote_char, 1)
        if len(parts) < 2:
            await message.reply_text("⚠️ Invalid quotes format for trigger.")
            return
        trigger = parts[0].strip().lower()
        content_text = parts[1].strip()
    else:
        parts = remaining.split(None, 1)
        trigger = parts[0].strip().lower()
        content_text = parts[1].strip() if len(parts) > 1 else ""
    chat_id = message.chat.id 
    reply_msg = message.reply_to_message
    reply_type = "text"
    reply_content = content_text
    reply_caption = None
    if reply_msg:
        if reply_msg.sticker:
            reply_type = "sticker"
            reply_content = reply_msg.sticker.file_id
        elif reply_msg.photo:
            reply_type = "photo"
            reply_content = reply_msg.photo.file_id
            reply_caption = reply_msg.caption
        elif reply_msg.animation:
            reply_type = "animation"
            reply_content = reply_msg.animation.file_id
            reply_caption = reply_msg.caption
        elif reply_msg.document:
            reply_type = "document"
            reply_content = reply_msg.document.file_id
            reply_caption = reply_msg.caption
        elif reply_msg.audio:
            reply_type = "audio"
            reply_content = reply_msg.audio.file_id
            reply_caption = reply_msg.caption
        elif reply_msg.video:
            reply_type = "video"
            reply_content = reply_msg.video.file_id
            reply_caption = reply_msg.caption
        elif reply_msg.text and not content_text:
            reply_type = "text"
            reply_content = reply_msg.text
    if not reply_content:
        await message.reply_text("⚠️ Please provide a text reply or reply to a sticker/media to set this filter.")
        return
    await CHAT_FILTERS_DB.update_one(
        {"chat_id": chat_id, "trigger": trigger},
        {
            "$set": {
                "reply_type": reply_type,
                "reply_content": reply_content,
                "reply_caption": reply_caption
            }
        }, upsert=True
    )
    await client.send_message(chat_id, f"✅ Successfully saved filter for exact trigger: `{trigger}`")
@app.on_message(filters.command("filters", prefixes=["/", "\\!", "."]) & ~filters.private)
async def list_filters(client: Client, message: Message):
    chat_id = message.chat.id
    count = await CHAT_FILTERS_DB.count_documents({"chat_id": chat_id})
    if count == 0:
        await message.reply_text("📭 No filters saved in this chat.")
        return
    text = f"📋 **Saved Filters in this Chat ({count}):**\n\n"
    async for filt in CHAT_FILTERS_DB.find({"chat_id": chat_id}):
        text += f"• `{filt['trigger']}` ({filt.get('reply_type', 'text')})\n"
    if len(text) > 4096:
        await message.reply_text("⚠️ Filter list is too long to display.")
    else:
        await message.reply_text(text)
@app.on_message(filters.command("stop", prefixes=["/", "\\!", "."]) & ~filters.private)
async def stop_filter(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("⚠️ Usage: `/stop <trigger>`")
        return
    trigger = message.command[1].strip().lower()
    chat_id = message.chat.id
    result = await CHAT_FILTERS_DB.delete_one({"chat_id": chat_id, "trigger": trigger})
    if result.deleted_count > 0:
        await message.reply_text(f"✅ Filter `{trigger}` has been deleted.")
    else:
        await message.reply_text(f"❌ No filter found for trigger `{trigger}`.") 
@app.on_message(filters.command("stopall", prefixes=["/", "\\!", "."]) & ~filters.private)
async def stop_all_filters(client: Client, message: Message):
    chat_id = message.chat.id
    result = await CHAT_FILTERS_DB.delete_many({"chat_id": chat_id})
    await message.reply_text(f"🗑️ Deleted all {result.deleted_count} filters in this chat permanently.")
# ==================== CALLBACK QUERIES ====================
@app.on_callback_query()
async def callback_handler(client: Client, callback_query: CallbackQuery):
    data = callback_query.data
    message = callback_query.message
    user_id = callback_query.from_user.id
    ALL_USERS.add(user_id)
    if data.startswith("accept_fedadmin_"):
        fed_id = data.split("accept_fedadmin_", 1)[1]
        await FED_ADMINS_DB.update_one({"fed_id": fed_id, "user_id": user_id}, {"$set": {"user_id": user_id}}, upsert=True)
        await FED_PENDING_ADMINS_DB.delete_one({"fed_id": fed_id, "user_id": user_id})
        await callback_query.answer("✅ You have accepted the federation admin role!", show_alert=True)
        try:
            await message.edit_text("✅ You are now a federation admin!")
        except Exception:
            pass
        return
    elif data.startswith("decline_fedadmin_"):
        fed_id = data.split("decline_fedadmin_", 1)[1]
        await FED_PENDING_ADMINS_DB.delete_one({"fed_id": fed_id, "user_id": user_id})
        await callback_query.answer("❌ You declined the federation admin role.", show_alert=True)
        try:
            await message.edit_text("❌ Invitation declined.")
        except Exception:
            pass
        return
    if data == "open_dashboard_new":
        await callback_query.answer()
        try: 
            await client.send_animation(message.chat.id, START_GIF_URL, caption="🎵 Welcome to Power Music Bot!", reply_markup=get_main_menu_keyboard())
        except Exception:
            await client.send_message(message.chat.id, "🎵 Welcome to Power Music Bot!", reply_markup=get_main_menu_keyboard())
        return
    elif data == "exciting":
        offset = 0
        keyboard_buttons = [
            [InlineKeyboardButton(f"Shayari #{offset + 1}", callback_data=f"shayari_act_{offset}")],
            [InlineKeyboardButton("Menu", callback_data="back_to_menu"), InlineKeyboardButton("Next ➡️", callback_data=f"shayari_page_{offset + 1}")]
        ]
        try:
            await message.edit_text(text="✨ Exclusive Shayari Feature:", reply_markup=InlineKeyboardMarkup(keyboard_buttons))
        except:
            pass
        await callback_query.answer()
        return
    elif data.startswith("shayari_page_"):
        offset = int(data.split("_")[2])
        keyboard_buttons = [
            [InlineKeyboardButton(f"Shayari #{offset + 1}", callback_data=f"shayari_act_{offset}")],
            [InlineKeyboardButton("« Back", callback_data=f"shayari_page_{offset-1}"), InlineKeyboardButton("Menu", callback_data="back_to_menu"), InlineKeyboardButton("Next ➡️", callback_data=f"shayari_page_{offset+1}")]
        ]
        try:
            await message.edit_text(text="✨ Exclusive Shayari Feature:", reply_markup=InlineKeyboardMarkup(keyboard_buttons))
        except:
            pass
        await callback_query.answer()
        return
    elif data.startswith("shayari_act_"):
        idx = int(data.split("_")[2])
        await callback_query.answer(f"TanjiroXMusic\n\nShayari #{idx + 1}\n\n{EXCLUSIVE_SHAYARI[idx]}", show_alert=True) 
        return
    elif data.startswith("opt1_"):
        song_query = data.split("opt1_", 1)[1]
        await callback_query.answer()
        try:
            await client.send_message(message.chat.id, f"🎶 Song Options Menu\nQuery: {song_query}", reply_markup=get_three_dots_menu(song_query))
        except:
            pass
        return
    elif data.startswith(("opt_performer_", "opt_artist_", "opt_similar_", "opt_albums_")):
        parts = data.split("_")
        track_type, song_query, offset = parts[1], parts[2], int(parts[3])
        tracks_map = {"performer": PERFORMER_TRACKS, "artist": ARTIST_TRACKS, "similar": SIMILAR_TRACKS, "albums": ALBUM_TRACKS}
        current_tracks = tracks_map.get(track_type, PERFORMER_TRACKS)[offset:offset+10]
        kb = [[InlineKeyboardButton(tr, callback_data=f"play_{tr[:50]}")] for tr in current_tracks]
        kb.append([InlineKeyboardButton("Menu", callback_data="back_to_menu")])
        try:
            await client.send_message(message.chat.id, "📂 Tracks List:", reply_markup=InlineKeyboardMarkup(kb))
        except:
            pass
        await callback_query.answer()
        return
    elif data in ["opt2_", "opt_dlt_"]:
        try:
            await message.delete()
        except:
            pass
        await callback_query.answer("Deleted!", show_alert=False)
        return
    elif data == "new_tracks":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🇮🇳 Hindi", callback_data="lang_hindi_0"), InlineKeyboardButton("🇬🇧 English", callback_data="lang_english_0")], 
            [InlineKeyboardButton("🇮🇳 Punjabi", callback_data="lang_punjabi_0"), InlineKeyboardButton("🌾 Haryanvi", callback_data="lang_haryanvi_0")],
            [InlineKeyboardButton("« Menu", callback_data="back_to_menu")]
        ])
        try:
            await message.edit_text(text="🎵 Select category:", reply_markup=keyboard)
        except:
            pass
        await callback_query.answer()
    elif data.startswith("lang_"):
        parts = data.split("_")
        lang_key, offset = parts[1], int(parts[2])
        songs_list = SONGS_DB.get(lang_key, [])
        current_songs = songs_list[offset:offset+10]
        kb = [[InlineKeyboardButton(song, callback_data=f"play_{song[:50]}")] for song in current_songs]
        nav_buttons = []
        if offset > 0:
            nav_buttons.append(InlineKeyboardButton("⬅️ Back", callback_data=f"lang_{lang_key}_{offset-10}"))
        if offset + 10 < len(songs_list):
            nav_buttons.append(InlineKeyboardButton("Next ➡️", callback_data=f"lang_{lang_key}_{offset+10}"))
        if nav_buttons:
            kb.append(nav_buttons)
        kb.append([InlineKeyboardButton("« Menu", callback_data="new_tracks")])
        try:
            await message.edit_text(text=f"🎵 {lang_key.capitalize()} Songs:", reply_markup=InlineKeyboardMarkup(kb))
        except:
            pass
        await callback_query.answer()
    elif data.startswith(("top_tracks_", "collections_")):
        prefix = "top_tracks_" if "top" in data else "collections_"
        offset = int(data.split(prefix)[1])
        source_list = TOP_SONGS if prefix == "top_tracks_" else COLLECTIONS_SONGS
        current_songs = source_list[offset:offset+10]
        kb = [[InlineKeyboardButton(song, callback_data=f"play_{song[:50]}")] for song in current_songs]
        nav_buttons = []
        if offset > 0:
            nav_buttons.append(InlineKeyboardButton("⬅️ Back", callback_data=f"{prefix}{offset-10}"))
        if offset + 10 < len(source_list):
            nav_buttons.append(InlineKeyboardButton("Next ➡️", callback_data=f"{prefix}{offset+10}"))
        if nav_buttons:
            kb.append(nav_buttons)
        kb.append([InlineKeyboardButton("« Menu", callback_data="back_to_menu")])
        try:
            await message.edit_text(text="🔥 Tracks List:", reply_markup=InlineKeyboardMarkup(kb))
        except:
            pass
        await callback_query.answer()
    elif data == "pro_mode":
        await callback_query.answer("TanjiroXMusic | Pro mode is active.", show_alert=True)
        return
    elif data == "playlists":
        WAITING_FOR_PLAYLIST_NAME.discard(user_id)
        try:
            await message.edit_text(text="🎵 Your Playlists:", reply_markup=get_playlists_menu(user_id))
        except:
            pass
        await callback_query.answer()
        return
    elif data == "create_playlist_prompt":
        WAITING_FOR_PLAYLIST_NAME.add(user_id)
        try:
            await message.edit_text(text="✍️ Please send playlist name:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Menu", callback_data="playlists")]]))
        except:
            pass
        await callback_query.answer()
        return
    elif data == "back_to_menu":
        WAITING_FOR_PLAYLIST_NAME.discard(user_id)
        try: 
            await message.edit_text(text="🎵 Welcome to Power Music Bot!", reply_markup=get_main_menu_keyboard())
        except:
            pass
        await callback_query.answer()
        return
    elif data.startswith("play_"):
        song_query = data[5:]
        await callback_query.answer()
        try:
            loop = asyncio.get_event_loop()
            file_path, thumb_path, title, duration, artist_name = await loop.run_in_executor(None, lightning_download_ytdlp, song_query)
            if file_path and os.path.exists(file_path):
                await client.send_audio(message.chat.id, audio=file_path, thumb=thumb_path if (thumb_path and os.path.exists(thumb_path)) else None, title=title, performer=artist_name, duration=duration, reply_markup=get_song_keyboard(song_query))
                if os.path.exists(file_path): 
                    os.remove(file_path)
                if thumb_path and os.path.exists(thumb_path):
                    os.remove(thumb_path)
        except Exception as e:
            await client.send_message(message.chat.id, f"Error: {str(e)[:100]}")
@app.on_message(filters.text & ~filters.command(["start"], prefixes=["/", "\\!", "."]))
async def message_dispatcher_handler(client: Client, message: Message):
    try:
        if not message.text or not message.from_user:
            return
        user_id = message.from_user.id
        user_text = message.text.strip()
        if user_id in WAITING_FOR_PLAYLIST_NAME:
            WAITING_FOR_PLAYLIST_NAME.remove(user_id)
            pl_name = user_text
            if user_id not in USER_PLAYLISTS: 
                USER_PLAYLISTS[user_id] = {}
            USER_PLAYLISTS[user_id][pl_name] = []
            await message.reply_text(f"✅ Playlist '{pl_name}' created successfully!", reply_markup=get_playlists_menu(user_id))
            return 
    except Exception as e:
        print(f"Message Dispatcher Error: {e}")
def lightning_download_ytdlp(query):
    ydl_opts = {
        'format': 'bestaudio', 'outtmpl': '%(id)s.%(ext)s', 'quiet': True, 'noplaylist': True,
        'socket_timeout': 15, 'writethumbnail': True,
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}, {'key': 'EmbedThumbnail'}]
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch1:{query}", download=True)
            if 'entries' in info: 
                info = info['entries'][0]
            duration, title = info.get('duration', 0), info.get('title', query)
            artist_name = info.get('uploader') or info.get('artist') or "TanjiroXMusic"
            video_id = info.get('id')
            filename = f"{video_id}.mp3"
            if not os.path.exists(filename):
                filename = os.path.splitext(ydl.prepare_filename(info))[0] + ".mp3"
            thumb_path = next((f"{video_id}{ext}" for ext in ['.jpg', '.jpeg', '.png', '.webp'] if os.path.exists(f"{video_id}{ext}")) , None)
            return (filename, thumb_path, title, duration, artist_name) if os.path.exists(filename) else (None, None, None, 0, "TanjiroXMusic")
        except:
            return None, None, None, 0, "TanjiroXMusic"
async def main():
    print("Starting Bot++")
    await app.start()
    print("Bot is successfully running with all features!")
    await asyncio.get_event_loop().create_future()
if __name__ == "__main__":
    app.run(main())
