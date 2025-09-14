import discord
from discord.ext import commands
from datetime import datetime, timedelta, timezone
import random
import re
import pytz
from collections import defaultdict, deque  
from typing import Optional
from discord.ui import View

# Définition des IDs et collections (à passer depuis bot.py)
# Ces variables seront initialisées dans bot.py et passées aux cogs via bot.db_collections et bot.config_ids
# Pour l'instant, je les mets ici pour que les fonctions utilitaires puissent les référencer.
# Elles seront remplacées par des accès via `bot.db_collections` et `bot.config_ids` dans les cogs.
db_collections = {}
config_ids = {}


# --- ID Etherya Partenariats ---
partnership_channel_id = 1355158081855688745
PARTNER_ROLE_ID = 1355157749994098860 # Renommé pour éviter le conflit avec ROLE_ID générique

# --- ID Etherya ---
BOUNTY_CHANNEL_ID = 1355298449829920950
ETHERYA_SERVER_ID = 1034007767050104892
AUTORIZED_SERVER_ID = 1034007767050104892
WELCOME_CHANNEL_ID = 1355198748296351854

# --- ID Etherya Pouvoir ---
# -- Oeil Démoniaque --
OEIL_ID = 1363949082653098094
OEIL_ROLE_ID = 1364123507532890182 # Renommé
# -- Float --
FLOAT_ID = 1363946902730575953
ROLE_FLOAT_ID = 1364121382908067890
# -- Pokeball --
POKEBALL_ID = 1363942048075481379
# -- Infini --
INFINI_ID = [1363939565336920084, 1363939567627145660, 1363939486844850388]
ANTI_ROB_ROLE = 1363964754678513664
# -- Armure du Berserker --
ARMURE_ID = 1363821649002238142
ANTI_ROB_ID = 1363964754678513664
# -- Rage du Berserker --
RAGE_ID = 1363821333624127618
ECLIPSE_ROLE_ID = 1364115033197510656
# -- Ultra Instinct --
ULTRA_ID = 1363821033060307106
# -- Haki des Rois --
HAKI_ROI_ID = 1363817645249527879
HAKI_SUBIS_ID = 1364109450197078026
# -- Arme Démoniaque Impérial --
ARME_DEMONIAQUE_ID = 1363817586466361514
# -- Heal (Appel de l'exorciste) --
HEAL_ID = 1363873859912335400
MALUS_ROLE_ID = 1363969965572755537
# -- Benediction --
BENEDICTION_ROLE_ID = 1364294230343684137
# -- Divin --
DIVIN_ROLE_ID = 1367567412886765589
# -- Bombe --
BOMBE_ID = 1365316070172393572
# -- Marine & Pirates --
ISEY_MARINE_ID = 1365631932964012142
ISEY_PIRATE_ID = 1365682636957421741

# --- ID Etherya Nen ---
PERMISSION_ROLE_ID = 1363928528587984998
LICENSE_ITEM_ID = 7
nen_roles = {
    "renforcement": 1363306813688381681,
    "emission": 1363817609916584057,
    "manipulation": 1363817536348749875,
    "materialisation": 1363817636793810966,
    "transformation": 1363817619529924740,
    "specialisation": 1363817593252876368,
}
nen_drop_rates = [
    ("renforcement", 24.5), ("emission", 24.5), ("manipulation", 16.5),
    ("materialisation", 16.5), ("transformation", 17.5), ("specialisation", 0.5),
]
MATERIALISATION_IDS = [1363817636793810966, 1363817593252876368]
ITEMS_INTERDITS = [202, 197, 425, 736, 872, 964, 987]
MANIPULATION_ROLE_ID = 1363974710739861676
AUTHORIZED_MANI_IDS = [1363817593252876368, 1363817536348749875]
EMISSION_IDS = [1363817593252876368, 1363817609916584057]
TARGET_ROLE_ID = 1363969965572755537 
RENFORCEMENT_IDS = [1363306813688381681, 1363817593252876368]
RENFORCEMENT_ROLE_ID = 1363306813688381681 

# --- ID Etherya Fruits du Démon ---
ROLE_UTILISATEUR_GLACE = 1365311608259346462
ROLE_GEL = 1365313259280007168

# --- ID Etherya Pirates & Marines ---
marine_roles = {
    "Amiral en chef": 1365683477868970204, "Commandant": 1365683407023243304,
    "Lieutenant": 1365683324831531049, "Matelot": 1365683175019516054,
}
pirate_roles = {
    "Roi des Pirates": 1365682989996052520, "Yonko": 1365682989996052520,
    "Corsaire": 1365682918243958826, "Pirate": 1365682795501977610,
}

