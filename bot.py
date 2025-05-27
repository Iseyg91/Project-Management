import discord
from discord.ext import commands, tasks
from discord import app_commands, Embed, ButtonStyle, ui
from discord.ui import Button, View, Select, Modal, TextInput, button
from discord.ui import Modal, TextInput, Button, View
from discord.utils import get
from discord import TextStyle
from functools import wraps
import os
from discord import app_commands, Interaction, TextChannel, Role
import io
import random
import asyncio
import time
import re
import subprocess
import sys
import math
import traceback
from keep_alive import keep_alive
from datetime import datetime, timedelta, timezone
from collections import defaultdict, deque
import pymongo
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
import psutil
import pytz
import platform
from discord.ui import Select, View
from typing import Optional
from discord import app_commands, Interaction, Embed, SelectOption
from discord.ui import View, Select
import uuid
from discord import app_commands, Interaction, Embed, Member, ui
from datetime import datetime

token = os.environ['ETHERYA']
intents = discord.Intents.all()
start_time = time.time()
bot = commands.Bot(command_prefix="-", intents=intents, help_command=None)
VERIFICATION_CODE = os.environ['VERIFICATION_CODE']
#Configuration du Bot:
# --- ID Owner Bot ---
ISEY_ID = 792755123587645461

# --- ID PROJECT : DELTA SERVER ---
GUILD_ID = 1359963854200639498

# --- ID DELTA PING ---
STATUT_CHANNEL_ID = 1360361796464021745
STATUT_MESSAGE_ID = 9876543210  # à remplacer
PING_ROLES = "<@&1376821268447236248> <@&1361306900981092548>"
DELTA_ID = 1356693934012891176
ID_CANAL = 1376899306719547503
# --- ID Staff Serveur Delta ---
PROJECT_DELTA = 1359963854200639498
STAFF_PROJECT = 1359963854422933876
STAFF_DELTA = 1362339333658382488
ALERT_CHANNEL_ID = 1361329246236053586
ALERT_NON_PREM_ID = 1364557116572172288
STAFF_ROLE_ID = 1362339195380568085
CHANNEL_ID = 1375496380499493004

# --- ID Sanctions Serveur Delta ---
WARN_LOG_CHANNEL = 1362435917104681230
UNWARN_LOG_CHANNEL = 1362435929452707910
BLACKLIST_LOG_CHANNEL = 1362435853997314269
UNBLACKLIST_LOG_CHANNEL = 1362435888826814586

# --- ID Gestion Delta ---
SUPPORT_ROLE_ID = 1359963854422933876
SALON_REPORT_ID = 1361362788672344290
ROLE_REPORT_ID = 1362339195380568085
TRANSCRIPT_CHANNEL_ID = 1361669998665535499
TICKET_CATEGORY_ID = 1362015652700754052

# --- ID Gestion Clients Delta ---
LOG_CHANNEL_RETIRE_ID = 1360864806957092934
LOG_CHANNEL_ID = 1360864790540582942

# --- ID Etherya ---
AUTORIZED_SERVER_ID = 1034007767050104892

log_channels = {
    "sanctions": 1361669286833426473,
    "messages": 1361669323139322066,
    "utilisateurs": 1361669350054039683,
    "nicknames": 1361669502839816372,
    "roles": 1361669524071383071,
    "vocal": 1361669536197251217,
    "serveur": 1361669784814485534,
    "permissions": 1361669810496209083,
    "channels": 1361669826011201598,
    "webhooks": 1361669963835773126,
    "bots": 1361669985705132172,
    "tickets": 1361669998665535499,
    "boosts": 1361670102818230324
}

def get_log_channel(guild, key):
    log_channel_id = log_channels.get(key)
    if log_channel_id:
        return guild.get_channel(log_channel_id)
    return None

# Fonction pour créer des embeds formatés
def create_embed(title, description, color=discord.Color.blue(), footer_text=""):
    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_footer(text=footer_text)
    return embed

# Connexion MongoDB
mongo_uri = os.getenv("MONGO_DB")  # URI de connexion à MongoDB
print("Mongo URI :", mongo_uri)  # Cela affichera l'URI de connexion (assure-toi de ne pas laisser cela en prod)
client = MongoClient(mongo_uri)
db = client['Cass-Eco2']
db2 = client['DELTA-ECO']

# Collections
collection = db['setup']  # Configuration générale
collection2 = db['setup_premium']  # Serveurs premium
collection3 = db['bounty']  # Primes et récompenses des joueurs
collection4 = db['protection'] #Serveur sous secu ameliorer
collection5 = db ['clients'] #Stock Clients 
collection6 = db ['partner'] #Stock Partner 
collection7= db ['sanction'] #Stock Sanction 
collection8 = db['idees'] #Stock Idées 
collection9 = db['stats'] #Stock Salon Stats 
collection10 = db['eco'] #Stock Les infos Eco 
collection11 = db['eco_daily'] #Stock le temps de daily 
collection12 = db['rank'] #Stock les Niveau 
collection13 = db['eco_work'] #Stock le temps de Work 
collection14 = db['eco_slut'] #Stock le temps de Slut 
collection15 = db['eco_crime'] #Stock le temps de Crime 
collection16 = db['ticket'] #Stock les Tickets
collection17 = db['team'] #Stock les Teams 
collection18 = db['logs'] #Stock les Salons Logs
collection19 = db['wl'] #Stock les whitelist 
collection20 = db['suggestions'] #Stock les Salons Suggestion 
collection21 = db['presentation'] #Stock les Salon Presentation 
collection22 = db['absence'] #Stock les Salon Absence 
collection23 = db['back_up'] #Stock les Back-up
collection24 = db['delta_warn'] #Stock les Warn Delta 
collection25 = db['delta_bl'] #Stock les Bl Delta 
collection26 = db['alerte'] #Stock les Salons Alerte
collection27 = db['guild_troll'] #Stock les serveur ou les commandes troll sont actif ou inactif
collection28 = db['sensible'] #Stock les mots sensibles actif des serveurs
collection29 = db['delta_invite'] #Stock les invitation des utilisateurs
collection30 = db['delta_points'] #Stock les points des utilisateurs
collection31 = db['delta_event']
collection32 = db['history_points'] 

# --- Charger les paramètres du serveur dynamiquement ---
def load_guild_settings(guild_id: int) -> dict:
    # Récupère la configuration spécifique au serveur à partir de la base MongoDB
    return collection21.find_one({'guild_id': guild_id}) or {}

def load_guild_settings(guild_id):
    # Charger les données de la collection principale
    setup_data = collection.find_one({"guild_id": guild_id}) or {}
    setup_premium_data = collection2.find_one({"guild_id": guild_id}) or {}
    bounty_data = collection3.find_one({"guild_id": guild_id}) or {}
    protection_data = collection4.find_one({"guild_id": guild_id}) or {}
    clients_data = collection5.find_one({"guild_id": guild_id}) or {}
    partner_data = collection6.find_one({"guild_id": guild_id}) or {}
    sanction_data = collection7.find_one({"guild_id": guild_id}) or {}
    idees_data = collection8.find_one({"guild_id": guild_id}) or {}
    stats_data = collection9.find_one({"guild_id": guild_id}) or {}
    eco_data = collection10.find_one({"guild_id": guild_id}) or {}
    eco_daily_data = collection11.find_one({"guild_id": guild_id}) or {}
    rank_data = collection12.find_one({"guild_id": guild_id}) or {}
    eco_work_data = collection13.find_one({"guild_id": guild_id}) or {}
    eco_slut_data = collection14.find_one({"guild_id": guild_id}) or {}
    eco_crime_data = collection15.find_one({"guild_id": guild_id}) or {}
    ticket_data = collection16.find_one({"guild_id": guild_id}) or {}
    team_data = collection17.find_one({"guild_id": guild_id}) or {}
    logs_data = collection18.find_one({"guild_id": guild_id}) or {}
    wl_data = collection19.find_one({"guild_id": guild_id}) or {}
    suggestions_data = collection20.find_one({"guild_id": guild_id}) or {}
    presentation_data = collection21.find_one({"guild_id": guild_id}) or {}
    absence_data = collection22.find_one({"guild_id": guild_id}) or {}
    back_up_data = collection23.find_one({"guild_id": guild_id}) or {}
    delta_warn_data = collection24.find_one({"guild_id": guild_id}) or {}
    delta_bl_data = collection25.find_one({"guild_id": guild_id}) or {}
    alerte_data = collection26.find_one({"guild_id": guild_id}) or {}
    guild_troll_data = collection27.find_one({"guild_id": guild_id}) or {}
    sensible_data = collection28.find_one({"guild_id": guild_id}) or {}
    delta_invite_data = collection29.find_one({"guild_id": guild_id}) or {}
    delta_points_data = collection30.find_one({"guild_id": guild_id}) or {}
    delta_event_data = collection31.find_one({"guild_id": guild_id}) or {}
    history_points_data = collection32.find_one({"guild_id": guild_id}) or {}
    
    # Débogage : Afficher les données de setup
    print(f"Setup data for guild {guild_id}: {setup_data}")

    combined_data = {
        "setup": setup_data,
        "setup_premium": setup_premium_data,
        "bounty": bounty_data,
        "protection": protection_data,
        "clients": clients_data,
        "partner": partner_data,
        "sanction": sanction_data,
        "idees": idees_data,
        "stats": stats_data,
        "eco": eco_data,
        "eco_daily": eco_daily_data,
        "rank": rank_data,
        "eco_work": eco_work_data,
        "eco_slut": eco_slut_data,
        "eco_crime": eco_slut_data,
        "ticket": ticket_data,
        "team": team_data,
        "logs": logs_data,
        "wl": wl_data,
        "suggestions": suggestions_data,
        "presentation": presentation_data,
        "absence": absence_data,
        "back_up": back_up_data,
        "delta_warn": delta_warn_data,
        "delta_bl": delta_bl_data,
        "alerte": alerte_data,
        "guild_troll": guild_troll_data,
        "sensible": sensible_data,
        "delta_invite": delta_invite_data,
        "delta_points": delta_points_data,
        "delta_event": delta_event_data,
        "history_points": history_points
    }

    return combined_data

