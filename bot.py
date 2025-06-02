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
bot = commands.Bot(command_prefix="!!", intents=intents, help_command=None)
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
PROJECT_DELTA_ID = 1356693934012891176
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

# --- Eco ---
ECO_ROLES_VIP = [1359963854402228315, 1361307897287675989]

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
collection29 = db['delta_invite'] #Stock les invitation des utilisateurs
collection30 = db['delta_points'] #Stock les points des utilisateurs
collection31 = db['delta_event']
collection32 = db['history_points']
#-------------------------------------------------------------------------- DB2
# Collections
collection28 = db2['ether_eco']  #Stock les Bal
collection44 = db2['ether_daily']  #Stock les cd de daily
collection45 = db2['ether_slut']  #Stock les cd de slut
collection46 = db2['ether_crime']  #Stock les cd de slut
collection47 = db2['ether_collect'] #Stock les cd de collect
collection33 = db2['ether_work'] #Stock les cd de Work
collection34 = db2['ether_inventory'] #Stock les inventaires
collection35 = db2['info_cf'] #Stock les Info du cf
collection36 = db2['info_logs'] #Stock le Salon logs
collection37 = db2['info_bj'] #Stock les Info du Bj
collection38 = db2['info_rr'] #Stock les Info de RR
collection39 = db2['info_roulette'] #Stock les Info de SM
collection40 = db2['info_sm'] #Stock les Info de SM
collection41 = db2['ether_rob'] #Stock les cd de Rob
collection42 = db2['anti_rob'] #Stock les rôle anti-rob
collection43 = db2['daily_badge'] #Stock les cd des daily badge

# --- Charger les paramètres du serveur dynamiquement ---
def load_guild_settings(guild_id: int) -> dict:
    # Récupère la configuration spécifique au serveur à partir de la base MongoDB
    return collection21.find_one({'guild_id': guild_id}) or {}

def get_cf_config(guild_id):
    config = collection35.find_one({"guild_id": guild_id})
    if not config:
        # Valeurs par défaut
        config = {
            "guild_id": guild_id,
            "start_chance": 50,
            "max_chance": 100,
            "max_bet": 20000
        }
        collection35.insert_one(config)
    return config
    
# Fonction pour récupérer les données d'un utilisateur
def get_user_eco(guild_id, user_id):
    user_data = collection28.find_one({"guild_id": guild_id, "user_id": user_id})
    if not user_data:
        # Si l'utilisateur n'a pas encore de données, on les crée
        collection10.insert_one({
            "guild_id": guild_id,
            "user_id": user_id,
            "coins": 0,
            "last_daily": None
        })
        return {"coins": 0, "last_daily": None}
    return user_data

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
    ether_eco_data = collection28.find_one({"guild_id": guild_id}) or {}
    ether_daily_data = collection44.find_one({"guild_id": guild_id}) or {}
    ether_slut_data = collection45.find_one({"guild_id": guild_id}) or {}
    ether_crime_data = collection46.find_one({"guild_id": guild_id}) or {}
    ether_collect_data = collection47.find_one({"guild_id": guild_id}) or {}
    ether_work_data = collection33.find_one({"guild_id": guild_id}) or {}
    ether_inventory_data = collection34.find_one({"guild_id": guild_id}) or {}
    info_cf_data = collection35.find_one({"guild_id": guild_id}) or {}
    info_logs_data = collection36.find_one({"guild_id": guild_id}) or {}
    info_bj_data = collection37.find_one({"guild_id": guild_id}) or {}
    info_rr_data = collection38.find_one({"guild_id": guild_id}) or {}
    info_roulette_data = collection39.find_one({"guild_id": guild_id}) or {}
    info_sm_data = collection40.find_one({"guild_id": guild_id}) or {}
    ether_rob_data = collection41.find_one({"guild_id": guild_id}) or {}
    anti_rob_data = collection42.find_one({"guild_id": guild_id}) or {}
    ether_daily_badge_data = collection43.find_one({"guild_id": guild_id}) or {}
    
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
        "history_points": history_points,
        "ether_eco": ether_eco_data,
        "ether_daily": ether_daily_data,
        "ether_slut": ether_slut_data,
        "ether_crime": ether_crime_data,
        "ether_collect": ether_collect_data,
        "ether_work": ether_work_data,
        "ether_inventory": ether_inventory_data,
        "info_cf": info_cf_data,
        "info_logs": info_logs_data,
        "info_bj": info_bj_data,
        "info_rr": info_rr_data,
        "info_roulette": info_roulette_data,
        "info_sm": info_sm_data,
        "ether_rob": ether_rob_data,
        "anti_rob": anti_rob_data,
        "daily_badge": daily_badge_data
    }

    return combined_data

# Dictionnaire pour stocker les paramètres de chaque serveur
GUILD_SETTINGS = {}

TOP_ROLES = {
    1: 1363923497885237298,  # ID du rôle Top 1
    2: 1363923494504501510,  # ID du rôle Top 2
    3: 1363923356688056401,  # ID du rôle Top 3
}

# Config des rôles
COLLECT_ROLES_CONFIG = [
    {
        "role_id": 1359963854402228315, #Membres
        "amount": 150,
        "cooldown": 3600,
        "auto": False,
        "target": "bank"
    },
        {
        "role_id": 1361307897287675989, #Membres
        "amount": 150,
        "cooldown": 3600,
        "auto": False,
        "target": "bank"
    },
    {
        "role_id": 1363969965572755537, #Nen Maudit
        "percent": -20,
        "cooldown": 7200,
        "auto": True,
        "target": "bank"
    },
]

#------------------------------------------------------------------------- Code Protection:                

@tasks.loop(minutes=5)
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

dernier_ping = None
delta_en_ligne = True

@tasks.loop(minutes=2)
async def verifier_presence_delta():
    canal_verification = bot.get_channel(ID_CANAL)  # Salon où Delta envoie ses messages de présence
    canal_alerte = bot.get_channel(STATUT_CHANNEL_ID)  # Salon où tu veux envoyer l'alerte

    if not canal_verification or not canal_alerte:
        return

    messages = [msg async for msg in canal_verification.history(limit=5)]
    maintenant = datetime.now(timezone.utc)

    # Cherche le dernier message de Delta
    dernier = next((m for m in messages if m.author.id == DELTA_ID), None)

    if not dernier or (maintenant - dernier.created_at > timedelta(minutes=2)):
        await canal_alerte.send(
            content=PING_ROLES,
            embed=discord.Embed(
                title="🚨 Project : Delta semble hors ligne !",
                description="Aucun message de présence détecté depuis plus de 2 minutes.",
                color=discord.Color.red(),
                timestamp=datetime.utcnow()
            )
        )
# --- Boucle auto-collecte (optimisée) ---
@tasks.loop(minutes=15)
async def auto_collect_loop():
    print("[Auto Collect] Lancement de la collecte automatique...")
    now = datetime.utcnow()

    for guild in bot.guilds:
        for config in COLLECT_ROLES_CONFIG:
            role = discord.utils.get(guild.roles, id=config["role_id"])
            if not role or not config["auto"]:
                continue

            # Parcourir uniquement les membres ayant le rôle
            for member in role.members:
                cd_data = collection47.find_one({
                    "guild_id": guild.id,
                    "user_id": member.id,
                    "role_id": role.id
                })
                last_collect = cd_data.get("last_collect") if cd_data else None

                if not last_collect or (now - last_collect).total_seconds() >= config["cooldown"]:
                    eco_data = collection28.find_one({
                        "guild_id": guild.id,
                        "user_id": member.id
                    }) or {"guild_id": guild.id, "user_id": member.id, "cash": 1500, "bank": 0}

                    eco_data.setdefault("cash", 0)
                    eco_data.setdefault("bank", 0)

                    before = eco_data[config["target"]]
                    if "amount" in config:
                        eco_data[config["target"]] += config["amount"]
                    elif "percent" in config:
                        eco_data[config["target"]] += eco_data[config["target"]] * (config["percent"] / 100)

                    collection28.update_one(
                        {"guild_id": guild.id, "user_id": member.id},
                        {"$set": {config["target"]: eco_data[config["target"]]}},
                        upsert=True
                    )

                    collection47.update_one(
                        {"guild_id": guild.id, "user_id": member.id, "role_id": role.id},
                        {"$set": {"last_collect": now}},
                        upsert=True
                    )

                    after = eco_data[config["target"]]
                    await log_eco_channel(bot, guild.id, member, f"Auto Collect ({role.name})", config.get("amount", config.get("percent")), before, after, note="Collect automatique")

# --- Boucle Top Roles (optimisée) ---
@tasks.loop(minutes=15)
async def update_top_roles():
    print("[Top Roles] Mise à jour des rôles de top...")
    for guild in bot.guilds:
        if guild.id != GUILD_ID:  # On ne traite qu'un seul serveur
            continue

        all_users_data = list(collection28.find({"guild_id": guild.id}))
        sorted_users = sorted(all_users_data, key=lambda u: u.get("cash", 0) + u.get("bank", 0), reverse=True)
        top_users = sorted_users[:3]

        # Récupérer une seule fois tous les membres nécessaires
        members = {member.id: member async for member in guild.fetch_members(limit=None)}

        for rank, user_data in enumerate(top_users, start=1):
            user_id = user_data["user_id"]
            role_id = TOP_ROLES[rank]
            role = discord.utils.get(guild.roles, id=role_id)
            if not role:
                print(f"Rôle manquant : {role_id} dans {guild.name}")
                continue

            member = members.get(user_id)
            if not member:
                print(f"Membre {user_id} non trouvé dans {guild.name}")
                continue

            if role not in member.roles:
                await member.add_roles(role)
                print(f"Ajouté {role.name} à {member.display_name}")

        # Nettoyer les rôles qui ne doivent plus être là
        for rank, role_id in TOP_ROLES.items():
            role = discord.utils.get(guild.roles, id=role_id)
            if not role:
                continue
            for member in role.members:
                if member.id not in [u["user_id"] for u in top_users]:
                    await member.remove_roles(role)
                    print(f"Retiré {role.name} de {member.display_name}")
                    
