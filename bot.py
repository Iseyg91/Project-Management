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

token = os.environ['ETHERYA']
intents = discord.Intents.all()
start_time = time.time()
bot = commands.Bot(command_prefix="-", intents=intents, help_command=None)

#Configuration du Bot:
# --- ID Owner Bot ---
ISEY_ID = 792755123587645461

# --- ID PROJECT : DELTA SERVER ---
GUILD_ID = 1359963854200639498

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
        "delta_invite": delta_invite_data
    }

    return combined_data

# Dictionnaire pour stocker les paramètres de chaque serveur
GUILD_SETTINGS = {}

#------------------------------------------------------------------------- Code Protection:                
# Événement quand le bot est prêt
@bot.event
async def on_ready():
    print(f"✅ Le bot {bot.user} est maintenant connecté ! (ID: {bot.user.id})")

    bot.uptime = time.time()

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

# --- VIEW POUR CRÉATION DE TICKET ---
class TicketView(ui.View):
    def __init__(self, author_id, emoji="📩"):
        super().__init__(timeout=None)
        self.author_id = author_id
        self.emoji = emoji

        self.add_item(ui.Button(
            label="Passé Commande",
            style=ButtonStyle.success,
            custom_id="open_ticket",
            emoji=self.emoji
        ))

# --- ÉCOUTEUR POUR BOUTON CUSTOM ---
@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.component and interaction.data["custom_id"] == "open_ticket":
        guild = interaction.guild
        category = guild.get_channel(1362015652700754052)
        emoji = interaction.message.components[0].children[0].emoji or "📩"

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        }

        channel_name = f"︱{emoji}・{interaction.user.name}"
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
    await ctx.send(embed=panel_embed(), view=TicketView(ctx.author.id, emoji="📩"))

@bot.command(name="panel2")
async def panel2(ctx):
    if ctx.author.id != ISEY_ID:
        return await ctx.send("❌ Tu n'es pas autorisé à utiliser cette commande.")
    await ctx.send(embed=panel_embed(), view=TicketView(ctx.author.id, emoji="🎨"))

@bot.command(name="panel3")
async def panel3(ctx):
    if ctx.author.id != ISEY_ID:
        return await ctx.send("❌ Tu n'es pas autorisé à utiliser cette commande.")
    await ctx.send(embed=panel_embed(), view=TicketView(ctx.author.id, emoji="🖇️"))

@bot.command(name="panel4")
async def panel4(ctx):
    if ctx.author.id != ISEY_ID:
        return await ctx.send("❌ Tu n'es pas autorisé à utiliser cette commande.")
    await ctx.send(embed=panel_embed(), view=TicketView(ctx.author.id, emoji="🎓"))

# --- EMBED COMMUN ---
def panel_embed():
    return discord.Embed(
        title="Passer commande",
        description="Vous souhaitez passer une commande ? N'hésitez pas à ouvrir un ticket et nous serons ravis de vous assister !",
        color=0x2ecc71
    )
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

# Token pour démarrer le bot (à partir des secrets)
# Lancer le bot avec ton token depuis l'environnement  
keep_alive()
bot.run(token)