# Dictionnaire pour stocker les paramètres de chaque serveur
GUILD_SETTINGS = {}

#------------------------------------------------------------------------- Code Protection:                

@tasks.loop(minutes=1)
async def add_voice_points():
    for guild in bot.guilds:
        for vc in guild.voice_channels:
            for member in vc.members:
                if member.bot:
                    continue
                collection30.update_one(
                    {"user_id": member.id, "guild_id": guild.id},
                    {"$inc": {"points": 1}},
                    upsert=True
                )

# Variables globales pour le système d'alerte
dernier_ping = None
delta_en_ligne = True

@tasks.loop(seconds=30)
async def verifier_presence_delta():
    global dernier_ping, delta_en_ligne

    canal_presence = bot.get_channel(ID_CANAL)
    salon_alerte = bot.get_channel(STATUT_CHANNEL_ID)
    maintenant = datetime.now(timezone.utc)

    if canal_presence is None or salon_alerte is None:
        return

    # Cherche un message récent de Delta
    dernier_msg_delta = None
    async for msg in canal_presence.history(limit=10):
        if msg.author.id == DELTA_ID:
            dernier_msg_delta = msg
            break

    if dernier_msg_delta and maintenant - dernier_msg_delta.created_at <= timedelta(minutes=2):
        # Delta est actif → réinitialiser
        if not delta_en_ligne:
            print("✅ Delta est de retour, alerte réinitialisée.")
        
        # ✅ Réponse stylée du bot à Delta
        await canal_presence.send(
            embed=discord.Embed(
                description=f"<a:b_yes:1376916710468354078> | **Présence confirmée :**{dernier_msg_delta.author.name}** est actif..",
                color=discord.Color.green(),
                timestamp=maintenant
            )
        )

        delta_en_ligne = True
        dernier_ping = None
        return

    # Si Delta semble hors ligne
    if delta_en_ligne:
        # Première fois qu'on le détecte hors ligne
        await salon_alerte.send(
            content=PING_ROLES,
            embed=discord.Embed(
                title="🚨 Project : Delta semble hors ligne !",
                description="Aucun message de présence détecté depuis plus de 2 minutes.",
                color=discord.Color.red(),
                timestamp=maintenant
            )
        )
        print("⚠️ Alerte envoyée pour Delta.")
        dernier_ping = maintenant
        delta_en_ligne = False
    else:
        # Delta est toujours hors ligne → vérifier si on doit relancer une alerte après 10 minutes
        if dernier_ping and maintenant - dernier_ping >= timedelta(minutes=10):
            await salon_alerte.send(
                content=PING_ROLES,
                embed=discord.Embed(
                    title="🚨 Project : Delta toujours hors ligne !",
                    description="Aucun message de présence depuis plus de 10 minutes.",
                    color=discord.Color.red(),
                    timestamp=maintenant
                )
            )
            print("🔁 Nouvelle alerte envoyée après 10 minutes.")
            dernier_ping = maintenant

# Événement quand le bot est prêt
@bot.event
async def on_ready():
    bot.add_view(TicketView(author_id=ISEY_ID))  # pour bouton "Passé Commande"
    bot.add_view(ClaimCloseView())               # pour "Claim" et "Fermer"
    bot.add_view(GlobalSupportView())  # Nécessaire pour les boutons persistants
    print(f"✅ Le bot {bot.user} est maintenant connecté ! (ID: {bot.user.id})")

    bot.uptime = time.time()
    # Démarrer les tâches de fond
    add_voice_points.start()
    verifier_presence_delta.start()
    
    guild_count = len(bot.guilds)
    member_count = sum(guild.member_count for guild in bot.guilds)

    print(f"\n📊 **Statistiques du bot :**")
    print(f"➡️ **Serveurs** : {guild_count}")
    print(f"➡️ **Utilisateurs** : {member_count}")

    activity_types = [
        discord.Activity(type=discord.ActivityType.streaming, name="Project : Delta"),
    ]

    status_types = [discord.Status.online, discord.Status.idle, discord.Status.dnd]

    await bot.change_presence(
        activity=random.choice(activity_types),
        status=random.choice(status_types)
    )

    print(f"\n🎉 **{bot.user}** est maintenant connecté et affiche ses statistiques dynamiques avec succès !")
    print("📌 Commandes disponibles 😊")
    for command in bot.commands:
        print(f"- {command.name}")

    try:
        synced = await bot.tree.sync()
        print(f"✅ Commandes slash synchronisées : {[cmd.name for cmd in synced]}")
    except Exception as e:
        print(f"❌ Erreur de synchronisation des commandes slash : {e}")

        for guild in bot.guilds:
            GUILD_SETTINGS[guild.id] = load_guild_settings(guild.id)

@bot.event
async def on_error(event, *args, **kwargs):
    print(f"Une erreur s'est produite : {event}")
    embed = discord.Embed(
        title="❗ Erreur inattendue",
        description="Une erreur s'est produite lors de l'exécution de la commande. Veuillez réessayer plus tard.",
        color=discord.Color.red()
    )
    
    # Vérifie si args[0] est une Interaction
    if isinstance(args[0], discord.Interaction):
        await args[0].response.send_message(embed=embed)
    elif isinstance(args[0], discord.Message):
        # Si c'est un message, envoie l'embed dans le canal du message
        await args[0].channel.send(embed=embed)
    elif isinstance(args[0], discord.abc.GuildChannel):
        # Si c'est un canal de type GuildChannel, assure-toi que c'est un canal textuel
        if isinstance(args[0], discord.TextChannel):
            await args[0].send(embed=embed)
        else:
            # Si c'est un autre type de canal (comme un canal vocal), essaye de rediriger le message vers un canal textuel spécifique
            text_channel = discord.utils.get(args[0].guild.text_channels, name='ton-salon-textuel')
            if text_channel:
                await text_channel.send(embed=embed)
            else:
                print("Erreur : Aucun salon textuel trouvé pour envoyer l'embed.")
    else:
        print("Erreur : Le type de l'objet n'est pas pris en charge pour l'envoi du message.")

# Cooldown pour éviter le spam de points
message_cooldowns = {}

# Liste des emojis animés à alterner
reaction_emojis = [
    "<a:4a_bubbleheart:1376670552676368557>",
    "<a:white_heart:1376670622071128185>",
    "<a:Heart:1376670687497818162>",
    "<a:pink_blue_heart:1376670720301469786>",
    "<a:heart:1376670580283146371>"
]

# Index pour alterner les emojis
current_emoji_index = 0

@bot.event
async def on_message(message):
    global current_emoji_index

    if message.author.bot:
        return

    # Salon spécifique
    if str(message.channel.id) == "1360359130161872957":
        try:
            # Réaction avec l’emoji actuel
            await message.add_reaction(reaction_emojis[current_emoji_index])

            # Passer à l’emoji suivant
            current_emoji_index = (current_emoji_index + 1) % len(reaction_emojis)
        except Exception as e:
            print(f"Erreur lors de la réaction : {e}")

    # Système de points avec cooldown
    key = f"{message.guild.id}-{message.author.id}"
    if key not in message_cooldowns:
        collection30.update_one(
            {"user_id": message.author.id, "guild_id": message.guild.id},
            {"$inc": {"points": 1}},
            upsert=True
        )
        message_cooldowns[key] = True
        await asyncio.sleep(60)
        del message_cooldowns[key]

    await bot.process_commands(message)
#-------------------------------------------------------------------------- Bot Event:
@bot.event
async def on_message_delete(message):
    if message.author.bot:
        return  # Ignore les messages de bots
    # Log du message supprimé (si sur le serveur ETHERYA)
    if message.guild and message.guild.id == PROJECT_DELTA:
        log_channel = get_log_channel(message.guild, "messages")
        if log_channel:
            embed = discord.Embed(
                title="🗑️ Message Supprimé",
                description=f"**Auteur :** {message.author.mention}\n**Salon :** {message.channel.mention}",
                color=discord.Color.red()
            )
            if message.content:
                embed.add_field(name="Contenu", value=message.content, inline=False)
            else:
                embed.add_field(name="Contenu", value="*Aucun texte (peut-être un embed ou une pièce jointe)*", inline=False)

            embed.set_footer(text=f"ID de l'utilisateur : {message.author.id}")
            embed.timestamp = message.created_at

            await log_channel.send(embed=embed)

