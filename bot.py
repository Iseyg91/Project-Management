import discord
from discord.ext import commands, tasks
from discord import app_commands, Embed, ButtonStyle, ui
from discord.ui import Button, View, Select, Modal, TextInput
from discord.utils import get
from discord import TextStyle
from functools import wraps
import os
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
from datetime import datetime, timedelta  # Tu as déjà la bonne importation pour datetime et timedelta
from collections import defaultdict, deque
import pymongo
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
import psutil
import pytz
import platform
from discord import Interaction
import logging
from typing import Optional

token = os.environ['ETHERYA']
intents = discord.Intents.all()
start_time = time.time()
bot = commands.Bot(command_prefix="!!", intents=intents, help_command=None)

#Configuration du Bot:
# --- ID Owner Bot ---
ISEY_ID = 792755123587645461
# Définir GUILD_ID
GUILD_ID = 1034007767050104892

# --- ID Etherya ---
BOUNTY_CHANNEL_ID = 1355298449829920950
ETHERYA_SERVER_ID = 1034007767050104892
AUTORIZED_SERVER_ID = 1034007767050104892
WELCOME_CHANNEL_ID = 1355198748296351854

log_channels = {
    "sanctions": 1365674258591912018,
    "messages": 1365674387700977684,
    "utilisateurs": 1365674425394921602,
    "nicknames": 1365674498791051394,
    "roles": 1365674530793586758,
    "vocal": 1365674563458826271,
    "serveur": 1365674597692997662,
    "permissions": 1365674740915765278,
    "channels": 1365674773107052644,
    "webhooks": 1365674805143146506,
    "bots": 1365674841344049162,
    "boosts": 1365674914740441158
}

# === CONFIGURATION DES RÉCOMPENSES PAR JOUR ===
daily_rewards = {
    1: {"coins": 10000, "badge": None, "item": None, "image_url": "https://github.com/Iseyg91/Shadow/blob/main/Season%20Beta/image.1.png?raw=true"},
    2: {"coins": 15000, "badge": None, "item": None, "image_url": "https://github.com/Iseyg91/Shadow/blob/main/Season%20Beta/image.2.png?raw=true"},
    3: {"coins": 20000, "badge": 4, "item": None, "image_url": "https://github.com/Iseyg91/Shadow/blob/main/Season%20Beta/image.3.png?raw=true"},
    4: {"coins": 25000, "badge": None, "item": None, "image_url": "https://github.com/Iseyg91/Shadow/blob/main/Season%20Beta/image.4.png?raw=true"},
    5: {
        "coins": 30000,
        "badge": None,
        "item": None,
        "random_items": [
            {"id": 763, "chance": 30},   # Bomu
            {"id": 203, "chance": 25},   # Tetsu
            {"id": 542, "chance": 20},   # Joki
            {"id": 352, "chance": 15},   # Gol
            {"id": 801, "chance": 5},    # Gura
            {"id": 802, "chance": 3},    # Hie
            {"id": 803, "chance": 1},    # Yami
            {"id": 804, "chance": 1},    # Gomu
            {"id": 805, "chance": 0},    # Nika
            {"id": 806, "chance": 0}     # Uo
        ],
        "image_url": "https://github.com/Iseyg91/Shadow/blob/main/Season%20Beta/image.5.png?raw=true"
    },
    6: {"coins": 40000, "badge": None, "item": None, "image_url": "https://github.com/Iseyg91/Shadow/blob/main/Season%20Beta/image.6.png?raw=true"},
    7: {"coins": 50000, "badge": 3, "item": None, "image_url": "https://github.com/Iseyg91/Shadow/blob/main/Season%20Beta/image.7.png?raw=true"}
}
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

# Collections
collection = db['ether_eco']  #Stock les Bal
collection2 = db['ether_daily']  #Stock les cd de daily
collection3 = db['ether_slut']  #Stock les cd de slut
collection4 = db['ether_crime']  #Stock les cd de slut
collection5 = db['ether_collect'] #Stock les cd de collect
collection6 = db['ether_work'] #Stock les cd de Work
collection7 = db['ether_inventory'] #Stock les inventaires
collection8 = db['info_cf'] #Stock les Info du cf
collection9 = db['info_logs'] #Stock le Salon logs
collection10 = db['info_bj'] #Stock les Info du Bj
collection11 = db['info_rr'] #Stock les Info de RR
collection12 = db['info_roulette'] #Stock les Info de SM
collection13 = db['info_sm'] #Stock les Info de SM
collection14 = db['ether_rob'] #Stock les cd de Rob
collection15 = db['anti_rob'] #Stock les rôle anti-rob
collection16 = db['ether_boutique'] #Stock les Items dans la boutique
collection17 = db['joueur_ether_inventaire'] #Stock les items de joueurs
collection18 = db['ether_effects'] #Stock les effets
collection19 = db['ether_badge'] #Stock les bagde
collection20 = db['inventaire_badge'] #Stock les bagde des joueurs
collection21 = db['daily_badge'] #Stock les cd des daily badge
collection22 = db['start_date'] #Stock la date de commencemant des rewards
collection23 = db['joueur_rewards'] #Stock ou les joueurs sont
collection24 = db['cd_renforcement'] #Stock les cd
collection25 = db['cd_emission'] #Stock les cd
collection26 = db['cd_manipulation'] #Stock les cd
collection27 = db['cd_materialisation'] #Stock les cd
collection28 = db['cd_transformation'] #Stock les cd
collection29 = db['cd_specialisation'] #Stock les cd
collection30 = db['cd_haki_attaque'] #Stock les cd
collection31 = db['cd_haki_subis'] #Stock les cd
collection32 = db['ether_quetes'] #Stock les quetes
collection33 = db['inventory_collect'] #Stock les items de quetes
collection34 = db['collect_items'] #Stock les items collector
collection35 = db['ether_guild'] #Stock les Guild
collection36 = db['guild_inventaire'] #Stock les inventaire de Guild
collection37 = db['ether_bounty'] #Stock les Primes de Pirates
collection38 = db['ether_honor'] #Stock les Honor des Marines
collection39 = db['cd_capture_ether'] #Stock les cd d'attaque
collection40 = db['cd_bombe'] #Stock les cd des bombes
collection41 = db['cd_gura'] #Stock les cd de seismes
collection42 = db['cd_glace'] #Stock les cd d'attaque de glace
collection43 = db['glace_subis'] #Stock le cd avant de retirer le rôle de subis de glace
collection44 = db['cd_tenebre'] #Stock les cd de Yami
collection45 = db['cd_protection_tenebre'] #Stock le temps de protection de Yami
collection46 = db['cd_gear_second'] #Stock le cd des Gear Second
collection47 = db['cd_gear_fourth'] #Stock les cd des Gear Fourth
collection48 = db['cd_use_fourth'] #Stock les cd des utilisation du Gear Fourth
collection49 = db['cd_royaume_nika'] #Stock le cd des utilisation du Royaume
collection50 = db['cd_acces_royaume'] #Stock le cd d'acces au Royaume
collection51 = db['cd_nika_collect'] #Stock le cd de reutilisation du Nika Collect
collection52 = db['cd_eveil_attaque'] #Stock le cd de reutilisation du Nika Eveil
collection53 = db['cd_eveil_subis'] #Stock le cd de soumission du Nika Eveil
collection54 = db['cd_bourrasque'] #Stock le cd de reutilisation du Uo Uo no Mi
collection55 = db['cd_bourrasque_subis'] #Stock le cd de soumission du Uo Uo no Mi
collection56 = db['cd_tonnerre_attaque'] #Stock les cd de reutillisation du Tonnerre Divin
collection57 = db['cd_tonnerre_subis'] #Stock les cd de soumission du Tonnerre Divin
collection58 = db['cd_eveil_uo'] #Stock les cd d'eveil du Dragon
collection59 = db['message_jour'] #Stock les message des membres chaque jour
collection60 = db['cd_wobservation'] #Stock les cd de W Observation
collection61 = db['cd_observation']

def load_guild_settings(guild_id):
    # Charger les données de la collection principale
    ether_eco_data = collection.find_one({"guild_id": guild_id}) or {}
    ether_daily_data = collection2.find_one({"guild_id": guild_id}) or {}
    ether_slut_data = collection3.find_one({"guild_id": guild_id}) or {}
    ether_crime_data = collection4.find_one({"guild_id": guild_id}) or {}
    ether_collect = collection5.find_one({"guild_id": guild_id}) or {}
    ether_work_data = collection6.find_one({"guild_id": guild_id}) or {}
    ether_inventory_data = collection7.find_one({"guild_id": guild_id}) or {}
    info_cf_data = collection8.find_one({"guild_id": guild_id}) or {}
    info_logs_data = collection9.find_one({"guild_id": guild_id}) or {}
    info_bj_data = collection10.find_one({"guild_id": guild_id}) or {}
    info_rr_data = collection11.find_one({"guild_id": guild_id}) or {}
    info_roulette_data = collection12.find_one({"guild_id": guild_id}) or {}
    info_sm_roulette_data = collection13.find_one({"guild_id": guild_id}) or {}
    ether_rob_data = collection14.find_one({"guild_id": guild_id}) or {}
    anti_rob_data = collection15.find_one({"guild_id": guild_id}) or {}
    ether_boutique_data = collection16.find_one({"guild_id": guild_id}) or {}
    joueur_ether_inventaire_data = collection17.find_one({"guild_id": guild_id}) or {}
    ether_effects_data = collection18.find_one({"guild_id": guild_id}) or {}
    ether_badge_data = collection19.find_one({"guild_id": guild_id}) or {}
    inventaire_badge_data = collection20.find_one({"guild_id": guild_id}) or {}
    daily_badge_data = collection21.find_one({"guild_id": guild_id}) or {}
    start_date_data = collection22.find_one({"guild_id": guild_id}) or {}
    joueur_rewards_data = collection23.find_one({"guild_id": guild_id}) or {}
    cd_renforcement_data = collection24.find_one({"guild_id": guild_id}) or {}
    cd_emission_data = collection25.find_one({"guild_id": guild_id}) or {}
    cd_manipultation_data = collection26.find_one({"guild_id": guild_id}) or {}
    cd_materialisation_data = collection27.find_one({"guidl_id": guild_id}) or {}
    cd_transformation_data = collection28.find_one({"guild_id": guild_id}) or {}
    cd_specialisation_data = collection29.find_one({"guild_id": guild_id}) or {}
    cd_haki_attaque_data = collection30.find_one({"guild_id": guild_id}) or {}
    cd_haki_subis_data = collection31.find_one({"guild_id": guild_id}) or {}
    ether_quetes_data = collection32.find_one({"guild_id": guild_id}) or {}
    inventory_collect_data = collection33.find_one({"guild_id": guild_id}) or {}
    collect_items_data = collection34.find_one({"guild_id": guild_id}) or {}
    ether_guild_data = collection35.find_one({"guild_id": guild_id}) or {}
    guild_inventaire_data = collection36.find_one({"guild_id": guild_id}) or {}
    ether_bounty_data = collection37.find_one({"guild_id": guild_id}) or {}
    ether_honnor_data = collection38.find_one({"guild_id": guild_id}) or {}
    cd_capture_ether_data = collection39.find_one({"guild_id": guild_id}) or {}
    cd_bombe_data = collection40.find_one({"guild_id": guild_id}) or {}
    cd_gura_data = collection41.find_one({"guild_id": guild_id}) or {}
    cd_glace_data = collection42.fing_one({"guild_id": guild_id}) or {}
    glace_subis_data = collection43.find_one({"guild_id": guild_id}) or {}
    cd_tenebre_data = collection44.find_one({"guild_id": guild_id}) or {}
    cd_protection_tenebre_data = collection45.find_one({"guild_id": guild_id}) or {}
    cd_gear_second_data = collection46.find_one({"guild_id": guild_id}) or {}
    cd_gear_fourth_data = collection47.find_one({"guild_id": guild_id}) or {}
    cd_use_fourth_data = collection48.find_one({"guild_id": guild_id}) or {}
    cd_royaume_nika_data = collection49.find_one({"guild_id": guild_id}) or {}
    cd_acces_royaume_data = collection50.find_one({"guild_id": guild_id}) or {}
    cd_nika_collect_data = collection51.find_one({"guild_id": guild_id}) or {}
    cd_eveil_attaque_data = collection52.find_one({"guild_id": guild_id}) or {}
    cd_eveil_subis_data = collection53.find_one({"guild_id": guild_id}) or {}
    cd_bourrasque_data = collection54.find_one({"guild_id": guild_id}) or {}
    cd_bourrasque_subis_data = collection55.find_one({"guild_id": guild_id}) or {}
    cd_tonnerre_attaque_data = collection56.find_one({"guild_id": guil_id}) or {}
    cd_tonnerre_subis_data = collection57.find_one({"guild_id": guild_id}) or {}
    cd_eveil_uo_data = collection58.find_one({"guild_id": guild_id}) or {}
    message_jour_data = collection59.find_one({"guild_id": guild_id}) or {}
    cd_wobservation_data = collection60.find_one({"guild_id": guild_id}) or {}
    cd_observation_data = collection61.find_one({"guild_id": guild_id}) or {}
    
    # Débogage : Afficher les données de setup
    print(f"Setup data for guild {guild_id}: {setup_data}")

    combined_data = {
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
        "ether_boutique": ether_boutique_data,
        "joueur_ether_inventaire": joueur_ether_inventaire_data,
        "ether_effects": ether_effects_data,
        "ether_badge": ether_badge_data,
        "inventaire_badge": inventaire_badge_data,
        "daily_badge": daily_badge_data,
        "start_date": start_date_data,
        "joueur_rewards": joueur_rewards_data,
        "cd_renforcement": cd_renforcement_data,
        "cd_emission": cd_emission_data,
        "cd_manipultation": cd_manipultation_data,
        "cd_materialisation": cd_materialisation_data,
        "cd_transformation" : cd_transformation_data,
        "cd_specialisation" : cd_specialisation_data,
        "cd_haki_attaque": cd_haki_attaque_data,
        "cd_haki_subis": cd_haki_subis_data,
        "ether_quetes": ether_quetes_data,
        "inventory_collect": inventory_collect_data,
        "collect_items": collect_items_data,
        "ether_guild": ether_guild_data,
        "guild_inventaire": guild_inventaire_data,
        "ether_bounty": ether_bounty_data,
        "ether_honnor": ether_honnor_data,
        "cd_capture_ether": cd_capture_ether_data,
        "cd_bombe": cd_bombe_data,
        "cd_gura": cd_gura_data,
        "cd_glace": cd_glace_data,
        "glace_subis": glace_subis_data,
        "cd_tenebre": cd_tenebre_data,
        "cd_protection_tenebre": cd_protection_tenebre_data,
        "cd_gear_second": cd_gear_second_data,
        "cd_gear_fourth": cd_gear_fourth_data,
        "cd_use_fourth": cd_use_fourth_data,
        "cd_royaume_nika": cd_royaume_nika_data,
        "cd_acces_royaume": cd_acces_royaume_data,
        "cd_nika_collect": cd_nika_collect_data,
        "cd_eveil_attaque": cd_eveil_attaque_data,
        "cd_eveil_subis": cd_eveil_subis_data,
        "cd_bourrasque": cd_bourrasque_data,
        "cd_bourrasque_subis": cd_bourrasque_subis_data,
        "cd_tonnerre_attaque": cd_tonnerre_attaque_data,
        "cd_tonnerre_subis": cd_tonnerre_subis_data,
        "cd_eveil_uo": cd_eveil_uo_data,
        "message_jour": message_jour_data,
        "cd_wobservation": cd_wobservation_data,
        "cd_observation": cd_observation_data
    }

    return combined_data

