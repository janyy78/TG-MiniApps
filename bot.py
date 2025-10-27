#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ChatMember,
    Chat,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ChatMemberHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from telegram.error import Forbidden

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

BOT_TOKEN = "8394064185"
OWNER_CHAT_ID = "AAEZqQw2x53yH42ttKlL50z8O3Gmi5cFQmg"

if not BOT_TOKEN or not OWNER_CHAT_ID:
    logger.error("Veuillez définir les variables d'environnement BOT_TOKEN et OWNER_CHAT_ID.")
    raise SystemExit("Variables d'environnement manquantes : BOT_TOKEN et OWNER_CHAT_ID")

OWNER_CHAT_ID = OWNER_CHAT_ID


# ================================
# === Menu principal (/start) ===
# ================================

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Affiche un message de bienvenue + menu burger."""
    user = update.effective_user

    keyboard = [
        [InlineKeyboardButton("📜 Menu", callback_data="menu_commands")],
        [InlineKeyboardButton("ℹ️ Informations", callback_data="menu_info")],
        [InlineKeyboardButton("❌ Fermer le menu", callback_data="menu_close")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    text = (
        f"👋 Salut {user.first_name or 'utilisateur'} !\n\n"
        "Bienvenue sur le bot 👾\n"
        "Utilise le menu ci-dessous pour voir les options disponibles :"
    )

    await update.message.reply_text(text, reply_markup=reply_markup)


# ==========================
# === Gestion des menus ====
# ==========================

async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère les clics sur les boutons du menu."""
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "menu_commands":
        text = (
            "📜 **Menu complet :**\n\n"

            "## Mandarina 🍊 🌿190/73u✨ Frzsh Frozen by JbalaFarmers\n"
            "*Description :* Du vrai Fresh Frozen avec une odeur très fruitée et un arrière goût de mandarine X Cali. C’est vraiment un met de luxe offert à ce prix 🍊🇺🇸\n\n"
            

            "## Yellow Bird Us 🇺🇸 🐤🍋\n"
            "*Description :* Découvrez Yellow Bird 🐤🍋✨, beuh jaune directement venue des US, forte odeur fruitée et goût doux pour une défonce chill 💨.\n\n"
            
            "## Tangerine Dream Cali us 🇺🇸\n"
            "*Description :* Weed Sativa, odeur forte et fruitée, très agréable et énergisante 💭💥✨.\n\n"
          

            "## Sunset ice cream 🍦🌅🌿 180-90u 🇺🇸\n"
            "*Description :* Une première chez CoffeeSnoop68, un Wpff venu des US, disponible uniquement au détail ✨🫣.\n\n"


            "## Ethos Cookie R2 190/73u fresh Frozen by jbala farms\n"
            "*Description :* Odeur très fruitée, forte, avec un arrière-goût délicieux de cookies X Cali 🍪🇺🇸.\n\n"
  

            "## Lemon Crasher 220/90u fresh Frozen by jbala farms\n"
            "*Description :* Odeur fraîche de citron et fruitée, super Cali, excellent rapport qualité-prix 🍋🥶.\n\n"


            "## Cherry popers Prenium Frozen by Lasource 120u\n"
            "*Description :* Burger 100% végétal avec galette de pois chiches et sauce maison.\n\n"


            "## Mandarina 90u by The King of Hash\n"
            "*Description :* Filtré avec une odeur fruitée et un arrière-goût de mandarine très agréable 🍊.\n\n"


            "## Super hash mousseux 🧽\n"
            "*Description :* Jaune mousseux avec un goût fort et une odeur prononcée de beuh 💛.\n\n"


            "## Olive super static 🫣\n"
            "*Description :* Olivette curée à la perfection avec une odeur intense de Cali et un goût exotique en bouche. Le caviar de sa catégorie 🍇.\n\n"

        )
        await query.edit_message_text(text, parse_mode="Markdown")



    elif data == "menu_close":
        await query.edit_message_text("🍔 Menu fermé. Tu peux le rouvrir avec /start.")


# ================================
# === Détection ajout du bot ====
# ================================

def extract_user_from_my_chat_member(update: Update):
    if update.effective_user:
        return update.effective_user.id
    return None


async def handle_my_chat_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    old: ChatMember = update.my_chat_member.old_chat_member
    new: ChatMember = update.my_chat_member.new_chat_member
    chat: Chat = update.effective_chat

    became_member = old.status in ("left", "kicked") and new.status in ("member", "administrator")

    if became_member:
        logger.info("Bot ajouté au chat %s (%s)", chat.title or chat.id, chat.id)

        await context.bot.send_message(
            chat_id=chat.id,
            text="👋 Bonjour tout le monde ! Merci de m’avoir ajouté au groupe 🎉",
        )

        adder_id = extract_user_from_my_chat_member(update)

        if adder_id:
            try:
                await context.bot.send_message(
                    chat_id=adder_id,
                    text="Merci de m’avoir ajouté au groupe 🙏",
                )
            except Forbidden:
                logger.info("Impossible d’envoyer un message privé à l’utilisateur %s", adder_id)

        try:
            await context.bot.send_message(
                chat_id=OWNER_CHAT_ID,
                text=f"Le bot a été ajouté au chat {chat.title or chat.id} (id: {chat.id})",
            )
        except Exception as e:
            logger.warning("Impossible de notifier l’owner : %s", e)


# ==========================
# === Gestion des erreurs ===
# ==========================

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(msg="Erreur dans un handler :", exc_info=context.error)


# ==========================
# === Lancement du bot ====
# ==========================

def main() -> None:
    application = Application.builder().token("8394064185:AAEZqQw2x53yH42ttKlL50z8O3Gmi5cFQmg").build()

    # Commande principale //start
    application.add_handler(CommandHandler("start", start_cmd, filters=filters.Regex(r"^/start")))

    # Gestion du menu interactif
    application.add_handler(CallbackQueryHandler(menu_callback))

    # Détection de l’ajout du bot dans un groupe
    application.add_handler(ChatMemberHandler(handle_my_chat_member, chat_member_types=ChatMemberHandler.MY_CHAT_MEMBER))

    # Gestion des erreurs
    application.add_error_handler(error_handler)

    logger.info("✅ Bot démarré et prêt à fonctionner...")
    application.run_polling(allowed_updates=["message", "callback_query", "my_chat_member"])


if __name__ == "__main__":
    main()