@bot.event
async def on_message_edit(before, after):
    if before.guild and before.guild.id == PROJECT_DELTA and before.content != after.content:
        channel = get_log_channel(before.guild, "messages")
        if channel:
            embed = discord.Embed(
                title="✏️ Message Édité",
                description=f"**Auteur :** {before.author.mention}\n**Salon :** {before.channel.mention}",
                color=discord.Color.orange()
            )
            embed.add_field(name="Avant", value=before.content or "*Vide*", inline=False)
            embed.add_field(name="Après", value=after.content or "*Vide*", inline=False)
            embed.set_footer(text=f"ID de l'utilisateur : {before.author.id}")
            embed.timestamp = after.edited_at or discord.utils.utcnow()

            await channel.send(embed=embed)

@bot.event
async def on_member_join(member):
    PROJECT_DELTA = 1359963854200639498

    if member.guild.id == PROJECT_DELTA:
        guild = member.guild

        # ───── Salon de bienvenue
        welcome_channel_id = 1359963854892957893
        welcome_channel = bot.get_channel(welcome_channel_id)
        if welcome_channel:
            await welcome_channel.send(f"Bienvenue {member.mention} ! 🎉")

            embed = discord.Embed(
                title="<a:fete:1172810362261880873> **Bienvenue sur Project : Delta !** <a:fete:1172810362261880873>",
                description=(
                    "<a:pin:1172810912386777119> Ce serveur est dédié au **support du bot Project : Delta** ainsi qu’à tout ce qui touche à la **création de bots Discord**, **serveurs sur-mesure**, **sites web**, et **services de graphisme**. **Tout est là pour t’accompagner dans tes projets !**\n\n"
                    "<a:Anouncements_Animated:1355647614133207330> **Avant de démarrer, voici quelques infos essentielles :**\n\n"
                    "<a:fleche2:1290296814397816927> ⁠︱** <#1359963854892957892> ** pour éviter les mauvaises surprises.\n"
                    "<a:fleche2:1290296814397816927> ⁠︱** <#1360365346275459274> ** pour bien comprendre comment utiliser le bot Project : Delta.\n"
                    "<a:fleche2:1290296814397816927> ⁠︱** <#1361710727986937877> ** pour découvrir nos services et produits.\n\n"
                    "<a:emojigg_1:1355608239835844850> **Tu rencontres un problème ou tu as une question ?** Ouvre un ticket, notre équipe de support est là pour t’aider !\n\n"
                    "Prêt à faire évoluer tes projets avec **Project : Delta** ? <a:fete:1172810362261880873>"
                ),
                color=discord.Color.blue()
            )
            embed.set_image(url="https://github.com/Iseyg91/KNSKS-ET/blob/3702f708294b49536cb70ffdcfc711c101eb0598/IMAGES%20Delta/uri_ifs___M_ff5898f7-21fa-42c9-ad22-6ea18af53e80.jpg?raw=true")

            await welcome_channel.send(embed=embed)

        # ───── Salon de comptage des membres
        member_count_channel_id = 1360904472456593489
        member_count_channel = bot.get_channel(member_count_channel_id)
        if member_count_channel:
            member_count = len([m for m in guild.members if not m.bot])
            await member_count_channel.send(
                f"Bienvenue {member.mention}, nous sommes maintenant {member_count} <a:WelcomePengu:1361709263839428608>"
            )

        # ───── Attribution automatique de rôles
        try:
            role_ids = [1359963854376931489]  # Remplace par les ID réels des rôles à attribuer
            roles = [guild.get_role(role_id) for role_id in role_ids if guild.get_role(role_id)]

            if roles:
                await member.add_roles(*roles, reason="Rôle(s) automatique(s) à l'arrivée du membre.")
        except Exception as e:
            print(f"Erreur lors de l'ajout des rôles à {member.name}: {e}")

        # ───── Log de l'événement
        channel = get_log_channel(guild, "utilisateurs")
        if channel:
            embed_log = discord.Embed(
                title="✅ Nouveau Membre",
                description=f"{member.mention} a rejoint le serveur.",
                color=discord.Color.green()
            )
            embed_log.set_thumbnail(url=member.display_avatar.url)
            embed_log.set_footer(text=f"ID de l'utilisateur : {member.id}")
            embed_log.timestamp = member.joined_at or discord.utils.utcnow()
            await channel.send(embed=embed_log)

