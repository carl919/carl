import telebot
from telethon import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest
import logging
import asyncio
import time

logging.basicConfig(level=logging.ERROR)

# ---------------------------- TOKEN ----------------------------#
bot = telebot.TeleBot('7757890724:AAHyAoP-45Q04-EP6PvFN1pKc-tqMYo53AI')


user_data = {}

from telebot import types




@bot.message_handler(commands=['start'])
def start(message):
   
    markup = types.InlineKeyboardMarkup()
    
    
    
# ---------------------------- حقوقي  ----------------------------#
    button_channel = types.InlineKeyboardButton("قناة المطور", url="https://t.me/M1telegramM1")
    
    
    button_developer = types.InlineKeyboardButton("المطور", url="https://t.me/M3_mo2")
    
    
    markup.add(button_channel, button_developer)
   
# ----------------------------بدايه دوال متلعبش ف حاجه  ----------------------------#
    
    bot.send_message(message.chat.id, """
اهلا بك عزيزي في بوت نقل الاعضاء 🔥🇪🇬

في هذا البوت يمكنك نقل اعضاء اي جروب الي جروب اخر بكل سهوله ✨

يمكنك الحصول علي Api id, api hash من موقع  ( https://my.telegram.org/auth )
😊

فقط اتبع الخطوات :
    """, reply_markup=markup)
    bot.send_message(message.chat.id,("ادخل ال api id الخاص بك الان"))


@bot.message_handler(func=lambda message: True)
def get_api_id(message):
    user_id = message.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {}

  
    if 'api_id' not in user_data[user_id]:
        user_data[user_id]['api_id'] = message.text.strip()
        bot.send_message(message.chat.id, "تم إدخال API ID بنجاح! الآن، أدخل API Hash الخاص بك:")
  
    elif 'api_hash' not in user_data[user_id]:
        user_data[user_id]['api_hash'] = message.text.strip()
        bot.send_message(message.chat.id, "تم إدخال API Hash بنجاح! الآن، أدخل معرف الجروب المصدر:")
    
    elif 'from_group' not in user_data[user_id]:
        user_data[user_id]['from_group'] = message.text.strip()
        bot.send_message(message.chat.id, "تم إدخال الجروب المصدر بنجاح! الآن، أدخل معرف الجروب الهدف:")
    
    elif 'to_group' not in user_data[user_id]:
        user_data[user_id]['to_group'] = message.text.strip()
        bot.send_message(message.chat.id, "تم إدخال الجروب الهدف بنجاح! الآن، ادخل sleep بين إضافة الأعضاء أو اكتب 'بدون وقت':")

    
    elif 'sleep_time' not in user_data[user_id]:
        sleep_time = message.text.strip()
        if sleep_time.lower() == 'بدون وقت':
            user_data[user_id]['sleep_time'] = 0
        else:
            try:
                user_data[user_id]['sleep_time'] = int(sleep_time)
            except ValueError:
                bot.send_message(message.chat.id, "الرجاء إدخال وقت صحيح بالثواني أو 'بدون وقت' لعدم إضافة فاصل.")
                return
        bot.send_message(message.chat.id, "تم تحديد وقت السكون بنجاح! انتظر قليلاً...")

        
        bot.send_message(message.chat.id, "جاري نقل الأعضاء... يرجى الانتظار.")
        
        asyncio.run(process_transfer(user_id))

async def process_transfer(user_id):
    api_id = user_data[user_id]['api_id']
    api_hash = user_data[user_id]['api_hash']
    from_group = user_data[user_id]['from_group']
    to_group = user_data[user_id]['to_group']
    sleep_time = user_data[user_id]['sleep_time']

   
    client = TelegramClient('session_name', api_id, api_hash)

    await client.start()

    try:
       
        participants = await client.get_participants(from_group)
        print(f"عدد الأعضاء في الجروب المصدر: {len(participants)}")

        
        for user in participants:
            try:
                
                await client(InviteToChannelRequest(to_group, [user.id]))
                print(f"تم إضافة العضو {user.username} إلى الجروب الهدف")

          
                if sleep_time > 0:
                    time.sleep(sleep_time)
            except Exception as e:
                print(f"فشل إضافة {user.username}: {e}")
        
        bot.send_message(user_id, "تم نقل الأعضاء بنجاح!")
    except Exception as e:
        print(f"حدث خطأ: {e}")
        bot.send_message(user_id, "حدث خطأ أثناء نقل الأعضاء. الرجاء المحاولة مرة أخرى.")
    finally:
        await client.disconnect()

# ----------------------------infinite ----------------------------#

# اي خدمه 😉
bot.polling(non_stop=True)