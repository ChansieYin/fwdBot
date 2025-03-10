from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# 你的 Telegram 账号 ID（可以是你的个人 ID 或群组的 ID）
ADMIN_ID = 123456789  # 这里填你的 Telegram ID

# 你的 USDT TRC20 地址
USDT_ADDRESS = "TnfxUShHxHceY5xHjw7qU6xH6DckCVdLqK1"  # 替换成你的 USDT TRC20 地址

# 频道介绍，强调使用 TRC20 网络
CHANNEL_DESCRIPTION = f"""👋 **欢迎加入我们的私密频道！**
🔒 这里提供：
✅ 高质量内容
✅ 会员专属福利

💰 **如何付款**：
🔹 **使用 USDT（TRC20 网络）转账**
🔹 **将转账发送到以下地址：**

📌 **USDT 地址：**
`{USDT_ADDRESS}`

⚠️ **请务必使用 TRC20 网络进行转账！**
   - 其他网络如 ERC20 或 BEP20 将导致转账失败。
   - 转账后请务必截图并发送给我。

🚨 **重要提示**：
1️⃣ 请确保使用**TRC20**网络转账，其他网络如 ERC20、BEP20 都无法接收。
2️⃣ 如果你不清楚如何选择 TRC20 网络，请在钱包中选择 **TRON** 或 **TRC20** 网络进行转账。
3️⃣ 付款后，请发送截图给我，我们会核对并手动邀请你加入频道。

"""

# 处理 /start 命令，发送 USDT 地址
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(CHANNEL_DESCRIPTION, parse_mode="Markdown", disable_web_page_preview=True)

# 处理付款截图，并转发给管理员
async def forward_payment(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user

    if update.message.photo:
        # 转发用户的付款截图
        await update.message.forward(chat_id=ADMIN_ID)

        # 发送额外的用户信息
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"💰 **收到付款截图**\n👤 用户名: @{user.username or '未设置'}\n🆔 用户 ID: {user.id}"
        )

        # 回复用户，告知已记录
        await update.message.reply_text("✅ **你的支付截图已提交，请等待审核！**")
    else:
        await update.message.reply_text("⚠️ 请发送**付款截图**，以便核对。")

# 机器人主函数
def main():
    application = Application.builder().token("YOUR_BOT_TOKEN").build()

    # 处理 /start 命令
    application.add_handler(CommandHandler("start", start))

    # 处理付款截图
    application.add_handler(MessageHandler(filters.PHOTO, forward_payment))

    # 启动机器人
    application.run_polling()

if __name__ == '__main__':
    main()
