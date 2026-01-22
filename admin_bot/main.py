from handlers.points import points_entry, ask_points_input, handle_points_input, confirm_points_action
from handlers.finance import finance_entry, list_withdraw_requests, handle_finance_decision
from handlers.ads import ads_entry, list_pending_ads, handle_ads_decision

# نقاط
app.add_handler(CallbackQueryHandler(points_entry, pattern="points"))
app.add_handler(CallbackQueryHandler(lambda u,c: ask_points_input(u,c,"add"), pattern="points_add"))
app.add_handler(CallbackQueryHandler(lambda u,c: ask_points_input(u,c,"deduct"), pattern="points_deduct"))
app.add_handler(CallbackQueryHandler(lambda u,c: ask_points_input(u,c,"add_all"), pattern="points_add_all"))
app.add_handler(CallbackQueryHandler(lambda u,c: ask_points_input(u,c,"deduct_all"), pattern="points_deduct_all"))
app.add_handler(CallbackQueryHandler(confirm_points_action, pattern="^confirm_points:"))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_points_input))

# سحب/إيداع
app.add_handler(CallbackQueryHandler(finance_entry, pattern="finance"))
app.add_handler(CallbackQueryHandler(list_withdraw_requests, pattern="withdraw_requests"))
app.add_handler(CallbackQueryHandler(handle_finance_decision, pattern="^(withdraw_|deposit_)"))

# إعلانات
app.add_handler(CallbackQueryHandler(ads_entry, pattern="ads"))
app.add_handler(CallbackQueryHandler(list_pending_ads, pattern="ads_pending"))
app.add_handler(CallbackQueryHandler(handle_ads_decision, pattern="^ads_"))