@bot.event
async def on_member_remove(member: discord.Member):
    guild_id = str(member.guild.id)

    # Traitement du départ de membre pour un serveur spécifique (PROJECT_DELTA)
    if member.guild.id == PROJECT_DELTA:
        channel = get_log_channel(member.guild, "utilisateurs")
        if channel:
            embed = discord.Embed(
                title="❌ Départ d'un Membre",
                description=f"{member.mention} a quitté le serveur.",
                color=discord.Color.red()
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(text=f"ID de l'utilisateur : {member.id}")
            embed.timestamp = discord.utils.utcnow()

            # Ajouter la durée de présence si disponible
            if member.joined_at:
                duration = discord.utils.utcnow() - member.joined_at
                days = duration.days
                hours = duration.seconds // 3600
                minutes = (duration.seconds % 3600) // 60

                formatted_duration = f"{days}j {hours}h {minutes}min"
                embed.add_field(name="Durée sur le serveur", value=formatted_duration, inline=False)

            await channel.send(embed=embed)

# --- Nickname update ---
@bot.event
async def on_user_update(before, after):
    # Check for username changes (this affects all mutual servers)
    for guild in bot.guilds:
        if guild.id == PROJECT_DELTA:
            if before.name != after.name:
                channel = get_log_channel(guild, "nicknames")
                if channel:
                    embed = discord.Embed(
                        title="📝 Changement de Pseudo Global",
                        description=f"{after.mention} a changé son pseudo global.",
                        color=discord.Color.blurple()
                    )
                    embed.add_field(name="Avant", value=f"`{before.name}`", inline=True)
                    embed.add_field(name="Après", value=f"`{after.name}`", inline=True)
                    embed.set_footer(text=f"ID de l'utilisateur : {after.id}")
                    embed.timestamp = discord.utils.utcnow()

                    await channel.send(embed=embed)

@bot.event
async def on_member_update(before, after):
    if before.guild.id != PROJECT_DELTA:  # Vérifier si c'est le bon serveur
        return

    # --- Stream logs ---
    if before.activity != after.activity:
        if after.activity and isinstance(after.activity, discord.Streaming):
            coins_to_add = random.randint(50, 75)
            add_coins(after.guild.id, str(after.id), coins_to_add)
            await after.send(f"Tu as reçu **{coins_to_add} Coins** pour ton stream !")

    # --- Nickname logs ---
    if before.nick != after.nick:
        channel = get_log_channel(before.guild, "nicknames")
        if channel:
            embed = discord.Embed(
                title="📝 Changement de Surnom",
                description=f"{before.mention} a modifié son surnom sur le serveur.",
                color=discord.Color.blue()
            )
            embed.add_field(name="Avant", value=f"`{before.nick}`" if before.nick else "*Aucun*", inline=True)
            embed.add_field(name="Après", value=f"`{after.nick}`" if after.nick else "*Aucun*", inline=True)
            embed.set_footer(text=f"ID de l'utilisateur : {after.id}")
            embed.timestamp = discord.utils.utcnow()

            await channel.send(embed=embed)

    # --- Boost du serveur ---
    if before.premium_since is None and after.premium_since is not None:
        channel = get_log_channel(before.guild, "boosts")
        if channel:
            embed = discord.Embed(
                title="💎 Nouveau Boost",
                description=f"{after.mention} a boosté le serveur !",
                color=discord.Color.green()
            )
            embed.set_thumbnail(url=after.display_avatar.url)
            embed.set_footer(text=f"ID de l'utilisateur : {after.id}")
            embed.timestamp = discord.utils.utcnow()

            await channel.send(embed=embed)

@bot.event
async def on_guild_role_create(role):
    guild_id = str(role.guild.id)
    # Log classique si protection désactivée
    if role.guild.id == PROJECT_DELTA:
        log_channel = get_log_channel(role.guild, "roles")
        if log_channel:
            embed = discord.Embed(
                title="🎭 Nouveau Rôle Créé",
                description=f"Un nouveau rôle a été créé : **{role.name}**",
                color=discord.Color.purple()
            )
            embed.add_field(name="ID du Rôle", value=str(role.id), inline=False)
            embed.set_footer(text="Rôle créé sur le serveur PROJECT_DELTA")
            embed.timestamp = discord.utils.utcnow()
            try:
                await log_channel.send(embed=embed)
                print(f"Log de création de rôle envoyé pour {role.name}.")
            except Exception as e:
                print(f"Erreur lors de l'envoi du log pour le rôle {role.name} : {e}")

@bot.event
async def on_guild_role_delete(role):
    guild_id = str(role.guild.id)

    # Log classique si suppression sans protection ou whitelistée
    if role.guild.id == PROJECT_DELTA:
        channel = get_log_channel(role.guild, "roles")
        if channel:
            embed = discord.Embed(
                title="🎭 Rôle Supprimé",
                description=f"Le rôle **{role.name}** a été supprimé.",
                color=discord.Color.red()
            )
            embed.add_field(name="ID du Rôle", value=str(role.id), inline=False)
            embed.set_footer(text="Rôle supprimé sur PROJECT_DELTA")
            embed.timestamp = discord.utils.utcnow()

            try:
                await channel.send(embed=embed)
                print(f"Log de suppression de rôle envoyé pour {role.name}.")
            except Exception as e:
                print(f"Erreur lors de l'envoi du log pour le rôle {role.name} : {e}")

# Logs pour les mises à jour de rôle
@bot.event
async def on_guild_role_update(before, after):
    if before.guild.id == PROJECT_DELTA:
        channel = get_log_channel(before.guild, "roles")
        if channel:
            embed = discord.Embed(
                title="🎭 Mise à Jour de Rôle",
                description=f"Le rôle **{before.name}** a été mis à jour :",
                color=discord.Color.orange()
            )
            embed.add_field(name="Avant", value=f"`{before.name}`", inline=False)
            embed.add_field(name="Après", value=f"`{after.name}`", inline=False)
            embed.add_field(name="ID du Rôle", value=str(after.id), inline=False)

            # Ajouter des informations supplémentaires, si nécessaire
            if before.permissions != after.permissions:
                embed.add_field(name="Permissions", value="Permissions modifiées", inline=False)
            
            embed.set_footer(text="Mise à jour du rôle")
            embed.timestamp = discord.utils.utcnow()

            await channel.send(embed=embed)

@bot.event
async def on_guild_channel_create(channel):
    guild_id = str(channel.guild.id)
    # Log de création si la protection n’est pas activée
    if channel.guild.id == PROJECT_DELTA:
        channel_log = get_log_channel(channel.guild, "channels")
        if channel_log:
            embed = discord.Embed(
                title="🗂️ Nouveau Salon Créé",
                description=f"Le salon **{channel.name}** a été créé.",
                color=discord.Color.blue()
            )
            embed.add_field(name="ID du Salon", value=str(channel.id), inline=False)
            embed.set_footer(text="Salon créé sur le serveur PROJECT_DELTA")
            embed.timestamp = discord.utils.utcnow()

            try:
                await channel_log.send(embed=embed)
            except Exception as e:
                print(f"Erreur lors du log de création de salon : {e}")

@bot.event
async def on_guild_channel_delete(channel):
    guild_id = str(channel.guild.id)
    # Log normal de suppression si protection non activée
    if channel.guild.id == PROJECT_DELTA:
        channel_log = get_log_channel(channel.guild, "channels")
        if channel_log:
            embed = discord.Embed(
                title="🗂️ Salon Supprimé",
                description=f"Le salon **{channel.name}** a été supprimé.",
                color=discord.Color.red()
            )
            embed.add_field(name="ID du Salon", value=str(channel.id), inline=False)
            embed.set_footer(text="Salon supprimé sur le serveur PROJECT_DELTA")
            embed.timestamp = discord.utils.utcnow()

            try:
                await channel_log.send(embed=embed)
                print(f"Log de suppression envoyé pour {channel.name}.")
            except Exception as e:
                print(f"Erreur lors de l'envoi du log pour la suppression : {e}")

# Log de la mise à jour de salon dans le serveur PROJECT_DELTA
@bot.event
async def on_guild_channel_update(before, after):
    if before.guild.id == PROJECT_DELTA:
        # Ignorer si c'est l'admin (toi) qui modifie le salon
        if before.guild.me.id == after.guild.me.id:
            return
        
        # Récupérer le salon de log pour les channels
        channel_log = get_log_channel(before.guild, "channels")
        if channel_log:
            embed = discord.Embed(
                title="🗂️ Mise à Jour de Salon",
                description=f"Le salon **{before.name}** a été mis à jour.",
                color=discord.Color.orange()
            )
            embed.add_field(name="Avant", value=f"`{before.name}`", inline=False)
            embed.add_field(name="Après", value=f"`{after.name}`", inline=False)

            # Log de modifications supplémentaires (comme les permissions, la description, etc.)
            if before.topic != after.topic:
                embed.add_field(name="Description", value=f"Avant : {before.topic if before.topic else 'Aucune'}\nAprès : {after.topic if after.topic else 'Aucune'}", inline=False)
            if before.position != after.position:
                embed.add_field(name="Position", value=f"Avant : {before.position}\nAprès : {after.position}", inline=False)

            embed.set_footer(text="Mise à jour du salon sur PROJECT_DELTA")
            embed.timestamp = discord.utils.utcnow()

            await channel_log.send(embed=embed)


# --- Voice state update ---
@bot.event
async def on_voice_state_update(member, before, after):
    if member.guild.id == PROJECT_DELTA:
        channel = get_log_channel(member.guild, "vocal")
        if channel:
            embed = discord.Embed(
                title="🎙️ Changement d'État Vocal",
                description=f"Changement d'état vocal pour {member.mention}",
                color=discord.Color.blue()
            )
            embed.set_footer(text="Logs des salons vocaux")
            embed.timestamp = discord.utils.utcnow()

            if after.channel:
                embed.add_field(name="Rejoint le salon vocal", value=f"{after.channel.name}", inline=False)
            if before.channel:
                embed.add_field(name="Quitte le salon vocal", value=f"{before.channel.name}", inline=False)

            await channel.send(embed=embed)

# --- Guild update ---
@bot.event
async def on_guild_update(before, after):
    if before.id == PROJECT_DELTA:
        channel = get_log_channel(after, "serveur")  # Assurez-vous que 'after' est le bon paramètre pour obtenir le canal
        if channel:
            embed = discord.Embed(
                title="⚙️ Mise à Jour du Serveur",
                description="Des modifications ont été apportées au serveur.",
                color=discord.Color.green()
            )
            embed.add_field(name="Nom du Serveur", value=f"{before.name} → {after.name}", inline=False)

            # Ajouter d'autres modifications si nécessaires (par exemple, les icônes ou les paramètres de vérification)
            if before.icon != after.icon:
                embed.add_field(name="Icône du Serveur", value="L'icône a été changée.", inline=False)

            if before.verification_level != after.verification_level:
                embed.add_field(name="Niveau de vérification", value=f"Avant : {before.verification_level}\nAprès : {after.verification_level}", inline=False)

            embed.set_footer(text="Mise à jour du serveur PROJECT_DELTA")
            embed.timestamp = discord.utils.utcnow()

            await channel.send(embed=embed)

# --- Webhooks update ---
@bot.event
async def on_webhooks_update(guild, channel):
    if guild.id == PROJECT_DELTA:
        webhook_channel = get_log_channel(guild, "webhooks")
        if webhook_channel:
            embed = discord.Embed(
                title="🛰️ Mise à Jour des Webhooks",
                description=f"Les webhooks ont été mis à jour dans le salon **{channel.name}**.",
                color=discord.Color.purple()
            )
            embed.add_field(name="Nom du Salon", value=channel.name, inline=False)
            embed.add_field(name="ID du Salon", value=str(channel.id), inline=False)
            embed.set_footer(text="Mise à jour des webhooks")
            embed.timestamp = discord.utils.utcnow()

            await webhook_channel.send(embed=embed)

@bot.event
async def on_member_ban(guild, user):
    guild_id = str(guild.id)
    # --- Logs de ban pour PROJECT_DELTA ---
    if guild.id == PROJECT_DELTA:
        channel = get_log_channel(guild, "sanctions")
        if channel:
            embed = discord.Embed(
                title="🔨 Membre Banni",
                description=f"Le membre **{user.mention}** a été banni du serveur.",
                color=discord.Color.red()
            )
            embed.add_field(name="ID du Membre", value=str(user.id), inline=False)
            embed.set_footer(text="Ban sur PROJECT_DELTA")
            embed.timestamp = discord.utils.utcnow()

            await channel.send(embed=embed)

# --- Logs de débannissement ---
@bot.event
async def on_member_unban(guild, user):
    if guild.id == PROJECT_DELTA:
        channel = get_log_channel(guild, "sanctions")
        if channel:
            embed = discord.Embed(
                title="🔓 Membre Débanni",
                description=f"Le membre **{user.mention}** a été débanni du serveur.",
                color=discord.Color.green()
            )
            embed.add_field(name="ID du Membre", value=str(user.id), inline=False)
            embed.set_footer(text="Débannissement sur PROJECT_DELTA")
            embed.timestamp = discord.utils.utcnow()

            await channel.send(embed=embed)

# --- Bot logs ---
@bot.event
async def on_guild_update(before, after):
    if before.id == PROJECT_DELTA:
        bot_channel = get_log_channel(after, "bots")
        if bot_channel:
            embed = discord.Embed(
                title="🤖 Mise à Jour du Serveur",
                description=f"Le serveur **{before.name}** a été mis à jour.",
                color=discord.Color.blue()
            )
            embed.add_field(name="Nom du Serveur", value=f"{before.name} → {after.name}", inline=False)

            # Ajouter d'autres informations si nécessaire
            if before.icon != after.icon:
                embed.add_field(name="Icône du Serveur", value="L'icône a été changée.", inline=False)

            embed.set_footer(text="Mise à jour du serveur sur PROJECT_DELTA")
            embed.timestamp = discord.utils.utcnow()

            await bot_channel.send(embed=embed)

# Fonction pour vérifier si l'utilisateur est administrateur
async def is_admin(interaction: discord.Interaction):
    # Utilisation de interaction.user pour accéder aux permissions
    return interaction.user.guild_permissions.administrator
#---------------------------------------------------------------------------- Ticket:
# --- MODAL POUR FERMETURE ---
class TicketModal(ui.Modal, title="Fermer le ticket"):
    reason = ui.TextInput(label="Raison de fermeture", style=discord.TextStyle.paragraph)

    async def on_submit(self, interaction: discord.Interaction):
        channel = interaction.channel
        guild = interaction.guild
        reason = self.reason.value

        transcript_channel = guild.get_channel(TRANSCRIPT_CHANNEL_ID)

        # Génération du transcript
        messages = [msg async for msg in channel.history(limit=None)]
        transcript_text = "\n".join([
            f"{msg.created_at.strftime('%Y-%m-%d %H:%M')} - {msg.author}: {msg.content}"
            for msg in messages if msg.content
        ])
        file = discord.File(fp=io.StringIO(transcript_text), filename="transcript.txt")

        # Récupération de qui a ouvert et claim
        ticket_data = collection16.find_one({"channel_id": str(channel.id)})
        opened_by = guild.get_member(int(ticket_data["user_id"])) if ticket_data else None
        claimed_by = None

        async for msg in channel.history(limit=50):
            if msg.embeds:
                embed = msg.embeds[0]
                if embed.footer and "Claimé par" in embed.footer.text:
                    user_id = int(embed.footer.text.split("Claimé par ")[-1].replace(">", "").replace("<@", ""))
                    claimed_by = guild.get_member(user_id)
                    break

        embed_log = discord.Embed(title="📁 Ticket Fermé", color=discord.Color.red())
        embed_log.add_field(name="Ouvert par", value=opened_by.mention if opened_by else "Inconnu", inline=True)
        embed_log.add_field(name="Claimé par", value=claimed_by.mention if claimed_by else "Non claim", inline=True)
        embed_log.add_field(name="Fermé par", value=interaction.user.mention, inline=True)
        embed_log.add_field(name="Raison", value=reason, inline=False)
        embed_log.set_footer(text=f"Ticket: {channel.name} | ID: {channel.id}")
        embed_log.timestamp = discord.utils.utcnow()

        await transcript_channel.send(embed=embed_log, file=file)

        await interaction.response.send_message("✅ Ticket fermé.", ephemeral=True)
        await channel.delete()

# --- VIEW AVEC CLAIM & FERMETURE ---
class ClaimCloseView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label="Claim", style=ButtonStyle.blurple, custom_id="claim")
    async def claim_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        if SUPPORT_ROLE_ID not in [role.id for role in interaction.user.roles]:
            return await interaction.response.send_message("❌ Tu n'as pas la permission de claim.", ephemeral=True)

        button.disabled = True
        await interaction.message.edit(view=self)

        embed = interaction.message.embeds[0]
        embed.set_footer(text=f"Claimé par {interaction.user.mention}")
        await interaction.message.edit(embed=embed)

        await interaction.response.send_message(f"📌 Ticket claim par {interaction.user.mention}.")

    @ui.button(label="Fermer", style=ButtonStyle.red, custom_id="close")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(TicketModal())

