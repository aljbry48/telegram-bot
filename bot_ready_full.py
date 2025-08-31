#© Mikey - All rights reserved.  
#Telegram: [@SSUU_R](https://t.me/SSUU_R)  
import os  
import asyncio
import re
import pyrogram
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import (PhoneCodeInvalid,
                              PhoneNumberInvalid,
                              PhoneCodeExpired,
                              SessionPasswordNeeded,
                              PasswordHashInvalid,
                              UsernameInvalid)

#© Mikey - All rights reserved.  
#Telegram: [@SSUU_R](https://t.me/SSUU_R)  
import os
import asyncio
import re
import pyrogram
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import (PhoneCodeInvalid,
                              PhoneNumberInvalid,
                              PhoneCodeExpired,
                              SessionPasswordNeeded,
                              PasswordHashInvalid,
                              UsernameInvalid)

# قراءة البيانات من المتغيرات البيئية
apid = int(25176901)        # API_ID
hash = "c3b3fd935218f48e80abbabaf0366632"     # API_HASH
bot_token = "1814026797:AAEGI-4-Q6UgC_n3qdZbOIdg73UhSfTVWJc"  # Bot Token

bot = Client('bots', api_id=apid, api_hash=hash, bot_token=bot_token)


#© Mikey - All rights reserved.  
#Telegram: [@SSUU_R](https://t.me/SSUU_R)  
accounts_folder = "accounts" 

#© Mikey - All rights reserved.  
#Telegram: [@SSUU_R](https://t.me/SSUU_R)  
if not os.path.exists(accounts_folder):
    os.makedirs(accounts_folder)

@bot.on_message(filters.command(["start"]))
async def start(bot, msg):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("إضافة حساب", callback_data="add"),
         InlineKeyboardButton("عرض الحسابات", callback_data="show")],
        [InlineKeyboardButton("حذف الحساب", callback_data="delet"),
         InlineKeyboardButton("جلب كود", callback_data="LastCode")],
        [InlineKeyboardButton("التحكم بالحسابات", callback_data="Control")]
    ])
    await msg.reply_text("""مرحبًا بك في بوت تخزين حسابات تيليجرام والتحكم بها !
• حسنًا صديقي هذه الازرار أمامك تستطيع اختيار ماتحتاجه وجميع الازرار تعمل 
• فقط لدينا زر جلب كود لايعمل مؤقتًا وسوف نحاول اصلاحه في وقت لاحق ، استمتع .

- اذا كانت لديك أي افكار بشأن تطوير البوت تستطيع التواصل مع مبرمج البوت ⧼ @A_1_1_T ⧽ وطلب منه اضافة مايلزمك .""", reply_markup=keyboard)

async def show_accounts(call):
    try:
        account_files = os.listdir(accounts_folder)
        if account_files:
            account_list = [file.replace(".txt", "") for file in account_files]  #
            account_count = len(account_list)
            accounts_text = "\n".join(account_list)
            response_text = f"عدد الحسابات: {account_count}\n#\nالحسابات:\n{accounts_text}"
        else:
            response_text = "لا توجد حسابات مخزنة."
        
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=response_text)
    except FileNotFoundError:
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="مجلد الحسابات غير موجود.")

