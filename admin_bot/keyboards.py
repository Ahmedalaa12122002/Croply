from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# ===== القائمة الرئيسية =====
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("👤 إدارة المستخدمين", callback_data="menu_users")],
        [InlineKeyboardButton("💰 النقاط / العملات", callback_data="menu_points")],
        [InlineKeyboardButton("📢 الإعلانات / المهام", callback_data="menu_ads")],
        [InlineKeyboardButton("🏦 السحب / الإيداع", callback_data="menu_finance")],
        [InlineKeyboardButton("📊 الإحصائيات", callback_data="menu_stats")],
        [InlineKeyboardButton("🛡 بيانات الأدمن", callback_data="menu_admin")],
        [InlineKeyboardButton("⚙️ صلاحيات الأدمن", callback_data="menu_permissions")]
    ])

# ===== إدارة المستخدمين ====
def users_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔍 كشف حساب مستخدم", callback_data="user_check")],
        [InlineKeyboardButton("🧹 تصفير بيانات مستخدم", callback_data="user_reset")],
        [InlineKeyboardButton("❌ حذف مستخدم نهائيًا", callback_data="user_delete")],
        [InlineKeyboardButton("⬅️ رجوع", callback_data="back_main")]
    ])

# ===== النقاط =====
def points_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ إضافة نقاط", callback_data="noop")],
        [InlineKeyboardButton("➖ خصم نقاط", callback_data="noop")],
        [InlineKeyboardButton("🎁 إرسال نقاط جماعي", callback_data="noop")],
        [InlineKeyboardButton("⬅️ رجوع", callback_data="back_main")]
    ])

# ===== الإعلانات / المهام =====
def ads_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⏳ إعلانات قيد الانتظار", callback_data="noop")],
        [InlineKeyboardButton("✅ إعلانات مقبولة", callback_data="noop")],
        [InlineKeyboardButton("❌ إعلانات مرفوضة", callback_data="noop")],
        [InlineKeyboardButton("➕ إضافة إعلان", callback_data="noop")],
        [InlineKeyboardButton("⬅️ رجوع", callback_data="back_main")]
    ])

# ===== السحب / الإيداع =====
def finance_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⏳ طلبات سحب معلقة", callback_data="noop")],
        [InlineKeyboardButton("⏳ طلبات إيداع معلقة", callback_data="noop")],
        [InlineKeyboardButton("📄 سجل السحب", callback_data="noop")],
        [InlineKeyboardButton("📄 سجل الإيداع", callback_data="noop")],
        [InlineKeyboardButton("⬅️ رجوع", callback_data="back_main")]
    ])

# ===== الإحصائيات =====
def stats_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📈 إحصائيات عامة", callback_data="noop")],
        [InlineKeyboardButton("👤 إحصائيات مستخدم", callback_data="noop")],
        [InlineKeyboardButton("⬅️ رجوع", callback_data="back_main")]
    ])

# ===== بيانات الأدمن =====
def admin_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🧾 سجل نشاط الأدمن", callback_data="noop")],
        [InlineKeyboardButton("⬅️ رجوع", callback_data="back_main")]
    ])

# ===== صلاحيات الأدمن =====
def permissions_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ إضافة أدمن", callback_data="noop")],
        [InlineKeyboardButton("➖ حذف أدمن", callback_data="noop")],
        [InlineKeyboardButton("✏️ تعديل صلاحيات أدمن", callback_data="noop")],
        [InlineKeyboardButton("⬅️ رجوع", callback_data="back_main")]
    ])
