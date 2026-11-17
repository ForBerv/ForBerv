ForBerv — بوت ديسكورد عربي

التشغيل:
1) أنشئ تطبيقاً وبوتاً من بوابة مطوري Discord:
   https://discord.com/developers/applications
2) من صفحة Bot انسخ التوكن (لا ترسله لأحد).
3) فعّل Server Members Intent و Message Content Intent من صفحة Bot.
4) أضف البوت لسيرفرك من OAuth2 > URL Generator:
   Scopes: bot و applications.commands
   Bot Permissions: Manage Channels, Manage Messages, Kick Members,
   Ban Members, Moderate Members, Send Messages, View Channels,
   Read Message History.
5) انسخ .env.example إلى ملف اسمه .env وضع التوكن داخله.
6) ثبّت المكتبات: pip install -r requirements.txt
7) شغّل: python bot.py

للتشغيل 24 ساعة:
ارفع الملفات إلى استضافة تدعم Python وشغّل الأمر: python bot.py
إغلاق تطبيق الجوال لا يوقف البوت إذا كان يعمل على استضافة سحابية.

الأوامر:
 /مساعدة /احصائيات /تذكرة /اغلاق /مسح /طرد /حظر /كتم /فك_كتم /ترحيب_تجربة

مهم:
- هذا مشروع جاهز كبداية عملية، وليس بوتاً منشوراً أو مستضافاً تلقائياً.
- لا تشارك التوكن مع أي شخص. إذا انكشف، أعد توليده من Discord Developer Portal.
- يجب أن يكون ترتيب رتبة البوت أعلى من الرتب التي يحتاج إدارتها.