# --- Initialisation au démarrage ---
@bot.event
async def on_ready():
    print(f"{bot.user.name} est connecté.")
    bot.uptime = time.time()
    activity = discord.Activity(
        type=discord.ActivityType.streaming,
        name="Etherya",
        url="https://discord.com/oauth2/authorize?client_id=1356693934012891176"
    )
    await bot.change_presence(activity=activity, status=discord.Status.online)

    print(f"🎉 **{bot.user}** est maintenant connecté et affiche son activité de stream avec succès !")
    print("📌 Commandes disponibles 😊")
    for command in bot.commands:
        print(f"- {command.name}")

    try:
        synced = await bot.tree.sync()
        print(f"✅ Commandes slash synchronisées : {[cmd.name for cmd in synced]}")
    except Exception as e:
        print(f"❌ Erreur de synchronisation des commandes slash : {e}")


# --- Gestion globale des erreurs ---
@bot.event
async def on_error(event, *args, **kwargs):
    print(f"Une erreur s'est produite : {event}")
    embed = discord.Embed(
        title="❗ Erreur inattendue",
        description="Une erreur s'est produite lors de l'exécution de la commande. Veuillez réessayer plus tard.",
        color=discord.Color.red()
    )
    try:
        await args[0].response.send_message(embed=embed)
    except Exception:
        pass

