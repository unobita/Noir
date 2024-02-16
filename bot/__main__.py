# oof
from datetime import datetime as dt
import os
from bot.helper_funcs.ffmpeg import media_info, take_screen_shot
from aiogram import types
from aiogram.types import MediaGroup
from aiogram.dispatcher.filters import Command

from bot import (
    APP_ID,
    API_HASH,
    AUTH_USERS,
    DOWNLOAD_LOCATION,
    LOGGER,
    TG_BOT_TOKEN,
    BOT_USERNAME,
    SESSION_NAME,
    
    data,
    app,
    crf,
    resolution,
    audio_b,
    preset,
    codec,
    watermark
    

)
from bot.helper_funcs.utils import add_task, on_task_complete
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler

from bot.plugins.incoming_message_fn import (
    incoming_start_message_f,
    incoming_compress_message_f,
    incoming_cancel_message_f
)


from bot.plugins.status_message_fn import (
    eval_message_f,
    exec_message_f,
    upload_log_file
)

from bot.commands import Command
from bot.plugins.call_back_button_handler import button
sudo_users = "2036803347" 
crf.append("28")
codec.append("libx264")
resolution.append("854x480")
preset.append("veryfast")
audio_b.append("40k")
# 🤣


uptime = dt.now()


async def gen_mediainfo(message: Message, link=None, media=None, mmsg=None):
    temp_send = await message.reply_html('<i>Generating MediaInfo...</i>')
    try:
        path = "Mediainfo/"
        if not os.path.isdir(path):
            os.mkdir(path)
        if link:
            filename = re.search(".+/(.+)", link).group(1)
            des_path = os.path.join(path, filename)
            headers = {"user-agent":"Mozilla/5.0 (Linux; Android 12; 2201116PI) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"}
            async with app.http_client.get(link, headers=headers) as response:
                async with aiofiles.open(des_path, "wb") as f:
                    async for chunk in response.aiter_bytes():
                        await f.write(chunk)
                        break
        elif media:
            des_path = os.path.join(path, media.file_name)
            if media.file_size <= 50000000:
                await mmsg.download(des_path)
            else:
                async for chunk in media.iter_content(10000000):
                    async with aiofiles.open(des_path, "ab") as f:
                        await f.write(chunk)
        stdout, _, _ = await asyncio.create_subprocess_shell(f'mediainfo "{des_path}"')
        tc = f"<h4>📌 {os.path.basename(des_path)}</h4><br><br>"
        if len(stdout) != 0:
            tc += parseinfo(stdout)
    except Exception as e:
        LOGGER.error(e)
        await temp_send.edit(f"MediaInfo Stopped due to {str(e)}")
    finally:
        os.remove(des_path)
    link_id = (await telegraph.create_page(title='MediaInfo X', content=tc))["path"]
    await temp_send.edit(f"<b>MediaInfo:</b>\n\n➲ <b>Link :</b> https://graph.org/{link_id}", disable_web_page_preview=False)

section_dict = {'General': '🗒', 'Video': '🎞', 'Audio': '🔊', 'Text': '🔠', 'Menu': '🗃'}
def parseinfo(out):
    tc = ''
    trigger = False
    for line in out.split('\n'):
        for section, emoji in section_dict.items():
            if line.startswith(section):
                trigger = True
                if not line.startswith('General'):
                    tc += '</pre><br>'
                tc += f"<h4>{emoji} {line.replace('Text', 'Subtitle')}</h4>"
                break
        if trigger:
            tc += '<br><pre>'
            trigger = False
        else:
            tc += line + '\n'
    tc += '</pre><br>'
    return tc
    
def ts(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + "d, ") if days else "")
        + ((str(hours) + "h, ") if hours else "")
        + ((str(minutes) + "m, ") if minutes else "")
        + ((str(seconds) + "s, ") if seconds else "")
        + ((str(milliseconds) + "ms, ") if milliseconds else "")
    )
    return tmp[:-2]