@bot.on_callback_query()
async def handle_callback_query(bot, call):
    if call.data == "add":
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="ارسل رقم الهاتف من فضلك")
        
        data = await bot.listen(chat_id=call.from_user.id, filters=filters.text & filters.private)
        phone_number = data.text
        
        message_data = await bot.send_message(chat_id=call.message.chat.id, text="انتظر يتم التحقق من رقم الهاتف")
        
        session_connect = Client(phone_number, api_id=apid, api_hash=hash)
        try:
            await session_connect.connect()
            code_data = await session_connect.send_code(phone_number=phone_number)
        except PhoneNumberInvalid:
            await bot.edit_message_text(chat_id=call.message.chat.id, text="الرقم غير صالح")
            await session_connect.disconnect()
            return

        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=message_data.id, text="ارسل الكود الذي وصل لحسابك")
        
        data = await bot.listen(chat_id=call.from_user.id, filters=filters.text & filters.private)
        
        message_data = await bot.send_message(chat_id=call.message.chat.id, text="يتم فحص صحة الكود")
        
        try:
            VerCode = int(data.text)
        except ValueError:
            await session_connect.disconnect()
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="حدث خطأ في تحويل الكود")
            return

        try:
            await session_connect.sign_in(phone_code=str(VerCode), phone_code_hash=code_data.phone_code_hash, phone_number=phone_number)
            
            # استخراج معلومات من الحساب
            user = await session_connect.get_me()
            username = user.username if user.username else "لايوجد يوزر"
            full_name = user.first_name + " " + (user.last_name if user.last_name else "")
            session_string = await session_connect.export_session_string()
            
            session_file_path = os.path.join(accounts_folder, f"{phone_number}.txt")
            with open(session_file_path, "w") as f:
                f.write(f"{phone_number}\n{session_string}\n")
                f.write(f"User - {username}\n")
                f.write(f"Name - {full_name}\n")
            
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="تم تسجيل الدخول بنجاح للحساب")
        except (PhoneCodeExpired, PhoneCodeInvalid):
            await session_connect.disconnect()
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="الكود خطأ أو انتهت صلاحيته.")
            return
        except SessionPasswordNeeded:
            await bot.send_message(chat_id=call.message.chat.id, text="حسابك محمي بكلمة سر التحقق بخطوتين ، قم بارسالها من فضلك")
            
            data = await bot.listen(chat_id=call.from_user.id, filters=filters.text & filters.private)
            Password = data.text
            message_data = await bot.send_message(chat_id=call.message.chat.id, text="يتم التأكد من التحقق بخطوتين")
            
            try:
                await session_connect.check_password(Password)

                user = await session_connect.get_me()
                username = user.username if user.username else "لايوجد يوزر"
                full_name = user.first_name + " " + (user.last_name if user.last_name else "")
                session_string = await session_connect.export_session_string()

                 
                 #© Mikey - All rights reserved.  
#Telegram: [@SSUU_R](https://t.me/SSUU_R)  
                session_file_path = os.path.join(accounts_folder, f"{phone_number}.txt")  # اسم الملف سيكون رقم الهاتف
                with open(session_file_path, "w") as f:
                    f.write(f"{phone_number}\n{session_string}\n")
                    f.write(f"User - {username}\n")
                    f.write(f"Name - {full_name}\n")
               
                await bot.send_message(chat_id=call.message.chat.id, text="تم تسجيل الدخول بنجاح للحساب")
            except PasswordHashInvalid:
                await session_connect.disconnect()
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="الباسورد خطأ")
                return

    elif call.data == "show":
        
        await show_accounts(call)

    elif call.data == "delet":
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="ارسل رقم الحساب الذي تريد حذفه")
        
        data = await bot.listen(chat_id=call.from_user.id, filters=filters.text & filters.private)
        phone_number = data.text
        
        session_path = os.path.join(accounts_folder, f"{phone_number}.txt")
        if os.path.exists(session_path):
            os.remove(session_path)
            await bot.send_message(chat_id=call.message.chat.id, text="تم حذف الحساب من التخزين")
        else:
            await bot.send_message(chat_id=call.message.chat.id, text="لايوجد حساب في التخزين بهذا الرقم")