#----------------------------------------------- ITEMS
ITEMS = [
    {
        "id": 8,
        "emoji": "<:infini:1363615903404785734>",
        "title": "Infini | ℕ𝕀𝕍𝔼𝔸𝕌 𝟙",
        "description": "L'infini protège des robs pendant 1h (utilisable 1 fois par items)",
        "price": 25000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 3,
        "tradeable": True,
        "usable": True,
        "use_effect": "L'infini protège des robs pendant 1h ",
        "requirements": {},
        "role_id": 1363939565336920084,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 66,
        "emoji": "<:exorciste:1363602480792994003>",
        "title": "Appel à un exorciste | 𝕊𝕆𝕀ℕ",
        "description": "Permet de retirer le nen que quelqu'un nous a posé grâce à un exorciste !",
        "price": 50000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 5,
        "tradeable": True,
        "usable": True,
        "use_effect": "Retire le rôle, faite !!heal",
        "requirements": {},
        "role_id": 1363873859912335400,
        "role_duration": 3600,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True,
        "remove_role_after_use": True
    },
    {
        "id": 88,
        "emoji": "<:infini:1363615925776941107>",
        "title": "Infini | ℕ𝕀𝕍𝔼𝔸𝕌 𝟚",
        "description": "L'infini protège des robs pendant 3h (utilisable 1 fois par items)",
        "price": 50000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 2,
        "tradeable": True,
        "usable": True,
        "use_effect": "L'infini protège des robs pendant 3h ",
        "requirements": {},
        "role_id": 1363939567627145660,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 763,
        "emoji": "<:BomuBomunoMi:1365056026784563261>",
        "title": "Bomu Bomu no Mi",
        "description": "Permet d'exploser 10% de la banque d’un joueur ciblé chaque semaine.",
        "price": 80000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 2,
        "tradeable": True,
        "usable": True,
        "use_effect": "Explose 10% de la banque d’un joueur ciblé. Faite !!bombe <@user> ",
        "blocked_roles": [1365316070172393572, 1365311588139274354, 1365313257279062067, 1365311602290851880, 1365313248269828116, 1365311608259346462, 1365313251201519697, 1365311611019202744, 1365311614332571739, 1365313292477927464],
        "requirements": {},
        "role_id": 1365316070172393572,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 203,
        "emoji": "<:tetsunomi:1365025648435003525>",
        "title": "Tetsu Tetsu no Mi",
        "description": "Réduit de 50% toutes les robs subies.",
        "price": 90000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 2,
        "tradeable": True,
        "usable": True,
        "use_effect": "Réduit de 50% toutes les robs subies.",
        "blocked_roles": [1365316070172393572, 1365311588139274354, 1365313257279062067, 1365311602290851880, 1365313248269828116, 1365311608259346462, 1365313251201519697, 1365311611019202744, 1365311614332571739, 1365313292477927464],
        "requirements": {},
        "role_id": 1365311588139274354,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 542,
        "emoji": "<:jokijokinomi:1365019733799338064>",
        "title": "Joki Joki no Mi",
        "description": "Crée une barrière bancaire : la première attaque de la journée est entièrement annulée. Se recharge automatiquement chaque jour a 00:00. ",
        "price": 100000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 2,
        "tradeable": True,
        "usable": True,
        "use_effect": "Crée une barrière bancaire : la première attaque de la journée est entièrement annulée. Se recharge automatiquement chaque jour a 00:00. ",
        "blocked_roles": [1365316070172393572, 1365311588139274354, 1365313257279062067, 1365311602290851880, 1365313248269828116, 1365311608259346462, 1365313251201519697, 1365311611019202744, 1365311614332571739, 1365313292477927464],
        "requirements": {},
        "role_id": 1365311602290851880,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 352,
        "emoji": "<:golgolnomi:1365018965646114890>",
        "title": "Gol Gol no Mi",
        "description": "Offre un collect de 10% de sa banque chaque semaine",
        "price": 100000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 2,
        "tradeable": True,
        "usable": True,
        "use_effect": "Offre un collect de 10% de sa banque chaque semaine",
        "blocked_roles": [1365316070172393572, 1365311588139274354, 1365313257279062067, 1365311602290851880, 1365313248269828116, 1365311608259346462, 1365313251201519697, 1365311611019202744, 1365311614332571739, 1365313292477927464],
        "requirements": {},
        "role_id": 1365313257279062067,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 81,
        "emoji": "<:armure:1363599057863311412>",
        "title": "Armure du Berserker",
        "description": "Offre à son utilisateur un anti-rob de 1h... (voir description complète)",
        "price": 100000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 3,
        "tradeable": True,
        "usable": True,
        "use_effect": "L'infini protège des robs pendant 1h",
        "requirements": {},
        "role_id": 1363821649002238142,
        "role_duration": 3600,
        "remove_after_purchase": {
            "roles": True,
            "items": False
        }
    },
    {
        "id": 31,
        "emoji": "<:demoncontrole:1363600359611695344>",
        "title": "Contrôle de démon",
        "description": "Donne accès a tous les équipements de contrôle des démons",
        "price": 100000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 3,
        "tradeable": True,
        "usable": True,
        "use_effect": "Donne accès a tous les équipements de contrôle des démons",
        "requirements": {},
        "role_id": 1363817629781069907,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 888,
        "emoji": "<:infini:1363615948090638490>",
        "title": "Infini | ℕ𝕀𝕍𝔼𝔸𝕌 𝟛",
        "description": "L'infini protège des robs pendant 6h (utilisable 1 fois par items)",
        "price": 100000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 1,
        "tradeable": True,
        "usable": True,
        "use_effect": "L'infini protège des robs pendant 3h",
        "requirements": {},
        "role_id": 1363939486844850388,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 91,
        "emoji": "<:oeildemoniaque:1363947226501484746>",
        "title": "Œil démoniaque",
        "description": "Permet de voir l'avenir grâce au pouvoir de Kishirika...",
        "price": 100000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 2,
        "tradeable": True,
        "usable": True,
        "use_effect": "Permet de visioner le prochain restock pendant 10 seconde",
        "requirements": {},
        "role_id": 1363949082653098094,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 553,
        "emoji": "<:haki_v1:1365669380083679252>",
        "title": "Haki de l’Armement | 𝕀𝕟𝕗𝕖𝕣𝕚𝕖𝕦𝕣",
        "description": "Offre un collect de 5,000, cooldown de 2 heures.",
        "price": 150000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 3,
        "tradeable": True,
        "usable": True,
        "use_effect": "Peut évoluer grâce à !!rayleigh. Vous devrez donner 100,000 à Rayleigh pour pouvoir débloquer la possibilité d'acheter le Haki de l'Armement avancé !",
        "requirements": {},
        "role_id": 1365698043684327424,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 652,
        "emoji": "<:haki_v2:1365669343685378160>",
        "title": "Haki de l’Armement | 𝔸𝕧𝕒𝕟𝕔𝕖",
        "description": "Offre un collect de 10,000, cooldown de 2 heures.",
        "price": 150000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 3,
        "tradeable": True,
        "usable": True,
        "use_effect": "???",
        "requirements": {
            "roles": [1365699319163785246]
        },
        "role_id": 1365389381246124084,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 555,
        "emoji": "<:observation_v1:1365671377595535431>",
        "title": "Haki de l’Observation | 𝕀𝕟𝕗𝕖𝕣𝕚𝕖𝕦𝕣",
        "description": "Permet de connaître l'heure du prochain restock grâce à !!observation. (Cooldown : 1 semaine)",
        "price": 150000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 3,
        "tradeable": True,
        "usable": True,
        "use_effect": "Peut évoluer grâce à !!rayleigh. Vous devrez donner 100k à Rayleigh pour débloquer la possibilité d'acheter le Haki de l'Observation avancé !",
        "requirements": {},
        "role_id": 1365698043684327424,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 653,
        "emoji": "<:observation_v2:1365669364979728554>",
        "title": "Haki de l’Observation | 𝔸𝕧𝕒𝕟𝕔𝕖",
        "description": "Permet de connaître l'heure et le contenu du prochain restock grâce à !!Wobservation. (Cooldown : 2 semaines)",
        "price": 150000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 3,
        "tradeable": True,
        "usable": True,
        "use_effect": "???",
        "requirements": {
            "roles": [1365699245377847448]
        },
        "role_id": 1365389687618928885,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 4,
        "emoji": "<:naturoermite:1363945371448905810>",
        "title": "Mode Ermite",
        "description": "Ce mode autrefois maîtrisé par Naruto lui même, il vous confère l’énergie de la nature. Grâce à cela, vous pourrez avoir plus d’ezryn !!!",
        "price": 150000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 2,
        "tradeable": True,
        "usable": True,
        "use_effect": "Vous donne un collect qui vous donne 5,000 <:ecoEther:1341862366249357374> toute les 2 heures",
        "requirements": {},
        "role_id": 1363948445282341135,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 7,
        "emoji": "<:licence:1363609202211422268>",
        "title": "Licence Hunter ",
        "description": "Donne accès a toutes les techniques De Hunter x Hunter, plus donne accès a un salon avec des quêtes",
        "price": 250000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 1,
        "tradeable": True,
        "usable": True,
        "use_effect": "Donne le rôle licence hunter et donne accès au nen et au quêtes destiné au hunter",
        "requirements": {},
        "role_id": 1363817603713339512,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 15,
        "emoji": "<:nen:1363607663010775300>",
        "title": "Nen | ℝ𝕆𝕃𝕃",
        "description": "Cet objet vous permet d’utiliser le Nen (attribué aléatoirement) à votre guise. Chaque technique repose sur un serment.\n— Renforcement : +renforcement donne un anti-rob de 24h (1 semaine de cooldown).\n— Émission : +emission @user maudit un joueur et lui inflige un collect de -20% (1 semaine de cooldown).\n— Manipulation : +manipulation accorde un collect de 1% toutes les 4h pendant 24h (cooldown : 1 semaine).\n— Matérialisation : +materialisation génère un objet aléatoire de la boutique (cooldown : 2 semaines).\n— Transformation : +transformation foudroie la banque d’un joueur, retirant 25% (cooldown : 2 semaines).\n— Spécialisation : donne accès à tout.",
        "price": 500000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 2,
        "tradeable": True,
        "usable": True,
        "use_effect": "Une fois le nen utilisé celui-ci vous attribue un nen aléatoirement avec la commande !!rollnen (avec 19.9% de chance pour chaque sauf la spécialisation qui est à 0.5%)",
        "requirements": {
            "items": [7]
        },
        "role_id": 1363928528587984998,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 22,
        "emoji": "<:imperiale:1363601099990241601>",
        "title": " Arme démoniaque impériale",
        "description": "Cette objet vous permet d'utiliser le démon dans votre arme et vous permet de voler votre adversaire",
        "price": 500000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 3,
        "tradeable": True,
        "usable": True,
        "use_effect": "Un /roll 50 devra être fait et vous permettra de voler le pourcentage de ce roll à l’utilisateur de votre choix à condition que celui-ci soit plus riche que vous ",
        "requirements": {
            "items": [31]
        },
        "role_id": 1363817586466361514,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 45,
        "emoji": "<:hakidesrois:1363623066667843616>",
        "title": "Haki des Rois",
        "description": "Apprenez le haki des rois comme les Empereurs des mers. Faites +haki <@user> pour le paralyser ainsi il n’aura pas accès aux salons économiques",
        "price": 500000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 2,
        "tradeable": True,
        "usable": True,
        "use_effect": "Donne accès a l'Haki des Rois",
        "requirements": {},
        "role_id": 1363817645249527879,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 28,
        "emoji": "<:rage:1363599799043227940>",
        "title": " Rage du Berserker",
        "description": "Tu perds tout contrôle. L’armure du Berserker te consume, et avec elle, ta dernière part d’humanité. Tu ne voles pas. Tu ne gagnes rien. Tu détruis, par pure haine. Ton seul objectif : voir l’ennemi ruiné.",
        "price": 500000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 2,
        "tradeable": True,
        "usable": True,
        "use_effect": "Utilisable une seule fois avec !!berserk <@user> → roll 100, % retiré à la banque de la cible (ex : roll 67 = -67%). Nécessite l’armure du Berserker. Cooldown de 7j après achat. Objet détruit après usage.",
        "requirements": {
            "items": [81]
        },
        "role_id": 1363821333624127618,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 23,
        "emoji": "<:pokeball:1363942456676061346>",
        "title": "Pokeball",
        "description": "Cet objet vous permet de voler un objet d’une personne au hasard",
        "price": 500000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 1,
        "tradeable": True,
        "usable": True,
        "use_effect": "Vous donne l'accès de voler un objet au hasard de l'inventaire d'un joueur",
        "requirements": {},
        "role_id": 1363942048075481379,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 34,
        "emoji": "<:nanashimura:1363942592156405830>",
        "title": "Float",
        "description": "Vous utilisez l’un des alters provenant du One for all, et plus précisément de Nana Shimura. En l’utilisant, vous pouvez voler aussi haut que personne ne peut y accéder.",
        "price": 500000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 2,
        "tradeable": True,
        "usable": True,
        "use_effect": "La commande +float vous donne accès au salon (nom du salon) durant 15min mais seulement possible 1/jour.",
        "requirements": {},
        "role_id": 1363946902730575953,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 99,
        "emoji": "<:ultrainstinct:1363601650123801027>",
        "title": "Ultra Instinct ",
        "description": "Vous utilisez la forme ultime du Ultra Instinct. Vous pouvez seulement l’utiliser pendant (mettre le temps d’immunité). Lorsque vous utilisez cette forme ultime, vous anticipez toutes attaques et vous l’esquivez (donc immunisé). Malheureusement cette forme utilise énormément de votre ki, il vous faudra donc 5 jours de repos pour réutiliser cette forme",
        "price": 750000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 1,
        "tradeable": True,
        "usable": True,
        "use_effect": "Donne accès a l'Ultra Instinct",
        "requirements": {},
        "role_id": 1363821033060307106,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 381,
        "emoji": "<:guraguranomi:1365020132048506991>",
        "title": "Gura Gura no Mi",
        "description": "Permet de créer des séismes dévastateurs à une échelle massive. Peut détruire des banques entières en faisant des secousses.",
        "price": 1000000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 1,
        "tradeable": True,
        "usable": True,
        "use_effect": "Créer des séismes dévastateurs à une échelle massive. Détruit des banques entières en faisant des secousses.",
        "blocked_roles": [1365316070172393572, 1365311588139274354, 1365313257279062067, 1365311602290851880, 1365313248269828116, 1365311608259346462, 1365313251201519697, 1365311611019202744, 1365311614332571739, 1365313292477927464],
        "requirements": {},
        "role_id": 1365313248269828116,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 666,
        "emoji": "<:MarshallDTeach:1365695681028821093>",
        "title": "Marshall D. Teach",
        "description": "Permet de posséder 2 Fruits du Démon a la fois.",
        "price": 1000000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 1,
        "tradeable": True,
        "usable": True,
        "use_effect": "Permet de posséder 2 Fruits du Démon a la fois.",
        "requirements": {},
        "role_id": 1365310665417556011,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 911,
        "emoji": "<:hiehienomi:1365020469547503698>",
        "title": "Hie Hie no Mi",
        "description": "Permet de geler le temps et les actions économiques des autres joueurs, le joueur ciblé n'a plus accès à l'économie",
        "price": 1800000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 1,
        "tradeable": True,
        "usable": True,
        "use_effect": "Permet de geler le temps et les actions économiques des autres joueurs, le joueur ciblé n'a plus accès à l'économie.",
        "blocked_roles": [1365316070172393572, 1365311588139274354, 1365313257279062067, 1365311602290851880, 1365313248269828116, 1365311608259346462, 1365313251201519697, 1365311611019202744, 1365311614332571739, 1365313292477927464],
        "requirements": {},
        "role_id": 1365311608259346462,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 797,
        "emoji": "<:yamiyaminomi:1365020675450081280>",
        "title": "Yami Yami no Mi",
        "description": "Absorbe tous les vols subis et les renvoie avec une puissance doublée (200%).\n-Bénéficie de 6 heures de protection. Rétablissement en 24h.",
        "price": 2500000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 1,
        "tradeable": True,
        "usable": True,
        "use_effect": "Absorbe les vols et les renvoie avec 200% de puissance. 6h de protection, 24h de cooldown.",
        "blocked_roles": [1365316070172393572, 1365311588139274354, 1365313257279062067, 1365311602290851880, 1365313248269828116, 1365311608259346462, 1365313251201519697, 1365311611019202744, 1365311614332571739, 1365313292477927464],
        "requirements": {},
        "role_id": 1365313251201519697,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 229,
        "emoji": "<:gomugomunomi:1365020813543215137>",
        "title": "Gomu Gomu no Mi",
        "description": "Permet de rendre ta banque extensible et malléable, quasiment indestructible. Tu peux l’étirer à volonté pour éviter toute perte.",
        "price": 3000000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 1,
        "tradeable": True,
        "usable": True,
        "use_effect": "Renvoie 150% des attaques bancaires, booste tes revenus de 5% (1 semaine) et bloque/renvoie 300% des attaques tout en doublant les revenus (24h).",
        "blocked_roles": [1365316070172393572, 1365311588139274354, 1365313257279062067, 1365311602290851880, 1365313248269828116, 1365311608259346462, 1365313251201519697, 1365311611019202744, 1365311614332571739, 1365313292477927464],
        "requirements": {},
        "role_id": 1365311611019202744,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 469,
        "emoji": "<:nikanikanomi:1365021787015876760>",
        "title": "Nika Nika no Mi",
        "description": "Le Fruit de Nika te confère des pouvoirs légendaires, au-delà de tout ce qui est imaginable, te permettant de réécrire les règles économiques et manipuler la réalité des finances à ta guise.",
        "price": 7000000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 1,
        "tradeable": True,
        "usable": True,
        "use_effect": "Le Nika Nika no Mi permet de créer des ressources, effacer dettes, et avec Gear Fifth, booste tes fonds de 500% et influe sur l'économie des autres.",
        "blocked_roles": [1365316070172393572, 1365311588139274354, 1365313257279062067, 1365311602290851880, 1365313248269828116, 1365311608259346462, 1365313251201519697, 1365311614332571739, 1365313292477927464],
        "requirements": {
            "roles": [1365311611019202744]
        },
        "role_id": 1365313292477927464,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 672,
        "emoji": "<:uouonomi:1365021938849677403>",
        "title": "Uo Uo no Mi, Modèle : Seiryu",
        "description": "Un fruit mythique qui permet à son utilisateur de se transformer en un dragon céleste, une créature d’une force inégalée, capable de manipuler les éléments et la destruction à une échelle dévastatrice. Ce fruit confère à son possesseur un pouvoir colossal, comparable à un typhon divin.",
        "price": 10000000,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 1,
        "tradeable": True,
        "usable": True,
        "use_effect": "Le **Uo Uo no Mi, Seiryu** transforme en dragon céleste, protège la banque (30% vol max) pendant 1 semaine, lance des flammes dévastatrices (vol de 75%) et invoque un orage réduisant les gains de 70% et renvoyant les attaques contre toi. *Colère Draconique* détruit l'économie d'un joueur une fois par mois.",
        "requirements": {},
        "blocked_roles": [1365316070172393572, 1365311588139274354, 1365313257279062067, 1365311602290851880, 1365313248269828116, 1365311608259346462, 1365313251201519697, 1365311611019202744, 1365311614332571739, 1365313292477927464],
        "role_id": 1365311614332571739,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": True
    },
    {
        "id": 202,
        "emoji": "<:bc1s1:1364217784439144488>",
        "title": "Boule de Cristal n°1",
        "description": "Une sphère mystérieuse et brillante, sans utilité apparente pour l'instant, mais qui semble receler un pouvoir caché en attente d'être découvert.",
        "price": 0,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 0,
        "tradeable": True,
        "usable": False,
        "use_effect": "???",
        "requirements": {},  # Aucun requirement
        "role_id": None,  # Aucun rôle à donner
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": False
    },
    {
        "id": 197,
        "emoji": "<:bc2s1:1364224502996930642>",
        "title": "Boule de Cristal n°2",
        "description": "Une sphère mystérieuse et brillante, sans utilité apparente pour l'instant, mais qui semble receler un pouvoir caché en attente d'être découvert.",
        "price": 0,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 0,
        "tradeable": True,
        "usable": False,
        "use_effect": "???",
        "requirements": {},  # Aucun requirement
        "role_id": None,  # Aucun rôle à donner
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": False
    },
    {
        "id": 425,
        "emoji": "<:bc3s1:1364224526476640306>",
        "title": "Boule de Cristal n°3",
        "description": "Une sphère mystérieuse et brillante, sans utilité apparente pour l'instant, mais qui semble receler un pouvoir caché en attente d'être découvert.",
        "price": 0,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 0,
        "tradeable": True,
        "usable": False,
        "use_effect": "???",
        "requirements": {},  # Aucun requirement
        "role_id": None,  # Aucun rôle à donner
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": False
    },
    {
        "id": 736,
        "emoji": "<:bc4s1:1364224543937396746>",
        "title": "Boule de Cristal n°4",
        "description": "Une sphère mystérieuse et brillante, sans utilité apparente pour l'instant, mais qui semble receler un pouvoir caché en attente d'être découvert.",
        "price": 0,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 0,
        "tradeable": True,
        "usable": False,
        "use_effect": "???",
        "requirements": {},  # Aucun requirement
        "role_id": None,  # Aucun rôle à donner
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": False
    },
    {
        "id": 872,
        "emoji": "<:bc5s1:1364224573306048522>",
        "title": "Boule de Cristal n°5",
        "description": "Une sphère mystérieuse et brillante, sans utilité apparente pour l'instant, mais qui semble receler un pouvoir caché en attente d'être découvert.",
        "price": 0,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 0,
        "tradeable": True,
        "usable": False,
        "use_effect": "???",
        "requirements": {},  # Aucun requirement
        "role_id": None,  # Aucun rôle à donner
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": False
    },
    {
        "id": 964,
        "emoji": "<:bc6s1:1364224591488221276>",
        "title": "Boule de Cristal n°6",
        "description": "Une sphère mystérieuse et brillante, sans utilité apparente pour l'instant, mais qui semble receler un pouvoir caché en attente d'être découvert.",
        "price": 0,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 0,
        "tradeable": True,
        "usable": False,
        "use_effect": "???",
        "requirements": {},  # Aucun requirement
        "role_id": None,  # Aucun rôle à donner
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": False
    },
    {
        "id": 987,
        "emoji": "<:bc7s1:1364224611536994315>",
        "title": "Boule de Cristal n°7",
        "description": "Une sphère mystérieuse et brillante, sans utilité apparente pour l'instant, mais qui semble receler un pouvoir caché en attente d'être découvert.",
        "price": 0,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 0,
        "tradeable": True,
        "usable": False,
        "use_effect": "???",
        "requirements": {},  # Aucun requirement
        "role_id": None,  # Aucun rôle à donner
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": False
    },
    {
        "id": 993,
        "emoji": "<:luffy:1367570815188729877>",
        "title": "Pièce Luffy",
        "description": "Une pièce  mystérieuse et brillante, sans utilité apparente pour l'instant, mais qui semble receler un pouvoir caché en attente d'être découvert.",
        "price": 0,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 0,
        "tradeable": True,
        "usable": False,
        "use_effect": "???",
        "requirements": {},  # Aucun requirement
        "role_id": None,  # Aucun rôle à donner
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": False
    },
    {
        "id": 221,
        "emoji": "<:zoro:1367570671244279912>",
        "title": "Pièce Zoro",
        "description": "Une pièce  mystérieuse et brillante, sans utilité apparente pour l'instant, mais qui semble receler un pouvoir caché en attente d'être découvert.",
        "price": 0,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 0,
        "tradeable": True,
        "usable": False,
        "use_effect": "???",
        "requirements": {},  # Aucun requirement
        "role_id": None,  # Aucun rôle à donner
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": False
    },
    {
        "id": 621,
        "emoji": "<:sanji:1367570434752778270>",
        "title": "Pièce Sanji",
        "description": "Une pièce  mystérieuse et brillante, sans utilité apparente pour l'instant, mais qui semble receler un pouvoir caché en attente d'être découvert.",
        "price": 0,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 0,
        "tradeable": True,
        "usable": False,
        "use_effect": "???",
        "requirements": {},  # Aucun requirement
        "role_id": None,  # Aucun rôle à donner
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": False
    },
    {
        "id": 413,
        "emoji": "<:nami:1367570885661429790>",
        "title": "Pièce Nami",
        "description": "Une pièce  mystérieuse et brillante, sans utilité apparente pour l'instant, mais qui semble receler un pouvoir caché en attente d'être découvert.",
        "price": 0,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 0,
        "tradeable": True,
        "usable": False,
        "use_effect": "???",
        "requirements": {},  # Aucun requirement
        "role_id": None,  # Aucun rôle à donner
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": False
    },
    {
        "id": 280,
        "emoji": "<:usopp:1367570730392223804>",
        "title": "Pièce Usopp",
        "description": "Une pièce  mystérieuse et brillante, sans utilité apparente pour l'instant, mais qui semble receler un pouvoir caché en attente d'être découvert.",
        "price": 0,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 0,
        "tradeable": True,
        "usable": False,
        "use_effect": "???",
        "requirements": {},  # Aucun requirement
        "role_id": None,  # Aucun rôle à donner
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": False
    },
    {
        "id": 682,
        "emoji": "<:chopper:1367570848549965935>",
        "title": "Pièce Chopper",
        "description": "Une pièce  mystérieuse et brillante, sans utilité apparente pour l'instant, mais qui semble receler un pouvoir caché en attente d'être découvert.",
        "price": 0,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 0,
        "tradeable": True,
        "usable": False,
        "use_effect": "???",
        "requirements": {},  # Aucun requirement
        "role_id": None,  # Aucun rôle à donner
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": False
    },
    {
        "id": 573,
        "emoji": "<:robin:1367570558581084231>",
        "title": "Pièce Robin",
        "description": "Une pièce  mystérieuse et brillante, sans utilité apparente pour l'instant, mais qui semble receler un pouvoir caché en attente d'être découvert.",
        "price": 0,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 0,
        "tradeable": True,
        "usable": False,
        "use_effect": "???",
        "requirements": {},  # Aucun requirement
        "role_id": None,  # Aucun rôle à donner
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": False
    },
    {
        "id": 132,
        "emoji": "<:franky:1367570517674033183>",
        "title": "Pièce Franky",
        "description": "Une pièce  mystérieuse et brillante, sans utilité apparente pour l'instant, mais qui semble receler un pouvoir caché en attente d'être découvert.",
        "price": 0,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 0,
        "tradeable": True,
        "usable": False,
        "use_effect": "???",
        "requirements": {},  # Aucun requirement
        "role_id": None,  # Aucun rôle à donner
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": False
    },
    {
        "id": 856,
        "emoji": "<:jinbe:1367570481720332448>",
        "title": "Pièce Jinbe",
        "description": "Une pièce  mystérieuse et brillante, sans utilité apparente pour l'instant, mais qui semble receler un pouvoir caché en attente d'être découvert.",
        "price": 0,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 0,
        "tradeable": True,
        "usable": False,
        "use_effect": "???",
        "requirements": {},  # Aucun requirement
        "role_id": None,  # Aucun rôle à donner
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": False
    },
    {
        "id": 869,
        "emoji": "<:brook:1367570627157954660>",
        "title": "Pièce Brook",
        "description": "Une pièce  mystérieuse et brillante, sans utilité apparente pour l'instant, mais qui semble receler un pouvoir caché en attente d'être découvert.",
        "price": 0,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 0,
        "tradeable": True,
        "usable": False,
        "use_effect": "???",
        "requirements": {},  # Aucun requirement
        "role_id": None,  # Aucun rôle à donner
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": False
    },
]