# Événement quand le bot est prêt
@bot.event
async def on_ready():
    bot.add_view(TicketView(author_id=ISEY_ID))  # pour bouton "Passé Commande"
    bot.add_view(ClaimCloseView())               # pour "Claim" et "Fermer"
    bot.add_view(GlobalSupportView())  # Nécessaire pour les boutons persistants
    print(f"✅ Le bot {bot.user} est maintenant connecté ! (ID: {bot.user.id})")

    bot.uptime = time.time()
    # Démarrer les tâches de fond
    update_top_roles.start()
    auto_collect_loop.start()
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

    if message.author.bot and message.author.id != PROJECT_DELTA_ID:
        return

    # ----- Partie 1 : Réaction dans un salon spécifique -----
    if str(message.channel.id) == "1360359130161872957":
        try:
            await message.add_reaction(reaction_emojis[current_emoji_index])
            current_emoji_index = (current_emoji_index + 1) % len(reaction_emojis)
        except Exception as e:
            print(f"Erreur lors de la réaction : {e}")

    # ----- Partie 2 : Confirmation de présence dans un autre salon -----
    if message.channel.id == ID_CANAL and message.author.id == PROJECT_DELTA_ID:
        canal_presence = bot.get_channel(ID_CANAL)
        maintenant = datetime.utcnow()
        embed = discord.Embed(
            description=f"<a:b_yes:1376916710468354078> | Présence confirmée : **{message.author.name}** est actif.",
            color=discord.Color.green(),
            timestamp=maintenant
        )
        await canal_presence.send(embed=embed)

    # ----- Partie 3 : Système de points avec cooldown -----
    key = f"{message.guild.id}-{message.author.id}"
    if key not in message_cooldowns:
        collection30.update_one(
            {"user_id": message.author.id, "guild_id": message.guild.id},
            {"$inc": {"points": 1}},
            upsert=True
        )

        # ----- Partie 3.1 : Gain automatique de cash -----
        try:
            from random import randint
            gain = randint(1, 5)
            user_data = collection28.find_one({"guild_id": message.guild.id, "user_id": message.author.id})

            if not user_data:
                user_data = {"guild_id": message.guild.id, "user_id": message.author.id, "cash": gain, "bank": 0}
                collection28.insert_one(user_data)
            else:
                collection28.update_one(
                    {"guild_id": message.guild.id, "user_id": message.author.id},
                    {"$inc": {"cash": gain}}
                )
        except Exception as e:
            print(f"Erreur lors du gain de cash automatique : {e}")

        message_cooldowns[key] = True
        await asyncio.sleep(300)
        del message_cooldowns[key]

    # ----- Partie 4 : Autoriser les commandes -----
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
            user: discord.PermissionOverwrite(view_channel=True, send_messages=True),  # ✅ Ajouté correctement
            guild.get_role(SUPPORT_ROLE_ID): discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }

        ticket_channel = await guild.create_text_channel(
            name=f"ticket-{user.name}",  # ✅ Nom corrigé pour éviter confusion avec "︱🚫・"
            category=category,
            overwrites=overwrites,
            reason="Ticket support global"
        )

        # ✅ Enregistrement dans MongoDB
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

        await ticket_channel.send(content=user.mention, embed=embed, view=GlobalSupportView())  # ✅ Mention du créateur dans le ticket
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

@bot.hybrid_command( 
    name="balance",
    aliases=["bal", "money"],
    description="Affiche ta balance ou celle d'un autre utilisateur."
)
async def bal(ctx: commands.Context, user: discord.User = None):
    if ctx.guild is None:
        return await ctx.send("Cette commande ne peut être utilisée qu'en serveur.")

    user = user or ctx.author
    guild_id = ctx.guild.id
    user_id = user.id

    # Utilisation de collection28
    def get_or_create_user_data(guild_id: int, user_id: int):
        data = collection28.find_one({"guild_id": guild_id, "user_id": user_id})
        if not data:
            data = {"guild_id": guild_id, "user_id": user_id, "cash": 0, "bank": 0}
            collection28.insert_one(data)
        return data

    data = get_or_create_user_data(guild_id, user_id)
    cash = data.get("cash", 0)
    bank = data.get("bank", 0)
    total = cash + bank

    # Classement des utilisateurs dans collection28
    all_users_data = list(collection28.find({"guild_id": guild_id}))
    sorted_users = sorted(
        all_users_data,
        key=lambda u: u.get("cash", 0) + u.get("bank", 0),
        reverse=True
    )
    rank = next((i + 1 for i, u in enumerate(sorted_users) if u["user_id"] == user_id), None)

    role_name = f"Tu as le rôle **[𝑺ץ] Top {rank}** ! Félicitations !" if rank in TOP_ROLES else None

    emoji_currency = "<:emoji_48:1362489008130621542>"

    def ordinal(n: int) -> str:
        return f"{n}{'st' if n == 1 else 'nd' if n == 2 else 'rd' if n == 3 else 'th'}"

    # Création de l'embed
    embed = discord.Embed(color=discord.Color.blue())
    embed.set_author(name=user.display_name, icon_url=user.display_avatar.url)

    # Ajout du champ classement seulement si rank existe
    if rank:
        embed.add_field(
            name="Leaderboard Rank",
            value=f"{ordinal(rank)}",
            inline=False
        )

    # Champ des finances (titre invisible)
    embed.add_field(
        name="Ton Solde:",
        value=(
            f"**Cash :** {int(cash):,} {emoji_currency}\n"
            f"**Banque :** {int(bank):,} {emoji_currency}\n"
            f"**Total :** {int(total):,} {emoji_currency}"
        ),
        inline=False
    )

    await ctx.send(embed=embed)

@bot.hybrid_command(name="deposit", aliases=["dep"], description="Dépose de l'argent de ton portefeuille vers ta banque.")
@app_commands.describe(amount="Montant à déposer (ou 'all')")
async def deposit(ctx: commands.Context, amount: str):
    user = ctx.author
    guild_id = ctx.guild.id
    user_id = user.id

    data = collection28.find_one({"guild_id": guild_id, "user_id": user_id}) or {"cash": 0, "bank": 0}
    cash = data.get("cash", 0)
    bank = data.get("bank", 0)

    # Cas "all"
    if amount.lower() == "all":
        if cash == 0:
            embed = discord.Embed(
                description=f"<:classic_x_mark:1362711858829725729> {user.mention}, tu n'as rien à déposer.",
                color=discord.Color.red()
            )
            embed.set_author(name=user.display_name, icon_url=user.display_avatar.url)
            return await ctx.send(embed=embed)
        deposit_amount = int(cash)

    else:
        # Vérification si le montant est valide (positif et numérique)
        if not amount.isdigit() or int(amount) <= 0:
            embed = discord.Embed(
                description=f"<:classic_x_mark:1362711858829725729> {user.mention}, montant invalide. Utilise un nombre positif ou `all`.",
                color=discord.Color.red()
            )
            embed.set_author(name=user.display_name, icon_url=user.display_avatar.url)
            return await ctx.send(embed=embed)

        deposit_amount = int(amount)

        # Vérifier si l'utilisateur a suffisamment d'argent
        if deposit_amount > cash:
            embed = discord.Embed(
                description=(
                    f"<:classic_x_mark:1362711858829725729> {user.mention}, tu n'as pas assez de cash à déposer. "
                    f"Tu as actuellement <:emoji_48:1362489008130621542> **{int(cash):,}** dans ton portefeuille."
                ),
                color=discord.Color.red()
            )
            embed.set_author(name=user.display_name, icon_url=user.display_avatar.url)
            return await ctx.send(embed=embed)

    # Mise à jour des données
    collection28.update_one(
        {"guild_id": guild_id, "user_id": user_id},
        {"$inc": {"cash": -deposit_amount, "bank": deposit_amount}},
        upsert=True
    )

    # Embed de succès
    embed = discord.Embed(
        description=f"<:Check:1362710665663615147> Tu as déposé <:emoji_48:1362489008130621542> **{int(deposit_amount):,}** dans ta banque !",
        color=discord.Color.green()
    )
    embed.set_author(name=user.display_name, icon_url=user.display_avatar.url)

    await ctx.send(embed=embed)

@bot.hybrid_command(name="withdraw", aliases=["with"], description="Retire de l'argent de ta banque vers ton portefeuille.")
async def withdraw(ctx: commands.Context, amount: str):
    user = ctx.author
    guild_id = ctx.guild.id
    user_id = user.id

    # Chercher les données actuelles
    data = collection28.find_one({"guild_id": guild_id, "user_id": user_id}) or {"cash": 0, "bank": 0}
    cash = data.get("cash", 0)
    bank = data.get("bank", 0)

    # Gérer le cas "all"
    if amount.lower() == "all":
        if bank == 0:
            embed = discord.Embed(
                description="💸 Tu n'as rien à retirer.",
                color=discord.Color.red()
            )
            embed.set_author(name=user.display_name, icon_url=user.display_avatar.url)
            return await ctx.send(embed=embed)
        withdrawn_amount = int(bank)
    else:
        # Vérifie que c'est un nombre valide
        if not amount.isdigit() or int(amount) <= 0:
            embed = discord.Embed(
                description="❌ Montant invalide. Utilise un nombre positif ou `all`.",
                color=discord.Color.red()
            )
            embed.set_author(name=user.display_name, icon_url=user.display_avatar.url)
            return await ctx.send(embed=embed)

        withdrawn_amount = int(amount)

        if withdrawn_amount > bank:
            embed = discord.Embed(
                description=(
                    f"<:classic_x_mark:1362711858829725729> Tu n'as pas autant à retirer. "
                    f"Tu as actuellement <:emoji_48:1362489008130621542> **{int(bank):,}** dans ta banque."
                ),
                color=discord.Color.red()
            )
            embed.set_author(name=user.display_name, icon_url=user.display_avatar.url)
            return await ctx.send(embed=embed)

    # Mise à jour dans la base de données
    collection28.update_one(
        {"guild_id": guild_id, "user_id": user_id},
        {"$inc": {"cash": withdrawn_amount, "bank": -withdrawn_amount}},
        upsert=True
    )

    # Création de l'embed de succès
    embed = discord.Embed(
        description=f"<:Check:1362710665663615147> Tu as retiré <:emoji_48:1362489008130621542> **{int(withdrawn_amount):,}** de ta banque !",
        color=discord.Color.green()
    )
    embed.set_author(name=user.display_name, icon_url=user.display_avatar.url)

    await ctx.send(embed=embed)

@bot.hybrid_command(name="add-money", description="Ajoute de l'argent à un utilisateur (réservé aux administrateurs).")
@app_commands.describe(
    user="L'utilisateur à créditer",
    amount="Le montant à ajouter",
    location="Choisis entre cash ou bank"
)
@app_commands.choices(location=[
    app_commands.Choice(name="Cash", value="cash"),
    app_commands.Choice(name="Bank", value="bank"),
])
@commands.has_permissions(administrator=True)
async def add_money(ctx: commands.Context, user: discord.User, amount: int, location: app_commands.Choice[str]):
    if amount <= 0:
        return await ctx.send("❌ Le montant doit être supérieur à 0.")

    guild_id = ctx.guild.id
    user_id = user.id
    field = location.value

    # Récupération du solde actuel
    data = collection28.find_one({"guild_id": guild_id, "user_id": user_id}) or {"cash": 0, "bank": 0}
    balance_before = int(data.get(field, 0))

    # Mise à jour du solde
    collection28.update_one(
        {"guild_id": guild_id, "user_id": user_id},
        {"$inc": {field: amount}},
        upsert=True
    )

    balance_after = balance_before + amount

    # Log dans le salon économique
    await log_eco_channel(
        bot,
        guild_id,
        user,
        "Ajout d'argent",
        int(amount),
        balance_before,
        balance_after,
        f"Ajout de {int(amount):,} <:emoji_48:1362489008130621542> dans le compte {field} de {user.mention} par {ctx.author.mention}."
    )

    # Embed de confirmation
    embed = discord.Embed(
        title="✅ Ajout effectué avec succès !",
        description=f"**{int(amount):,} <:emoji_48:1362489008130621542>** ont été ajoutés à la **{field}** de {user.mention}.",
        color=discord.Color.green()
    )
    embed.set_footer(text=f"Action réalisée par {ctx.author}", icon_url=ctx.author.display_avatar.url)

    await ctx.send(embed=embed)

