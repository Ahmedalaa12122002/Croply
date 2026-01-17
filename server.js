const express = require("express");
const TelegramBot = require("node-telegram-bot-api");
const path = require("path");

const BOT_TOKEN = process.env.BOT_TOKEN;
const APP_URL = process.env.APP_URL;
const PORT = process.env.PORT || 3000;

if (!BOT_TOKEN || !APP_URL) {
  console.error("❌ Missing BOT_TOKEN or APP_URL");
  process.exit(1);
}

const app = express();
app.use(express.json());

// Telegram Bot (Webhook فقط – بدون polling)
const bot = new TelegramBot(BOT_TOKEN);

app.post(`/bot${BOT_TOKEN}`, (req, res) => {
  bot.processUpdate(req.body);
  res.sendStatus(200);
});

bot.onText(/\/start/, (msg) => {
  bot.sendMessage(
    msg.chat.id,
    "👋 أهلاً بك\n\nاضغط الزر بالأسفل لفتح الويب 👇",
    {
      reply_markup: {
        inline_keyboard: [[
          { text: "🚀 فتح الويب", url: APP_URL }
        ]]
      }
    }
  );
});

bot.setWebHook(`${APP_URL}/bot${BOT_TOKEN}`);

// Web App
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "web", "index.html"));
});

// Server
app.listen(PORT, "0.0.0.0", () => {
  console.log("✅ Server running on port", PORT);
});