# Fonction pour insérer les items dans MongoDB
def insert_items_into_db():
    for item in ITEMS:
        if not collection16.find_one({"id": item["id"]}):
            collection16.insert_one(item)

def get_page_embed(page: int, items_per_page=10):
    start = page * items_per_page
    end = start + items_per_page
    items = ITEMS[start:end]

    embed = discord.Embed(title="🛒 Boutique", color=discord.Color.blue())

    for item in items:
        formatted_price = f"{item['price']:,}".replace(",", " ")
        name_line = f"ID: {item['id']} | {formatted_price} {item['emoji_price']} - {item['title']} {item['emoji']}"

        # Seulement la description, sans les "requirements" et "bonus"
        value = item["description"]

        embed.add_field(name=name_line, value=value, inline=False)

    total_pages = (len(ITEMS) - 1) // items_per_page + 1
    embed.set_footer(text=f"Page {page + 1}/{total_pages}")
    return embed

# Vue pour les boutons de navigation
class Paginator(discord.ui.View):
    def __init__(self, user: discord.User):
        super().__init__(timeout=60)
        self.page = 0
        self.user = user

    async def update(self, interaction: discord.Interaction):
        embed = get_page_embed(self.page)
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="◀️", style=discord.ButtonStyle.secondary)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.user:
            embed = discord.Embed(
                title="❌ Erreur",
                description="Tu n'as pas la permission de naviguer dans ce menu.",
                color=discord.Color.red()
            )
            return await interaction.response.edit_message(embed=embed, view=self)
        if self.page > 0:
            self.page -= 1
            await self.update(interaction)

    @discord.ui.button(label="▶️", style=discord.ButtonStyle.secondary)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.user:
            embed = discord.Embed(
                title="❌ Erreur",
                description="Tu n'as pas la permission de naviguer dans ce menu.",
                color=discord.Color.red()
            )
            return await interaction.response.edit_message(embed=embed, view=self)
        if (self.page + 1) * 10 < len(ITEMS):
            self.page += 1
            await self.update(interaction)

# Fonction de vérification des requirements (rôles et items)
async def check_requirements(user: discord.Member, requirements: dict):
    # Vérifier les rôles requis
    if "roles" in requirements:
        user_roles = [role.id for role in user.roles]
        for role_id in requirements["roles"]:
            if role_id not in user_roles:
                return False, f"Tu n'as pas le rôle requis <@&{role_id}>."

    # Vérifier les items requis (dans un système de base de données par exemple)
    if "items" in requirements:
        for item_id in requirements["items"]:
            item_in_inventory = await check_user_has_item(user, item_id)  # Fonction fictive à implémenter
            if not item_in_inventory:
                return False, f"Tu n'as pas l'item requis ID:{item_id}."

    return True, "Requirements vérifiés avec succès."

# Fonction d'achat d'un item
async def buy_item(user: discord.Member, item_id: int):
    # Chercher l'item dans la boutique
    item = next((i for i in ITEMS if i["id"] == item_id), None)
    if not item:
        return f"L'item avec l'ID {item_id} n'existe pas."

    # Vérifier les requirements
    success, message = await check_requirements(user, item["requirements"])
    if not success:
        return message

    # Vérifier si le rôle doit être ajouté ou supprimé après l'achat
    if item["remove_after_purchase"]["roles"]:
        role = discord.utils.get(user.guild.roles, id=item["role_id"])
        if role:
            await user.remove_roles(role)
            return f"Le rôle {role.name} a été supprimé après l'achat de {item['title']}."

    if item["remove_after_purchase"]["items"]:
        # Logique pour supprimer l'item (par exemple, de l'inventaire du joueur)
        pass

    return f"L'achat de {item['title']} a été effectué avec succès."

# Slash command /item-store
@bot.tree.command(name="item-store", description="Affiche la boutique d'items")
async def item_store(interaction: discord.Interaction):
    embed = get_page_embed(0)
    view = Paginator(user=interaction.user)
    await interaction.response.send_message(embed=embed, view=view)

# Appel de la fonction pour insérer les items dans la base de données lors du démarrage du bot
insert_items_into_db()

from discord import app_commands
from discord.ext import commands
import discord

async def item_autocomplete(interaction: discord.Interaction, current: str):
    # On filtre les items qui contiennent ce que l'utilisateur est en train d'écrire
    results = []
    for item in ITEMS:
        if current.lower() in item["title"].lower():
            results.append(app_commands.Choice(name=item["title"], value=item["title"]))

    # On limite à 25 résultats max (Discord ne permet pas plus)
    return results[:25]