class TicketView(ui.View):
    def __init__(self, author_id, emoji="📩"):
        super().__init__(timeout=None)
        self.author_id = author_id
        self.emoji = emoji

        self.add_item(ui.Button(
            label="Passé Commande",
            style=ButtonStyle.success,
            custom_id="open_ticket"
        ))


@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.component and interaction.data["custom_id"] == "open_ticket":
        guild = interaction.guild
        category = guild.get_channel(1362015652700754052)

        # Récupérer l'emoji du bouton cliqué
        emoji = None
        for row in interaction.message.components:
            for component in row.children:
                if component.custom_id == "open_ticket":
                    emoji = component.emoji
        emoji_str = str(emoji) if emoji else "📩"

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        }

        # Créer le salon avec l'emoji dans le nom
        channel_name = f"{emoji_str}・{interaction.user.name}"
        ticket_channel = await guild.create_text_channel(
            name=channel_name,
            overwrites=overwrites,
            category=category
        )

        await ticket_channel.send("@everyone")
        await ticket_channel.purge(limit=1)

        embed = discord.Embed(
            title="Bienvenue dans votre ticket commande",
            description=(
                "**Bonjour,**\n\n"
                "Avant de passer votre commande, merci de vous assurer que vous disposez bien des fonds nécessaires...\n\n"
                "**Cordialement,**\n"
                "*Le staff Project : Delta*"
            ),
            color=0x5865F2
        )
        embed.set_image(url="https://github.com/Iseyg91/KNSKS-ET/blob/main/IMAGES%20Delta/uri_ifs___M_a08ff46b-5005-4ddb-86d9-a73f638d5cf2.jpg?raw=true")

        await ticket_channel.send(embed=embed, view=ClaimCloseView())

        collection16.insert_one({
            "guild_id": str(guild.id),
            "user_id": str(interaction.user.id),
            "channel_id": str(ticket_channel.id),
            "opened_at": datetime.utcnow(),
            "status": "open"
        })

        await interaction.response.send_message(f"✅ Ton ticket a été créé : {ticket_channel.mention}", ephemeral=True)

# --- COMMANDES PANEL ---
@bot.command(name="panel")
async def panel(ctx):
    if ctx.author.id != ISEY_ID:
        return await ctx.send("❌ Tu n'es pas autorisé à utiliser cette commande.")
    await ctx.send(embed=panel_embed(), view=TicketView(ctx.author.id, emoji="🤖"))

@bot.command(name="panel2")
async def panel2(ctx):
    if ctx.author.id != ISEY_ID:
        return await ctx.send("❌ Tu n'es pas autorisé à utiliser cette commande.")
    await ctx.send(embed=panel_embed(), view=TicketView(ctx.author.id, emoji="🎨"))

@bot.command(name="panel3")
async def panel3(ctx):
    if ctx.author.id != ISEY_ID:
        return await ctx.send("❌ Tu n'es pas autorisé à utiliser cette commande.")
    await ctx.send(embed=panel_embed(), view=TicketView(ctx.author.id, emoji="🌐"))

@bot.command(name="panel4")
async def panel4(ctx):
    if ctx.author.id != ISEY_ID:
        return await ctx.send("❌ Tu n'es pas autorisé à utiliser cette commande.")
    await ctx.send(embed=panel_embed(), view=TicketView(ctx.author.id, emoji="🖥️"))

# --- EMBED COMMUN ---
def panel_embed():
    return discord.Embed(
        title="Passer commande",
        description="Vous souhaitez passer une commande ? N'hésitez pas à ouvrir un ticket et nous serons ravis de vous assister !",
        color=0x2ecc71
    )

@bot.command(name="rename")
async def rename_ticket(ctx, *, new_name: str):
    # Vérifie que la commande est utilisée dans un salon de ticket
    ticket_data = collection16.find_one({"channel_id": str(ctx.channel.id)})
    if not ticket_data:
        return await ctx.send("❌ Cette commande ne peut être utilisée que dans un ticket.", delete_after=10)

    # Vérifie que l'auteur a le rôle staff
    if SUPPORT_ROLE_ID not in [role.id for role in ctx.author.roles]:
        return await ctx.send("❌ Tu n'as pas la permission d'utiliser cette commande.", delete_after=10)

    # Renommage du salon
    try:
        await ctx.channel.edit(name=new_name)
        await ctx.send(f"✅ Le ticket a été renommé en **{new_name}**.")
    except discord.Forbidden:
        await ctx.send("❌ Je n'ai pas la permission de renommer ce salon.")
    except discord.HTTPException:
        await ctx.send("❌ Une erreur est survenue lors du renommage.")

@bot.tree.command(name="close", description="Fermer ce ticket (réservé au staff)")
async def close_ticket(interaction: discord.Interaction):
    ticket_data = collection16.find_one({"channel_id": str(interaction.channel.id)})
    if not ticket_data:
        return await interaction.response.send_message("❌ Cette commande ne peut être utilisée que dans un ticket.", ephemeral=True)

    if SUPPORT_ROLE_ID not in [role.id for role in interaction.user.roles]:
        return await interaction.response.send_message("❌ Tu n'as pas la permission de fermer ce ticket.", ephemeral=True)

    await interaction.response.send_modal(TicketModal())