# Gestion des erreurs de permissions
@add_money.error
async def add_money_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("🚫 Tu n'as pas la permission d'utiliser cette commande.")
    else:
        await ctx.send("❌ Une erreur est survenue lors de l'exécution de la commande.")

@bot.hybrid_command(name="remove-money", description="Retire de l'argent à un utilisateur.")
@app_commands.describe(user="L'utilisateur ciblé", amount="Le montant à retirer", location="Choisis entre cash ou bank")
@app_commands.choices(location=[
    app_commands.Choice(name="Cash", value="cash"),
    app_commands.Choice(name="Bank", value="bank"),
])
@commands.has_permissions(administrator=True)
async def remove_money(ctx: commands.Context, user: discord.User, amount: int, location: app_commands.Choice[str]):
    if amount <= 0:
        return await ctx.send("❌ Le montant doit être supérieur à 0.")

    guild_id = ctx.guild.id
    user_id = user.id
    field = location.value

    # Récupération du solde actuel
    data = collection28.find_one({"guild_id": guild_id, "user_id": user_id}) or {"cash": 0, "bank": 0}
    current_balance = int(data.get(field, 0))
    balance_before = current_balance
    balance_after = balance_before - amount

    # Mise à jour du solde (peut devenir négatif)
    collection28.update_one(
        {"guild_id": guild_id, "user_id": user_id},
        {"$inc": {field: -amount}},
        upsert=True
    )

    # Log dans le salon éco
    await log_eco_channel(
        bot,
        guild_id,
        user,
        "Retrait d'argent",
        -int(amount),
        balance_before,
        balance_after,
        f"Retrait de {int(amount):,} <:emoji_48:1362489008130621542> dans le compte {field} de {user.mention} par {ctx.author.mention}."
    )

    # Embed confirmation
    embed = discord.Embed(
        title="✅ Retrait effectué avec succès !",
        description=f"**{int(amount):,} <:emoji_48:1362489008130621542>** a été retiré de la **{field}** de {user.mention}.\nNouveau solde : **{balance_after:,}** <:emoji_48:1362489008130621542>",
        color=discord.Color.green()
    )
    embed.set_footer(text=f"Action réalisée par {ctx.author}", icon_url=ctx.author.display_avatar.url)

    await ctx.send(embed=embed)

# Gestion des erreurs
@remove_money.error
async def remove_money_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Tu dois être administrateur pour utiliser cette commande.")
    else:
        await ctx.send("❌ Une erreur est survenue.")

@bot.hybrid_command(name="set-money", description="Définit un montant exact dans le cash ou la bank d’un utilisateur.")
@app_commands.describe(user="L'utilisateur ciblé", amount="Le montant à définir", location="Choisis entre cash ou bank")
@app_commands.choices(location=[
    app_commands.Choice(name="Cash", value="cash"),
    app_commands.Choice(name="Bank", value="bank"),
])
@commands.has_permissions(administrator=True)
async def set_money(ctx: commands.Context, user: discord.User, amount: int, location: app_commands.Choice[str]):
    if amount < 0:
        return await ctx.send("❌ Le montant ne peut pas être négatif.")

    guild_id = ctx.guild.id
    user_id = user.id
    field = location.value

    # Récupération du solde actuel
    data = collection28.find_one({"guild_id": guild_id, "user_id": user_id}) or {"cash": 0, "bank": 0}
    balance_before = int(data.get(field, 0))

    # Mise à jour de la base de données
    collection28.update_one(
        {"guild_id": guild_id, "user_id": user_id},
        {"$set": {field: int(amount)}},
        upsert=True
    )

    # Log dans le salon de logs économiques
    await log_eco_channel(
        bot,
        guild_id,
        user,
        "Définition du solde",
        int(amount) - balance_before,
        balance_before,
        int(amount),
        f"Le solde du compte `{field}` de {user.mention} a été défini à {int(amount):,} <:emoji_48:1362489008130621542> par {ctx.author.mention}."
    )

    # Création de l'embed
    embed = discord.Embed(
        title=f"{user.display_name} - {user.name}",
        description=f"Le montant de **{field}** de {user.mention} a été défini à **{int(amount):,} <:emoji_48:1362489008130621542>**.",
        color=discord.Color.green()
    )
    embed.set_author(name=user.display_name, icon_url=user.display_avatar.url)
    embed.set_footer(text=f"Action réalisée par {ctx.author}", icon_url=ctx.author.display_avatar.url)

    await ctx.send(embed=embed)

# Gestion des erreurs de permissions
@set_money.error
async def set_money_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Tu dois être administrateur pour utiliser cette commande.")
    else:
        await ctx.send("❌ Une erreur est survenue.")