# Commande d'achat avec recherche par nom d'item
@bot.tree.command(name="item-buy", description="Achète un item de la boutique via son nom.")
@app_commands.describe(item_name="Nom de l'item à acheter", quantity="Quantité à acheter (défaut: 1)")
@app_commands.autocomplete(item_name=item_autocomplete)  # Lier l'autocomplétion à l'argument item_name
async def item_buy(interaction: discord.Interaction, item_name: str, quantity: int = 1):
    user_id = interaction.user.id
    guild_id = interaction.guild.id

    # Chercher l'item en utilisant le nom récupéré via l'autocomplétion
    item = collection16.find_one({"title": item_name})
    if not item:
        embed = discord.Embed(
            title="<:classic_x_mark:1362711858829725729> Item introuvable",
            description="Aucun item avec ce nom n'a été trouvé dans la boutique.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed, ephemeral=True)

    if quantity <= 0:
        embed = discord.Embed(
            title="<:classic_x_mark:1362711858829725729> Quantité invalide",
            description="La quantité doit être supérieure à zéro.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed, ephemeral=True)

    if item.get("quantity", 0) < quantity:
        embed = discord.Embed(
            title="<:classic_x_mark:1362711858829725729> Stock insuffisant",
            description=f"Il ne reste que **{item.get('quantity', 0)}x** de cet item en stock.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed, ephemeral=True)

    # Vérifier les requirements avant de permettre l'achat
    valid, message = await check_requirements(interaction.user, item.get("requirements", {}))
    if not valid:
        embed = discord.Embed(
            title="<:classic_x_mark:1362711858829725729> Prérequis non remplis",
            description=message,
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed, ephemeral=True)

    user_data = collection.find_one({"user_id": user_id, "guild_id": guild_id}) or {"cash": 0}
    total_price = int(item["price"]) * quantity

    if user_data.get("cash", 0) < total_price:
        embed = discord.Embed(
            title="<:classic_x_mark:1362711858829725729> Fonds insuffisants",
            description=f"Tu n'as pas assez de <:ecoEther:1341862366249357374> pour cet achat.\nPrix total : **{total_price:,}**",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed, ephemeral=True)

    # Retirer l'argent du joueur
    collection.update_one(
        {"user_id": user_id, "guild_id": guild_id},
        {"$inc": {"cash": -total_price}},
        upsert=True
    )

    # Mise à jour de l'inventaire simple (collection7)
    inventory_data = collection7.find_one({"user_id": user_id, "guild_id": guild_id})
    if inventory_data:
        inventory = inventory_data.get("items", {})
        inventory[str(item["id"])] = inventory.get(str(item["id"]), 0) + quantity
        collection7.update_one(
            {"user_id": user_id, "guild_id": guild_id},
            {"$set": {"items": inventory}}
        )
    else:
        collection7.insert_one({
            "user_id": user_id,
            "guild_id": guild_id,
            "items": {str(item["id"]): quantity}
        })

    # Mise à jour de l'inventaire structuré (collection17)
    documents = [{
        "guild_id": guild_id,
        "user_id": user_id,
        "item_id": item["id"],
        "item_name": item["title"],
        "emoji": item.get("emoji"),
        "price": item["price"],
        "acquired_at": datetime.utcnow()
    } for _ in range(quantity)]
    if documents:
        collection17.insert_many(documents)

    # Mise à jour du stock boutique
    collection16.update_one(
        {"id": item["id"]},
        {"$inc": {"quantity": -quantity}}
    )

    # Gestion de la suppression des rôles et items après achat
    if item.get("remove_after_purchase"):
        remove_config = item["remove_after_purchase"]

        if remove_config.get("roles", False) and item.get("role_id"):
            role = discord.utils.get(interaction.guild.roles, id=item["role_id"])
            if role:
                await interaction.user.remove_roles(role)
                print(f"Rôle {role.name} supprimé pour {interaction.user.name} après l'achat.")

        if remove_config.get("items", False):
            inventory_data = collection7.find_one({"user_id": user_id, "guild_id": guild_id})
            if inventory_data:
                inventory = inventory_data.get("items", {})
                if str(item["id"]) in inventory:
                    inventory[str(item["id"])] -= quantity
                    if inventory[str(item["id"])] <= 0:
                        del inventory[str(item["id"])]
                    collection7.update_one(
                        {"user_id": user_id, "guild_id": guild_id},
                        {"$set": {"items": inventory}}
                    )
                    print(f"{quantity} de l'item {item['title']} supprimé de l'inventaire de {interaction.user.name}.")

    # Envoi du message de succès
    embed = discord.Embed(
        title="<:Check:1362710665663615147> Achat effectué",
        description=(
            f"Tu as acheté **{quantity}x {item['title']}** {item.get('emoji', '')} "
            f"pour **{total_price:,}** {item.get('emoji_price', '')} !"
        ),
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed)
    
@bot.tree.command(name="item-inventory", description="Affiche l'inventaire d'un utilisateur")
async def item_inventory(interaction: discord.Interaction, user: discord.User = None):
    user = user or interaction.user
    guild_id = interaction.guild.id

    # Curseur synchrone avec pymongo
    items_cursor = collection17.find({"guild_id": guild_id, "user_id": user.id})

    item_counts = {}
    item_details = {}

    for item in items_cursor:
        item_id = item["item_id"]
        item_counts[item_id] = item_counts.get(item_id, 0) + 1
        if item_id not in item_details:
            item_details[item_id] = {
                "title": item.get("item_name", "Nom inconnu"),
                "emoji": item.get("emoji", ""),
            }

    # Bleu doux (ex : #89CFF0)
    soft_blue = discord.Color.from_rgb(137, 207, 240)

    embed = discord.Embed(
        title="Use an item with the /item-use command.",
        color=soft_blue
    )

    embed.set_author(name=user.name, icon_url=user.avatar.url if user.avatar else user.default_avatar.url)

    if not item_counts:
        embed.title = "<:classic_x_mark:1362711858829725729> Inventaire vide"
        embed.description = "Use an item with the `/item-use` command."
        embed.color = discord.Color.red()
    else:
        lines = []
        for item_id, quantity in item_counts.items():
            details = item_details[item_id]
            lines.append(f"**{quantity}x** {details['title']} {details['emoji']} (ID: `{item_id}`)")
        embed.description = "\n".join(lines)

    await interaction.response.send_message(embed=embed)

from typing import List

async def item_autocomplete(interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
    results = []
    items = list(collection16.find().limit(100))  # Charger les 100 premiers items de la collection

    for item in items:
        title = item.get("title", "Sans nom")
        
        # On vérifie si l'input actuel de l'utilisateur est dans le nom de l'item
        if current.lower() in title.lower():
            results.append(app_commands.Choice(name=title, value=title))

    return results[:25]  # On limite à 25 résultats

@bot.tree.command(name="item-info", description="Affiche toutes les informations d'un item de la boutique")
@app_commands.describe(id="Nom de l'item à consulter")
@app_commands.autocomplete(id=item_autocomplete)  # <-- On associe l'autocomplétion ici
async def item_info(interaction: discord.Interaction, id: str):
    # On cherche l'item par le nom
    item = collection16.find_one({"title": id})

    if not item:
        embed = discord.Embed(
            title="❌ Item introuvable",
            description="Aucun item trouvé avec ce nom.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed, ephemeral=True)

    formatted_price = f"{item['price']:,}".replace(",", " ")

    embed = discord.Embed(
        title=f"📦 Détails de l'item : {item['title']}",
        color=discord.Color.blue()
    )
    embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)

    embed.add_field(name="**Nom de l'item**", value=item['title'], inline=False)
    embed.add_field(name="**Description**", value=item['description'], inline=False)
    embed.add_field(name="ID", value=str(item['id']), inline=True)
    embed.add_field(name="Prix", value=f"{formatted_price} {item['emoji_price']}", inline=True)
    embed.add_field(name="Quantité", value=str(item.get('quantity', 'Indisponible')), inline=True)

    tradeable = "✅ Oui" if item.get("tradeable", False) else "❌ Non"
    usable = "✅ Oui" if item.get("usable", False) else "❌ Non"
    embed.add_field(name="Échangeable", value=tradeable, inline=True)
    embed.add_field(name="Utilisable", value=usable, inline=True)

    if item.get("use_effect"):
        embed.add_field(name="Effet à l'utilisation", value=item["use_effect"], inline=False)

    if item.get("requirements"):
        requirements = item["requirements"]
        req_message = []

        if "roles" in requirements:
            for role_id in requirements["roles"]:
                role = discord.utils.get(interaction.guild.roles, id=role_id)
                if role:
                    req_message.append(f"• Rôle requis : <@&{role_id}> ({role.name})")
                else:
                    req_message.append(f"• Rôle requis : <@&{role_id}> (Introuvable)")

        if "items" in requirements:
            for required_item_id in requirements["items"]:
                item_in_inventory = await check_user_has_item(interaction.user, required_item_id)
                if item_in_inventory:
                    req_message.append(f"• Item requis : ID {required_item_id} (Possédé)")
                else:
                    req_message.append(f"• Item requis : ID {required_item_id} (Non possédé)")

        embed.add_field(
            name="Prérequis",
            value="\n".join(req_message) if req_message else "Aucun prérequis",
            inline=False
        )
    else:
        embed.add_field(name="Prérequis", value="Aucun prérequis", inline=False)

    emoji = item.get("emoji")
    if emoji:
        try:
            emoji_id = emoji.split(":")[2].split(">")[0]
            embed.set_thumbnail(url=f"https://cdn.discordapp.com/emojis/{emoji_id}.png")
        except Exception as e:
            print(f"Erreur lors de l'extraction de l'emoji : {e}")

    embed.set_footer(text="🛒 Etherya • Détails de l'item")

    await interaction.response.send_message(embed=embed)

from typing import List

async def item_autocomplete(interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
    user = interaction.user
    user_id = user.id
    guild_id = interaction.guild.id

    # Chercher les items dans l'inventaire de l'utilisateur
    owned_items = collection17.find({"user_id": user_id, "guild_id": guild_id})
    
    results = []
    
    for owned_item in owned_items:
        item_id = owned_item["item_id"]
        item_data = collection16.find_one({"id": item_id})
        
        if item_data and current.lower() in item_data["title"].lower():
            results.append(app_commands.Choice(name=item_data["title"], value=str(item_id)))
    
    return results[:25]  # Limiter à 25 résultats

@bot.tree.command(name="item-use", description="Utilise un item de ton inventaire.")
@app_commands.describe(item_id="Nom de l'item à utiliser")
@app_commands.autocomplete(item_id=item_autocomplete)  # <-- On ajoute l'autocomplétion ici
async def item_use(interaction: discord.Interaction, item_id: int):
    user = interaction.user
    user_id = user.id
    guild = interaction.guild
    guild_id = guild.id

    # Vérifie si l'item est dans l'inventaire
    owned_item = collection17.find_one({"user_id": user_id, "guild_id": guild_id, "item_id": item_id})
    if not owned_item:
        embed = discord.Embed(
            title="<:classic_x_mark:1362711858829725729> Item non possédé",
            description="Tu ne possèdes pas cet item dans ton inventaire.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed)

    # Récupère les infos de l'item
    item_data = collection16.find_one({"id": item_id})
    if not item_data or not item_data.get("usable", False):
        embed = discord.Embed(
            title="<:classic_x_mark:1362711858829725729> Utilisation impossible",
            description="Cet item n'existe pas ou ne peut pas être utilisé.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed)

    # Vérifier si l'utilisateur a le rôle spécifique qui permet d'utiliser des items malgré les rôles bloquants
    special_role_id = 1365310665417556011
    if special_role_id in [role.id for role in user.roles]:
        embed = discord.Embed(
            title=f"<:Check:1362710665663615147> Utilisation de l'item",
            description=f"Tu as utilisé **{item_data['title']}** {item_data.get('emoji', '')}, malgré les restrictions de rôle.",
            color=discord.Color.green()
        )
        return await interaction.response.send_message(embed=embed)

    # Vérification des rôles bloquants
# Vérification des rôles bloquants
if item_data.get("blocked_roles"):
    blocked_roles = item_data["blocked_roles"]
    
    # Compter combien de rôles bloquants l'utilisateur possède
    user_blocked_roles = [role for role in user.roles if role.id in blocked_roles]
    
    # Vérification si l'utilisateur a le rôle spécial qui permet de dépasser la limite
    special_role_id = 1365310665417556011
    limit = 1  # Limite par défaut si l'utilisateur n'a pas le rôle spécial
    
    if special_role_id in [role.id for role in user.roles]:
        limit = 2  # Si l'utilisateur a le rôle spécial, on augmente la limite à 2

    # Si l'utilisateur a trop de rôles bloquants (>= limite), on bloque l'utilisation
    if len(user_blocked_roles) >= limit:
        embed = discord.Embed(
            title="<:classic_x_mark:1362711858829725729> Utilisation bloquée",
            description="Tu ne peux pas utiliser cet item en raison de tes rôles bloquants.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed)

    # Si aucun rôle ne bloque, continuer normalement (comme dans ton code actuel)
    # Supprime un exemplaire dans l'inventaire
    collection17.delete_one({
        "user_id": user_id,
        "guild_id": guild_id,
        "item_id": item_id
    })

    embed = discord.Embed(
        title=f"<:Check:1362710665663615147> Utilisation de l'item",
        description=f"Tu as utilisé **{item_data['title']}** {item_data.get('emoji', '')}.",
        color=discord.Color.green()
    )

    # Ajout du rôle si défini
    role_id = item_data.get("role_id")
    if role_id:
        role = guild.get_role(int(role_id))
        if role:
            # Vérification de la hiérarchie des rôles
            if interaction.guild.me.top_role.position > role.position:
                try:
                    await user.add_roles(role)
                    embed.add_field(name="🎭 Rôle attribué", value=f"Tu as reçu le rôle **{role.name}**.", inline=False)
                except discord.Forbidden:
                    embed.add_field(
                        name="⚠️ Rôle non attribué",
                        value="Je n’ai pas la permission d’attribuer ce rôle. Vérifie mes permissions ou la hiérarchie des rôles.",
                        inline=False
                    )
            else:
                embed.add_field(
                    name="⚠️ Rôle non attribué",
                    value="Le rôle est trop élevé dans la hiérarchie pour que je puisse l’attribuer.",
                    inline=False
                )

    # Ajout d'un item bonus s'il y en a
    reward_item_id = item_data.get("gives_item_id")
    if reward_item_id:
        collection17.insert_one({
            "user_id": user_id,
            "guild_id": guild_id,
            "item_id": reward_item_id
        })
        reward_data = collection16.find_one({"id": reward_item_id})
        if reward_data:
            reward_title = reward_data["title"]
            reward_emoji = reward_data.get("emoji", "")
            embed.add_field(name="🎁 Récompense reçue", value=f"Tu as reçu **{reward_title}** {reward_emoji}.", inline=False)

    # Gestion de la suppression après utilisation
    if item_data.get("remove_after_use"):
        if item_data["remove_after_use"].get("roles", False):
            role = discord.utils.get(interaction.guild.roles, id=item_data["role_id"])
            if role and role in user.roles:
                await user.remove_roles(role)
                embed.add_field(name="⚠️ Rôle supprimé", value=f"Le rôle **{role.name}** a été supprimé après l'utilisation de l'item.", inline=False)
                print(f"Rôle {role.name} supprimé pour {interaction.user.name} après l'utilisation de l'item.")
        
        if item_data["remove_after_use"].get("items", False):
            collection17.delete_one({
                "user_id": user_id,
                "guild_id": guild_id,
                "item_id": item_id
            })
            print(f"Item ID {item_id} supprimé de l'inventaire de {interaction.user.name}.")

    await interaction.response.send_message(embed=embed)


from discord.app_commands import Choice, autocomplete

# Fonction d'autocomplétion pour l'ID des items
async def item_autocomplete(interaction: discord.Interaction, current: str):
    results = []
    # Recherche parmi les items dans la collection
    items = collection16.find()
    
    # Ajoute les items dont le nom correspond à ce que l'utilisateur tape
    for item in items:
        if current.lower() in item["title"].lower():
            results.append(Choice(name=f"{item['title']} (ID: {item['id']})", value=item['id']))
    
    return results[:25]  # Limite à 25 résultats maximum

@bot.tree.command(name="item-give", description="(Admin) Donne un item à un utilisateur.")
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(
    member="Utilisateur à qui donner l'item",
    item_id="ID de l'item à donner",
    quantity="Quantité d'items à donner"
)
@app_commands.autocomplete(item_id=item_autocomplete)  # Ajout de l'autocomplétion pour item_id
async def item_give(interaction: discord.Interaction, member: discord.Member, item_id: int, quantity: int = 1):
    guild_id = interaction.guild.id
    user_id = member.id

    # Vérifie si l'item existe dans la boutique
    item_data = collection16.find_one({"id": item_id})
    if not item_data:
        embed = discord.Embed(
            title="<:classic_x_mark:1362711858829725729> Item introuvable",
            description="Cet item n'existe pas dans la boutique.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed)

    if quantity < 1:
        embed = discord.Embed(
            title="<:classic_x_mark:1362711858829725729> Quantité invalide",
            description="La quantité doit être d'au moins **1**.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed)

    # Ajoute l'item dans la collection17 (inventaire structuré)
    for _ in range(quantity):
        collection17.insert_one({
            "user_id": user_id,
            "guild_id": guild_id,
            "item_id": item_id,
            "item_name": item_data["title"],
            "emoji": item_data.get("emoji", ""),
            "price": item_data.get("price"),
            "acquired_at": datetime.utcnow()
        })

    item_name = item_data["title"]
    emoji = item_data.get("emoji", "")

    embed = discord.Embed(
        title=f"<:Check:1362710665663615147> Item donné",
        description=f"**{quantity}x {item_name}** {emoji} ont été donnés à {member.mention}.",
        color=discord.Color.green()
    )

    await interaction.response.send_message(embed=embed)

# Fonction d'autocomplétion pour l'ID des items
async def item_autocomplete(interaction: discord.Interaction, current: str):
    results = []
    # Recherche parmi les items dans la collection
    items = collection16.find()
    
    # Ajoute les items dont le nom correspond à ce que l'utilisateur tape
    for item in items:
        if current.lower() in item["title"].lower():
            results.append(Choice(name=f"{item['title']} (ID: {item['id']})", value=item['id']))
    
    return results[:25]  # Limite à 25 résultats maximum

@bot.tree.command(name="item-take", description="(Admin) Retire un item d'un utilisateur.")
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(
    member="Utilisateur à qui retirer l'item",
    item_id="ID de l'item à retirer",
    quantity="Quantité d'items à retirer"
)
@app_commands.autocomplete(item_id=item_autocomplete)  # Ajout de l'autocomplétion pour item_id
async def item_take(interaction: discord.Interaction, member: discord.Member, item_id: int, quantity: int = 1):
    guild_id = interaction.guild.id
    user_id = member.id

    # Vérifie si l'item existe
    item_data = collection16.find_one({"id": item_id})
    if not item_data:
        embed = discord.Embed(
            title="<:classic_x_mark:1362711858829725729> Item introuvable",
            description="Cet item n'existe pas dans la boutique.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed)

    item_name = item_data["title"]
    emoji = item_data.get("emoji", "")

    # Vérifie combien l'utilisateur en possède
    owned_count = collection17.count_documents({
        "user_id": user_id,
        "guild_id": guild_id,
        "item_id": item_id
    })

    if owned_count < quantity:
        embed = discord.Embed(
            title="<:classic_x_mark:1362711858829725729> Quantité insuffisante",
            description=f"{member.mention} ne possède que **{owned_count}x {item_name}** {emoji}. Impossible de retirer {quantity}.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed)

    # Supprime les exemplaires un par un
    for _ in range(quantity):
        collection17.delete_one({
            "user_id": user_id,
            "guild_id": guild_id,
            "item_id": item_id
        })

    embed = discord.Embed(
        title="<:Check:1362710665663615147> Item retiré",
        description=f"**{quantity}x {item_name}** {emoji} ont été retirés de l'inventaire de {member.mention}.",
        color=discord.Color.green()
    )

    await interaction.response.send_message(embed=embed)

# Fonction d'autocomplétion pour l'ID des items, filtrée par l'inventaire de l'utilisateur
async def item_autocomplete(interaction: discord.Interaction, current: str):
    results = []
    guild_id = interaction.guild.id
    user_id = interaction.user.id

    # Recherche des items que le joueur possède dans son inventaire
    owned_items = collection17.find({"user_id": user_id, "guild_id": guild_id})

    # Ajoute les items dont le nom correspond à ce que l'utilisateur tape
    for item in owned_items:
        item_data = collection16.find_one({"id": item["item_id"]})
        if item_data and current.lower() in item_data["title"].lower():
            results.append(Choice(name=f"{item_data['title']} (ID: {item_data['id']})", value=item_data['id']))
    
    return results[:25]  # Limite à 25 résultats maximum

@bot.tree.command(name="item-sell", description="Vends un item à un autre utilisateur pour un prix donné.")
@app_commands.describe(
    member="L'utilisateur à qui vendre l'item",
    item_id="ID de l'item à vendre",
    price="Prix de vente de l'item",
    quantity="Quantité d'items à vendre (par défaut 1)"
)
@app_commands.autocomplete(item_id=item_autocomplete)  # Ajout de l'autocomplétion pour item_id
async def item_sell(interaction: discord.Interaction, member: discord.User, item_id: int, price: int, quantity: int = 1):
    guild_id = interaction.guild.id
    seller_id = interaction.user.id
    buyer_id = member.id

    item_data = collection16.find_one({"id": item_id})
    if not item_data:
        embed = discord.Embed(
            title="<:classic_x_mark:1362711858829725729> Item introuvable",
            description="Cet item n'existe pas dans la boutique.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed)

    item_name = item_data["title"]
    emoji = item_data.get("emoji", "")

    owned_count = collection17.count_documents({
        "user_id": seller_id,
        "guild_id": guild_id,
        "item_id": item_id
    })

    if owned_count < quantity:
        embed = discord.Embed(
            title="<:classic_x_mark:1362711858829725729> Vente impossible",
            description=f"Tu ne possèdes que **{owned_count}x {item_name}** {emoji}.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed)

    buyer_data = collection.find_one({"guild_id": guild_id, "user_id": buyer_id}) or {"cash": 1500}
    total_price = price * quantity

    # Vérification du cash uniquement
    if buyer_data.get("cash", 0) < total_price:
        embed = discord.Embed(
            title="<:classic_x_mark:1362711858829725729> Fonds insuffisants",
            description=f"{member.mention} n'a pas assez d'argent en **cash** pour acheter **{quantity}x {item_name}** {emoji}.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed)

    # Boutons
    class SellView(View):
        def __init__(self):
            super().__init__(timeout=60)

        @discord.ui.button(label="✅ Accepter", style=discord.ButtonStyle.green)
        async def accept_sell(self, interaction_btn: discord.Interaction, button: Button):
            if interaction_btn.user.id != buyer_id:
                return await interaction_btn.response.send_message("❌ Ce n'est pas ton offre.", ephemeral=True)

            # Transfert de l'item
            for _ in range(quantity):
                collection17.insert_one({
                    "user_id": buyer_id,
                    "guild_id": guild_id,
                    "item_id": item_id,
                    "item_name": item_name,
                    "emoji": emoji,
                    "price": price,
                    "acquired_at": datetime.utcnow()
                })
                collection17.delete_one({
                    "user_id": seller_id,
                    "guild_id": guild_id,
                    "item_id": item_id
                })

            # Paiement
            collection.update_one(
                {"guild_id": guild_id, "user_id": buyer_id},
                {"$inc": {"cash": -total_price}},  # Décrémentation du cash de l'acheteur
                upsert=True
            )
            collection.update_one(
                {"guild_id": guild_id, "user_id": seller_id},
                {"$inc": {"cash": total_price}},  # Ajout du cash au vendeur
                upsert=True
            )

            confirm_embed = discord.Embed(
                title="<:Check:1362710665663615147> Vente conclue",
                description=f"{member.mention} a acheté **{quantity}x {item_name}** {emoji} pour **{total_price:,}** <:ecoEther:1341862366249357374>.",
                color=discord.Color.green()
            )
            await interaction_btn.response.edit_message(embed=confirm_embed, view=None)

        @discord.ui.button(label="❌ Refuser", style=discord.ButtonStyle.red)
        async def decline_sell(self, interaction_btn: discord.Interaction, button: Button):
            if interaction_btn.user.id != buyer_id:
                return await interaction_btn.response.send_message("❌ Ce n'est pas ton offre.", ephemeral=True)

            cancel_embed = discord.Embed(
                title="<:classic_x_mark:1362711858829725729> Offre refusée",
                description=f"{member.mention} a refusé l'offre.",
                color=discord.Color.red()
            )
            await interaction_btn.response.edit_message(embed=cancel_embed, view=None)

    view = SellView()

    offer_embed = discord.Embed(
        title=f"💸 Offre de {interaction.user.display_name}",
        description=f"{interaction.user.mention} te propose **{quantity}x {item_name}** {emoji} pour **{total_price:,}** <:ecoEther:1341862366249357374>.",
        color=discord.Color.gold()
    )
    offer_embed.set_footer(text="Tu as 60 secondes pour accepter ou refuser.")

    await interaction.response.send_message(embed=offer_embed, content=member.mention, view=view)

# Fonction d'autocomplétion pour les items disponibles en boutique
async def item_shop_autocomplete(interaction: discord.Interaction, current: str):
    results = []
    # Cherche tous les items de la boutique qui correspondent à ce que tape l'utilisateur
    items = collection16.find({"title": {"$regex": current, "$options": "i"}}).limit(25)

    for item in items:
        results.append(Choice(name=f"{item['title']} (ID: {item['id']})", value=item['id']))

    return results

@bot.tree.command(name="item-leaderboard", description="Affiche le leaderboard des utilisateurs possédant un item spécifique.")
@app_commands.describe(
    item_id="ID de l'item dont vous voulez voir le leaderboard"
)
@app_commands.autocomplete(item_id=item_shop_autocomplete)  # <<<<<< ajoute ici l'autocomplete
async def item_leaderboard(interaction: discord.Interaction, item_id: int):
    guild = interaction.guild
    guild_id = guild.id

    item_data = collection16.find_one({"id": item_id})
    if not item_data:
        embed = discord.Embed(
            title="<:classic_x_mark:1362711858829725729> Item introuvable",
            description="Aucun item n'existe avec cet ID.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed)

    item_name = item_data["title"]
    item_emoji = item_data.get("emoji", "")

    # Agrégation des quantités par utilisateur
    pipeline = [
        {"$match": {"guild_id": guild_id, "item_id": item_id}},
        {"$group": {"_id": "$user_id", "quantity": {"$sum": 1}}},
        {"$sort": {"quantity": -1}},
        {"$limit": 10}
    ]
    leaderboard = list(collection17.aggregate(pipeline))

    if not leaderboard:
        embed = discord.Embed(
            title="📉 Aucun résultat",
            description=f"Aucun utilisateur ne possède **{item_name}** {item_emoji} dans ce serveur.",
            color=discord.Color.dark_grey()
        )
        return await interaction.response.send_message(embed=embed)

    embed = discord.Embed(
        title=f"🏆 Leaderboard : {item_name} {item_emoji}",
        description="Classement des membres qui possèdent le plus cet item :",
        color=discord.Color.blurple()
    )

    for i, entry in enumerate(leaderboard, start=1):
        user = guild.get_member(entry["_id"])
        name = user.display_name if user else f"<Utilisateur inconnu `{entry['_id']}`>"
        embed.add_field(
            name=f"{i}. {name}",
            value=f"{entry['quantity']}x {item_name} {item_emoji}",
            inline=False
        )

    await interaction.response.send_message(embed=embed)

# Fonction d'autocomplétion pour les items de la boutique (déjà faite, donc on réutilise !)
async def item_shop_autocomplete(interaction: discord.Interaction, current: str):
    results = []
    items = collection16.find({"title": {"$regex": current, "$options": "i"}}).limit(25)

    for item in items:
        results.append(Choice(name=f"{item['title']} (ID: {item['id']})", value=item['id']))

    return results

@bot.tree.command(name="restock", description="Restock un item dans la boutique")
@app_commands.describe(
    item_id="ID de l'item à restock",
    quantity="Nouvelle quantité à définir"
)
@app_commands.autocomplete(item_id=item_shop_autocomplete)  # <<<< ajoute ici l'autocomplete
async def restock(interaction: discord.Interaction, item_id: int, quantity: int):
    if interaction.user.id != ISEY_ID:
        return await interaction.response.send_message("❌ Tu n'as pas la permission d'utiliser cette commande.", ephemeral=True)

    item = collection16.find_one({"id": item_id})
    if not item:
        return await interaction.response.send_message(f"❌ Aucun item trouvé avec l'ID {item_id}.", ephemeral=True)

    collection16.update_one({"id": item_id}, {"$set": {"quantity": quantity}})
    return await interaction.response.send_message(
        f"✅ L'item **{item['title']}** a bien été restocké à **{quantity}** unités.", ephemeral=True
    )


# Même autocomplétion que pour /restock (items de la boutique)
async def item_shop_autocomplete(interaction: discord.Interaction, current: str):
    results = []
    items = collection16.find({"title": {"$regex": current, "$options": "i"}}).limit(25)

    for item in items:
        results.append(app_commands.Choice(name=f"{item['title']} (ID: {item['id']})", value=item['id']))

    return results

@bot.tree.command(name="reset-item", description="Supprime tous les items de la boutique")
async def reset_item(interaction: discord.Interaction):
    if interaction.user.id != ISEY_ID:
        return await interaction.response.send_message("❌ Tu n'as pas la permission d'utiliser cette commande.", ephemeral=True)

    deleted = collection16.delete_many({})  # Supprime tous les documents de la collection

    return await interaction.response.send_message(
        f"🗑️ {deleted.deleted_count} item(s) ont été supprimés de la boutique.", ephemeral=True
    )

@bot.tree.command(name="delete-item", description="Supprime un item spécifique de la boutique")
@app_commands.describe(item_id="L'identifiant de l'item à supprimer")
async def delete_item(interaction: discord.Interaction, item_id: str):
    if interaction.user.id != ISEY_ID:
        return await interaction.response.send_message("❌ Tu n'as pas la permission d'utiliser cette commande.", ephemeral=True)

    result = collection16.delete_one({"id": item_id})

    if result.deleted_count == 0:
        return await interaction.response.send_message("❌ Aucun item trouvé avec cet ID.", ephemeral=True)

    return await interaction.response.send_message(f"🗑️ L'item avec l'ID `{item_id}` a été supprimé de la boutique.", ephemeral=True)

#-------------------------------------------------------- Badges

BADGES = [
    {
        "id": 1,
        "emoji": "<:hxh:1363923320256463088>",
        "title": "Badge Hunter X Hunter",
        "description": "Badge Collector.",
        "price": 100,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 10,
        "tradeable": True,
        "usable": False,
        "use_effect": "???",
        "requirements": {},
        "role_id": None,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": False
    },
    {
        "id": 2,
        "emoji": "<:gon:1363923253134889082>",
        "title": "Badge Gon",
        "description": "Badge Collector",
        "price": 150,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 5,
        "tradeable": True,
        "usable": False,
        "use_effect": "???",
        "requirements": {},
        "role_id": None,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": False
    },
    {
        "id": 3,
        "emoji": "<:onepiece:1364713455981957260>",
        "title": "Badge One Piece",
        "description": "Badge Collector.",
        "price": 200,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 3,
        "tradeable": True,
        "usable": False,
        "use_effect": "???",
        "requirements": {},
        "role_id": None,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": False
    },
    {
        "id": 4,
        "emoji": "<:luffy:1364713438768533585>",
        "title": "Badge Luffy",
        "description": "Badge Collector.",
        "price": 250,
        "emoji_price": "<:ecoEther:1341862366249357374>",
        "quantity": 2,
        "tradeable": True,
        "usable": False,
        "use_effect": "???",
        "requirements": {},
        "role_id": None,
        "remove_after_purchase": {
            "roles": False,
            "items": False
        },
        "used": False
    },
]

# Fonction pour obtenir les badges dans un format de page avec pagination
def get_badge_embed(page: int = 0, items_per_page=10):
    start = page * items_per_page
    end = start + items_per_page
    badges_page = BADGES[start:end]

    embed = discord.Embed(title="🛒 Boutique de Badges", color=discord.Color.purple())

    for badge in badges_page:
        formatted_price = f"{badge['price']:,}".replace(",", " ")
        name_line = f"ID: {badge['id']} | {formatted_price} {badge['emoji_price']} - {badge['title']} {badge['emoji']}"

        # Seulement la description, sans les "requirements" et "bonus"
        value = badge["description"]

        embed.add_field(name=name_line, value=value, inline=False)

    total_pages = (len(BADGES) - 1) // items_per_page + 1
    embed.set_footer(text=f"Page {page + 1}/{total_pages}")
    return embed

# Vue pour les boutons de navigation
class BadgePaginator(discord.ui.View):
    def __init__(self, user):
        super().__init__(timeout=60)
        self.page = 0
        self.user = user

    async def update(self, interaction):
        embed = get_badge_embed(self.page)
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="◀️", style=discord.ButtonStyle.secondary)
    async def prev(self, interaction, button):
        if interaction.user.id != self.user.id:
            return await interaction.response.send_message("❌ Tu ne peux pas utiliser ces boutons.", ephemeral=True)
        if self.page > 0:
            self.page -= 1
            await self.update(interaction)

    @discord.ui.button(label="▶️", style=discord.ButtonStyle.secondary)
    async def next(self, interaction, button):
        if interaction.user.id != self.user.id:
            return await interaction.response.send_message("❌ Tu ne peux pas utiliser ces boutons.", ephemeral=True)
        if (self.page + 1) * 10 < len(BADGES):
            self.page += 1
            await self.update(interaction)

# Commande pour afficher la boutique de badges
@bot.tree.command(name="badge-store", description="Affiche la boutique de badges")
async def badge_store(interaction: discord.Interaction):
    view = BadgePaginator(interaction.user)
    embed = get_badge_embed(0)  # Initial page (0)
    await interaction.channel.send(embed=embed, view=view)  # Envoi à tout le monde dans le canal

# Fonction pour insérer les badges dans la base de données lors du démarrage du bot
def insert_badge_into_db():
    for badge in BADGES:
        if not collection19.find_one({"id": badge["id"]}):
            collection19.insert_one(badge)

# Appel de la fonction pour insérer les badges dans la base de données lors du démarrage du bot
insert_badge_into_db()

from discord import app_commands

@app_commands.autocomplete(badge_id=True)
async def badge_autocomplete_by_name(interaction: discord.Interaction, current: str):
    results = collection19.find(
        {"title": {"$regex": f"^{current}", "$options": "i"}}
    ).limit(20)

    choices = []
    for badge in results:
        title = badge.get("title", "Sans titre")
        emoji = badge.get("emoji", "")
        badge_id = badge["id"]
        # Le name est affiché, le value est ce qui sera envoyé à la commande
        choices.append(app_commands.Choice(name=f"{title} {emoji} (ID: {badge_id})", value=badge_id))

    return choices

@bot.tree.command(name="badge-give", description="(Admin) Donne un badge à un utilisateur.")
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(
    member="Utilisateur à qui donner le badge",
    badge_id="Badge à donner (autocomplete par nom)"
)
@app_commands.autocomplete(badge_id=badge_autocomplete_by_name)
async def badge_give(interaction: discord.Interaction, member: discord.Member, badge_id: int):
    badge = collection19.find_one({"id": badge_id})
    if not badge:
        embed = discord.Embed(
            title="❌ Badge introuvable",
            description="Ce badge n'existe pas.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed)

    user_data = collection20.find_one({"user_id": member.id})
    if user_data and badge_id in user_data.get("badges", []):
        embed = discord.Embed(
            title="❌ Badge déjà possédé",
            description=f"{member.mention} possède déjà ce badge.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed)

    collection20.update_one(
        {"user_id": member.id},
        {"$addToSet": {"badges": badge_id}},
        upsert=True
    )

    embed = discord.Embed(
        title="🎖️ Badge donné",
        description=f"Le badge **{badge['title']}** {badge['emoji']} a été donné à {member.mention}.",
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="badge-inventory", description="Affiche les badges de l'inventaire d'un utilisateur.")
async def badge_inventory(interaction: discord.Interaction):
    # Récupérer les données de l'utilisateur
    user_data = collection20.find_one({"user_id": interaction.user.id})
    
    if not user_data or not user_data.get("badges"):
        embed = discord.Embed(
            title="❌ Aucun badge trouvé",
            description="Tu ne possèdes aucun badge.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed)

    # Récupérer les badges de l'utilisateur
    badge_ids = user_data["badges"]
    badges = collection19.find({"id": {"$in": badge_ids}})

    embed = discord.Embed(title=f"Inventaire de Badges de {interaction.user.display_name}", color=discord.Color.blue())

    if badges:
        for badge in badges:
            embed.add_field(
                name=f"{badge['emoji']} {badge['title']}",
                value=f"{badge['description']}\nPrix: {badge['price']} {badge['emoji_price']}",
                inline=False
            )
    else:
        embed.add_field(
            name="Aucun badge trouvé",
            value="Tu ne possèdes aucun badge.",
            inline=False
        )

    await interaction.response.send_message(embed=embed)

# Fonction pour récupérer le leaderboard des utilisateurs ayant un badge spécifique
@bot.tree.command(name="badge-leaderboard", description="Affiche le classement des utilisateurs ayant un badge spécifique.")
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(badge_id="Badge à filtrer")
@app_commands.autocomplete(badge_id=badge_autocomplete_by_name)  # Utilisation de l'autocomplétion pour le badge
async def badge_leaderboard(interaction: discord.Interaction, badge_id: int):
    # Récupérer les utilisateurs qui ont ce badge spécifique
    leaderboard = collection20.find({"badges": badge_id}).sort("badges", -1).limit(10)  # Trier par nombre de badges

    # Chercher les données du badge
    badge = collection19.find_one({"id": badge_id})
    if not badge:
        embed = discord.Embed(
            title="❌ Badge introuvable",
            description="Ce badge n'existe pas.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed)

    embed = discord.Embed(
        title=f"🏅 Classement des utilisateurs ayant le badge **{badge['title']}**",
        description=f"Voici les 10 utilisateurs ayant le badge {badge['emoji']}",
        color=discord.Color.gold()
    )

    # Utilisez count_documents pour obtenir le nombre de documents correspondants
    if collection20.count_documents({"badges": badge_id}) == 0:
        embed.add_field(name="Aucun utilisateur", value="Aucun utilisateur ne possède ce badge.", inline=False)
    else:
        # Ajouter les utilisateurs au classement
        for idx, user_data in enumerate(leaderboard, start=1):
            user = await bot.fetch_user(user_data["user_id"])
            badge_count = len(user_data.get("badges", []))  # Compter le nombre total de badges
            embed.add_field(name=f"{idx}. {user.display_name}", value=f"{badge_count} badges", inline=False)

    await interaction.response.send_message(embed=embed)

# Fonction d'autocomplétion pour filtrer par badge dans le leaderboard
@app_commands.autocomplete(badge_id=True)
async def badge_autocomplete_by_name(interaction: discord.Interaction, current: str):
    results = collection19.find(
        {"title": {"$regex": f"^{current}", "$options": "i"}}  # Autocomplétion par titre de badge
    ).limit(20)

    choices = []
    for badge in results:
        choices.append(app_commands.Choice(name=f"{badge['title']} {badge['emoji']} (ID: {badge['id']})", value=badge["id"]))

    return choices

@bot.tree.command(name="badge-take", description="(Admin) Retire un badge d'un utilisateur.")
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(
    member="Utilisateur à qui retirer le badge",
    badge_id="ID du badge à retirer"
)
async def badge_take(interaction: discord.Interaction, member: discord.Member, badge_id: int):
    badge = collection19.find_one({"id": badge_id})
    if not badge:
        embed = discord.Embed(
            title="❌ Badge introuvable",
            description="Ce badge n'existe pas.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed)

    user_data = collection20.find_one({"user_id": member.id})
    if not user_data or badge_id not in user_data.get("badges", []):
        embed = discord.Embed(
            title="❌ Badge non possédé",
            description=f"{member.mention} ne possède pas ce badge.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed)

    collection20.update_one(
        {"user_id": member.id},
        {"$pull": {"badges": badge_id}}
    )

    embed = discord.Embed(
        title="🧼 Badge retiré",
        description=f"Le badge **{badge['title']}** {badge['emoji']} a été retiré à {member.mention}.",
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="reset-badge", description="Réinitialise ou supprime un badge de la boutique")
@app_commands.describe(badge_id="ID du badge à réinitialiser ou supprimer")
async def reset_badge(interaction: discord.Interaction, badge_id: int):
    if interaction.user.id != ISEY_ID:
        return await interaction.response.send_message("❌ Tu n'as pas la permission d'utiliser cette commande.", ephemeral=True)

    badge = collection19.find_one({"id": badge_id})
    if not badge:
        return await interaction.response.send_message(f"❌ Aucun badge trouvé avec l'ID {badge_id}.", ephemeral=True)

    # Supprime le badge de la boutique
    collection19.delete_one({"id": badge_id})

    return await interaction.response.send_message(
        f"✅ Le badge **{badge['title']}** {badge.get('emoji', '')} a été supprimé de la boutique.", ephemeral=True
    )

#------------------------------------------------ Connexion Season

def get_start_date(guild_id):
    data = collection22.find_one({"guild_id": guild_id})
    if not data or "start_date" not in data:
        return None
    return datetime.fromisoformat(data["start_date"])


@bot.tree.command(name="start-rewards", description="Définit la date de début des rewards (réservé à ISEY)")
async def start_rewards(interaction: discord.Interaction):
    if interaction.user.id != ISEY_ID:
        await interaction.response.send_message("❌ Tu n'es pas autorisé à utiliser cette commande.", ephemeral=True)
        return

    guild_id = interaction.guild.id
    now = datetime.utcnow()
    timestamp = int(now.timestamp())

    existing = collection22.find_one({"guild_id": guild_id})

    if existing:
        # Cas où un cycle est en cours
        if 'end_timestamp' not in existing:
            await interaction.response.send_message(
                f"⚠️ Un cycle de rewards est déjà en cours depuis le <t:{int(existing['start_timestamp'])}:F>.",
                ephemeral=True
            )
            return

        # Cas où le cycle précédent est terminé → on en relance un nouveau
        collection22.update_one(
            {"guild_id": guild_id},
            {"$set": {
                "start_date": now.isoformat(),
                "start_timestamp": timestamp
            }, "$unset": {
                "end_date": "",
                "end_timestamp": ""
            }}
        )
        await interaction.response.send_message(
            f"🔁 Nouveau cycle de rewards lancé ! Début : <t:{timestamp}:F>",
            ephemeral=True
        )
        return

    # Cas où aucun document n’existe encore → premier lancement
    collection22.insert_one({
        "guild_id": guild_id,
        "start_date": now.isoformat(),
        "start_timestamp": timestamp
    })

    await interaction.response.send_message(
        f"✅ Le système de rewards a bien été lancé pour la première fois ! Début : <t:{timestamp}:F>",
        ephemeral=True
    )

# === COMMANDE SLASH /rewards ===
@bot.tree.command(name="rewards", description="Récupère ta récompense quotidienne")
async def rewards(interaction: discord.Interaction):
    guild_id = interaction.guild.id
    user_id = interaction.user.id

    # Vérifier la date de début des récompenses
    start_date = get_start_date(guild_id)
    if not start_date:
        await interaction.response.send_message("Le système de récompenses n'est pas encore configuré.", ephemeral=True)
        return

    # Calculer le nombre de jours écoulés depuis le début
    days_elapsed = (datetime.utcnow() - start_date).days + 1
    if days_elapsed > 7:
        await interaction.response.send_message("La période de récompenses est terminée.", ephemeral=True)
        return

    # Récupérer les données de l'utilisateur
    user_data = collection23.find_one({"guild_id": guild_id, "user_id": user_id})
    received = user_data.get("rewards_received", {}) if user_data else {}

    # Vérifier si la récompense d’aujourd’hui a déjà été récupérée
    if str(days_elapsed) in received:
        await interaction.response.send_message("Tu as déjà récupéré ta récompense aujourd'hui.", ephemeral=True)
        return

    # Vérifier si une récompense a été manquée
    for i in range(1, days_elapsed):
        if str(i) not in received:
            await interaction.response.send_message("Tu as manqué un jour. Tu ne peux plus récupérer les récompenses.", ephemeral=True)
            return

    # Si toutes les vérifications sont passées, donner la récompense
    await give_reward(interaction, days_elapsed)

# === Fonction pour donner la récompense ===
async def give_reward(interaction: discord.Interaction, day: int):
    reward = daily_rewards.get(day)
    if not reward:
        await interaction.response.send_message("Aucune récompense disponible pour ce jour.", ephemeral=True)
        return

    coins = reward.get("coins", 0)
    badge = reward.get("badge")
    item = reward.get("item")
    random_items = reward.get("random_items")

    # Si random_items est défini, choisir un item au hasard en fonction des chances
    if random_items and isinstance(random_items, list):
        total_chance = sum(entry["chance"] for entry in random_items)  # Somme des chances
        roll = random.uniform(0, total_chance)  # Tirage au sort entre 0 et la somme totale des chances
        cumulative_chance = 0
        for entry in random_items:
            cumulative_chance += entry["chance"]
            if roll <= cumulative_chance:  # Si le tirage est inférieur ou égal à la chance cumulative
                item = entry["id"]  # Choisir cet item
                break

    # === Récompense enregistrée (collection23) ===
    user_data = collection23.find_one({"guild_id": interaction.guild.id, "user_id": interaction.user.id})
    if not user_data:
        user_data = {"guild_id": interaction.guild.id, "user_id": interaction.user.id, "rewards_received": {}}

    user_data["rewards_received"][str(day)] = reward
    collection23.update_one(
        {"guild_id": interaction.guild.id, "user_id": interaction.user.id},
        {"$set": user_data},
        upsert=True
    )

    # === Coins (collection économie) ===
    eco_data = collection.find_one({"guild_id": interaction.guild.id, "user_id": interaction.user.id})
    if not eco_data:
        collection.insert_one({
            "guild_id": interaction.guild.id,
            "user_id": interaction.user.id,
            "cash": coins,
            "bank": 0
        })
    else:
        collection.update_one(
            {"guild_id": interaction.guild.id, "user_id": interaction.user.id},
            {"$inc": {"cash": coins}}
        )

    # === Badge (collection20) ===
    if badge:
        badge_data = collection20.find_one({"user_id": interaction.user.id})
        if not badge_data:
            collection20.insert_one({"user_id": interaction.user.id, "badges": [badge]})
        elif badge not in badge_data.get("badges", []):
            collection20.update_one(
                {"user_id": interaction.user.id},
                {"$push": {"badges": badge}}
            )

    # === Item (collection17) ===
    item_config = None
    if item:
        item_config = collection18.find_one({"id": item})
        if item_config:
            collection17.insert_one({
                "guild_id": interaction.guild.id,
                "user_id": interaction.user.id,
                "item_id": item,
                "item_name": item_config.get("title", "Nom inconnu"),
                "emoji": item_config.get("emoji", "")
            })

    # === Embed de récompense ===
    days_received = len(user_data["rewards_received"])
    total_days = 7
    embed = discord.Embed(
        title="🎁 Récompense de la journée",
        description=f"Voici ta récompense pour le jour {day} !",
        color=discord.Color.green()
    )
    embed.add_field(name="Coins", value=f"{coins} <:ecoEther:1341862366249357374>", inline=False)
    if badge:
        embed.add_field(name="Badge", value=f"Badge ID {badge}", inline=False)
    if item and item_config:
        embed.add_field(name="Item", value=f"{item_config.get('title', 'Nom inconnu')} {item_config.get('emoji', '')} (ID: {item})", inline=False)
    embed.set_image(url=reward["image_url"])

    progress = "█" * days_received + "░" * (total_days - days_received)
    embed.add_field(name="Progression", value=f"{progress} ({days_received}/{total_days})", inline=False)

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="zero-rewards", description="Réinitialise les récompenses de tous les utilisateurs")
async def zero_rewards(interaction: discord.Interaction):
    # Vérifier si l'utilisateur est ISEY_ID
    if interaction.user.id != 792755123587645461:
        await interaction.response.send_message("Tu n'as pas l'autorisation d'utiliser cette commande.", ephemeral=True)
        return
    
    # Parcourir tous les utilisateurs dans la collection de récompenses
    all_users = collection23.find({"rewards_received": {"$exists": True}})
    
    updated_count = 0
    for user_data in all_users:
        # Réinitialiser les récompenses de l'utilisateur
        collection23.update_one(
            {"guild_id": user_data["guild_id"], "user_id": user_data["user_id"]},
            {"$set": {"rewards_received": {}}}
        )
        updated_count += 1

    # Répondre avec un message de confirmation
    await interaction.response.send_message(f"Les récompenses ont été réinitialisées pour {updated_count} utilisateur(s).", ephemeral=True)

@bot.tree.command(name="end-rewards", description="Définit la date de fin des rewards (réservé à ISEY)")
async def end_rewards(interaction: discord.Interaction):
    if interaction.user.id != ISEY_ID:
        await interaction.response.send_message("❌ Tu n'es pas autorisé à utiliser cette commande.", ephemeral=True)
        return

    guild_id = interaction.guild.id
    existing = collection22.find_one({"guild_id": guild_id})

    if not existing:
        await interaction.response.send_message("⚠️ Aucun début de rewards trouvé. Utilise d'abord `/start-rewards`.", ephemeral=True)
        return

    if 'end_timestamp' in existing:
        await interaction.response.send_message(
            f"⚠️ Les rewards ont déjà été terminés le <t:{int(existing['end_timestamp'])}:F>.",
            ephemeral=True
        )
        return

    now = datetime.utcnow()
    timestamp = int(now.timestamp())

    collection22.update_one(
        {"guild_id": guild_id},
        {"$set": {
            "end_date": now.isoformat(),
            "end_timestamp": timestamp
        }}
    )

    updated = collection22.find_one({"guild_id": guild_id})

    await interaction.response.send_message(
        f"✅ Les rewards ont été clôturés !\nPériode : du <t:{updated['start_timestamp']}:F> au <t:{updated['end_timestamp']}:F>",
        ephemeral=True
    )


#------------------------------------- Quetes

# Fonction pour insérer des quêtes de départ dans la base de données
def insert_quetes_into_db():
    # Quêtes à insérer au démarrage
    quetes_debut = [
        {"id": 1, "nom": "Quête de début", "description": "Commencez votre aventure !", "emoji": "🌟", "recompense": "100"},
        {"id": 2, "nom": "Quête de récolte", "description": "Récoltez des ressources.", "emoji": "🌾", "recompense": "200"}
    ]
    
    for quete in quetes_debut:
        # Vérifier si la quête existe déjà dans la base de données
        if not collection32.find_one({"id": quete["id"]}):
            collection32.insert_one(quete)

@bot.tree.command(name="add-quete", description="Ajoute une nouvelle quête.")
@app_commands.describe(
    quest_id="L'ID unique de la quête",
    nom="Nom de la quête",
    description="Description de la quête",
    reward_item_id="ID de l'item en récompense (doit exister dans la boutique)",
    reward_coins="Montant de pièces en récompense"
)
async def add_quete(interaction: discord.Interaction, quest_id: int, nom: str, description: str, reward_item_id: int, reward_coins: int):
    if interaction.user.id != 792755123587645461:
        return await interaction.response.send_message("❌ Tu n'as pas la permission d'utiliser cette commande.", ephemeral=True)

    # Vérifie que l'item existe
    item = collection16.find_one({"id": reward_item_id})
    if not item:
        return await interaction.response.send_message("❌ L'item spécifié n'existe pas dans la boutique.", ephemeral=True)

    existing = collection32.find_one({"id": quest_id})
    if existing:
        return await interaction.response.send_message("❌ Une quête avec cet ID existe déjà.", ephemeral=True)

    quest = {
        "id": quest_id,
        "nom": nom,
        "description": description,
        "reward_item_id": reward_item_id,
        "reward_coins": reward_coins
    }

    collection32.insert_one(quest)
    await interaction.response.send_message(f"✅ Quête **{nom}** ajoutée avec succès !", ephemeral=True)

@bot.tree.command(name="quetes", description="Affiche la liste des quêtes disponibles")
async def quetes(interaction: discord.Interaction):
    quests = list(collection32.find({}))

    if not quests:
        return await interaction.response.send_message("❌ Aucune quête enregistrée.", ephemeral=True)

    # Créez l'embed avec l'utilisateur comme auteur
    embed = discord.Embed(title=f"Quêtes disponibles", color=discord.Color.blue())
    
    # Ajout de la photo de profil de l'utilisateur
    embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)

    # Ajout de l'emoji personnalisé en haut à droite
    embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1364316821196640306.png")  # Utilisation du lien direct pour l'emoji personnalisé

    for quest in quests:
        item = collection16.find_one({"id": quest["reward_item_id"]})
        item_name = item["title"] if item else "Inconnu"
        item_emoji = item["emoji"] if item else ""

        # Si la quête a été réalisée, on la barre et on affiche la personne qui l'a complétée
        if 'completed_by' in quest:
            completed_by = quest['completed_by']
            quest_name = f"~~{quest['nom']}~~"
            quest_value = f"{quest['description']}\n**Récompense**: {item_name} {item_emoji} + {quest['reward_coins']} <:ecoEther:1341862366249357374>\n**Complétée par**: {completed_by}"
        else:
            quest_name = f"🔹 {quest['nom']} (ID: {quest['id']})"
            quest_value = f"{quest['description']}\n**Récompense**: {item_name} {item_emoji} + {quest['reward_coins']} <:ecoEther:1341862366249357374>"

        embed.add_field(
            name=quest_name,
            value=quest_value,
            inline=False
        )

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="quete-faite", description="Valide une quête et donne les récompenses à un utilisateur.")
@app_commands.describe(quest_id="ID de la quête", user="Utilisateur à récompenser")
async def quete_faite(interaction: discord.Interaction, quest_id: int, user: discord.User):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("❌ Tu n'as pas la permission d'utiliser cette commande.", ephemeral=True)

    quest = collection32.find_one({"id": quest_id})
    if not quest:
        return await interaction.response.send_message("❌ Quête introuvable.", ephemeral=True)

    # Ajouter item dans l'inventaire
    collection17.insert_one({
        "guild_id": interaction.guild.id,
        "user_id": user.id,
        "item_id": quest["reward_item_id"],
        "item_name": collection16.find_one({"id": quest["reward_item_id"]})["title"],
        "emoji": collection16.find_one({"id": quest["reward_item_id"]})["emoji"]
    })

    # Ajouter des coins
    user_data = collection.find_one({"guild_id": interaction.guild.id, "user_id": user.id})
    if not user_data:
        user_data = {"guild_id": interaction.guild.id, "user_id": user.id, "cash": 0, "bank": 0}
        collection.insert_one(user_data)

    new_cash = user_data["cash"] + quest["reward_coins"]
    collection.update_one(
        {"guild_id": interaction.guild.id, "user_id": user.id},
        {"$set": {"cash": new_cash}}
    )

    # Marquer la quête comme complétée par l'utilisateur
    collection32.update_one(
        {"id": quest_id},
        {"$set": {"completed_by": user.name}}
    )

    await interaction.response.send_message(
        f"✅ Récompenses de la quête **{quest['nom']}** données à {user.mention} !",
        ephemeral=True
    )

@bot.tree.command(name="reset-quetes", description="Supprime toutes les quêtes (ADMIN)")
async def reset_quetes(interaction: discord.Interaction):
    if interaction.user.id != ISEY_ID:
        await interaction.response.send_message("Tu n'as pas l'autorisation d'utiliser cette commande.", ephemeral=True)
        return

    result = collection32.delete_many({})
    await interaction.response.send_message(f"🧹 Collection `ether_quetes` reset avec succès. {result.deleted_count} quêtes supprimées.")

from discord import Embed
import matplotlib.pyplot as plt
import numpy as np
import io
import discord

# Fonction d'union des plages (par exemple, union de [6;7] et [11;19])
def union_intervals(intervals):
    # Tri des intervalles par le début de chaque intervalle
    intervals.sort(key=lambda x: x[0])
    merged = []
    
    for interval in intervals:
        if not merged or merged[-1][1] < interval[0]:
            merged.append(interval)
        else:
            merged[-1][1] = max(merged[-1][1], interval[1])
    return merged

# Fonction d'intersection des plages
def intersection_intervals(intervals):
    # Intersection de toutes les plages disponibles
    min_end = min(interval[1] for interval in intervals)
    max_start = max(interval[0] for interval in intervals)
    
    if max_start <= min_end:
        return [(max_start, min_end)]  # Renvoie l'intersection
    return []

import discord
from discord import Embed
import matplotlib.pyplot as plt
import io

@bot.tree.command(name="id-items", description="📚 Affiche les IDs d'items utilisés et les plages libres")
async def id_items(interaction: discord.Interaction):
    # Récupérer uniquement les documents qui possèdent un champ 'id'
    all_items = list(collection16.find({"id": {"$exists": True}}, {"id": 1, "_id": 0}))
    used_ids = sorted(item["id"] for item in all_items)

    # IDs totaux possibles
    total_ids = list(range(1, 1001))

    # Calcul des IDs libres
    free_ids = [i for i in total_ids if i not in used_ids]

    # Génération des plages libres
    free_intervals = []
    current_start = None

    for i in total_ids:
        if i in free_ids:
            if current_start is None:
                current_start = i
        else:
            if current_start is not None:
                free_intervals.append((current_start, i - 1))
                current_start = None
    if current_start is not None:
        free_intervals.append((current_start, 1000))

    # Graphique de l'utilisation
    usage_percentage = len(used_ids) / len(total_ids) * 100
    free_percentage = 100 - usage_percentage

    fig, ax = plt.subplots(figsize=(6, 4))
    labels = ['Utilisés', 'Libres']
    sizes = [usage_percentage, free_percentage]
    colors = ['#FF6B6B', '#4ECDC4']
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
    ax.axis('equal')

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
    buf.seek(0)
    plt.close()

    # Création de l'embed Discord
    embed = Embed(
        title="📚 Analyse des IDs d'Items",
        description="Voici l'état actuel des IDs utilisés et disponibles.",
        color=discord.Color.blurple()
    )

    # Gestion du champ des IDs utilisés
    ids_used_text = ', '.join(map(str, used_ids))
    if len(ids_used_text) > 1024:
        ids_used_text = ids_used_text[:1020] + "..."

    embed.add_field(
        name="🛠️ IDs Utilisés",
        value=f"`{len(used_ids)}` IDs utilisés\n`{ids_used_text}`",
        inline=False
    )

    # Gestion du champ des plages d'IDs libres
    free_intervals_text = "\n".join(
        f"`[{start} ➔ {end}]`" if start != end else f"`[{start}]`" for start, end in free_intervals
    )
    if len(free_intervals_text) > 1024:
        free_intervals_text = free_intervals_text[:1020] + "..."

    embed.add_field(
        name="📖 Plages d'IDs Libres",
        value=free_intervals_text,
        inline=False
    )

    embed.add_field(
        name="📊 Statistiques",
        value=f"**Total IDs :** `{len(total_ids)}`\n"
              f"**Utilisés :** `{len(used_ids)} ({usage_percentage:.2f}%)`\n"
              f"**Libres :** `{len(free_ids)} ({free_percentage:.2f}%)`",
        inline=False
    )

    embed.set_image(url="attachment://usage_graph.png")
    embed.set_footer(text="Etherya • Visualisation des IDs", icon_url=interaction.guild.icon.url if interaction.guild.icon else None)

    file = discord.File(buf, filename="usage_graph.png")
    await interaction.response.send_message(embed=embed, file=file)

import random
import discord
from discord import Embed, ButtonStyle
from discord.ui import View, Button

@bot.tree.command(name="id-random", description="🎲 Tire un ID libre automatiquement parmi ceux disponibles en boutique")
async def id_random(interaction: discord.Interaction):
    # Aller chercher tous les IDs utilisés directement depuis MongoDB
    used_ids = [doc["id"] for doc in collection16.find({}, {"id": 1}) if "id" in doc]

    # IDs possibles de 1 à 1000 (par exemple)
    total_ids = list(range(1, 1001))

    # IDs libres = ceux pas utilisés
    free_ids = [i for i in total_ids if i not in used_ids]

    # Fonction pour tirer un ID libre au hasard
    def pick_random_id():
        return random.choice(free_ids) if free_ids else None

    random_id = pick_random_id()

    if random_id is None:
        await interaction.response.send_message("❌ Aucun ID disponible.", ephemeral=True)
        return

    # Embed de réponse
    embed = Embed(
        title="🎲 ID Libre Tiré",
        description=f"Voici un ID libre :\n\n`{random_id}`",
        color=discord.Color.gold()
    )
    embed.set_footer(text="Clique sur 🔄 pour tirer un autre ID !", icon_url=interaction.guild.icon.url if interaction.guild.icon else None)

    # Vue avec bouton Re-roll
    class RandomIDView(View):
        def __init__(self):
            super().__init__(timeout=30)

        @discord.ui.button(label="Re-roll 🔄", style=ButtonStyle.primary)
        async def reroll(self, interaction_button: discord.Interaction, button: Button):
            new_id = pick_random_id()
            if new_id is None:
                await interaction_button.response.edit_message(content="❌ Aucun ID disponible.", embed=None, view=None)
                return

            new_embed = Embed(
                title="🎲 ID Libre Tiré",
                description=f"Voici un nouvel ID libre :\n\n`{new_id}`",
                color=discord.Color.gold()
            )
            new_embed.set_footer(text="Clique sur 🔄 pour tirer un autre ID !", icon_url=interaction.guild.icon.url if interaction.guild.icon else None)

            await interaction_button.response.edit_message(embed=new_embed)

    await interaction.response.send_message(embed=embed, view=RandomIDView())

@bot.hybrid_command(
    name="uptime",
    description="Affiche l'uptime du bot."
)
async def uptime(ctx):
    uptime_seconds = round(time.time() - start_time)
    days = uptime_seconds // (24 * 3600)
    hours = (uptime_seconds % (24 * 3600)) // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60
    embed = discord.Embed(
        title="Uptime du bot",
        description=f"Le bot est en ligne depuis : {days} jours, {hours} heures, {minutes} minutes, {seconds} secondes",
        color=discord.Color.blue()
    )
    embed.set_footer(text=f"♥️by Iseyg", icon_url=ctx.author.avatar.url)
    await ctx.send(embed=embed)

# Token pour démarrer le bot (à partir des secrets)
# Lancer le bot avec ton token depuis l'environnement  
keep_alive()
bot.run(token)