#-------------------------------------------------------------------------- Support:
class GlobalSupportModal(ui.Modal):
    def __init__(self):
        super().__init__(title="Fermer le ticket support")
        self.reason = ui.TextInput(
            label="Raison de fermeture",
            style=discord.TextStyle.paragraph,
            required=True
        )
        self.add_item(self.reason)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            if SUPPORT_ROLE_ID not in [role.id for role in interaction.user.roles]:
                return await interaction.response.send_message("❌ Tu n'as pas la permission de fermer ce ticket.", ephemeral=True)

            channel = interaction.channel
            guild = interaction.guild
            reason = self.reason.value
            transcript_channel = guild.get_channel(TRANSCRIPT_CHANNEL_ID)

            if not transcript_channel:
                return await interaction.response.send_message("❌ Salon de transcript introuvable.", ephemeral=True)

            # Génération du transcript
            messages = [msg async for msg in channel.history(limit=None)]
            transcript_text = "\n".join(
                f"{msg.created_at.strftime('%Y-%m-%d %H:%M')} - {msg.author}: {msg.content}"
                for msg in messages if msg.content
            )
            file = discord.File(fp=io.StringIO(transcript_text), filename="transcript.txt")

            # Récupération des données du ticket
            ticket_data = collection16.find_one({"channel_id": str(channel.id)})
            opened_by = guild.get_member(int(ticket_data["user_id"])) if ticket_data else None
            claimed_by = None

            # Recherche du membre ayant claim
            async for msg in channel.history(limit=50):
                if msg.embeds:
                    embed = msg.embeds[0]
                    if embed.footer and "Claimé par" in embed.footer.text:
                        try:
                            user_id = int(embed.footer.text.split("Claimé par ")[-1].replace(">", "").replace("<@", ""))
                            claimed_by = guild.get_member(user_id)
                        except:
                            pass
                        break

            # Embed de log
            embed_log = discord.Embed(title="🎫 Ticket Support Fermé", color=discord.Color.red())
            embed_log.add_field(name="Ouvert par", value=opened_by.mention if opened_by else "Inconnu", inline=True)
            embed_log.add_field(name="Claimé par", value=claimed_by.mention if claimed_by else "Non claim", inline=True)
            embed_log.add_field(name="Fermé par", value=interaction.user.mention, inline=True)
            embed_log.add_field(name="Raison", value=reason, inline=False)
            embed_log.set_footer(text=f"Ticket: {channel.name} | ID: {channel.id}")
            embed_log.timestamp = discord.utils.utcnow()

            await transcript_channel.send(embed=embed_log, file=file)

            await interaction.response.send_message("✅ Ticket support fermé.", ephemeral=True)

            await channel.edit(name=f"︱🚫・{interaction.user.name}")
            await asyncio.sleep(2)
            await channel.delete()

        except Exception as e:
            print(f"Erreur dans la modal : {e}")
            try:
                if not interaction.response.is_done():
                    await interaction.response.send_message("❌ Une erreur est survenue.", ephemeral=True)
                else:
                    await interaction.followup.send("❌ Une erreur est survenue.", ephemeral=True)
            except:
                pass
# ========== VUE SUPPORT ==========

class GlobalSupportView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label="Claim", style=discord.ButtonStyle.primary, custom_id="claim_support")
    async def claim_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        if SUPPORT_ROLE_ID not in [role.id for role in interaction.user.roles]:
            return await interaction.response.send_message("❌ Tu n'as pas la permission de claim.", ephemeral=True)

        button.disabled = True
        await interaction.message.edit(view=self)

        embed = interaction.message.embeds[0]
        embed.set_footer(text=f"Claimé par {interaction.user.mention}")
        await interaction.message.edit(embed=embed)

        await interaction.response.send_message(f"📌 Ticket support claim par {interaction.user.mention}.")

    @ui.button(label="Fermer", style=discord.ButtonStyle.red, custom_id="close_support")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        if SUPPORT_ROLE_ID not in [role.id for role in interaction.user.roles]:
            return await interaction.response.send_message("❌ Tu n'as pas la permission de fermer ce ticket.", ephemeral=True)
    
        await interaction.response.send_modal(GlobalSupportModal())

# ========== VUE POUR OUVERTURE DE TICKET ==========
class GlobalSupportTicketView(ui.View):
    def __init__(self, author_id, emoji="🎟️"):
        super().__init__(timeout=None)
        self.author_id = author_id
        self.emoji = emoji

        self.add_item(ui.Button(
            label="Support Global",
            style=discord.ButtonStyle.primary,
            custom_id="open_global_support"
        ))

# ========== COMMANDE POUR PANEL SUPPORT ==========

@bot.command(name="panel-support")
async def panel_support(ctx):
    if ctx.author.id != ISEY_ID:
        return await ctx.send("❌ Tu n'es pas autorisé à utiliser cette commande.")
    await ctx.send(embed=discord.Embed(
        title="Panel Support Global",
        description="Cliquez sur le bouton ci-dessous pour ouvrir un ticket support.",
        color=discord.Color.red()
    ), view=GlobalSupportTicketView(ctx.author.id))


# ========== HANDLER POUR L'OUVERTURE DU TICKET ==========

@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.component and interaction.data.get("custom_id") == "open_global_support":
        guild = interaction.guild
        user = interaction.user

        existing_channel = discord.utils.get(guild.text_channels, name=f"ticket-{user.id}")
        if existing_channel:
            return await interaction.response.send_message(f"❌ Tu as déjà un ticket ouvert : {existing_channel.mention}", ephemeral=True)

        category = guild.get_channel(TICKET_CATEGORY_ID)
        if not category or not isinstance(category, discord.CategoryChannel):
            return await interaction.response.send_message("❌ Catégorie de tickets introuvable.", ephemeral=True)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            guild.get_role(SUPPORT_ROLE_ID): discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }

        ticket_channel = await guild.create_text_channel(
            name=f"︱🚫・{user.name}",
            category=category,
            overwrites=overwrites,
            reason="Ticket support global"
        )

        collection16.insert_one({
            "user_id": str(user.id),
            "channel_id": str(ticket_channel.id)
        })

        embed = discord.Embed(
            title="📩 Ticket ouvert",
            description=(
                "Merci d’avoir ouvert un ticket sur notre système de support.\n\n"
                "Notre équipe a bien reçu ta demande et un membre du staff viendra te répondre dès que possible. "
                "Nous faisons notre maximum pour traiter chaque requête rapidement et efficacement, alors merci de faire preuve d’un peu de patience.\n\n"
                "Pendant ce temps, pense à détailler au maximum ton problème ou ta question dans ce ticket. Plus tu es précis, plus nous pourrons t’aider rapidement et efficacement. "
                "Voici quelques conseils :\n"
                "- Explique clairement ce que tu veux signaler ou demander\n"
                "- Si possible, joins des captures d’écran ou des liens utiles\n"
                "- Évite de mentionner plusieurs fois le staff, cela ne fera pas accélérer le processus\n\n"
                "🔒 Ce ticket est privé : seuls toi et les membres du staff peuvent le voir.\n"
                "📌 Une fois ta demande résolue, un membre du staff ou toi-même pourrez fermer le ticket en utilisant le bouton prévu à cet effet.\n\n"
                "Merci de ta confiance et de faire partie de notre communauté ❤️"
            ),
            color=discord.Color.green()
        )
        await ticket_channel.send(content=user.mention, embed=embed, view=GlobalSupportView())
        await interaction.response.send_message(f"✅ Ton ticket a été ouvert ici : {ticket_channel.mention}", ephemeral=True)


#--------------------------------------------------------------------------- Gestion Clients

@bot.tree.command(name="add-client", description="Ajoute un client via mention ou ID")
@app_commands.describe(
    user="Mentionne un membre du serveur",
    service="Type de service acheté",
    service_name="Nom du service acheté (ex: Project : Delta)"
)
@app_commands.choices(
    service=[
        app_commands.Choice(name="Graphisme", value="Graphisme"),
        app_commands.Choice(name="Serveur Discord", value="Serveur"),
        app_commands.Choice(name="Site Web", value="Site"),
        app_commands.Choice(name="Bot Discord", value="Bot"),
    ]
)
async def add_client(
    interaction: discord.Interaction,
    user: discord.Member,
    service: app_commands.Choice[str],
    service_name: str
):
    try:
        if not interaction.response.is_done():
            await interaction.response.defer(thinking=True)

        if not interaction.guild or interaction.guild.id != PROJECT_DELTA:
            return await interaction.followup.send("❌ Cette commande n'est autorisée que sur le serveur Project : Delta.", ephemeral=True)

        role = discord.utils.get(interaction.user.roles, id=STAFF_PROJECT)
        if not role:
            return await interaction.followup.send("🚫 Tu dois avoir le rôle `Staff Project` pour utiliser cette commande.", ephemeral=True)
        
        print(f"🔧 Commande /add_client lancée par {interaction.user} ({interaction.user.id}) pour {user} ({user.id})")

        existing_data = collection5.find_one({"guild_id": interaction.guild.id}) or {}
        existing_clients = existing_data.get("clients", [])

        if any(client.get("user_id") == user.id for client in existing_clients):
            return await interaction.followup.send(f"⚠️ {user.mention} est déjà enregistré comme client !", ephemeral=True)

        purchase_date = datetime.utcnow().strftime("%d/%m/%Y à %H:%M:%S")
        client_data = {
            "user_id": user.id,
            "service": service.value,
            "service_name": service_name,
            "purchase_date": purchase_date,
            "creator_id": interaction.user.id,
            "done_by": {
                "name": str(interaction.user),
                "id": interaction.user.id
            }
        }

        if existing_data:
            collection5.update_one(
                {"guild_id": interaction.guild.id},
                {"$push": {"clients": client_data}}
            )
        else:
            collection5.insert_one({
                "guild_id": interaction.guild.id,
                "clients": [client_data]
            })

        role = discord.utils.get(interaction.guild.roles, id=1359963854389379241)
        if role:
            await user.add_roles(role)

        confirmation_embed = discord.Embed(
            title="🎉 Nouveau client enregistré !",
            description=f"Bienvenue à {user.mention} en tant que **client officiel** ! 🛒",
            color=discord.Color.green()
        )
        confirmation_embed.add_field(name="🛠️ Service", value=f"`{service.value}`", inline=True)
        confirmation_embed.add_field(name="📌 Nom du Service", value=f"`{service_name}`", inline=True)
        confirmation_embed.add_field(name="👨‍💻 Réalisé par", value=f"`{interaction.user}`", inline=False)
        confirmation_embed.add_field(name="🗓️ Date d'achat", value=f"`{purchase_date}`", inline=False)
        confirmation_embed.set_footer(text=f"Ajouté par {interaction.user}", icon_url=interaction.user.display_avatar.url)
        confirmation_embed.set_thumbnail(url=user.display_avatar.url)

        await interaction.followup.send(embed=confirmation_embed)

        log_channel = bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            log_embed = discord.Embed(
                title="📋 Nouveau client ajouté",
                color=discord.Color.green(),
                timestamp=datetime.utcnow()
            )
            log_embed.add_field(name="👤 Client", value=f"{user.mention} (`{user.id}`)", inline=False)
            log_embed.add_field(name="🛠️ Service", value=service.value, inline=True)
            log_embed.add_field(name="📌 Nom", value=service_name, inline=True)
            log_embed.add_field(name="👨‍💻 Fait par", value=f"{interaction.user} (`{interaction.user.id}`)", inline=False)
            log_embed.add_field(name="🗓️ Date", value=purchase_date, inline=False)
            log_embed.set_footer(text="Log automatique", icon_url=interaction.user.display_avatar.url)

            await log_channel.send(embed=log_embed)

    except Exception as e:
        print("❌ Erreur inattendue :", e)
        traceback.print_exc()
        await interaction.followup.send("⚠️ Une erreur est survenue. Merci de réessayer plus tard.", ephemeral=True)