# ID des rôles et combien ils touchent
ROLE_PAY = {
    1355157636009427096: 100_000,  # CROWN_ISEY
    1355234995555270768: 90_000,   # BRAS_DROIT
    1355157638521815236: 80_000,   # CO-OWNER
    1357258052147089450: 70_000,   # ADMINISTRATEUR
    1355157640640200864: 60_000,   # RESP_ID
    1355157686815293441: 50_000    # STAFF_ID
}
# -- ID TICKET --
TRANSCRIPT_CHANNEL_ID_ECO = 1355158107956707498 # Renommé pour éviter le conflit
SUPPORT_ROLE_ID_ECO = 1355157686815293441 # Renommé

# --- ID Etherya ---
ETHERYA_SERVER_ID = 1034007767050104892
AUTORIZED_SERVER_ID = 1034007767050104892
WELCOME_CHANNEL_ID = 1355198748296351854

log_channels_eco = { # Renommé pour éviter le conflit
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

# Fonctions utilitaires
def create_embed(title, description, color=discord.Color.blue(), footer_text=""):
    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_footer(text=footer_text)
    return embed

def has_permission(ctx, perm):
    # Vérifie si l'utilisateur a la permission spécifiée ou s'il est l'owner du bot
    return ctx.author.id == config_ids.get("ISEY_ID") or getattr(ctx.author.guild_permissions, perm, False)

def is_higher_or_equal(ctx, member):
    # Vérifie si le rôle de l'auteur est supérieur ou égal à celui du membre ciblé
    return member.top_role >= ctx.author.top_role

async def send_log(ctx, member, action, reason, duration=None):
    # Cette fonction devra être adaptée pour utiliser les IDs de log_channels
    # qui sont maintenant dans bot.config_ids ou une structure similaire.
    # Pour l'exemple, je vais utiliser un ID générique ou un print.
    # Dans un vrai bot, vous auriez une logique pour trouver le bon canal de log.
    log_channel_id = config_ids.get("WARN_LOG_CHANNEL") # Exemple
    if log_channel_id:
        log_channel = ctx.guild.get_channel(log_channel_id)
        if log_channel:
            embed = create_embed("🚨 Sanction appliquée", f"{member.mention} a été sanctionné.", discord.Color.red(), ctx, member, action, reason, duration)
            await log_channel.send(embed=embed)
    else:
        print(f"LOG: {member.name} {action} for {reason} (Duration: {duration})")

async def send_dm(member, action, reason, duration=None):
    try:
        embed = create_embed("🚨 Vous avez reçu une sanction", "Consultez les détails ci-dessous.", discord.Color.red())
        embed.add_field(name="⚖️ Sanction", value=action, inline=True)
        embed.add_field(name="📜 Raison", value=reason, inline=False)
        if duration:
            embed.add_field(name="⏳ Durée", value=duration, inline=True)
        await member.send(embed=embed)
    except discord.Forbidden:
        print(f"Impossible d'envoyer un DM à {member.display_name}.")

# utils.py
def load_guild_settings(bot, guild_id: int) -> dict:
    """Charge la configuration d'une guild depuis MongoDB"""
    try:
        return bot.db_collections["setup"].find_one({'guild_id': str(guild_id)}) or {}
    except Exception as e:
        print(f"[WARN] Impossible de charger les paramètres pour le serveur {guild_id}: {e}")
        return {}




def get_premium_servers():
    """Récupère les IDs des serveurs premium depuis la base de données."""
    premium_docs = db_collections.get("setup_premium", {}).find({}, {"_id": 0, "guild_id": 1})
    return {doc["guild_id"] for doc in premium_docs}

async def is_blacklisted(user_id: int) -> bool:
    result = db_collections.get("delta_bl", {}).find_one({"user_id": str(user_id)})
    return result is not None

def add_sanction(guild_id, user_id, action, reason, duration=None):
    sanction_data = {
        "guild_id": guild_id,
        "user_id": user_id,
        "action": action,
        "reason": reason,
        "duration": duration,
        "timestamp": datetime.utcnow()
    }
    db_collections.get("sanction", {}).insert_one(sanction_data)

def get_log_channel(guild, key):
    # Cette fonction dépendra de la structure de vos IDs de log_channels
    # Pour l'instant, elle est simplifiée.
    log_channel_id = {
        "sanctions": config_ids.get("WARN_LOG_CHANNEL"),
        "messages": None, # Ajoutez les IDs réels ici
        # ... autres clés
    }.get(key)
    if log_channel_id:
        return guild.get_channel(log_channel_id)
    return None

# Nouvelle fonction pour les logs économiques, utilisant les collections passées
async def log_eco_channel(bot_instance, guild_id, user, action, amount, balance_before, balance_after, note=""):
    config = bot_instance.db_collections["logs"].find_one({"guild_id": str(guild_id)})
    channel_id = config.get("eco_log_channel") if config else None

    if not channel_id:
        return  # Aucun salon configuré

    channel = bot_instance.get_channel(channel_id)
    if not channel:
        return  # Salon introuvable (peut avoir été supprimé)

    embed = discord.Embed(
        title="💸 Log Économique",
        color=discord.Color.gold(),
        timestamp=datetime.utcnow()
    )
    embed.set_author(name=str(user), icon_url=user.avatar.url if user.avatar else None)
    embed.add_field(name="Action", value=action, inline=True)
    embed.add_field(name="Montant", value=f"{amount} <:ecoEther:1341862366249357374>", inline=True)
    embed.add_field(name="Solde", value=f"Avant: {balance_before}\nAprès: {balance_after}", inline=False)

    if note:
        embed.add_field(name="Note", value=note, inline=False)

    await channel.send(embed=embed)

def get_cf_config(guild_id):
    config = db_collections.get("idees", {}).find_one({"guild_id": guild_id})
    if not config:
        config = {
            "guild_id": guild_id,
            "start_chance": 50,
            "max_chance": 100,
            "max_bet": 20000
        }
        db_collections.get("idees", {}).insert_one(config)
    return config

def get_presentation_channel_id(guild_id: int):
    data = db_collections.get("presentation", {}).find_one({"guild_id": guild_id})
    return data.get("presentation_channel") if data else None

def get_user_partner_info(user_id: str):
    partner_data = db_collections.get("partner", {}).find_one({"user_id": user_id})
    if partner_data:
        return partner_data['rank'], partner_data['partnerships']
    return None, None

async def get_protection_data(guild_id):
    data = db_collections.get("protection", {}).find_one({"guild_id": str(guild_id)})
    return data or {}

def format_mention(id, type_mention):
    if not id or id == "Non défini":
        return "❌ **Non défini**"
    if isinstance(id, int) or (isinstance(id, str) and id.isdigit()):
        if type_mention == "user":
            return f"<@{id}>"
        elif type_mention == "role":
            return f"<@&{id}>"
        elif type_mention == "channel":
            return f"<#{id}>"
        return "❌ **Mention invalide**"
    return "❌ **Format invalide**"

PROTECTIONS = [
    "anti_massban", "anti_masskick", "anti_bot", "anti_createchannel",
    "anti_deletechannel", "anti_createrole", "anti_deleterole",
    "anti_everyone", "anti_spam", "anti_links", "whitelist"
]

PROTECTION_DETAILS = {
    "anti_massban": ("🚫 Anti-MassBan", "Empêche les bannissements massifs."),
    "anti_masskick": ("👢 Anti-MassKick", "Empêche les expulsions massives."),
    "anti_bot": ("🤖 Anti-Bot", "Bloque l'ajout de bots non autorisés."),
    "anti_createchannel": ("📤 Anti-Création de salon", "Empêche la création non autorisée de salons."),
    "anti_deletechannel": ("📥 Anti-Suppression de salon", "Empêche la suppression non autorisée de salons."),
    "anti_createrole": ("➕ Anti-Création de rôle", "Empêche la création non autorisée de rôles."),
    "anti_deleterole": ("➖ Anti-Suppression de rôle", "Empêche la suppression non autorisée de rôles."),
    "anti_everyone": ("📣 Anti-Everyone", "Empêche l'utilisation abusive de @everyone ou @here."),
    "anti_spam": ("💬 Anti-Spam", "Empêche le spam excessif de messages."),
    "anti_links": ("🔗 Anti-Liens", "Empêche l'envoi de liens non autorisés."),
    "whitelist": ("✅ Liste blanche", "Utilisateurs exemptés des protections.")
}

def generate_global_status_bar(data: dict) -> str:
    protections = [prot for prot in PROTECTIONS if prot != "whitelist"]
    total = len(protections)
    enabled_count = sum(1 for prot in protections if data.get(prot, False))
    ratio = enabled_count / total

    bar_length = 10
    filled_length = round(bar_length * ratio)
    bar = "🟩" * filled_length + "⬛" * (bar_length - filled_length)
    return f"**Sécurité Globale :** `{enabled_count}/{total}`\n{bar}"

def format_protection_field(prot, data, guild, bot):
    name, desc = PROTECTION_DETAILS[prot]
    enabled = data.get(prot, False)
    status = "✅ Activée" if enabled else "❌ Désactivée"
    updated_by_id = data.get(f"{prot}_updated_by")
    updated_at = data.get(f"{prot}_updated_at")

    modifier = None
    if updated_by_id:
        modifier = guild.get_member(int(updated_by_id)) or updated_by_id

    formatted_date = ""
    if updated_at:
        dt = updated_at.replace(tzinfo=pytz.utc).astimezone(pytz.timezone("Europe/Paris"))
        formatted_date = f"🕓 {dt.strftime('%d/%m/%Y à %H:%M')}"

    mod_info = f"\n👤 Modifié par : {modifier.mention if isinstance(modifier, discord.Member) else modifier}" if modifier else ""
    date_info = f"\n{formatted_date}" if formatted_date else ""

    value = f"> {desc}\n> **Statut :** {status}{mod_info}{date_info}"
    return name, value

async def notify_owner_of_protection_change(guild, prot, new_value, interaction):
    if guild and guild.owner:
        try:
            embed = discord.Embed(
                title="🔐 Mise à jour d'une protection sur votre serveur",
                description=f"**Protection :** {PROTECTION_DETAILS[prot][0]}\n"
                            f"**Statut :** {'✅ Activée' if new_value else '❌ Désactivée'}",
                color=discord.Color.green() if new_value else discord.Color.red()
            )
            embed.add_field(
                name="👤 Modifiée par :",
                value=f"{interaction.user.mention} (`{interaction.user}`)",
                inline=False
            )
            embed.add_field(name="🏠 Serveur :", value=guild.name, inline=False)
            embed.add_field(
                name="🕓 Date de modification :",
                value=f"<t:{int(datetime.utcnow().timestamp())}:f>",
                inline=False
            )
            embed.add_field(
                name="ℹ️ Infos supplémentaires :",
                value="Vous pouvez reconfigurer vos protections à tout moment avec la commande `/protection`.",
                inline=False
            )

            await guild.owner.send(embed=embed)
        except discord.Forbidden:
            print("Impossible d’envoyer un DM à l’owner.")
        except Exception as e:
            print(f"Erreur lors de l'envoi du DM : {e}")

def is_admin_or_isey():
    async def predicate(ctx):
        return ctx.author.guild_permissions.administrator or ctx.author.id == config_ids.get("ISEY_ID")
    return commands.check(predicate)

THUMBNAIL_URL = "images_GITHUB/3e3bd3c24e33325c7088f43c1ae0fadc.png" # Chemin corrigé

# 🎭 Emojis dynamiques pour chaque serveur
EMOJIS_SERVEURS = ["🌍", "🚀", "🔥", "👾", "🏆", "🎮", "🏴‍☠️", "🏕️"]

# ⚜️ ID du serveur Etherya
ETHERYA_ID = 1034007767050104892 # Utiliser l'ID réel si différent

def boost_bar(level):
    """Génère une barre de progression pour le niveau de boost."""
    filled = "🟣" * level
    empty = "⚫" * (3 - level)
    return filled + empty

# Dictionnaire pour stocker les messages supprimés {channel_id: deque[(timestamp, auteur, contenu)]}
sniped_messages = defaultdict(deque)

# Liste des catégories sensibles
sensitive_categories = {
    "insultes_graves": ["fils de pute"],
    "discours_haineux": ["nigger", "nigga", "negro", "chintok", "bougnoule", "pédé","sale pédé","sale arabe", "sale noir", "sale juif", "sale blanc", "race inférieure", "sale race", "enculé de ta race", "triso"],
    "ideologies_haineuses": ["raciste", "homophobe", "xénophobe", "transphobe", "antisémite", "islamophobe", "suprémaciste", "fasciste", "nazi", "néonazi", "dictateur", "extrémiste", "fanatique", "radicalisé", "djihadiste"],
    "violences_crimes": ["viol", "pédophilie", "inceste", "pédocriminel", "grooming", "agression", "assassin", "meurtre", "homicide", "génocide", "extermination", "décapitation", "lynchage", "massacre", "torture", "suicidaire", "prise d'otage", "terrorisme", "attentat", "bombardement", "exécution", "immolation", "traite humaine", "esclavage sexuel", "kidnapping", "tueur en série", "infanticide", "parricide"],
    "drogues_substances": ["cocaïne", "héroïne", "crack", "LSD", "ecstasy", "GHB", "fentanyl", "méthamphétamine", "cannabis", "weed", "opium", "drogue", "drogue de synthèse", "trafic de drogue","overdose", "shooté", "stoned", "sniffer", "shit"],
    "contenus_sexuels": ["pornographie", "porno", "prostitution", "escort", "masturbation", "fellation", "pipe", "sodomie", "exhibition", "fétichisme", "orgie", "gode", "pénétration", "nudité", "camgirl", "onlyfans", "porno enfant", "sextape", "branlette", "bite",],
    "fraudes_financières": ["scam", "arnaque", "fraude", "chantage", "extorsion", "évasion fiscale", "fraude fiscale", "détournement de fonds","blanchiment d'argent", "crypto scam", "phishing bancaire", "vol d'identité", "usurpation"],
    "attaques_menaces": ["raid", "ddos", "dox", "doxx", "hack", "hacking", "botnet", "crash bot", "flood", "booter", "keylogger", "phishing", "malware", "trojan", "ransomware", "brute force", "cheval de troie", "injection SQL"],
    "raids_discord": ["mass ping", "raid bot", "join raid", "leaver bot", "spam bot", "token grabber", "auto join", "multi account", "alt token", "webhook spam", "webhook nuker", "selfbot", "auto spam"],
    "harcèlement_haine": ["swat", "swatting", "harass", "threaten", "kill yourself", "kys", "suicide", "death threat", "pedo", "grooming", "harcèlement", "cyberharcèlement", "intimidation", "menace de mort", "appel au suicide"],
    "personnages_problématiques": ["Hitler", "Mussolini", "Staline", "Pol Pot", "Mao Zedong", "Benito Mussolini", "Joseph Staline", "Adolf Hitler", "Kim Jong-il","Kim Jong-un", "Idi Amin", "Saddam Hussein", "Bachar el-Assad", "Ben Laden", "Oussama Ben Laden", "Ayman al-Zawahiri", "Heinrich Himmler", "Joseph Goebbels", "Hermann Göring", "Adolf Eichmann", "Rudolf Hess", "Slobodan Milošević", "Radovan Karadžić", "Ratko Mladić", "Francisco Franco", "Augusto Pinochet", "Fidel Castro", "Che Guevara", "Ayatollah Khomeini", "Al-Baghdadi", "Abu Bakr al-Baghdadi", "Anders Behring Breivik", "Charles Manson", "Ted Bundy", "Jeffrey Dahmer", "Richard Ramirez", "John Wayne Gacy", "Albert Fish", "Ed Gein", "Luca Magnotta", "Peter Kürten", "David Berkowitz", "Ariel Castro", "Yitzhak Shamir", "Meir Kahane", "Nicolae Ceaușescu", "Vladimir Poutine", "Alexander Lukashenko", "Mengistu Haile Mariam", "Yahya Jammeh", "Omar el-Béchir", "Jean-Bédel Bokassa", "Robert Mugabe", "Mobutu Sese Seko", "Laurent-Désiré Kabila", "Joseph Kony", "Enver Hoxha", "Gaddafi", "Muammar Kadhafi", "Ríos Montt", "Reinhard Heydrich", "Ismail Enver", "Anton Mussert", "Ante Pavelić", "Vidkun Quisling", "Stepan Bandera", "Ramush Haradinaj", "Slobodan Praljak", "Milomir Stakić", "Theodore Kaczynski", "Eric Harris", "Dylan Klebold", "Brenton Tarrant", "Seung-Hui Cho", "Stephen Paddock", "Patrick Crusius", "Elliot Rodger", "Nikolas Cruz", "Dylann Roof", "Timothy McVeigh", "Tamerlan Tsarnaev", "Dzhokhar Tsarnaev", "Sayfullo Saipov", "Mohamed Merah", "Amedy Coulibaly", "Chérif Kouachi", "Salah Abdeslam", "Abdelhamid Abaaoud", "Mohammed Atta", "Khalid Sheikh Mohammed", "Ramzi Yousef", "Richard Reid", "Umar Farouk Abdulmutallab", "Anwar al-Awlaki"]
}

word_to_category = {}
for category, words in sensitive_categories.items():
    for word in words:
        word_to_category[word.lower()] = category

# Dictionnaire global pour les cooldowns des sondages
user_cooldown = {}

# Dictionnaires pour les giveaways
giveaways = {}
ended_giveaways = {}
fast_giveaways = {}

# Dictionnaire pour les alertes d'urgence
active_alerts = {}

# Fonction pour vérifier si une URL est valide
def is_valid_url(url):
    regex = re.compile(
        r'^(https?://)?'  # http:// ou https:// (optionnel)
        r'([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}'  # domaine
        r'(/.*)?$'  # chemin (optionnel)
    )
    return bool(re.match(regex, url))

# Pour les stats globales
stats_collection33 = None # Sera initialisé dans bot.py

# === UTILITAIRE POUR RÉCUPÉRER LA DATE DE DÉBUT ===
def get_start_date(guild_id, db_collections):
    start_date_data = db_collections["start_date"].find_one({"guild_id": guild_id})
    if start_date_data:
        return datetime.fromisoformat(start_date_data["start_date"])
    return None

# Config des rôles pour l'auto-collecte (déplacé ici pour être globalement accessible)
COLLECT_ROLES_CONFIG = [
    {
        "role_id": 1355157715550470335, #Membres
        "amount": 1000,
        "cooldown": 3600,
        "auto": False,
        "target": "bank"
    },
    {
        "role_id": 1365683057591582811, #Roi des Pirates
        "amount": 12500,
        "cooldown": 43200,
        "auto": False,
        "target": "bank"
    },
    {
        "role_id": 1365683477868970204, #Amiral en Chef
        "amount": 15000,
        "cooldown": 43200,
        "auto": False,
        "target": "bank"
    },
    {
        "role_id": 1365682989996052520, #Yonko
        "amount": 5000,
        "cooldown": 43200,
        "auto": False,
        "target": "bank"
    },
    {
        "role_id": 1365683407023243304, #Commandant
        "amount": 7500,
        "cooldown": 43200,
        "auto": False,
        "target": "bank"
    },
    {
        "role_id": 1365682918243958826, #Corsaires
        "amount": 3000,
        "cooldown": 43200,
        "auto": False,
        "target": "bank"
    },
    {
        "role_id": 1365683324831531049, #Lieutenant
        "amount": 5000,
        "cooldown": 43200,
        "auto": False,
        "target": "bank"
    },
    {
        "role_id": 1365682795501977610, #Pirates
        "amount": 1000,
        "cooldown": 43200,
        "auto": False,
        "target": "bank"
    },
    {
        "role_id": 1365683175019516054, #Matelot
        "amount": 2000,
        "cooldown": 43200,
        "auto": False,
        "target": "bank"
    },
    {
        "role_id": 1365698043684327424, #Haki de l'armement Inferieur
        "amount": 5000,
        "cooldown": 7200,
        "auto": False,
        "target": "bank"
    },
    {
        "role_id": 1365389381246124084, #Haki de l'Armement Avancé
        "amount": 10000,
        "cooldown": 7200,
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
    {
        "role_id": 1365313255471579297, #Soumsi a Nika
        "percent": -10,
        "cooldown": 86400,
        "auto": True,
        "target": "bank"
    },
    {
        "role_id": 1365313257279062067, #Gol Gol no Mi
        "percent": 3,
        "cooldown": 86400,
        "auto": True,
        "target": "bank"
    },
    {
        "role_id": 1365313261129568297, #Gear Second
        "percent": 5,
        "cooldown": 3600,
        "auto": True,
        "target": "bank"
    },
    {
        "role_id": 1365312301900501063, #Nika Collect
        "percent": 500,
        "cooldown": 3600,
        "auto": True,
        "target": "bank"
    },
    {
        "role_id": 1365313287964725290, #Soumis Bourrasque Devastatrice
        "percent": -50,
        "cooldown": 3600,
        "auto": True,
        "target": "bank"
    },
    {
        "role_id": 1365312292069048443, #Tonnere Divin
        "percent": -70,
        "cooldown": 86400,
        "auto": True,
        "target": "bank"
    },
    {
        "role_id": 1355903910635770098, #God of Glory
        "amount": 12500,
        "cooldown": 86400,
        "auto": False,
        "target": "bank"
    },
    {
        "role_id": 1034546767104069663, #Booster
        "amount": 5000,
        "cooldown": 7200,
        "auto": False,
        "target": "bank"
    },
    {
        "role_id": 1363974710739861676, #Collect Bank
        "percent": 1,
        "cooldown": 3600,
        "auto": True,
        "target": "bank"
    },
    {
        "role_id": 1363948445282341135, #Mode Ermite
        "amount": 5000,
        "cooldown": 7200,
        "auto": False,
        "target": "bank"
    },
    {
        "role_id": 1355157729362313308, #Grade E
        "amount": 1000,
        "cooldown": 7100,
        "auto": False,
        "target": "bank"
    },
    {
        "role_id": 1355157728024072395, #Grade D
        "amount": 2000,
        "cooldown": 7100,
        "auto": False,
        "target": "bank"
    },
    {
        "role_id": 1355157726032035881, #Grade C
        "amount": 3000,
        "cooldown": 7100,
        "auto": False,
        "target": "bank"
    },
    {
        "role_id": 1355157725046243501, #Grade B
        "amount": 4000,
        "cooldown": 7100,
        "auto": False,
        "target": "bank"
    },
    {
        "role_id": 1355157723960049787, #Grade A
        "amount": 5000,
        "cooldown": 7100,
        "auto": False,
        "target": "bank"
    },
    {
        "role_id": 1355157722907279380, #Grade S
        "amount": 6000,
        "cooldown": 7100,
        "auto": False,
        "target": "bank"
    },
    {
        "role_id": 1355157721812435077, #Grade National
        "amount": 7000,
        "cooldown": 7100,
        "auto": False,
        "target": "bank"
    },
    {
        "role_id": 1355157720730439701, #Grade Etheryens
        "amount": 8000,
        "cooldown": 7100,
        "auto": False,
        "target": "bank"
    },
    {
        "role_id": 1367567412886765589, #Grade Divin
        "amount": 8000,
        "cooldown": 3600,
        "auto": False,
        "target": "bank"
    },
    {
        "role_id": 1372978490256920586, #Grade Divin
        "amount": 5000,
        "cooldown": 3600,
        "auto": False,
        "target": "bank"
    }
]

TOP_ROLES = {
    1: 1363923497885237298,  # ID du rôle Top 1
    2: 1363923494504501510,  # ID du rôle Top 2
    3: 1363923356688056401,  # ID du rôle Top 3
}

# Fonctions utilitaires pour l'économie (déplacées de eco0.py)
async def check_user_has_item(db_collections, user: discord.Member, item_id: int):
    # Ici tu devras interroger la base de données MongoDB ou autre pour savoir si l'utilisateur possède cet item
    # Par exemple:
    result = db_collections["joueur_ether_inventaire"].find_one({"user_id": user.id, "item_id": item_id})
    return result is not None

def get_cf_config_eco(db_collections, guild_id):
    config = db_collections["info_cf"].find_one({"guild_id": guild_id})
    if not config:
        # Valeurs par défaut
        config = {
            "guild_id": guild_id,
            "start_chance": 50,
            "max_chance": 100,
            "max_bet": 20000
        }
        db_collections["info_cf"].insert_one(config)
    return config

async def initialize_bounty_or_honor(db_collections, user_id, is_pirate, is_marine):
    # Vérifier si le joueur est un pirate et n'a pas encore de prime
    if is_pirate:
        bounty_data = db_collections["ether_bounty"].find_one({"user_id": user_id})
        if not bounty_data:
            # Si le joueur n'a pas de prime, initialiser à 50
            db_collections["ether_bounty"].insert_one({"user_id": user_id, "bounty": 50})

    # Vérifier si le joueur est un marine et n'a pas encore d'honneur
    if is_marine:
        honor_data = db_collections["ether_honor"].find_one({"user_id": user_id})
        if not honor_data:
            # Si le joueur n'a pas d'honneur, initialiser à 50
            db_collections["ether_honor"].insert_one({"user_id": user_id, "honor": 50})

def get_or_create_user_data(db_collections, guild_id: int, user_id: int):
    data = db_collections["ether_eco"].find_one({"guild_id": guild_id, "user_id": user_id})
    if not data:
        data = {"guild_id": guild_id, "user_id": user_id, "cash": 1500, "bank": 0}
        db_collections["ether_eco"].insert_one(data)
    return data

# Placeholder pour les badges, à définir si nécessaire
BADGES = [] 

def insert_badge_into_db(db_collections):
    # Insérer les badges définis dans la base de données MongoDB
    for badge in BADGES:
        # Vérifier si le badge est déjà présent
        if not db_collections["ether_badge"].find_one({"id": badge["id"]}):
            db_collections["ether_badge"].insert_one(badge)

# Fonction pour enregistrer un message du joueur dans la base de données
async def enregistrer_message_jour(db_collections, user_id, message_content):
    date_aujourdhui = datetime.utcnow().strftime('%Y-%m-%d')
    db_collections["message_jour"].update_one(
        {"user_id": user_id, "date": date_aujourdhui},
        {"$push": {"messages": message_content}},
        upsert=True
    )

# Fonctions pour les vues (déplacées ici pour être importables)
class GuideView(View):
    def __init__(self, thread):
        super().__init__(timeout=180) # Ajout d'un timeout
        self.thread = thread
        self.message_sent = False

    @discord.ui.button(label="📘 Guide", style=discord.ButtonStyle.success, custom_id="guide_button_unique")
    async def guide(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.message_sent:
            await interaction.response.defer()
            await start_tutorial(self.thread, interaction.user)
            self.message_sent = True
            button.disabled = True # Désactiver le bouton après utilisation
            await interaction.message.edit(view=self) # Mettre à jour la vue

    @discord.ui.button(label="❌ Non merci", style=discord.ButtonStyle.danger, custom_id="no_guide_button_unique")
    async def no_guide(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🔒 Fermeture du fil...", ephemeral=True)
        await asyncio.sleep(2)
        await self.thread.delete()

class NextStepView(View):
    def __init__(self, thread):
        super().__init__(timeout=180) # Ajout d'un timeout
        self.thread = thread

    @discord.ui.button(label="➡️ Passer à la suite", style=discord.ButtonStyle.primary, custom_id="next_button")
    async def next_step(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        user = interaction.user

        await send_economy_info(user)

        await self.thread.send("📩 Les détails de cette étape ont été envoyés en message privé.")
        await asyncio.sleep(2)
        await self.thread.send("🗑️ Ce fil sera supprimé dans quelques instants.")
        await asyncio.sleep(3)
        await self.thread.delete()

async def wait_for_command(thread, user, command):
    def check(msg):
        return msg.channel == thread and msg.author == user and msg.content.startswith(command)

    await thread.send(f"🕒 En attente de `{command}`...")
    await thread.bot.wait_for("message", check=check) # Utiliser thread.bot pour accéder au bot
    await thread.send("✅ Commande exécutée ! Passons à la suite. 🚀")
    await asyncio.sleep(2)

async def start_tutorial(thread, user):
    tutorial_steps = [
        ("💼 **Commande Travail**", "Utilise `!!work` pour gagner un salaire régulièrement !", "!!work"),
        ("📦 **Commande Quotidient**", "Utilise !!daily pour gagner un salaire quotidient !", "!!daily"),
        ("💃 **Commande Slut**", "Avec `!!slut`, tente de gagner de l'argent... Mais attention aux risques !", "!!slut"),
        ("🔫 **Commande Crime**", "Besoin de plus de frissons ? `!!crime` te plonge dans des activités illégales !", "!!crime"),
        ("🌿 **Commande Collecte**", "Avec `!!collect`, tu peux ramasser des ressources utiles !", "!!collect"),
        ("📊 **Classement**", "Découvre qui a le plus d'argent en cash avec `!!lb -cash` !", "!!lb -cash"),
        ("🕵️ **Voler un joueur**", "Tente de dérober l'argent d'un autre avec `!!rob @user` !", "!!rob"),
        ("🏦 **Dépôt Bancaire**", "Pense à sécuriser ton argent avec `!!dep all` !", "!!dep all"),
        ("💰 **Solde Bancaire**", "Vérifie ton argent avec `!!bal` !", "!!bal"),
    ]

    for title, desc, cmd in tutorial_steps:
        embed = discord.Embed(title=title, description=desc, color=discord.Color.blue())
        await thread.send(embed=embed)
        await wait_for_command(thread, user, cmd)

    games_embed = discord.Embed(
        title="🎲 **Autres Commandes de Jeux**",
        description="Découvre encore plus de moyens de t'amuser et gagner des Ezryn Coins !",
        color=discord.Color.gold()
    )
    games_embed.add_field(name="🐔 Cock-Fight", value="`!!cf <amount>` - Combat de Poulet !", inline=False)
    games_embed.add_field(name="🃏 Blackjack", value="`!!bj <amount>` - Jeux de Carte !", inline=False)
    games_embed.add_field(name="🎰 Slot Machine", value="`!!sm <amount>` - Tente un jeu risqué !", inline=False)
    games_embed.add_field(name="🔫 Roulette Russe", value="`!!rr <amount>` - Joue avec le destin !", inline=False)
    games_embed.add_field(name="🎡 Roulette", value="`!!roulette <amount>` - Fais tourner la roue de la fortune !", inline=False)
    games_embed.set_footer(text="Amuse-toi bien sur Etherya ! 🚀")

    await thread.send(embed=games_embed)
    await thread.send("Clique sur **Passer à la suite** pour découvrir les systèmes impressionnants de notre Economie !", view=NextStepView(thread))

async def send_economy_info(user: discord.Member):
    try:
        economy_embed = discord.Embed(
            title="📌 **Lis ces salons pour optimiser tes gains !**",
            description=(
                "Bienvenue dans l'économie du serveur ! Pour en tirer le meilleur profit, assure-toi de lire ces salons :\n\n"
                "💰 **Comment accéder à l'economie ?**\n➜ <#1355190022047011117>\n\n"
                "📖 **Informations générales**\n➜ <#1355158018517500086>\n\n"
                "💰 **Comment gagner des Coins ?**\n➜ <#1355157853299675247>\n\n"
                "🏦 **Banque de l'Économie **\n➜ <#1364531840144244819>\n\n"
                "🎟️ **Ticket Finances** *(Pose tes questions ici !)*\n➜ <#1355157942005006558>\n\n"
                "📈 **Astuce :** Plus tu en sais, plus tu gagnes ! Alors prends quelques minutes pour lire ces infos. 🚀"
            ),
            color=discord.Color.gold()
        )
        economy_embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1168755764760559637.webp?size=96&quality=lossless")
        economy_embed.set_footer(text="Bon jeu et bons profits ! 💰")

        dm_channel = await user.create_dm()
        await dm_channel.send(embed=economy_embed)
    except discord.Forbidden:
        print(f"Impossible d'envoyer un MP à {user.name} ({user.id})")

# Placeholder pour TicketView et ClaimCloseView (à définir si elles sont utilisées ailleurs)
class TicketView(View):
    def __init__(self, author_id):
        super().__init__(timeout=None)
        self.author_id = author_id

class ClaimCloseView(View):
    def __init__(self):
        super().__init__(timeout=None)

