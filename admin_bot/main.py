from handlers.stats import (
    stats_entry, global_stats,
    handle_global_stats_period,
    user_stats_request, handle_user_stats_input
)
from handlers.admin_activity import (
    admin_activity_entry, handle_admin_logs_period
)

# إحصائيات
app.add_handler(CallbackQueryHandler(stats_entry, pattern="stats"))
app.add_handler(CallbackQueryHandler(global_stats, pattern="stats_global"))
app.add_handler(CallbackQueryHandler(handle_global_stats_period, pattern="global_stats:"))
app.add_handler(CallbackQueryHandler(user_stats_request, pattern="stats_user"))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_stats_input))

# سجل الأدمن
app.add_handler(CallbackQueryHandler(admin_activity_entry, pattern="admin_activity"))
app.add_handler(CallbackQueryHandler(handle_admin_logs_period, pattern="admin_logs:"))