@bot.hybrid_command(name="pay", description="Paie un utilisateur avec tes coins.")
@app_commands.describe(user="L'utilisateur à qui envoyer de l'argent", amount="Montant à transférer ou 'all' pour tout envoyer")
async def pay(ctx: commands.Context, user: discord.User, amount: str):
    sender = ctx.author
    guild_id = ctx.guild.id

    if user.id == sender.id:
        embed = discord.Embed(
            description=f"<:classic_x_mark:1362711858829725729> {sender.mention}, tu ne peux pas te payer toi-même.",
            color=discord.Color.red()
        )
        embed.set_author(name=sender.display_name, icon_url=sender.display_avatar.url)
        return await ctx.send(embed=embed)

    sender_data = collection28.find_one({"guild_id": guild_id, "user_id": sender.id}) or {"cash": 0}
    sender_cash = int(sender_data.get("cash", 0))

    # Gestion du mot-clé "all"
    if amount.lower() == "all":
        if sender_cash <= 0:
            embed = discord.Embed(
                description=f"<:classic_x_mark:1362711858829725729> {sender.mention}, tu n'as pas d'argent à envoyer.",
                color=discord.Color.red()
            )
            embed.set_author(name=sender.display_name, icon_url=sender.display_avatar.url)
            return await ctx.send(embed=embed)
        amount = sender_cash
    else:
        try:
            amount = int(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            embed = discord.Embed(
                description=f"<:classic_x_mark:1362711858829725729> {sender.mention}, le montant doit être un nombre positif ou 'all'.",
                color=discord.Color.red()
            )
            embed.set_author(name=sender.display_name, icon_url=sender.display_avatar.url)
            return await ctx.send(embed=embed)

        if sender_cash < amount:
            embed = discord.Embed(
                description=(
                    f"<:classic_x_mark:1362711858829725729> {sender.mention}, tu n'as pas assez de cash. "
                    f"Tu as actuellement <:emoji_48:1362489008130621542> **{sender_cash:,}** dans ton portefeuille."
                ),
                color=discord.Color.red()
            )
            embed.set_author(name=sender.display_name, icon_url=sender.display_avatar.url)
            return await ctx.send(embed=embed)

    # Mise à jour des soldes
    collection28.update_one(
        {"guild_id": guild_id, "user_id": sender.id},
        {"$inc": {"cash": -amount}},
        upsert=True
    )

    collection28.update_one(
        {"guild_id": guild_id, "user_id": user.id},
        {"$inc": {"cash": amount}},
        upsert=True
    )

    # Log dans le salon économique
    await log_eco_channel(
        bot,
        guild_id,
        user,
        "Paiement reçu",
        amount,
        None,
        None,
        f"{user.mention} a reçu **{amount:,} <:emoji_48:1362489008130621542>** de la part de {sender.mention}."
    )

    # Embed de succès
    embed = discord.Embed(
        description=(
            f"<:Check:1362710665663615147> {user.mention} a reçu **{amount:,}** <:emoji_48:1362489008130621542> de ta part."
        ),
        color=discord.Color.green()
    )
    embed.set_author(name=sender.display_name, icon_url=sender.display_avatar.url)
    embed.set_footer(text=f"Paiement effectué à {user.display_name}", icon_url=user.display_avatar.url)

    await ctx.send(embed=embed)

# Gestion des erreurs
@pay.error
async def pay_error(ctx, error):
    embed = discord.Embed(
        description="<:classic_x_mark:1362711858829725729> Une erreur est survenue lors du paiement.",
        color=discord.Color.red()
    )
    await ctx.send(embed=embed)

@bot.hybrid_command(name="work", aliases=["wk"], description="Travaille et gagne de l'argent !")
async def work(ctx: commands.Context):
    if ctx.guild is None:
        return await ctx.send("Cette commande ne peut être utilisée qu'en serveur.")

    user = ctx.author
    guild_id = ctx.guild.id
    user_id = user.id

    # Vérification que l'utilisateur a un rôle dans ECO_ROLES_VIP
    if not any(role.id in ECO_ROLES_VIP for role in user.roles):
        embed = discord.Embed(
            description=f"<:classic_x_mark:1362711858829725729> {user.mention}, cette commande est réservée aux membres VIP.",
            color=discord.Color.red()
        )
        return await ctx.send(embed=embed)

    now = datetime.utcnow()

    # Vérification du cooldown
    cooldown_data = collection33.find_one({"guild_id": guild_id, "user_id": user_id}) or {}
    last_work_time = cooldown_data.get("last_work_time")

    if last_work_time:
        time_diff = now - last_work_time
        cooldown = timedelta(hours=6)
        if time_diff < cooldown:
            remaining = cooldown - time_diff
            minutes_left = int(remaining.total_seconds() // 60)

            embed = discord.Embed(
                description=f"<:classic_x_mark:1362711858829725729> {user.mention}, tu dois attendre **{minutes_left} minutes** avant de pouvoir retravailler.",
                color=discord.Color.red()
            )
            embed.set_author(name=user.display_name, icon_url=user.display_avatar.url)
            return await ctx.send(embed=embed)

    # Gain aléatoire
    amount = random.randint(1, 150)

    # Récupération ou création des données utilisateur
    user_data = collection28.find_one({"guild_id": guild_id, "user_id": user_id})
    if not user_data:
        user_data = {"guild_id": guild_id, "user_id": user_id, "cash": 1500, "bank": 0}
        collection28.insert_one(user_data)

    initial_cash = user_data.get("cash", 0)

    # Mise à jour du cooldown
    collection33.update_one(
        {"guild_id": guild_id, "user_id": user_id},
        {"$set": {"last_work_time": now}},
        upsert=True
    )

    # Mise à jour du cash
    collection28.update_one(
        {"guild_id": guild_id, "user_id": user_id},
        {"$inc": {"cash": amount}},
        upsert=True
    )

    # Log + messages variés
    messages = [
        f"Tu as travaillé dur et gagné **{amount:,} <:emoji_48:1362489008130621542>**. Bien joué !",
        f"Bravo ! Tu as gagné **{amount:,} <:emoji_48:1362489008130621542>** après ton travail.",
        f"Tu as travaillé avec assiduité et récolté **{amount:,} <:emoji_48:1362489008130621542>**.",
        f"Du bon travail ! Voici **{amount:,} <:emoji_48:1362489008130621542>** pour toi.",
        f"Félicitations, tu as gagné **{amount:,} <:emoji_48:1362489008130621542>** pour ton travail.",
        f"Tu as gagné **{amount:,} <:emoji_48:1362489008130621542>** après une journée de travail bien remplie !",
        f"Bien joué ! **{amount:,} <:emoji_48:1362489008130621542>** ont été ajoutés à ta balance.",
        f"Voici ta récompense pour ton travail : **{amount:,} <:emoji_48:1362489008130621542>**.",
        f"Tu es payé pour ton dur labeur : **{amount:,} <:emoji_48:1362489008130621542>**.",
    ]
    message = random.choice(messages)

    # Log de l'action
    await log_eco_channel(
        bot,
        guild_id,
        user,
        "Travail effectué",
        amount,
        initial_cash,
        initial_cash + amount,
        f"{user.mention} a gagné **{amount:,} <:emoji_48:1362489008130621542>>** pour son travail."
    )

    # Embed de succès
    embed = discord.Embed(
        description=message,
        color=discord.Color.green()
    )
    embed.set_author(name=user.display_name, icon_url=user.display_avatar.url)
    embed.set_footer(text="Commande de travail", icon_url=user.display_avatar.url)

    await ctx.send(embed=embed)
    
# Gestion des erreurs
@work.error
async def work_error(ctx, error):
    embed = discord.Embed(
        description="<:classic_x_mark:1362711858829725729> Une erreur est survenue lors de l'utilisation de la commande `work`.",
        color=discord.Color.red()
    )
    await ctx.send(embed=embed)

@bot.hybrid_command(name="slut", description="Tente ta chance dans une aventure sexy pour gagner de l'argent... ou tout perdre.")
async def slut(ctx: commands.Context):
    user = ctx.author
    guild_id = ctx.guild.id
    user_id = user.id
    now = datetime.utcnow()

    # Vérification que l'utilisateur a un rôle dans ECO_ROLES_VIP
    if not any(role.id in ECO_ROLES_VIP for role in user.roles):
        embed = discord.Embed(
            description=f"<:classic_x_mark:1362711858829725729> {user.mention}, cette commande est réservée aux membres VIP.",
            color=discord.Color.red()
        )
        return await ctx.send(embed=embed)
        
    # Cooldown 30 min
    cooldown_data = collection45.find_one({"guild_id": guild_id, "user_id": user_id}) or {}
    last_slut_time = cooldown_data.get("last_slut_time")

    if last_slut_time:
        time_diff = now - last_slut_time
        if time_diff < timedelta(hours=3):
            remaining = timedelta(hours=3) - time_diff
            minutes_left = int(remaining.total_seconds() // 60)
            return await ctx.send(f"<:classic_x_mark:1362711858829725729> Tu dois encore patienter **{minutes_left} minutes** avant de retenter une nouvelle aventure sexy.")

    # Déterminer le résultat
    outcome = random.choice(["gain", "loss"])
    amount_gain = random.randint(1, 75)
    amount_loss = random.randint(1, 75)

    # Récupérer ou créer les données du joueur
    user_data = collection28.find_one({"guild_id": guild_id, "user_id": user_id})
    if not user_data:
        user_data = {"guild_id": guild_id, "user_id": user_id, "cash": 1500, "bank": 0}
        collection28.insert_one(user_data)

    balance_before = user_data.get("cash", 0)

    # Vérifier si l'utilisateur a le rôle spécial
    has_special_role = discord.utils.get(user.roles, id=1365313292477927464) is not None

    # Si gain ou rôle spécial, on gagne
    if outcome == "gain" or has_special_role:
        message = random.choice([
            f"<:Check:1362710665663615147> Tu as séduit la bonne personne et reçu **{amount_gain} <:emoji_48:1362489008130621542>** en cadeau.",
            f"<:Check:1362710665663615147> Une nuit torride t’a valu **{amount_gain} <:emoji_48:1362489008130621542>**.",
            f"<:Check:1362710665663615147> Tu as été payé pour tes charmes : **{amount_gain} <:emoji_48:1362489008130621542>**.",
            f"<:Check:1362710665663615147> Ta prestation a fait des ravages, tu gagnes **{amount_gain} <:emoji_48:1362489008130621542>**.",
            f"<:Check:1362710665663615147> Ce client généreux t’a offert **{amount_gain} <:emoji_48:1362489008130621542>**.",
            f"<:Check:1362710665663615147> Tu as chauffé la salle et récolté **{amount_gain} <:emoji_48:1362489008130621542>**.",
            f"<:Check:1362710665663615147> Tes talents ont été récompensés avec **{amount_gain} <:emoji_48:1362489008130621542>**.",
            f"<:Check:1362710665663615147> Tu as dominé la scène, et gagné **{amount_gain} <:emoji_48:1362489008130621542>**.",
        ])
        collection28.update_one(
            {"guild_id": guild_id, "user_id": user_id},
            {"$inc": {"cash": amount_gain}},
            upsert=True
        )
        balance_after = balance_before + amount_gain
        await log_eco_channel(bot, guild_id, user, "Gain après slut", amount_gain, balance_before, balance_after)

    else:
        message = random.choice([
            f"<:classic_x_mark:1362711858829725729> Ton plan a échoué, tu perds **{amount_loss} <:emoji_48:1362489008130621542>**.",
            f"<:classic_x_mark:1362711858829725729> Ton client a disparu sans payer. Tu perds **{amount_loss} <:emoji_48:1362489008130621542>**.",
            f"<:classic_x_mark:1362711858829725729> T’as glissé pendant ton show… Résultat : **{amount_loss} <:emoji_48:1362489008130621542>** de frais médicaux.",
            f"<:classic_x_mark:1362711858829725729> Mauvais choix de client, il t’a volé **{amount_loss} <:emoji_48:1362489008130621542>**.",
            f"<:classic_x_mark:1362711858829725729> Une nuit sans succès… Tu perds **{amount_loss} <:emoji_48:1362489008130621542>**.",
            f"<:classic_x_mark:1362711858829725729> Ton charme n’a pas opéré… Pertes : **{amount_loss} <:emoji_48:1362489008130621542>**.",
            f"<:classic_x_mark:1362711858829725729> Tu as été arnaqué par un faux manager. Tu perds **{amount_loss} <:emoji_48:1362489008130621542>**.",
        ])
        collection28.update_one(
            {"guild_id": guild_id, "user_id": user_id},
            {"$inc": {"cash": -amount_loss}},
            upsert=True
        )
        balance_after = balance_before - amount_loss
        await log_eco_channel(bot, guild_id, user, "Perte après slut", -amount_loss, balance_before, balance_after)

    # Mise à jour du cooldown
    collection45.update_one(
        {"guild_id": guild_id, "user_id": user_id},
        {"$set": {"last_slut_time": now}},
        upsert=True
    )

    # Envoi de l'embed
    embed = discord.Embed(
        title="💋 Résultat de ta prestation",
        description=message,
        color=discord.Color.green() if outcome == "gain" or has_special_role else discord.Color.dark_red()
    )
    embed.set_footer(text=f"Aventure tentée par {user}", icon_url=user.display_avatar.url)
    await ctx.send(embed=embed)

@slut.error
async def slut_error(ctx, error):
    await ctx.send("<:classic_x_mark:1362711858829725729> Une erreur est survenue pendant la commande.")

@bot.hybrid_command(name="crime", description="Participe à un crime pour essayer de gagner de l'argent, mais attention, tu pourrais perdre !")
async def crime(ctx: commands.Context):
    user = ctx.author
    guild_id = ctx.guild.id
    user_id = user.id
    now = datetime.utcnow()

    # Vérification que l'utilisateur a un rôle dans ECO_ROLES_VIP
    if not any(role.id in ECO_ROLES_VIP for role in user.roles):
        embed = discord.Embed(
            description=f"<:classic_x_mark:1362711858829725729> {user.mention}, cette commande est réservée aux membres VIP.",
            color=discord.Color.red()
        )
        return await ctx.send(embed=embed)
        
    # Cooldown 30 minutes
    cooldown_data = collection46.find_one({"guild_id": guild_id, "user_id": user_id}) or {}
    last_crime_time = cooldown_data.get("last_crime_time")

    if last_crime_time:
        time_diff = now - last_crime_time
        if time_diff < timedelta(hours=1):
            remaining = timedelta(hours=1) - time_diff
            minutes_left = int(remaining.total_seconds() // 60)
            return await ctx.send(f"<:classic_x_mark:1362711858829725729> Tu dois attendre encore **{minutes_left} minutes** avant de pouvoir recommencer.")

    outcome = random.choice(["gain", "loss"])
    gain_amount = random.randint(1, 50)
    loss_amount = random.randint(1, 50)

    # Récupérer ou créer les données joueur
    user_data = collection28.find_one({"guild_id": guild_id, "user_id": user_id})
    if not user_data:
        user_data = {"guild_id": guild_id, "user_id": user_id, "cash": 1500, "bank": 0}
        collection28.insert_one(user_data)

    balance_before = user_data.get("cash", 0)

    # Rôle spécial : ne perd jamais
    has_special_role = any(role.id == 1365313292477927464 for role in user.roles)

    if outcome == "gain" or has_special_role:
        messages = [
            f"Tu as braqué une banque sans te faire repérer et gagné **{gain_amount} <:emoji_48:1362489008130621542>**.",
            f"Tu as volé une mallette pleine de billets ! Gain : **{gain_amount} <:emoji_48:1362489008130621542>**.",
            f"Ton casse a été un succès, tu empoche **{gain_amount} <:emoji_48:1362489008130621542>**.",
            f"Tu as braqué une bijouterie et revendu le tout pour **{gain_amount} <:emoji_48:1362489008130621542>**.",
            f"Le vol de voiture a payé ! Tu gagnes **{gain_amount} <:emoji_48:1362489008130621542>**.",
            f"Tu as escroqué un riche touriste : **{gain_amount} <:emoji_48:1362489008130621542>**.",
            f"Ton hacking a fonctionné, transfert réussi de **{gain_amount} <:emoji_48:1362489008130621542>**.",
        ]
        message = random.choice(messages)

        collection28.update_one(
            {"guild_id": guild_id, "user_id": user_id},
            {"$inc": {"cash": gain_amount}},
            upsert=True
        )

        balance_after = balance_before + gain_amount
        await log_eco_channel(bot, guild_id, user, "Gain après crime", gain_amount, balance_before, balance_after)

        embed = discord.Embed(
            title="💸 Tu as réussi ton crime !",
            description=message,
            color=discord.Color.green()
        )

    else:
        messages = [
            f"Tu t’es fait attraper par la police et tu perds **{loss_amount} <:emoji_48:1362489008130621542>** en caution.",
            f"Ton complice t’a trahi et s’est enfui avec **{loss_amount} <:emoji_48:1362489008130621542>**.",
            f"Le système de sécurité t’a eu, tu paies **{loss_amount} <:emoji_48:1362489008130621542>**.",
            f"Le plan a foiré, tu dois rembourser **{loss_amount} <:emoji_48:1362489008130621542>**.",
            f"La victime t’a reconnu, tu files une amende de **{loss_amount} <:emoji_48:1362489008130621542>**.",
            f"Un piège de la police t’a coûté **{loss_amount} <:emoji_48:1362489008130621542>**.",
            f"Tu t’es blessé pendant le casse. Soins : **{loss_amount} <:emoji_48:1362489008130621542>**.",
        ]
        message = random.choice(messages)

        collection28.update_one(
            {"guild_id": guild_id, "user_id": user_id},
            {"$inc": {"cash": -loss_amount}},
            upsert=True
        )

        balance_after = balance_before - loss_amount
        await log_eco_channel(bot, guild_id, user, "Perte après crime", -loss_amount, balance_before, balance_after)

        embed = discord.Embed(
            title="🚨 Échec du crime !",
            description=message,
            color=discord.Color.red()
        )

    # Mise à jour cooldown
    collection46.update_one(
        {"guild_id": guild_id, "user_id": user_id},
        {"$set": {"last_crime_time": now}},
        upsert=True
    )
    embed.set_footer(text=f"Action effectuée par {user}", icon_url=user.display_avatar.url)
    await ctx.send(embed=embed)

@crime.error
async def crime_error(ctx, error):
    await ctx.send("<:classic_x_mark:1362711858829725729> Une erreur est survenue lors de la commande.")

@bot.command(name="buy", aliases=["chicken", "c", "h", "i", "k", "e", "n"])
async def buy_item(ctx, item: str = "chicken"):
    user = ctx.author
    guild_id = ctx.guild.id
    user_id = user.id

    item = "chicken"  # Forcer l'achat du chicken

    # Vérifier si l'utilisateur possède déjà un chicken
    data = collection34.find_one({"guild_id": guild_id, "user_id": user_id})
    if data and data.get("chicken", False):
        embed = discord.Embed(
            description="<:classic_x_mark:1362711858829725729> Vous possédez déjà un chicken.\nEnvoyez-le au combat avec la commande `cock-fight <pari>`.",
            color=discord.Color.red()
        )
        embed.set_author(name=f"{user.display_name}", icon_url=user.display_avatar.url)
        await ctx.send(embed=embed)
        return

    # Vérifier le solde (champ cash)
    balance_data = collection28.find_one({"guild_id": guild_id, "user_id": user_id})
    balance = balance_data.get("cash", 0) if balance_data else 0

    items_for_sale = {
        "chicken": 10,
    }

    if item in items_for_sale:
        price = items_for_sale[item]

        if balance >= price:
            # Retirer du cash
            collection28.update_one(
                {"guild_id": guild_id, "user_id": user_id},
                {"$inc": {"cash": -price}},
                upsert=True
            )

            # Ajouter le chicken
            collection34.update_one(
                {"guild_id": guild_id, "user_id": user_id},
                {"$set": {item: True}},
                upsert=True
            )

            # Logs économiques
            balance_after = balance - price
            await log_eco_channel(
                bot, guild_id, user, "Achat", price, balance, balance_after,
                f"Achat d'un **{item}**"
            )

            # Embed de confirmation
            embed = discord.Embed(
                description="<:Check:1362710665663615147> Vous avez acheté un chicken pour combattre !\nUtilisez la commande `cock-fight <pari>`",
                color=discord.Color.green()
            )
            embed.set_author(name=f"{user.display_name}", icon_url=user.display_avatar.url)
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(
                description=f"<:classic_x_mark:1362711858829725729> Vous n'avez pas assez de coins pour acheter un **{item}** !",
                color=discord.Color.red()
            )
            embed.set_author(name=f"{user.display_name}", icon_url=user.display_avatar.url)
            await ctx.send(embed=embed)

    else:
        embed = discord.Embed(
            description=f"<:classic_x_mark:1362711858829725729> Cet item n'est pas disponible à l'achat.",
            color=discord.Color.red()
        )
        embed.set_author(name=f"{user.display_name}", icon_url=user.display_avatar.url)
        await ctx.send(embed=embed)

@bot.command(name="cock-fight", aliases=["cf"])
async def cock_fight(ctx, amount: str):
    user = ctx.author
    guild_id = ctx.guild.id
    user_id = user.id

    config = get_cf_config(guild_id)
    max_bet = config.get("max_bet", 500)
    max_chance = config.get("max_chance", 52)
    start_chance = config.get("start_chance", 45)

    # Vérifier si l'utilisateur a un chicken
    data = collection34.find_one({"guild_id": guild_id, "user_id": user_id})
    if not data or not data.get("chicken", False):
        embed = discord.Embed(
            description=f"<:classic_x_mark:1362711858829725729> {user.mention}, tu n'as pas de poulet ! Utilise la commande `!!buy chicken` pour en acheter un.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return

    # Vérifier le solde de l'utilisateur
    balance_data = collection28.find_one({"guild_id": guild_id, "user_id": user_id})
    balance = balance_data.get("cash", 0) if balance_data else 0

    # Gérer les mises "all" ou "half"
    if amount.lower() == "all":
        if balance == 0:
            embed = discord.Embed(
                description=f"<:classic_x_mark:1362711858829725729> {user.mention}, ton cash est vide.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        if balance > max_bet:
            embed = discord.Embed(
                description=f"<:classic_x_mark:1362711858829725729> {user.mention}, ta mise dépasse la limite de **{max_bet} <:emoji_48:1362489008130621542>**.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        amount = balance

    elif amount.lower() == "half":
        if balance == 0:
            embed = discord.Embed(
                description=f"<:classic_x_mark:1362711858829725729> {user.mention}, ton cash est vide.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        amount = balance // 2
        if amount > max_bet:
            embed = discord.Embed(
                description=f"<:classic_x_mark:1362711858829725729> {user.mention}, la moitié de ton cash dépasse la limite de **{max_bet} <:emoji_48:1362489008130621542>**.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

    else:
        try:
            amount = int(amount)
        except ValueError:
            embed = discord.Embed(
                description=f"<:classic_x_mark:1362711858829725729> {user.mention}, entre un montant valide, ou utilise `all` ou `half`.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

    # Vérifier que l'utilisateur a assez d'argent
    if amount > balance:
        embed = discord.Embed(
            description=f"<:classic_x_mark:1362711858829725729> {user.mention}, tu n'as pas assez de cash pour cette mise.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    if amount <= 0:
        embed = discord.Embed(
            description=f"<:classic_x_mark:1362711858829725729> {user.mention}, la mise doit être positive.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    if amount > max_bet:
        embed = discord.Embed(
            description=f"<:classic_x_mark:1362711858829725729> {user.mention}, la mise est limitée à **{max_bet} <:emoji_48:1362489008130621542>**.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return

    # Chance de victoire
    win_data = collection33.find_one({"guild_id": guild_id, "user_id": user_id})
    win_chance = (win_data or {}).get("win_chance", start_chance)

    did_win = random.randint(1, 100) <= win_chance

    if did_win:
        win_amount = amount
        new_chance = min(win_chance + 1, max_chance)

        # Mise à jour de la base
        collection28.update_one(
            {"guild_id": guild_id, "user_id": user_id},
            {"$inc": {"cash": win_amount}},
            upsert=True
        )
        collection33.update_one(
            {"guild_id": guild_id, "user_id": user_id},
            {"$set": {"win_chance": new_chance}},
            upsert=True
        )

        # Embed victoire
        embed = discord.Embed(
            description=f"<:Check:1362710665663615147> {user.mention}, ton poulet a **gagné** le combat et t’a rapporté <:emoji_48:1362489008130621542> **{win_amount}** ! 🐓",
            color=discord.Color.green()
        )
        embed.set_author(name=str(user), icon_url=user.avatar.url if user.avatar else user.default_avatar.url)

        embed.set_footer(text=f"Chicken strength (chance of winning): {new_chance}%")

        await ctx.send(embed=embed)

        balance_after = balance + win_amount
        await log_eco_channel(
            bot, guild_id, user, "Victoire au Cock-Fight", win_amount, balance, balance_after,
            f"Victoire au Cock-Fight avec un gain de **{win_amount}**"
        )

    else:
        # Défaite : poulet meurt
        collection34.update_one(
            {"guild_id": guild_id, "user_id": user_id},
            {"$set": {"chicken": False}}
        )
        collection28.update_one(
            {"guild_id": guild_id, "user_id": user_id},
            {"$inc": {"cash": -amount}},
            upsert=True
        )
        collection33.update_one(
            {"guild_id": guild_id, "user_id": user_id},
            {
                "$set": {"win_chance": start_chance},
            },
            upsert=True
        )

        embed = discord.Embed(
            description=f"<:classic_x_mark:1362711858829725729> {user.mention}, ton poulet est **mort** au combat... <:imageremovebgpreview53:1362693948702855360>",
            color=discord.Color.red()
        )
        embed.set_author(name=str(user), icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
        await ctx.send(embed=embed)

        balance_after = balance - amount
        await log_eco_channel(
            bot, guild_id, user, "Défaite au Cock-Fight", -amount, balance, balance_after,
            f"Défaite au Cock-Fight avec une perte de **{amount}**"
        )

@bot.command(name="set-cf-depart-chance")
@commands.has_permissions(administrator=True)
async def set_depart_chance(ctx, pourcent: str = None):
    if pourcent is None:
        return await ctx.send("⚠️ Merci de spécifier un pourcentage (entre 1 et 100). Exemple : `!set-cf-depart-chance 50`")

    if not pourcent.isdigit():
        return await ctx.send("⚠️ Le pourcentage doit être un **nombre entier**.")

    pourcent = int(pourcent)
    if not 1 <= pourcent <= 100:
        return await ctx.send("❌ Le pourcentage doit être compris entre **1** et **100**.")

    # Mettre à jour la base de données avec la nouvelle valeur
    collection35.update_one({"guild_id": ctx.guild.id}, {"$set": {"start_chance": pourcent}}, upsert=True)

    # Envoyer un message dans le salon de log spécifique (si configuré)
    config = collection36.find_one({"guild_id": ctx.guild.id})
    channel_id = config.get("eco_log_channel") if config else None

    if channel_id:
        channel = bot.get_channel(channel_id)
        if channel:
            embed = discord.Embed(
                title="🔧 Log de Configuration",
                color=discord.Color.green(),
                timestamp=datetime.utcnow()
            )
            embed.add_field(name="Action", value="Mise à jour de la chance de départ", inline=True)
            embed.add_field(name="Chance de départ", value=f"{pourcent}%", inline=True)
            await channel.send(embed=embed)

    await ctx.send(f"✅ La chance de départ a été mise à **{pourcent}%**.")


@bot.command(name="set-cf-max-chance")
@commands.has_permissions(administrator=True)
async def set_max_chance(ctx, pourcent: str = None):
    if pourcent is None:
        return await ctx.send("⚠️ Merci de spécifier un pourcentage (entre 1 et 100). Exemple : `!set-cf-max-chance 90`")

    if not pourcent.isdigit():
        return await ctx.send("⚠️ Le pourcentage doit être un **nombre entier**.")

    pourcent = int(pourcent)
    if not 1 <= pourcent <= 100:
        return await ctx.send("❌ Le pourcentage doit être compris entre **1** et **100**.")

    # Mettre à jour la base de données avec la nouvelle valeur
    collection35.update_one({"guild_id": ctx.guild.id}, {"$set": {"max_chance": pourcent}}, upsert=True)

    # Envoyer un message dans le salon de log spécifique (si configuré)
    config = collection36.find_one({"guild_id": ctx.guild.id})
    channel_id = config.get("eco_log_channel") if config else None

    if channel_id:
        channel = bot.get_channel(channel_id)
        if channel:
            embed = discord.Embed(
                title="🔧 Log de Configuration",
                color=discord.Color.green(),
                timestamp=datetime.utcnow()
            )
            embed.add_field(name="Action", value="Mise à jour de la chance maximale de victoire", inline=True)
            embed.add_field(name="Chance maximale", value=f"{pourcent}%", inline=True)
            await channel.send(embed=embed)

    await ctx.send(f"✅ La chance maximale de victoire est maintenant de **{pourcent}%**.")

@bot.command(name="set-cf-mise-max")
@commands.has_permissions(administrator=True)
async def set_max_mise(ctx, amount: str = None):
    if amount is None:
        return await ctx.send("⚠️ Merci de spécifier une mise maximale (nombre entier positif). Exemple : `!set-cf-mise-max 1000`")

    if not amount.isdigit():
        return await ctx.send("⚠️ La mise maximale doit être un **nombre entier**.")

    amount = int(amount)
    if amount <= 0:
        return await ctx.send("❌ La mise maximale doit être un **nombre supérieur à 0**.")

    # Mettre à jour la base de données avec la nouvelle mise maximale
    collection35.update_one({"guild_id": ctx.guild.id}, {"$set": {"max_bet": amount}}, upsert=True)

    # Envoyer un message dans le salon de log spécifique (si configuré)
    config = collection36.find_one({"guild_id": ctx.guild.id})
    channel_id = config.get("eco_log_channel") if config else None

    if channel_id:
        channel = bot.get_channel(channel_id)
        if channel:
            embed = discord.Embed(
                title="🔧 Log de Configuration",
                color=discord.Color.green(),
                timestamp=datetime.utcnow()
            )
            embed.add_field(name="Action", value="Mise à jour de la mise maximale", inline=True)
            embed.add_field(name="Mise maximale", value=f"{amount} <:emoji_48:1362489008130621542>", inline=True)
            await channel.send(embed=embed)

    await ctx.send(f"✅ La mise maximale a été mise à **{amount} <:emoji_48:1362489008130621542>**.")

# Gestion des erreurs liées aux permissions
@set_depart_chance.error
@set_max_chance.error
@set_max_mise.error
async def cf_config_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Vous n'avez pas la permission d'utiliser cette commande.")
    elif isinstance(error, commands.CommandInvokeError):
        await ctx.send("❌ Une erreur est survenue lors de l’exécution de la commande.")
        print(f"[ERREUR] {error}")
    else:
        await ctx.send("⚠️ Une erreur inconnue est survenue.")
        print(f"[ERREUR INCONNUE] {error}")

class CFConfigView(ui.View):
    def __init__(self, guild_id):
        super().__init__(timeout=60)
        self.guild_id = guild_id

    @ui.button(label="🔄 Reset aux valeurs par défaut", style=discord.ButtonStyle.red)
    async def reset_defaults(self, interaction: Interaction, button: ui.Button):
        # Vérifier si l'utilisateur est admin
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("Tu n'as pas la permission de faire ça.", ephemeral=True)
            return

        # Reset config
        default_config = {
            "start_chance": 50,
            "max_chance": 100,
            "max_bet": 20000
        }
        collection35.update_one(
            {"guild_id": self.guild_id},
            {"$set": default_config},
            upsert=True
        )
        await interaction.response.send_message("✅ Les valeurs par défaut ont été rétablies.", ephemeral=True)

@bot.command(name="cf-config")
@commands.has_permissions(administrator=True)
async def cf_config(ctx):
    guild_id = ctx.guild.id
    config = get_cf_config(guild_id)

    start_chance = config.get("start_chance", 50)
    max_chance = config.get("max_chance", 100)
    max_bet = config.get("max_bet", 20000)

    embed = discord.Embed(
        title="⚙️ Configuration Cock-Fight",
        color=discord.Color.gold()
    )
    embed.add_field(name="🎯 Chance de départ", value=f"**{start_chance}%**", inline=False)
    embed.add_field(name="📈 Chance max", value=f"**{max_chance}%**", inline=False)
    embed.add_field(name="💰 Mise maximale", value=f"**{max_bet} <:ecoEther:1341862366249357374>**", inline=False)
    embed.set_footer(text=f"Demandé par {ctx.author.display_name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

    await ctx.send(embed=embed, view=CFConfigView(guild_id))

@bot.command(name="set-eco-log")
@commands.has_permissions(administrator=True)
async def set_eco_log(ctx, channel: discord.TextChannel):
    guild_id = ctx.guild.id
    collection36.update_one(
        {"guild_id": guild_id},
        {"$set": {"eco_log_channel": channel.id}},
        upsert=True
    )
    await ctx.send(f"✅ Les logs économiques seront envoyés dans {channel.mention}")

# Fonction pour récupérer ou créer les données utilisateur
def get_or_create_user_data(guild_id: int, user_id: int):
    data = collection28.find_one({"guild_id": guild_id, "user_id": user_id})
    if not data:
        data = {"guild_id": guild_id, "user_id": user_id, "cash": 1500, "bank": 0}
        collection28.insert_one(data)
    return data

@bot.hybrid_command(name="rob", description="Voler entre 30% et 80% du portefeuille d'un autre utilisateur.")
async def rob(ctx, user: discord.User):
    guild_id = ctx.guild.id
    user_id = ctx.author.id
    target_id = user.id

    if user.bot or user_id == target_id:
        reason = "Tu ne peux pas voler un bot." if user.bot else "Tu ne peux pas voler des coins à toi-même."
        embed = discord.Embed(description=reason, color=discord.Color.red())
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
        return await ctx.send(embed=embed)

    # Cooldown check
    last_rob = collection41.find_one({"guild_id": guild_id, "user_id": user_id})
    if last_rob and (last_rob_time := last_rob.get("last_rob")):
        time_left = last_rob_time + timedelta(hours=1) - datetime.utcnow()
        if time_left > timedelta(0):
            mins, secs = divmod(int(time_left.total_seconds()), 60)
            hrs, mins = divmod(mins, 60)
            time_str = f"{hrs}h {mins}min" if hrs else f"{mins}min"
            embed = discord.Embed(
                description=f"⏳ Attends encore **{time_str}** avant de pouvoir voler à nouveau.",
                color=discord.Color.red()
            )
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
            return await ctx.send(embed=embed)

    # Récupération du membre cible
    target_member = ctx.guild.get_member(target_id)
    if not target_member:
        return await ctx.send(embed=discord.Embed(
            description=f"Utilisateur introuvable sur ce serveur.",
            color=discord.Color.red()
        ))

    # Anti rob par rôles stockés dans MongoDB
    anti_rob_data = collection42.find_one({"guild_id": guild_id}) or {"roles": []}
    if any(role.name in anti_rob_data["roles"] for role in target_member.roles):
        return await ctx.send(embed=discord.Embed(
            description=f"{user.display_name} est protégé contre le vol.",
            color=discord.Color.red()
        ))

    # Vérifier si la cible a le rôle qui repousse les vols (300% banque)
    has_anti_rob_reflect = discord.utils.get(target_member.roles, id=1365313284584116264)
    user_data = collection28.find_one({"guild_id": guild_id, "user_id": user_id}) or {"cash": 1500, "bank": 0}
    if has_anti_rob_reflect:
        penalty = round(user_data["bank"] * 3.00, 2)
        penalty = min(penalty, user_data["bank"])
        collection.update_one({"guild_id": guild_id, "user_id": user_id}, {"$inc": {"bank": -penalty}})

        await log_eco_channel(bot, guild_id, ctx.author, "Vol repoussé", -penalty, user_data["bank"], user_data["bank"] - penalty, f"Repoussé par {user.display_name}")

        return await ctx.send(embed=discord.Embed(
            description=f"⚠️ {user.display_name} a tenté de voler **{target_member.display_name}**, mais a été **repoussé par une aura protectrice** !\n"
                        f"💸 Il perd **{int(penalty)}** coins de sa banque !",
            color=discord.Color.red()
        ).set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url))

    # Data utilisateur/target
    target_data = collection28.find_one({"guild_id": guild_id, "user_id": target_id}) or {"cash": 1500, "bank": 0}
    collection.update_one({"guild_id": guild_id, "user_id": user_id}, {"$setOnInsert": user_data}, upsert=True)
    collection.update_one({"guild_id": guild_id, "user_id": target_id}, {"$setOnInsert": target_data}, upsert=True)

    if target_data["cash"] <= 0:
        return await ctx.send(embed=discord.Embed(
            description=f"{user.display_name} n’a pas de monnaie à voler.",
            color=discord.Color.red()
        ))
    # Calcul succès du vol
    robber_total = user_data["cash"] + user_data["bank"]
    rob_chance = max(80 - (robber_total // 1000), 10)
    success = random.randint(1, 100) <= rob_chance

    # Enregistrement du cooldown
    collection41.update_one(
        {"guild_id": guild_id, "user_id": user_id},
        {"$set": {"last_rob": datetime.utcnow()}},
        upsert=True
    )

    if success:
        percentage = random.randint(30, 80)
        stolen = (percentage / 100) * target_data["cash"]

        if has_half_rob_protection:
            stolen /= 2

        # Limiter à 30% si protection active
        if has_30_percent_protection:
            max_stealable = target_data["cash"] * 0.30
            stolen = min(stolen, max_stealable)

        stolen = round(stolen, 2)
        stolen = min(stolen, target_data["cash"])
        initial_stolen = stolen

        # Application du vol
        collection28.update_one({"guild_id": guild_id, "user_id": user_id}, {"$inc": {"cash": stolen}})
        collection28.update_one({"guild_id": guild_id, "user_id": target_id}, {"$inc": {"cash": -stolen}})

        # Contre-attaque si rôle
        if has_counter_role:
            counter_amount = round(initial_stolen * 2, 2)
            collection28.update_one({"guild_id": guild_id, "user_id": user_id}, {"$inc": {"cash": -counter_amount}})
            collection28.update_one({"guild_id": guild_id, "user_id": target_id}, {"$inc": {"cash": counter_amount}})

            new_cash = user_data["cash"] - counter_amount
            await log_eco_channel(bot, guild_id, ctx.author, "Contre-vol subi", -counter_amount, user_data["cash"], new_cash, f"Contre-attaque de {user.display_name}")
            await log_eco_channel(bot, guild_id, target_member, "Contre-vol réussi", counter_amount, target_data["cash"], target_data["cash"] + counter_amount, f"Contre-attaque sur {ctx.author.display_name}")

            return await ctx.send(embed=discord.Embed(
                description=f"🔥 Mauvais choix ! {user.display_name} a été **contre-attaqué** et a perdu **{int(counter_amount)}** — il est maintenant **dans le négatif** !",
                color=discord.Color.red()
            ).set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url))

        await log_eco_channel(bot, guild_id, ctx.author, "Vol", stolen, user_data["cash"], user_data["cash"] + stolen, f"Volé à {user.display_name}")

        return await ctx.send(embed=discord.Embed(
            description=f"<:emoji_48:1362489008130621542> Tu as volé **{int(stolen)}** à **{user.display_name}** !",
            color=discord.Color.green()
        ).set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url))

    else:
        percentage = random.uniform(1, 5)
        loss = (percentage / 100) * user_data["cash"]
        loss = round(loss, 2)
        loss = min(loss, user_data["cash"])

        collection28.update_one({"guild_id": guild_id, "user_id": user_id}, {"$inc": {"cash": -loss}})

        await log_eco_channel(bot, guild_id, ctx.author, "Échec vol", -loss, user_data["cash"], user_data["cash"] - loss, f"Échec de vol sur {user.display_name}")

        return await ctx.send(embed=discord.Embed(
            description=f"🚨 Tu as échoué et perdu **{int(loss)}** !",
            color=discord.Color.red()
        ).set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url))

@bot.command(name="set-anti_rob")
async def set_anti_rob(ctx):
    if not ctx.author.guild_permissions.administrator:
        return await ctx.send(embed=discord.Embed(
            description="Tu n'as pas la permission d'exécuter cette commande.",
            color=discord.Color.red()
        ))

    guild_id = ctx.guild.id
    data = collection42.find_one({"guild_id": guild_id}) or {"guild_id": guild_id, "roles": []}
    anti_rob_roles = data["roles"]

    embed = discord.Embed(
        title="🔐 Gestion des rôles anti-rob",
        description="Choisis une action à effectuer ci-dessous.\n\n"
                    "**Rôles actuellement protégés :**\n"
                    f"{', '.join(anti_rob_roles) if anti_rob_roles else 'Aucun rôle protégé.'}",
        color=discord.Color.blurple()
    )

    class ActionSelect(Select):
        def __init__(self):
            options = [
                discord.SelectOption(label="Ajouter un rôle", value="add", emoji="✅"),
                discord.SelectOption(label="Supprimer un rôle", value="remove", emoji="❌")
            ]
            super().__init__(
                placeholder="Choisis une action",
                min_values=1,
                max_values=1,
                options=options
            )

        async def callback(self, interaction: discord.Interaction):
            if interaction.user != ctx.author:
                return await interaction.response.send_message("Cette interaction ne t'est pas destinée.", ephemeral=True)

            await interaction.response.send_message(
                f"Tu as choisi **{self.values[0]}**. Merci de **mentionner un rôle** dans le chat.",
                ephemeral=True
            )

            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel and msg.role_mentions

            try:
                msg = await bot.wait_for("message", timeout=30.0, check=check)
                role = msg.role_mentions[0]
                role_name = role.name

                if self.values[0] == "add":
                    if role_name in anti_rob_roles:
                        await ctx.send(f"🔸 Le rôle **{role_name}** est déjà protégé.")
                    else:
                        anti_rob_roles.append(role_name)
                        await ctx.send(f"✅ Le rôle **{role_name}** a été ajouté à la protection anti-rob.")
                elif self.values[0] == "remove":
                    if role_name in anti_rob_roles:
                        anti_rob_roles.remove(role_name)
                        await ctx.send(f"❌ Le rôle **{role_name}** a été retiré de la protection anti-rob.")
                    else:
                        await ctx.send(f"🔸 Le rôle **{role_name}** n’est pas protégé.")

                # Mise à jour BDD
                collection42.update_one({"guild_id": guild_id}, {"$set": {"roles": anti_rob_roles}}, upsert=True)

            except asyncio.TimeoutError:
                await ctx.send("⏱️ Temps écoulé. Merci de réessayer.")

    view = View()
    view.add_item(ActionSelect())
    await ctx.send(embed=embed, view=view)

@bot.hybrid_command(
    name="set-rr-limite",
    description="Fixe une limite de mise pour la roulette russe. (Admin seulement)"
)
@commands.has_permissions(administrator=True)  # Permet uniquement aux admins de modifier la limite
async def set_rr_limite(ctx: commands.Context, limite: int):
    if limite <= 0:
        return await ctx.send("La limite de mise doit être un nombre positif.")
    
    guild_id = ctx.guild.id

    # Mettre à jour la limite dans la collection info_rr
    collection38.update_one(
        {"guild_id": guild_id},
        {"$set": {"rr_limite": limite}},
        upsert=True  # Si la donnée n'existe pas, elle sera créée
    )

    await ctx.send(f"La limite de mise pour la roulette russe a été fixée à {limite:,} coins.")

active_rr_games = {}

@bot.command(aliases=["rr"])
async def russianroulette(ctx, arg: str):
    guild_id = ctx.guild.id
    user = ctx.author

    # Fonction pour récupérer le cash
    def get_user_cash(guild_id: int, user_id: int):
        data = collection28.find_one({"guild_id": guild_id, "user_id": user_id})
        if data:
            return data.get("cash", 0)
        return 0

    # Fonction pour créer ou récupérer les données utilisateur
    def get_or_create_user_data(guild_id, user_id):
        data = collection28.find_one({"guild_id": guild_id, "user_id": user_id})
        if not data:
            data = {"guild_id": guild_id, "user_id": user_id, "cash": 1500, "bank": 0}
            collection28.insert_one(data)
        return data

    # Fonction pour parser le montant avec notation exponentielle (ex: 5e2 -> 500)
    def parse_mise(mise):
        match = re.match(r"(\d+)e(\d+)", mise)
        if match:
            base = int(match.group(1))
            exponent = int(match.group(2))
            return base * (10 ** exponent)
        else:
            return int(mise)

    if arg.isdigit() or arg.lower() == "all" or arg.lower() == "half":
        if arg.lower() == "all":
            bet = get_user_cash(guild_id, user.id)
        elif arg.lower() == "half":
            bet = get_user_cash(guild_id, user.id) // 2
        else:
            try:
                bet = parse_mise(arg)  # Utilisation de la fonction parse_mise
            except ValueError:
                return await ctx.send(embed=discord.Embed(
                    description=f"<:classic_x_mark:1362711858829725729> La mise spécifiée est invalide.",
                    color=discord.Color.from_rgb(255, 92, 92)
                ))

        if bet < 1:
            return await ctx.send(embed=discord.Embed(
                description=f"<:classic_x_mark:1362711858829725729> La mise minimale est de 1 coin.",
                color=discord.Color.from_rgb(255, 92, 92)
            ))

        if bet > 10000:
            return await ctx.send(embed=discord.Embed(
                description=f"<:classic_x_mark:1362711858829725729> La mise maximale autorisée est de 10,000 coins.",
                color=discord.Color.from_rgb(255, 92, 92)
            ))

        user_cash = get_user_cash(guild_id, user.id)

        if bet > user_cash:
            return await ctx.send(embed=discord.Embed(
                description=f"<:classic_x_mark:1362711858829725729> Tu n'as pas assez de cash pour cette mise. Tu as {user_cash} coins.",
                color=discord.Color.from_rgb(255, 92, 92)
            ))

        if guild_id in active_rr_games:
            game = active_rr_games[guild_id]
            if user in game["players"]:
                return await ctx.send(embed=discord.Embed(
                    description=f"<:classic_x_mark:1362711858829725729> Tu as déjà rejoint cette partie.",
                    color=discord.Color.from_rgb(255, 92, 92)
                ))
            if bet != game["bet"]:
                return await ctx.send(embed=discord.Embed(
                    description=f"<:classic_x_mark:1362711858829725729> Tu dois miser exactement {game['bet']} coins pour rejoindre cette partie.",
                    color=discord.Color.from_rgb(255, 92, 92)
                ))
            game["players"].append(user)
            return await ctx.send(embed=discord.Embed(
                description=f"{user.mention} a rejoint cette partie de Roulette Russe avec une mise de <:ecoEther:1341862366249357374> {bet}.",
                color=0x00FF00
            ))

        else:
            embed = discord.Embed(
                title="Nouvelle partie de Roulette Russe",
                description="> Pour démarrer cette partie : `!!rr start`\n"
                            "> Pour rejoindre : `!!rr <montant>`\n\n"
                            "**Temps restant :** 5 minutes ou 5 joueurs maximum",
                color=discord.Color.from_rgb(100, 140, 230)
            )
            msg = await ctx.send(embed=embed)

            active_rr_games[guild_id] = {
                "starter": user,
                "bet": bet,
                "players": [user],
                "message_id": msg.id
            }

            async def cancel_rr():
                await asyncio.sleep(300)
                if guild_id in active_rr_games and len(active_rr_games[guild_id]["players"]) == 1:
                    await ctx.send(embed=discord.Embed(
                        description="<:classic_x_mark:1362711858829725729> Personne n'a rejoint la roulette russe. La partie est annulée.",
                        color=discord.Color.from_rgb(255, 92, 92)
                    ))
                    del active_rr_games[guild_id]

            active_rr_games[guild_id]["task"] = asyncio.create_task(cancel_rr())

    elif arg.lower() == "start":
        game = active_rr_games.get(guild_id)
        if not game:
            return await ctx.send(embed=discord.Embed(
                description="<:classic_x_mark:1362711858829725729> Aucune partie en cours.",
                color=discord.Color.from_rgb(240, 128, 128)
            ))
        if game["starter"] != user:
            return await ctx.send(embed=discord.Embed(
                description="<:classic_x_mark:1362711858829725729> Seul le créateur de la partie peut la démarrer.",
                color=discord.Color.from_rgb(255, 92, 92)
            ))

        if len(game["players"]) < 2:
            await ctx.send(embed=discord.Embed(
                description="<:classic_x_mark:1362711858829725729> Pas assez de joueurs pour démarrer. La partie est annulée.",
                color=discord.Color.from_rgb(255, 92, 92)
            ))
            game["task"].cancel()
            del active_rr_games[guild_id]
            return

        # Début du jeu
        await ctx.send(embed=discord.Embed(
            description="<:Check:1362710665663615147> La roulette russe commence...",
            color=0x00FF00
        ))
        await asyncio.sleep(1)

        eliminated = random.choice(game["players"])
        survivors = [p for p in game["players"] if p != eliminated]

        # Phase 1 : qui meurt
        embed1 = discord.Embed(
            description=f"{eliminated.display_name} tire... et se fait avoir <:imageremovebgpreview53:1362693948702855360>",
            color=discord.Color.from_rgb(255, 92, 92)
        )
        await ctx.send(embed=embed1)
        await asyncio.sleep(1)

        # Phase 2 : les survivants
        result_embed = discord.Embed(
            title="Survivants de la Roulette Russe",
            description="\n".join([f"{p.mention} remporte <:emoji_48:1362489008130621542> {game['bet'] * 2}" for p in survivors]),
            color=0xFF5C5C
        )
        await ctx.send(embed=result_embed)

        # Distribution des gains
        for survivor in survivors:
            data = get_or_create_user_data(guild_id, survivor.id)
            data["cash"] += game["bet"] * 2  # Leur propre mise + celle du perdant
            collection28.update_one(
                {"guild_id": guild_id, "user_id": survivor.id},
                {"$set": {"cash": int(data["cash"])}}  # Arrondir le cash des survivants
            )

        # Retirer la mise au perdant
        loser_data = get_or_create_user_data(guild_id, eliminated.id)
        loser_data["cash"] -= game["bet"]
        collection28.update_one(
            {"guild_id": guild_id, "user_id": eliminated.id},
            {"$set": {"cash": int(loser_data["cash"])}}  # Arrondir le cash du perdant
        )

        # Suppression de la partie
        game["task"].cancel()
        del active_rr_games[guild_id]

    else:
        await ctx.send(embed=discord.Embed(
            description="Utilise `!!rr <montant>` pour lancer ou rejoindre une roulette russe.",
            color=discord.Color.from_rgb(255, 92, 92)
        ))
#-------------------------------------------------------------- Daily

@bot.hybrid_command(name="daily", aliases=["dy"], description="Réclame tes Coins quotidiens.")
async def daily(ctx: commands.Context):
    if ctx.guild is None:
        return await ctx.send("Cette commande ne peut être utilisée qu'en serveur.")
    
    guild_id = ctx.guild.id
    user_id = ctx.author.id
    now = datetime.utcnow()

    cooldown_data = collection44.find_one({"guild_id": guild_id, "user_id": user_id})
    cooldown_duration = timedelta(hours=24)

    if cooldown_data and "last_claim" in cooldown_data:
        last_claim = cooldown_data["last_claim"]
        next_claim = last_claim + cooldown_duration

        if now < next_claim:
            remaining = next_claim - now
            hours, remainder = divmod(remaining.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            cooldown_embed = discord.Embed(
                description=f"<:classic_x_mark:1362711858829725729> Vous devez attendre encore "
                            f"**{remaining.days * 24 + hours} heures, {minutes} minutes et {seconds} secondes** "
                            f"avant de pouvoir recevoir vos Coins quotidiens.",
                color=discord.Color.red()
            )
            return await ctx.send(embed=cooldown_embed)

    # Génération du montant (retirer la décimale)
    amount = int(random.randint(1, 100))

    # Récupération ou création du document utilisateur
    user_data = collection28.find_one({"guild_id": guild_id, "user_id": user_id})
    if not user_data:
        user_data = {"guild_id": guild_id, "user_id": user_id, "cash": 1500, "bank": 0}
        collection28.insert_one(user_data)

    # Mise à jour du solde
    old_cash = user_data["cash"]
    new_cash = old_cash + amount
    collection28.update_one(
        {"guild_id": guild_id, "user_id": user_id},
        {"$inc": {"cash": amount}}
    )

    # Mise à jour du cooldown
    collection44.update_one(
        {"guild_id": guild_id, "user_id": user_id},
        {"$set": {"last_claim": now}},
        upsert=True
    )

    # Embed de succès
    success_embed = discord.Embed(
        description=f"<:emoji_48:1362489008130621542> Vous avez reçu vos **{amount}** Coins quotidiens.\n"
                    f"Votre prochaine récompense sera disponible dans **24 heures**.",
        color=discord.Color.green()
    )
    await ctx.send(embed=success_embed)

    # Log
    await log_eco_channel(
        bot=bot,
        guild_id=guild_id,
        user=ctx.author,
        action="Récompense quotidienne",
        amount=amount,
        balance_before=old_cash,
        balance_after=new_cash,
        note="Commande /daily"
    )
#----------------------------------------------------- Leaderbaord

@bot.hybrid_command(
    name="leaderboard",
    aliases=["lb"],
    description="Affiche le classement des plus riches"
)
@app_commands.describe(sort="Choisir le critère de classement: 'cash' pour l'argent, 'bank' pour la banque, ou 'total' pour la somme des deux.")
@app_commands.choices(
    sort=[
        app_commands.Choice(name="Cash", value="cash"),
        app_commands.Choice(name="Banque", value="bank"),
        app_commands.Choice(name="Total", value="total")
    ]
)
async def leaderboard(
    ctx: commands.Context,
    sort: Optional[str] = "total"
):
    if ctx.guild is None:
        return await ctx.send("Cette commande ne peut être utilisée qu'en serveur.")

    guild_id = ctx.guild.id
    emoji_currency = "<:emoji_48:1362489008130621542>"
    bank_logo = "https://github.com/Iseyg91/Isey_aime_Cass/blob/main/1344747420159967293.png?raw=true"

    # Détection du tri via arguments dans le message
    if isinstance(ctx, commands.Context) and ctx.message.content:
        content = ctx.message.content.lower()
        if "-cash" in content:
            sort = "cash"
        elif "-bank" in content:
            sort = "bank"
        else:
            sort = "total"

    if sort == "cash":
        sort_key = lambda u: u.get("cash", 0)
        title = f"Leaderboard - Cash"
    elif sort == "bank":
        sort_key = lambda u: u.get("bank", 0)
        title = f"Leaderboard - Banque"
    else:
        sort_key = lambda u: u.get("cash", 0) + u.get("bank", 0)
        title = f"Leaderboard - Total"

    all_users_data = list(collection28.find({"guild_id": guild_id}))
    sorted_users = sorted(all_users_data, key=sort_key, reverse=True)

    page_size = 10
    total_pages = (len(sorted_users) + page_size - 1) // page_size

    def get_page(page_num: int):
        start_index = page_num * page_size
        end_index = start_index + page_size
        users_on_page = sorted_users[start_index:end_index]

        embed = discord.Embed(color=discord.Color.blue())
        embed.set_author(name="Leaderboard", icon_url=bank_logo)

        lines = []
        for i, user_data in enumerate(users_on_page, start=start_index + 1):
            user_id = user_data.get("user_id")
            if not user_id:
                continue
            user = ctx.guild.get_member(user_id)
            name = user.display_name if user else f"Utilisateur {user_id}"
            cash = user_data.get("cash", 0)
            bank = user_data.get("bank", 0)
            total = cash + bank

            # Formater les montants pour enlever les décimales
            if sort == "cash":
                amount = int(cash)
            elif sort == "bank":
                amount = int(bank)
            else:
                amount = int(total)

            line = f"{str(i).rjust(2)}. `{name}` • {emoji_currency} {amount:,}"
            lines.append(line)

        embed.add_field(name=title, value="\n".join(lines), inline=False)

        author_data = collection28.find_one({"guild_id": guild_id, "user_id": ctx.author.id})
        user_rank = next((i + 1 for i, u in enumerate(sorted_users) if u["user_id"] == ctx.author.id), None)
        embed.set_footer(text=f"Page {page_num + 1}/{total_pages}  •  Ton rang: {user_rank}")
        return embed

    class LeaderboardView(View):
        def __init__(self, page_num):
            super().__init__(timeout=60)
            self.page_num = page_num

        @discord.ui.button(label="⬅️ Précédent", style=discord.ButtonStyle.primary)
        async def previous_page(self, interaction: discord.Interaction, button: Button):
            if self.page_num > 0:
                self.page_num -= 1
                embed = get_page(self.page_num)
                await interaction.response.edit_message(embed=embed, view=self)

        @discord.ui.button(label="➡️ Suivant", style=discord.ButtonStyle.primary)
        async def next_page(self, interaction: discord.Interaction, button: Button):
            if self.page_num < total_pages - 1:
                self.page_num += 1
                embed = get_page(self.page_num)
                await interaction.response.edit_message(embed=embed, view=self)

    view = LeaderboardView(0)
    embed = get_page(0)
    await ctx.send(embed=embed, view=view)

#----------------------------------------------- Collect
@bot.hybrid_command(
    name="collect-income",
    aliases=["collect"],
    description="Collecte tes revenus associés à tes rôles spéciaux, si le cooldown est terminé."
)
async def collect_income(ctx: commands.Context):
    member = ctx.author
    guild = ctx.guild
    now = datetime.utcnow()
    collected = []
    cooldowns = []

    for config in COLLECT_ROLES_CONFIG:
        role = guild.get_role(config["role_id"])
        if role is None or config.get("auto", False):
            continue

        if role not in member.roles:
            continue

        # Vérifie le cooldown
        cd_data = collection47.find_one({
            "guild_id": guild.id,
            "user_id": member.id,
            "role_id": role.id
        })
        last_collect = cd_data.get("last_collect") if cd_data else None

        try:
            if last_collect:
                elapsed = (now - last_collect).total_seconds()
                if elapsed < config["cooldown"]:
                    remaining = config["cooldown"] - elapsed
                    cooldowns.append((remaining, role))
                    continue
        except Exception as e:
            print(f"[DEBUG] Erreur sur cooldown pour {role.name}: {e}")

        # Traitement éco
        eco_data = collection28.find_one({
            "guild_id": guild.id,
            "user_id": member.id
        }) or {"guild_id": guild.id, "user_id": member.id, "cash": 1500, "bank": 0}

        amount = config.get("amount", 0)
        target = config.get("target", "cash")
        eco_data[target] = eco_data.get(target, 0) + amount

        collection28.update_one(
            {"guild_id": guild.id, "user_id": member.id},
            {"$set": {target: eco_data[target]}},
            upsert=True
        )

        collection47.update_one(
            {"guild_id": guild.id, "user_id": member.id, "role_id": role.id},
            {"$set": {"last_collect": now}},
            upsert=True
        )

        collected.append(f"{role.mention} | <:emoji_48:1362489008130621542>**{amount}** ({target})")

        await log_eco_channel(
            bot, guild.id, member,
            f"Collect ({role.name})", amount, eco_data[target] - amount, eco_data[target],
            note=f"Collect manuel → {target}"
        )

    if collected:
        embed = discord.Embed(
            title=f"{member.display_name}",
            description="<:Check:1362710665663615147> Revenus collectés avec succès !\n\n" + "\n".join(collected),
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        await ctx.send(embed=embed)
        return

    if cooldowns:
        shortest = min(cooldowns, key=lambda x: x[0])
        remaining_minutes = int(shortest[0] // 60) or 1
        embed = discord.Embed(
            title="⏳ Collect en cooldown",
            description=f"Tu dois attendre encore **{remaining_minutes} min** pour le rôle {shortest[1].mention}.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return

    await ctx.send("Tu n'as aucun rôle collect actif ou tous sont en cooldown.")

# Token pour démarrer le bot (à partir des secrets)
# Lancer le bot avec ton token depuis l'environnement  
keep_alive()
bot.run(token)