@bot.tree.command(name="remove-client", description="Supprime un client enregistré")
@app_commands.describe(
    user="Mentionne le client à supprimer"
)
async def remove_client(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.defer(thinking=True)

    # Vérifier que la commande est exécutée sur le bon serveur
    if interaction.guild.id != PROJECT_DELTA:
        return await interaction.response.send_message("❌ Cette commande n'est autorisée que sur le serveur Project : Delta.", ephemeral=True)

        role = discord.utils.get(interaction.user.roles, id=STAFF_PROJECT)
        if not role:
            return await interaction.followup.send("🚫 Tu dois avoir le rôle `Staff Project` pour utiliser cette commande.", ephemeral=True)

    if not interaction.guild:
        return await interaction.followup.send("❌ Cette commande ne peut être utilisée qu'en serveur.", ephemeral=True)

    try:
        print(f"🗑️ Commande /remove_client lancée par {interaction.user} pour {user}")

        # Suppression du await ici
        existing_data = collection5.find_one({"guild_id": interaction.guild.id})
        if not existing_data:
            return await interaction.followup.send("❌ Aucun client enregistré pour ce serveur.")

        clients = existing_data.get("clients", [])
        client_found = None

        for client in clients:
            if client.get("user_id") == user.id:
                client_found = client
                break

        if not client_found:
            return await interaction.followup.send(f"⚠️ {user.mention} n'est pas enregistré comme client.")

        # Suppression du client dans la base de données
        collection5.update_one(
            {"guild_id": interaction.guild.id},
            {"$pull": {"clients": {"user_id": user.id}}}
        )

        # Retirer le rôle de l'utilisateur
        role = discord.utils.get(interaction.guild.roles, id=1359963854389379241)
        if role:
            await user.remove_roles(role)
            print(f"🔧 Rôle retiré de {user} avec succès.")
        else:
            print("⚠️ Rôle introuvable.")

        # Embed public de confirmation
        embed = discord.Embed(
            title="🗑️ Client retiré",
            description=f"{user.mention} a été retiré de la liste des clients.",
            color=discord.Color.red()
        )
        embed.add_field(name="🛠️ Ancien service", value=f"`{client_found['service']}`", inline=True)
        embed.add_field(name="📌 Nom du service", value=f"`{client_found['service_name']}`", inline=True)
        embed.add_field(name="🗓️ Achat le", value=f"`{client_found['purchase_date']}`", inline=False)
        embed.set_footer(text=f"Retiré par {interaction.user}", icon_url=interaction.user.display_avatar.url)
        embed.set_thumbnail(url=user.display_avatar.url)

        await interaction.followup.send(embed=embed)

        # Log dans le salon des logs
        log_channel = bot.get_channel(LOG_CHANNEL_RETIRE_ID)
        if log_channel:
            log_embed = discord.Embed(
                title="🔴 Client retiré",
                description=f"👤 {user.mention} (`{user.id}`)\n❌ Supprimé de la base de clients.",
                color=discord.Color.red()
            )
            log_embed.set_footer(text=f"Retiré par {interaction.user}", icon_url=interaction.user.display_avatar.url)
            log_embed.timestamp = discord.utils.utcnow()
            await log_channel.send(embed=log_embed)
        else:
            print("⚠️ Salon de log introuvable.")

    except Exception as e:
        print("❌ Erreur inattendue :", e)
        traceback.print_exc()
        await interaction.followup.send("⚠️ Une erreur est survenue pendant la suppression. Merci de réessayer plus tard.", ephemeral=True)


class ClientListView(View):
    def __init__(self, clients, author):
        super().__init__(timeout=60)
        self.clients = clients
        self.author = author
        self.page = 0
        self.per_page = 5

    def format_embed(self):
        start = self.page * self.per_page
        end = start + self.per_page
        embed = discord.Embed(
            title="📋 Liste des Clients",
            description=f"Voici les clients enregistrés sur ce serveur ({len(self.clients)} total) :",
            color=discord.Color.blurple()
        )

        for i, client in enumerate(self.clients[start:end], start=1 + start):
            user_mention = f"<@{client['user_id']}>"
            creator_mention = f"<@{client.get('creator_id', 'inconnu')}>"

            embed.add_field(
                name=f"👤 Client #{i}",
                value=(
                    f"**Utilisateur :** {user_mention}\n"
                    f"**Service :** `{client['service']}`\n"
                    f"**Nom :** `{client['service_name']}`\n"
                    f"**📅 Date :** `{client['purchase_date']}`\n"
                    f"**👨‍🔧 Réalisé par :** {creator_mention}"
                ),
                inline=False
            )

        total_pages = ((len(self.clients) - 1) // self.per_page) + 1
        embed.set_footer(text=f"Page {self.page + 1} / {total_pages}")
        return embed

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author.id:
            await interaction.response.send_message("❌ Tu ne peux pas interagir avec cette vue.", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="⬅️", style=discord.ButtonStyle.gray)
    async def previous(self, interaction: discord.Interaction, button: Button):
        if self.page > 0:
            self.page -= 1
            await interaction.response.edit_message(embed=self.format_embed(), view=self)

    @discord.ui.button(label="➡️", style=discord.ButtonStyle.gray)
    async def next(self, interaction: discord.Interaction, button: Button):
        if (self.page + 1) * self.per_page < len(self.clients):
            self.page += 1
            await interaction.response.edit_message(embed=self.format_embed(), view=self)

@bot.tree.command(name="list-clients", description="Affiche tous les clients enregistrés")
async def list_clients(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)

    # Vérifier que la commande est exécutée sur le bon serveur
    if interaction.guild.id != PROJECT_DELTA:
        return await interaction.response.send_message("❌ Cette commande n'est autorisée que sur le serveur Project : Delta.", ephemeral=True)

        role = discord.utils.get(interaction.user.roles, id=STAFF_PROJECT)
        if not role:
            return await interaction.followup.send("🚫 Tu dois avoir le rôle `Staff Project` pour utiliser cette commande.", ephemeral=True)

    try:
        data = collection5.find_one({"guild_id": interaction.guild.id})
        if not data or not data.get("clients"):
            return await interaction.followup.send("❌ Aucun client enregistré sur ce serveur.")

        clients = data["clients"]
        view = ClientListView(clients, interaction.user)
        embed = view.format_embed()
        await interaction.followup.send(embed=embed, view=view)

    except Exception as e:
        print("❌ Erreur lors de la récupération des clients :", e)
        traceback.print_exc()
        await interaction.followup.send("⚠️ Une erreur est survenue pendant l'affichage.")

@bot.command(name="points")
async def points(ctx, member: discord.Member = None):
    member = member or ctx.author

    # Récupération des données depuis MongoDB
    user_data = collection30.find_one({"user_id": member.id, "guild_id": ctx.guild.id})
    points = user_data.get("points", 0) if user_data else 0

    # Création de l'embed
    embed = discord.Embed(
        title="<a:fete:1375944789035319470> Événement de Lancement - Points Collectés !",
        description=(
            f"<a:blblbl:1376554956550705182> **{member.mention}**, voici tes points actuel :\n\n"
            f"> <a:fleche3:1376557416216268921> **{points}** points\n\n"
            f"Continue à participer pour en gagner encore plus ! "
        ),
        color=discord.Color.gold()
    )
    embed.set_author(name=member.name, icon_url=member.display_avatar.url)
    embed.set_footer(
        text="Delta • Système de points événementiel",
        icon_url=ctx.guild.icon.url if ctx.guild.icon else None
    )
    embed.timestamp = ctx.message.created_at

    await ctx.send(embed=embed)

# Modal de vérification pour le reset
class ResetPointsVerificationModal(ui.Modal, title="❗ Confirmation requise"):

    code = ui.TextInput(label="Code de vérification", placeholder="Entre le code fourni", required=True)

    def __init__(self, interaction: Interaction):
        super().__init__()
        self.interaction = interaction

    async def on_submit(self, interaction: Interaction):
        if self.code.value != VERIFICATION_CODE:
            await interaction.response.send_message("❌ Code incorrect. Suppression annulée.", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True, thinking=True)

        try:
            result = collection30.delete_many({})
            await interaction.followup.send(
                f"✅ Suppression réussie : `{result.deleted_count}` documents supprimés.",
                ephemeral=True
            )
        except Exception as e:
            print(f"[ERREUR - reset-points] : {e}")
            await interaction.followup.send("⚠️ Une erreur est survenue pendant la suppression.", ephemeral=True)

# Commande slash /reset-points
@bot.tree.command(name="reset-points", description="Supprime tous les points (réservé à Isey).")
async def reset_points(interaction: Interaction):
    if interaction.user.id != ISEY_ID:
        await interaction.response.send_message("❌ Seul Isey peut utiliser cette commande.", ephemeral=True)
        return

    await interaction.response.send_modal(ResetPointsVerificationModal(interaction))

@bot.tree.command(name="give-points", description="Donne des points à un utilisateur.")
@app_commands.describe(
    user="L'utilisateur à qui donner des points",
    amount="Le nombre de points à donner",
    reason="La raison pour laquelle les points sont donnés"
)
async def give_points(interaction: discord.Interaction, user: discord.Member, amount: int, reason: str):
    # Vérification des permissions
    if not (interaction.user.guild_permissions.administrator or interaction.user.id == ISEY_ID):
        embed = discord.Embed(
            title="❌ Permission refusée",
            description="Tu n'as pas la permission d'utiliser cette commande.",
            color=0xe74c3c
        )
        return await interaction.response.send_message(embed=embed, ephemeral=True)

    if amount <= 0:
        embed = discord.Embed(
            title="⚠️ Montant invalide",
            description="Le montant doit être supérieur à 0.",
            color=0xe74c3c
        )
        return await interaction.response.send_message(embed=embed, ephemeral=True)

    if not reason.strip():
        embed = discord.Embed(
            title="⚠️ Raison manquante",
            description="Tu dois fournir une raison pour donner des points.",
            color=0xe67e22
        )
        return await interaction.response.send_message(embed=embed, ephemeral=True)

    # Récupération des données depuis MongoDB
    user_data = collection30.find_one({"user_id": user.id, "guild_id": interaction.guild.id})

    if user_data:
        new_points = user_data.get("points", 0) + amount
        collection30.update_one(
            {"user_id": user.id, "guild_id": interaction.guild.id},
            {"$set": {"points": new_points}}
        )
    else:
        new_points = amount
        collection30.insert_one({
            "user_id": user.id,
            "guild_id": interaction.guild.id,
            "points": new_points
        })

    # ⏺️ Enregistrement dans l'historique
    collection32.insert_one({
        "guild_id": interaction.guild.id,
        "user_id": user.id,
        "amount": amount,
        "remaining_points": new_points,
        "reason": reason,
        "staff_id": interaction.user.id,
        "staff_name": interaction.user.name,
        "timestamp": datetime.utcnow(),
        "action": "add"
    })

    # ✅ Confirmation
    embed = discord.Embed(
        title="✅ Points ajoutés",
        description=(
            f"{amount} points ont été donnés à {user.mention} !\n"
            f"Il a maintenant **{new_points}** points.\n\n"
            f"**Raison :** {reason}"
        ),
        color=0x2ecc71
    )
    await interaction.response.send_message(embed=embed)
    
@bot.tree.command(name="remove-points", description="Retire des points à un utilisateur.")
@app_commands.describe(
    user="L'utilisateur à qui retirer des points", 
    amount="Le nombre de points à retirer",
    reason="La raison du retrait"
)
async def remove_points(interaction: discord.Interaction, user: discord.Member, amount: int, reason: str):
    # Vérification des permissions
    if not (interaction.user.guild_permissions.administrator or interaction.user.id == ISEY_ID):
        embed = discord.Embed(
            title="❌ Permission refusée",
            description="Tu n'as pas la permission d'utiliser cette commande.",
            color=0xe74c3c
        )
        return await interaction.response.send_message(embed=embed, ephemeral=True)

    if amount <= 0:
        embed = discord.Embed(
            title="⚠️ Montant invalide",
            description="Le montant doit être supérieur à 0.",
            color=0xe74c3c
        )
        return await interaction.response.send_message(embed=embed, ephemeral=True)

    if not reason.strip():
        embed = discord.Embed(
            title="⚠️ Raison requise",
            description="Tu dois spécifier une raison pour retirer des points.",
            color=0xe67e22
        )
        return await interaction.response.send_message(embed=embed, ephemeral=True)

    # Récupération des données depuis MongoDB
    user_data = collection30.find_one({"user_id": user.id, "guild_id": interaction.guild.id})

    if user_data:
        current_points = user_data.get("points", 0)
        new_points = max(0, current_points - amount)
        
        # Mise à jour des points
        collection30.update_one(
            {"user_id": user.id, "guild_id": interaction.guild.id},
            {"$set": {"points": new_points}}
        )

        # Enregistrement dans l'historique
        collection32.insert_one({
            "guild_id": interaction.guild.id,
            "user_id": user.id,
            "user_name": str(user),
            "action": "remove",
            "amount": amount,
            "remaining_points": new_points,
            "reason": reason,
            "staff_id": interaction.user.id,
            "staff_name": str(interaction.user),
            "timestamp": datetime.utcnow()
        })

        embed = discord.Embed(
            title="✅ Points retirés",
            description=(
                f"{amount} points ont été retirés à {user.mention}.\n"
                f"Il lui reste maintenant **{new_points}** points.\n\n"
                f"**Raison :** {reason}"
            ),
            color=0xf1c40f
        )
    else:
        embed = discord.Embed(
            title="⚠️ Utilisateur introuvable",
            description=f"{user.mention} n’a aucun point enregistré.",
            color=0xe74c3c
        )

    await interaction.response.send_message(embed=embed)

class HistoryView(ui.View):
    def __init__(self, pages):
        super().__init__(timeout=120)
        self.pages = pages
        self.current_page = 0

    async def update_message(self, interaction: Interaction):
        for child in self.children:
            if isinstance(child, ui.Button):
                child.disabled = False
        if self.current_page == 0:
            self.children[0].disabled = True  # Précédent
        if self.current_page == len(self.pages) - 1:
            self.children[1].disabled = True  # Suivant
        await interaction.response.edit_message(embed=self.pages[self.current_page], view=self)

    @ui.button(label="⬅️ Précédent", style=discord.ButtonStyle.blurple)
    async def previous_page(self, interaction: Interaction, button: ui.Button):
        self.current_page -= 1
        await self.update_message(interaction)

    @ui.button(label="➡️ Suivant", style=discord.ButtonStyle.blurple)
    async def next_page(self, interaction: Interaction, button: ui.Button):
        self.current_page += 1
        await self.update_message(interaction)

@bot.tree.command(name="history", description="Affiche l'historique des points d'un utilisateur.")
@app_commands.describe(user="L'utilisateur dont tu veux voir l'historique.")
async def history(interaction: Interaction, user: Member):
    records = list(collection32.find({"user_id": user.id, "guild_id": interaction.guild.id}).sort("timestamp", -1))

    if not records:
        embed = Embed(
            title="📜 Historique vide",
            description=f"Aucune action trouvée pour {user.mention}.",
            color=0x95a5a6
        )
        return await interaction.response.send_message(embed=embed, ephemeral=True)

    entries_per_page = 5
    pages = []

    for i in range(0, len(records), entries_per_page):
        chunk = records[i:i+entries_per_page]
        description = ""

        for entry in chunk:
            action = entry.get("action", "add")
            amount = entry.get("amount", 0)
            sign = "+" if action == "add" else "-"
            emoji = "✅" if action == "add" else "❌"
            reason = entry.get("reason", "Aucune raison")
            staff_name = entry.get("staff_name", "Inconnu")
            timestamp = entry.get("timestamp")
            time_str = timestamp.strftime("%Y-%m-%d %H:%M") if timestamp else "inconnue"

            description += f"{emoji} `{sign}{amount}` | **{reason}**\nPar `{staff_name}` le {time_str} UTC\n\n"

        embed = Embed(
            title=f"📊 Historique de {user.name}",
            description=description,
            color=0x3498db
        )
        embed.set_footer(text=f"Page {len(pages)+1} / {((len(records)-1)//entries_per_page)+1}")
        pages.append(embed)

    view = HistoryView(pages)
    await interaction.response.send_message(embed=pages[0], view=view, ephemeral=True)

# Token pour démarrer le bot (à partir des secrets)
# Lancer le bot avec ton token depuis l'environnement  
keep_alive()
bot.run(token)
