
# GmailNotifyBot Overview


این برنامه چالش مدیریت یک صندوق ورودی پر مشغله‌ی جیمیل را با اطلاع رسانی به شما درباره ایمیل‌های خاص و مهم از طریق یک ربات تلگرام برطرف می‌کند. به عنوان مثال، اگر شما یک آسیب‌پذیری را در یک پلتفرم بانتی گزارش داده‌اید و منتظر پاسخ از شرکت مربوطه هستید، این ابزار تضمین می‌کند که به محض دریافت ایمیل، بلافاصله مطلع شوید، حتی اگر صندوق ورودی خود را به طور منظم چک نکنید.

## ویژگی‌های کلیدی

- نظارت بر صندوق ورودی جیمیل شما: به طور مداوم ایمیل‌های جدید و خوانده نشده را اسکن می‌کند.
- فیلتر کردن ایمیل‌های مهم: فقط زمانی به شما اطلاع می‌دهد که ایمیلی از فرستنده‌های مشخص شده دریافت شود.
- اطلاع رسانی فوری از طریق تلگرام: به محض شناسایی ایمیل، یک پیام به ربات تلگرام شما ارسال می‌کند.
این برنامه برای مواقعی که نیاز به پاسخ سریع به ایمیل‌های خاص دارید بدون اینکه با پیام‌های کم اهمیت‌تر منحرف شوید، ایده‌آل است.

## Installation 

The only setup required is to download an OAuth 2.0 Client ID file from Google that will authorize your application.

You can see tutorial video from here.

1. Go to https://console.developers.google.com/

2. Select a project or create new project

3. Search "Gmail API" in search bar

4. Enable it

5. Create credentials
  a. What data will you be accessing -> User data

  b. Select "Add or remove scopes and check all APIs related to "Gmail API ".

6. Go to OAuth consent screen section

7. Select "Test users " and add your current Gmail.

8. Clone this repository:
```bash
  git clone https://github.com/maverick0o0/Gmail-Notify-Bot.git
```
9. Navigate to the project directory:
Clone this repository:
```bash
  cd GmailNotifyBot
```
10. Install the required dependencies:
```bash
  pip install -r requirements.txt
```
11. Move your "OAuth 2.0 Client ID file" to root directory and change its name to "client_secret.json"
12. If you are on the server :
14. Run the main.py
```bash
python main.py
```
15. Then you have to copy that prompted link, paste in a visual browser and login into Gmail with the authorized account (The account you add in Test users).
16. After the authorization completed you face with "Unable to connect" page , That's OK just copy the URL and send cURL request to that URL in the server.
```bash
curl http://localhost:8080/?code=YOUR_CODE&scope=https://www.googleapis.com/auth/gmail.settings.basic%20https://www.googleapis.com/auth/gmail.modify
```
17. If you have access to visual browser do the same thing but you don't have to send cURL request.
18. Edit config.json file

```bash
nano config.json
```
- Enter your telegram bot token, obtained from [@BotFather](https://t.me/BotFather)
- Enter your Email that you want to monitor
You can use tmux and run the main.py
```bash
tmux new -s gmail-notify-bot
python main.py
```


