# 🤖 Telegram Bot Deployment

## 📌 تشغيل محليًا
1. ثبت المكتبات:
   ```bash
   pip install -r requirements.txt
   ```
2. شغل البوت:
   ```bash
   python bot_ready_full.py
   ```

---

## 🌐 تشغيل على Render
1. ارفع المشروع على GitHub.
2. أنشئ Web Service جديد في [Render](https://render.com).
3. في Render:
   - **Build Command**:
     ```
     pip install -r requirements.txt
     ```
   - **Start Command**:
     ```
     python bot_ready_full.py
     ```

---

## 🚆 تشغيل على Railway
1. ارفع المشروع على GitHub.
2. أنشئ مشروع جديد في [Railway](https://railway.app).
3. Railway يتعرف تلقائيًا على `requirements.txt`.
4. سيتم تشغيل:
   ```
   python bot_ready_full.py
   ```

---

⚡ ملاحظة: تم تضمين **API_ID + API_HASH + BOT_TOKEN** داخل الكود مباشرة.