#© Mikey - All rights reserved.  
#Telegram: [@SSUU_R](https://t.me/SSUU_R)  

    elif call.data == "LastCode":
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="ارسل الرقم الذي تريد جلب اخر رسالة من محادثة معينة")
    
        data = await bot.listen(chat_id=call.from_user.id, filters=filters.text & filters.private)
        phone_number = data.text
        
        session_path = os.path.join(accounts_folder, f"{phone_number}.txt")
        if os.path.exists(session_path):
            with open(session_path, "r") as f:
                lines = f.readlines()
                if len(lines) > 1:
                    session_string = lines[1].strip()
                    session_connect = Client(phone_number, api_id=apid, api_hash=hash, session_string=session_string)
                    
                    await session_connect.start()
                    
                    try:
                        await bot.send_message(chat_id=call.message.chat.id, text="ارسل يوزر القناة التي تريد جلب اخر رسالة منها")
                        data = await bot.listen(chat_id=call.from_user.id, filters=filters.text & filters.private)
                        dialo = data.text
                        async for dialog in session_connect.get_dialogs():
                            if dialog.chat.title == dialo:
                                async for message in session_connect.get_chat_history(dialog.chat.id, limit=1):
                                    if message:
                                        # إرسال نص الرسالة بالكامل
                                        await bot.send_message(chat_id=call.message.chat.id, text=f"آخر رسالة من حساب الدعم: {message.text}")
                                    else:
                                        await bot.send_message(chat_id=call.message.chat.id, text="لا توجد رسائل في الدردشة.")
                                break
                        else:
                            await bot.send_message(chat_id=call.message.chat.id, text="لم يتم العثور على حساب الدعم.")
                    except Exception as e:
                        await bot.send_message(chat_id=call.message.chat.id, text=f"حدث خطأ: {str(e)}")
                else:
                    await bot.send_message(chat_id=call.message.chat.id, text="لا توجد معلومات للجلسة.")
        else:
            await bot.send_message(chat_id=call.message.chat.id, text="لا يوجد حساب بهذا الرقم.")
#
    elif call.data == "Control":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("الانضمام لقناة", callback_data="join_channel"),
             InlineKeyboardButton("مغادرة قناة", callback_data="leaving_channel")]])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="اختر الخيار الذي تريده:", reply_markup=keyboard)
# شرط النقر على زر انضمام لقناة
    elif call.data == "join_channel":
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="""ارسل رابط القناة التي تريد الانضمام إليها

ملاحظة : يجب عليك ارسال رابط القناة بهذا الشكل @SSUU_R
استبدل SSUU_R بـ يوزر قناتك""")
        
        data = await bot.listen(chat_id=call.from_user.id, filters=filters.text & filters.private)
        link_channel = data.text
        
        session_files = [f for f in os.listdir(accounts_folder) if f.endswith(".txt")]
        
        tasks = []
        
        for session_file in session_files:
            session_path = os.path.join(accounts_folder, session_file)
            with open(session_path, "r") as f:
                lines = f.readlines()
                if len(lines) > 1:
                    session_string = lines[1].strip()
                    phone_number = session_file.replace(".txt", "")
                    
                    session_connect = Client(phone_number, api_id=apid, api_hash=hash, session_string=session_string)
                    
                    tasks.append(join_channel(session_connect, link_channel, call.message.chat.id))
        
        await asyncio.gather(*tasks)
    elif call.data == "leaving_channel":
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="""ارسل رابط القناة التي تريد المغادرة منها

ملاحظة : يجب عليك ارسال رابط القناة بهذا الشكل @SSUU_R
استبدل SSUU_R بـ يوزر قناتك""")
        
        data = await bot.listen(chat_id=call.from_user.id, filters=filters.text & filters.private)
        link_leaving = data.text
        
        session_files = [f for f in os.listdir(accounts_folder) if f.endswith(".txt")]
        
        tasks = []
        
        for session_file in session_files:
            session_path = os.path.join(accounts_folder, session_file)
            with open(session_path, "r") as f:
                lines = f.readlines()
                if len(lines) > 1:
                    session_string = lines[1].strip()
                    phone_number = session_file.replace(".txt", "")
                    
                    session_connect = Client(phone_number, api_id=apid, api_hash=hash, session_string=session_string)
                                        
                    tasks.append(leaving_channel(session_connect, link_leaving, call.message.chat.id))
        
        await asyncio.gather(*tasks)
async def join_channel(session_connect, link_channel, chat_id):
    async with session_connect:
        try:
            await session_connect.join_chat(link_channel)
            await bot.send_message(chat_id=chat_id, text="تم الانضمام بنجاح")
        except Exception as e:
            await bot.send_message(chat_id=chat_id, text="فشل الانضمام: " + str(e))
async def leaving_channel(session_connect, link_leaving, chat_id):
    async with session_connect:
        try:
            await session_connect.leave_chat(link_leaving)
            
            await bot.send_message(chat_id=chat_id, text="تم مغادرة القناة")
        except Exception as e:
            await bot.send_message(chat_id=chat_id, text="فشل المغادرة: " + str(e))

#© Mikey - All rights reserved.  
#Telegram: [@SSUU_R](https://t.me/SSUU_R)  
bot.run()