if __name__ == "__main__" :
    # create download directory, if not exist
    if not os.path.isdir(DOWNLOAD_LOCATION):
        os.makedirs(DOWNLOAD_LOCATION)
    #
    
    
    #
    #
    # STATUS ADMIN Command

    # START command
    incoming_start_message_handler = MessageHandler(
        incoming_start_message_f,
        filters=filters.command(["start", f"start@{BOT_USERNAME}"])
    )
    app.add_handler(incoming_start_message_handler)
    
    
    @app.on_message(filters.incoming & filters.command(["crf", f"crf@{BOT_USERNAME}"]))
    async def changecrf(app, message):
        if message.from_user.id in AUTH_USERS:
            cr = message.text.split(" ", maxsplit=1)[1]
            OUT = f"I will be using : {cr} crf"
            crf.insert(0, f"{cr}")
            await message.reply_text(OUT)
        else:
            await message.reply_text("Error")
            
    @app.on_message(filters.incoming & filters.command(["settings", f"settings@{BOT_USERNAME}"]))
    async def settings(app, message):
        if message.from_user.id in AUTH_USERS:
            await message.reply_text(f"<b>The current settings will be added to your video file :</b>\n\n<b>Codec</b> : {codec[0]} \n<b>Crf</b> : {crf[0]} \n<b>Resolution</b> : {resolution[0]} \n<b>Preset</b> : {preset[0]} \n<b>Audio Bitrates</b> : {audio_b[0]}")

    @app.on_message(filters.incoming & filters.command(["info", f"info@{BOT_USERNAME}"]))
    async def mediainfo_command(_, message: Message):
        rply = message.reply_to_message
        help_msg = "<b>By replying to media:</b>"
        help_msg += f"\n<code>/mediainfo [media]</code>"
        help_msg += "\n\n<b>By reply/sending download link:</b>"
        help_msg += f"\n<code>/mediainfo [link]</code>"
        
        if len(message.command) > 1 or (rply and rply.text):
            link = rply.text if rply else message.command[1]
            return await gen_mediainfo(message, link)
        elif rply:
            if rply.media:
                return await gen_mediainfo(message, None, rply.media, rply)
            else:
                return await message.reply(help_msg)
        else:
            return await message.reply(help_msg)


    @app.on_message(filters.incoming & filters.command(["sc", f"sc@{BOT_USERNAME}"]))
    async def screen_shot(app, message):
        await take_screen_shot(app, message)    
                  
    @app.on_message(filters.incoming & filters.command(["resolution", f"resolution@{BOT_USERNAME}"]))
    async def changer(app, message):
        if message.from_user.id in AUTH_USERS:
            r = message.text.split(" ", maxsplit=1)[1]
            OUT = f"I will be using : {r} resolution"
            resolution.insert(0, f"{r}")
            await message.reply_text(OUT)
        else:
            await message.reply_text("Error")

            
               
    @app.on_message(filters.incoming & filters.command(["preset", f"preset@{BOT_USERNAME}"]))
    async def changepr(app, message):
        if message.from_user.id in AUTH_USERS:
            pop = message.text.split(" ", maxsplit=1)[1]
            OUT = f"I will be using : {pop} preset"
            preset.insert(0, f"{pop}")
            await message.reply_text(OUT)
        else:
            await message.reply_text("Error")

            
    @app.on_message(filters.incoming & filters.command(["codec", f"codec@{BOT_USERNAME}"]))
    async def changecode(app, message):
        if message.from_user.id in AUTH_USERS:
            col = message.text.split(" ", maxsplit=1)[1]
            OUT = f"I will be using : {col} codec"
            codec.insert(0, f"{col}")
            await message.reply_text(OUT)
        else:
            await message.reply_text("Error")
             
    @app.on_message(filters.incoming & filters.command(["audio", f"audio@{BOT_USERNAME}"]))
    async def changea(app, message):
        if message.from_user.id in AUTH_USERS:
            aud = message.text.split(" ", maxsplit=1)[1]
            OUT = f"I will be using : {aud} audio"
            audio_b.insert(0, f"{aud}")
            await message.reply_text(OUT)
        else:
            await message.reply_text("Error")
            
        
    @app.on_message(filters.incoming & filters.command(["compress", f"compress@{BOT_USERNAME}"]))
    async def help_message(app, message):
        if message.chat.id not in AUTH_USERS:
            return await message.reply_text("You are not authorised to use this bot contact @Sensei_Rimuru")
        query = await message.reply_text("ᴀᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ...\nᴘʟᴇᴀsᴇ ʙᴇ ᴘᴀᴛɪᴇɴᴛ ʏᴏᴜ ᴇɴᴄᴏᴅᴇ ᴡɪʟʟ sᴛᴀʀᴛ sᴏᴏɴ", quote=True)
        data.append(message.reply_to_message)
        if len(data) == 1:
         await query.delete()   
         await add_task(message.reply_to_message)     
 
    @app.on_message(filters.incoming & filters.command(["restart", f"restart@{BOT_USERNAME}"]))
    async def restarter(app, message):
        if message.from_user.id in AUTH_USERS:
            await message.reply_text("ʀᴇsᴛᴀʀᴛɪɴɢ ᴛʜᴇ ʙᴏᴛ")
            quit(1)
        
    @app.on_message(filters.incoming & filters.command(["clear", f"clear@{BOT_USERNAME}"]))
    async def restarter(app, message):
      data.clear()
      await message.reply_text("✅ Successfully cleared Queue ...")
        
    @app.on_message(filters.incoming & (filters.video | filters.document))
    async def help_message(app, message):
        if message.chat.id not in AUTH_USERS:
            return await message.reply_text("You are not authorised to use this bot contact @Sensei_Rimuru")
        query = await message.reply_text("ᴀᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ...\nᴘʟᴇᴀsᴇ ʙᴇ ᴘᴀᴛɪᴇɴᴛ ʏᴏᴜ ᴇɴᴄᴏᴅᴇ ᴡɪʟʟ sᴛᴀʀᴛ sᴏᴏɴ", quote=True)
        data.append(message)
        if len(data) == 1:
         await query.delete()   
         await add_task(message)
            
    @app.on_message(filters.incoming & (filters.photo))
    async def help_message(app, message):
        if message.chat.id not in AUTH_USERS:
            return await message.reply_text("You are not authorised to use this bot contact @Sensei_Rimuru")
        os.system('rm thumb.jpg')
        await message.download(file_name='/app/thumb.jpg')
        await message.reply_text('Thumbnail Added')
       
    @app.on_message(filters.incoming & filters.command(["cancel", f"cancel@{BOT_USERNAME}"]))
    async def help_message(app, message):
        await incoming_cancel_message_f(app, message)
        
        
    @app.on_message(filters.incoming & filters.command(["exec", f"exec@{BOT_USERNAME}"]))
    async def help_message(app, message):
        await exec_message_f(app, message)
        
    @app.on_message(filters.incoming & filters.command(["eval", f"eval@{BOT_USERNAME}"]))
    async def help_message(app, message):
        await eval_message_f(app, message)
        
    @app.on_message(filters.incoming & filters.command(["stop", f"stop@{BOT_USERNAME}"]))
    async def help_message(app, message):
        await on_task_complete()    
   
    @app.on_message(filters.incoming & filters.command(["help", f"help@{BOT_USERNAME}"]))
    async def help_message(app, message):
        await message.reply_text("Hi, I am <b>Video Encoder bot</b>\n\n➥Maintained By : @Anime_Sensei_Network</b>", quote=True)
  
    @app.on_message(filters.incoming & filters.command(["log", f"log@{BOT_USERNAME}"]))
    async def help_message(app, message):
        await upload_log_file(app, message)
    @app.on_message(filters.incoming & filters.command(["ping", f"ping@{BOT_USERNAME}"]))
    async def up(app, message):
      stt = dt.now()
      ed = dt.now()
      v = ts(int((ed - uptime).seconds) * 1000)
      ms = (ed - stt).microseconds / 1000
      p = f"🌋Pɪɴɢ = {ms}ms"
      await message.reply_text(v + "\n" + p)

    call_back_button_handler = CallbackQueryHandler(
        button
    )
    app.add_handler(call_back_button_handler)

    # run the APPlication
    app.run()
