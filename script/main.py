# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
import json
from discord.errors import Forbidden
import random
import logging
from colorlog import ColoredFormatter
import time
import uuid
import traceback
import os



# A Quark group bot
# Quark-dev.com---2024
VERSION = "3.5"

# LOG system

bot_logger = logging.getLogger(__name__)

#créer les handlers
bot_handler1 = logging.FileHandler("./files/logs/discord.log")
bot_console_handler = logging.StreamHandler()

#créer les formats
formatter =  logging.Formatter("[%(asctime)s - %(levelname)s]%(name)s: %(message)s")
coloredFormat = ColoredFormatter("%(log_color)s[%(asctime)s - %(levelname)s]%(name)s: %(message)s",datefmt=None,
    reset=True,
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    })

#ajouter les format
bot_console_handler.setFormatter(coloredFormat)
bot_handler1.setFormatter(formatter)

#set le logging level
bot_logger.setLevel(logging.INFO)

#ajouter les handlers
bot_logger.addHandler(bot_console_handler)
bot_logger.addHandler(bot_handler1)

# END LOG system





#Get inv func
async def get_inv(id : int):
    if os.path.exists(f"./files/inventory/{str(id)}.json"):
        with open(f"./files/inventory/{str(id)}.json") as f:
            data = json.load(f)
    else :
        #retrun nothing if there's nothing to :/
        data = {}
       
    return data



#save inv func
async def save_inv(data : dict, id : int):
    with open(f"./files/inventory/{str(id)}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)





#A func to get .json data into dict
def get_data(path : str) -> dict:
   #get json data
    with open(path) as f:
        data = json.load(f)
       
    return data




#A func to save dict data into .json
def save_data(path : str, data : dict) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)




# Get configuration.json
with open("./files/configuration.json", "r") as config:
    config_data = json.load(config)
    token = config_data["token"]
    prefix = config_data["prefix"]
    team_member_id = config_data["team_members_id"]
  
  
    
#Get Yo-kai lists :
with open("./files/yokai_list.json") as yokai_list:
    yokai_data = json.load(yokai_list)
    list_len = {
        "E" : len(yokai_data["E"]["yokai_list"]),
        "D" : len(yokai_data["D"]["yokai_list"]),
        "C" : len(yokai_data["C"]["yokai_list"]),
        "B" : len(yokai_data["B"]["yokai_list"]),
        "A" : len(yokai_data["A"]["yokai_list"]),
        "S" : len(yokai_data["S"]["yokai_list"]),
        "LegendaryS" : len(yokai_data["LegendaryS"]["yokai_list"]),
        "treasureS" : len(yokai_data["treasureS"]["yokai_list"]),
        "DivinityS" : len(yokai_data["DivinityS"]["yokai_list"]),
        "SpecialS" : len(yokai_data["SpecialS"]["yokai_list"]),
        "Boss" : len(yokai_data["Boss"]["yokai_list"])
    }
#Make the class list and the proba    
Class_list = ['E', 'D', 'C', 'B', 'A', 'S', 'LegendaryS', "treasureS", "SpecialS", 'DivinityS', "Boss"]
Proba_list = [0.4175, 0.2, 0.12, 0.12, 0.08, 0.04, 0.0075, 0.0075, 0.0075, 0.005, 0.0025]



#A func that convert class-id to class name and reverse
def classid_to_class(id, reverse : bool = False):
    if reverse == False :
        return yokai_data[id]["class_name"]
    else :
        for classes in yokai_data :
            if yokai_data[classes]["class_name"] == id :
                return classes
        
    #return nothing if the id or the name was not fund    
    return ""





#get image list :
with open("./files/bot-data.json") as bot_data:
    bot_data = json.load(bot_data)
    image_link = {}
    for link in bot_data["image_link"]:
        image_link[link] = bot_data["image_link"][link]
        
    emoji = {}
    for emojis in bot_data["emoji"] :
        emoji[emojis] = bot_data["emoji"][emojis]



# Embeds
async def send_embed(ctx, embed):
    """
    Function that handles the sending of embeds
    -> Takes context and embed to send
    - tries to send embed in channel
    - tries to send normal message when that fails
    - tries to send embed private with information about missing permissions
    If this all fails: https://youtu.be/dQw4w9WgXcQ
    """
    try:
        await ctx.send(embed=embed)
    except Forbidden:
        try:
            await ctx.send("Hey, seems like I can't send embeds. Please check my permissions :)")
        except Forbidden:
            await ctx.author.send(
                f"Hey, seems like I can't send any message in {ctx.channel.name} on {ctx.guild.name}\n"
                f"May you inform the server team about this issue? :slight_smile: ", embed=embed)




 
# Error manager
async def mk_error_file(error, ctx, command):
    error_trace = traceback.format_exc()

    error_info = ("\nError message :"
                  f"\n{error_trace}"
                  "\n"
                  f"\n- Nom d'utilisateur / id : {ctx.author.name}/{ctx.author.id}" 
                  f"\n- Heure de l'erreur : {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}"
                  f"\n- Commande qui a causé l'erreur : {command}")
    file_name = uuid.uuid4()
    
    with open(f"./files/error/{file_name}.txt", "w", encoding="utf-8") as f:
        f.write(error_info)
    
    error_embed = discord.Embed(
                title="Oh non, une erreur s'est produite !",
                description="Vous pouvez réessayez plus tard. Ou transmettres les info suivantes :",
                color= discord.Color.red()
            )
    error_embed.add_field(name="Information :",
                          value=f"> - Code d'erreur : {file_name}")
    error_embed.add_field(name="Merci de transmettre le code d'erreur à :",
                          value="> **DM :** `__hubble`",
                          inline=False)
    await ctx.send(embed=error_embed)
    return error_info

 
 
   



# Help cog
class Help(commands.Cog):
    """
    Envoie ce message d'aide
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="help")
    # @commands.bot_has_permissions(add_reactions=True,embed_links=True)
    async def help(self, ctx, input : str = ""):
        """Affiche tous les modules de ce bot"""
        #Log
        bot_logger.info(f"{ctx.author.name} a utilisé le /help dans {ctx.guild.name}")
        

        input = tuple(input.split())


        # !SET THOSE VARIABLES TO MAKE THE COG FUNCTIONAL!
        prefix = '.'  # METTEZ VOTRE PRÉFIXE - chargé depuis la config, en string ou comme vous voulez !
        version = VERSION  # indiquez la version de votre code

        # Paramétrage du nom du propriétaire - si vous ne voulez pas être mentionné, supprimez ces lignes et ajustez le texte d'aide
        owner = 882241177578004542  # ENTREZ VOTRE ID DISCORD
        owner_name = '__hubble'  # ENTREZ VOTRE NOM D'UTILISATEUR#1234
        
        co_owner = 902270379186323487
        co_owner_name = "Mart1Max"

        serv_discord = "https://discord.gg/K4H4xhHqUb"

        # Vérifie si un paramètre de cog a été donné
        # sinon : envoie tous les modules et commandes non associés à un cog
        if not input:
            # Vérifie si le propriétaire est sur ce serveur - utilisé pour 'taguer' le propriétaire
            try:
                owner = ctx.guild.get_member(owner).mention

            except AttributeError:
                owner = owner_name

            try:
                co_owner = ctx.guild.get_member(co_owner).mention

            except AttributeError:
                co_owner = co_owner_name
                
                
            # Commence à construire l'embed
            emb = discord.Embed(title='Commandes et modules', color=discord.Color.blue(),
                                description=f'Utilisez `{prefix}help <module>` pour obtenir plus d\'informations sur ce module '
                                            f':smiley:\n')

            # Itère à travers les cogs et récupère les descriptions
            cogs_desc = ''
            for cog in self.bot.cogs:
                cogs_desc += f'`{cog}` {self.bot.cogs[cog].__doc__}\n'

            # Ajoute la 'liste' des cogs à l'embed
            emb.add_field(name='Modules', value=cogs_desc, inline=False)

            # Itère à travers les commandes non classées
            commands_desc = ''
            for command in self.bot.walk_commands():
                # Si la commande n'est pas dans un cog
                # Liste la commande si le nom du cog est None et que la commande n'est pas cachée
                if not command.cog_name and not command.hidden:
                    commands_desc += f'{command.name} - {command.help}\n'

            # Ajoute ces commandes à l'embed
            if commands_desc:
                emb.add_field(name='Ne faisant pas partie d\'un module', value=commands_desc, inline=False)

            # Ajoute des informations sur l'auteur
            emb.add_field(name="À propos", value=f"Le bot est développé par {owner}, basé sur discord.py. La liste des Yokais est faite par {co_owner} \n\
                                    ")
            emb.add_field(name="Serveur discord de support :", value=f"{serv_discord}", inline=False)
            emb.set_footer(text=f"bot version {version}")

        # Bloc appelé lorsqu'un seul nom de cog est donné
        # Tente de trouver le cog correspondant et ses commandes
        elif len(input) == 1:

            # Itère à travers les cogs
            for cog in self.bot.cogs:
                # Vérifie si le cog est celui correspondant
                if cog.lower() == input[0].lower():

                    # Crée un titre - récupère la description à partir de la doc-string sous la classe
                    emb = discord.Embed(title=f'{cog} - Commandes', description=self.bot.cogs[cog].__doc__,
                                        color=discord.Color.green())

                    # Récupère les commandes du cog
                    for command in self.bot.get_cog(cog).get_commands():
                        # Si la commande n'est pas cachée
                        if not command.hidden:
                            emb.add_field(name=f"`{prefix}{command.name}`", value=command.help, inline=False)
                    # Cog trouvé - sortir de la boucle
                    break

            # Si le module demandé n'est pas trouvé
            else:
                emb = discord.Embed(title="Qu'est-ce que c'est ?!",
                                    description=f"Je n'ai jamais entendu parler d'un module appelé `{input[0]}` :scream:",
                                    color=discord.Color.orange())

        # Trop de modules demandés - un seul à la fois est autorisé
        elif len(input) > 1:
            emb = discord.Embed(title="C'est trop.",
                                description="Merci de ne demander qu'un module à la fois :sweat_smile:",
                                color=discord.Color.orange())

        else:
            emb = discord.Embed(title="C'est un endroit magique.",
                                description="Je ne sais pas comment vous êtes arrivé ici. Je ne m'attendais vraiment pas à ça.\n"
                                            "Pourriez-vous s'il vous plaît signaler ce problème En dm ?\n"
                                            "__hubble"
                                            "Merci !",
                                color=discord.Color.red())

        
        
        """else:
            emb = discord.Embed(title="C'est un endroit magique.",
                                description="Je ne sais pas comment vous êtes arrivé ici. Je ne m'attendais vraiment pas à ça.\n"
                                            "Pourriez-vous s'il vous plaît signaler ce problème sur github ?\n"
                                            "https://github.com/nonchris/discord-fury/issues\n"
                                            "Merci ! ~Chris",
                                color=discord.Color.red())"""

        # Envoie la réponse embed en utilisant notre propre fonction définie ci-dessus
        await send_embed(ctx, emb)


#Bot admin commands
class Admin_command(commands.Cog):
    """
    Commande d'administration. Utilisable seulement par l'équipe de développement.

    """
    
    
    
    
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    
    
    
    
    
    @commands.command(name="reset")
    async def reset(self, ctx, input_id : str):
        """
        Reset le Médallium de l'utilisateur donné.
        """
        
        try :
            #verify if author is in the Admin list.
            verify = False
            for ids in team_member_id :
                if ctx.author.id == ids :
                    verify = True
                    break
                    
            if verify == True :
                #is the input id fine ?
                try:
                    int(input_id)
                except :
                    error_embed = discord.Embed(
                        title="Merci de fournir un identifiant corect !",
                        color= discord.Color.red()
                    )
                    return await send_embed(ctx, error_embed)
                
                #is the inv already empty ?
                brute_inventory = await get_inv(input_id)

                if brute_inventory == {}:
                    error_embed = discord.Embed(
                    title="Le Médallium de cette utilisateur est déjà vide !",
                    color= discord.Color.red()
                )
                    return await send_embed(ctx, error_embed)
                
                #empt the inv and send the message
                brute_inventory = {}
                await save_inv(brute_inventory, input_id)
                sucess_embed = discord.Embed(
                    title="Le Médallium de cette utilisateur a été vidé !",
                    color= discord.Color.green()
                )
                #Log
                bot_logger.warning(f"{ctx.author.name} a utilisé le /reset dans {ctx.guild.name}")
                return await send_embed(ctx, sucess_embed)
                    
                    
            #if member is not in the admin team        
            else :
                error_embed = discord.Embed(
                    title="Vous n'êtes pas dans l'équipe de développement.",
                    description="Vous n'avez pas la permission de faire ceci !",
                    color= discord.Color.red()
                )
                bot_logger.warning(f"{ctx.author.name} n'avais pas les permissions pour utiliser le /reset dans {ctx.guild.name}")
                return await send_embed(ctx, error_embed)
            
            
        #Main exception
        except Exception as e:
            error = await mk_error_file(e, ctx, command="reset")
            bot_logger.error(error)
    
    
    
    @commands.command(name="stats")
    async def stats(self, ctx, input):
        """give stats about input data."""
        
        try:
            
            #verify if author is in the Admin list.
            verify = False
            for ids in team_member_id :
                if ctx.author.id == ids :
                    verify = True
                    break
                
            if verify == False :
                error_embed = discord.Embed(
                    title="Vous n'êtes pas dans l'équipe de développement.",
                    description="Vous n'avez pas la permission de faire ceci !",
                    color= discord.Color.red()
                )
                bot_logger.warning(f"{ctx.author.name} n'avais pas les permissions pour utiliser le /stats dans {ctx.guild.name}, sur l'input {input}")
                return await send_embed(ctx, error_embed)
            
            
            
            if input == "inventory":

                total_user = 0
                total_size = 0
                for dirpath, dirnames, filenames in os.walk("./files/inventory"):
                    for f in filenames:
                        fp = os.path.join(dirpath, f)
                        # skip if it is symbolic link
                        if not os.path.islink(fp):
                            total_user += 1
                            total_size += os.path.getsize(fp)
                
                #mk the embed
                stats_embed = discord.Embed(color=discord.Color.green(), title="Voici les stats de l'inventaire :")
                stats_embed.add_field(name="Le nombre d'utilisateurs qui ont un inventaire :", value=f"`{total_user}` utilisateurs", inline=False)
                stats_embed.add_field(name="Taille du dossier `inventory`", value=f"`{total_size}` octet", inline=False)
                bot_logger.warning(f"{ctx.author.name} a utilisé le /stats dans {ctx.guild.name}, sur l'input {input}")
                return await send_embed(ctx, stats_embed)
                        
        
        
        #Main exception
        except Exception as e :
            error = await mk_error_file(e, ctx, command="stats")
            bot_logger.error(error)
            
        
        
        
        
    @commands.command(name="give")
    async def give(self, ctx, input_id : int, yokai : str, rang : str, number = "1" ):
        """
        Give un Yo-kai à un utilisateur donné.
        `.give {id de l'utilisateur} {"yokai"} {rang} {quantité}`
        """
        
        try :
            #verify if author is in the Admin list.
            verify = False
            for ids in team_member_id :
                if ctx.author.id == ids :
                    verify = True
                    break
                    
            if verify == False :
                error_embed = discord.Embed(
                    title="Vous n'êtes pas dans l'équipe de développement.",
                    description="Vous n'avez pas la permission de faire ceci !",
                    color= discord.Color.red()
                )
                bot_logger.warning(f"{ctx.author.name} n'avais pas les permissions pour utiliser le /give dans {ctx.guild.name}, sur l'input {input_id}")
                return await send_embed(ctx, error_embed)
            
            
            
            
            
            #First, verify if the command is used to mod the inv .json directly
            if rang == "json-mod" :
                    #we format the input as we can :
                    #try into a int
                    try : 
                        number = int(number)
                    except :
                        pass
                    
                    
                    
                    #verify if the inv is empty :
                    inv = await get_inv(input_id)
                    if inv == {}:
                        inv = {
                                "last_claim" : 10000,
                                "E" : 0,
                                "D" : 0,
                                "C" : 0,
                                "B" : 0,
                                "A" : 0,
                                "S" : 0,
                                "LegendaryS" : 0,
                                "treasureS" : 0,
                                "SpecialS" : 0,
                                "DivinityS" : 0,
                                "Boss" : 0
                            }
                        
                    #now, mod the json as asked
                    inv[yokai] = number
                    await save_inv(inv, input_id)
                    sucess_embed = discord.Embed(title=f"La valeur `{yokai}` a été modifié sur `{number}` dans le Médallium de `{input_id}`",
                                                color=discord.Color.green(),
                                                description=""
                                                )
                    bot_logger.warning(msg=f"{ctx.author.name} a utilisé le /give sur l'id {input_id}, en mode json-mod")
                    return await ctx.send(embed=sucess_embed)
                        
                    
            
            
            
            
            
            
            #so, now that we know that the command is used to give a yokai, we have to: 
            # format the input:
            try :
                number = int(number)
            
            except :
                error_embed = discord.Embed(
                        title="La quantité fournie n'est pas valide.",
                        description="Merci de verifier si la commande est utilisée de manière valide (`/help Admin_command`)",
                        color= discord.Color.red()
                    )
                return await send_embed(ctx, error_embed)
            
            
            
            
            
            
            #Verify if the class (rang) is fine :
            class_name = rang
            class_id = classid_to_class(class_name, True)
            if class_id == "" :
                #if the class does not exist, it return "" and we can catch it
                error_embed = discord.Embed(
                    title="Le rang fourni n'est pas valide.",
                    description="Merci de verifier si la commande est utilisée de manière valide (`/help Admin_command`)",
                    color= discord.Color.red()
                )
                return await send_embed(ctx, error_embed)
            

            
            
            
            #Verify if the input id has an inventory file :
            inv = await get_inv(input_id)
            if inv == {}:
                inv = {
                        "last_claim" : 10000,
                        "E" : 0,
                        "D" : 0,
                        "C" : 0,
                        "B" : 0,
                        "A" : 0,
                        "S" : 0,
                        "LegendaryS" : 0,
                        "treasureS" : 0,
                        "SpecialS" : 0,
                        "DivinityS" : 0,
                        "Boss" : 0,
                        yokai : [class_name]
                    }
                inv[class_id] = 1
                if not number == 1 :
                    inv[yokai].append(int(number))
                await save_inv(data=inv, id=input_id)
                
            else :
                #we have to verify :
                # 1. If the yokai is already in the inv
                # 2. If yes, if there is already many oh this yokai
                # and we do it in range(number) to give several yokai
                for i in range(number) :
                    try:
                        inv[yokai]
                        try:
                            #stack the yokai
                            inv[yokai][1] += 1
                        except :
                            #return an exception if the yokai was not stacked
                            #so we know there is only one and we can add the mention of two yokai ( .append(2) )
                            inv[yokai].append(2)
                    except KeyError:
                        #return an exception if the yokai was not in the inv
                        #add it
                        inv[yokai] = [class_id]
                        #add one more to the yokai count of the coresponding class
                        inv[class_id] += 1
                    #save the inv
                    await save_inv(data=inv, id=input_id)
                
            sucess_embed = discord.Embed(title=f"Le(s) Yo-Kai a été ajouté au Médallium de {input_id}",
                                         color=discord.Color.green(),
                                         description=f"**{yokai}** de rang **{rang}**\n> quantité : {number}"
                                         )
            bot_logger.warning(msg=f"{ctx.author.name} a utilisé le /give sur l'id {input_id}")
            return await ctx.send(embed=sucess_embed)
                
                
        #Main exception
        except Exception as e :
            error = await mk_error_file(e, ctx, command="give")
            bot_logger.error(error)
        
    
    
    
    
    @commands.command(name="remove")
    async def remove(self, ctx, input_id : int, yokai : str, rang : str, number = "1"): 
        """
        Remove un Yo-kai à un utilisateur donné.
        `.give {id de l'utilisateur} {"yokai"} {rang}`
        """
        
        try :
            
            #first of all, format the input:
            try :
                number = int(number)
            
            except :
                error_embed = discord.Embed(
                        title="La quantité fournie n'est pas valide.",
                        description="Merci de verifier si la commande est utilisée de manière valide (`/help Admin_command`)",
                        color= discord.Color.red()
                    )
                return await send_embed(ctx, error_embed)
            
            
            #verify if author is in the Admin list.
            verify = False
            for ids in team_member_id :
                if ctx.author.id == ids :
                    verify = True
                    break
                    
            if verify == False :
                error_embed = discord.Embed(
                    title="Vous n'êtes pas dans l'équipe de développement.",
                    description="Vous n'avez pas la permission de faire ceci !",
                    color= discord.Color.red()
                )
                bot_logger.warning(f"{ctx.author.name} n'avais pas les permissions pour utiliser le /give sur l'input {input_id},  le yokai {yokai}, la quantité {number}")
                return await send_embed(ctx, error_embed)
            
            #Verify if the class (rang) is fine :
            class_name = rang
            class_id = classid_to_class(class_name, True)
            if class_id == "" :
                #if the class does not exist, it return "" and we can catch it
                error_embed = discord.Embed(
                    title="Le rang fourni n'est pas valide.",
                    description="Merci de verifier si la commande est utilisée de manière valide (`/help Admin_command`)",
                    color= discord.Color.red()
                )
                return await send_embed(ctx, error_embed)
            
            
            #Verify if the input id has an inventory file :
            inv = await get_inv(input_id)
            if inv == {}:
                error_embed = discord.Embed(
                    title=f"Ce Yo-kai n'est pas dans le Médallium de {input_id}",
                    description="Merci de verifier si la commande est utilisée de manière valide (`/help Admin_command`)",
                    color= discord.Color.red()
                )
                return await send_embed(ctx, error_embed)
                
            else :
                #we have to verify :
                # 1. If the yokai is already in the inv
                # 2. If yes, if there is already many oh this yokai
                # and we do it in range(number) to delete several yokai
                
                for i in range(number) :
                    try :
                        one_more_author = inv[yokai][1] > 1
                    
                    
                    except KeyError:
                        error_embed = discord.Embed(
                            title=f"Ce Yo-kai n'est pas dans le Médallium de {input_id}",
                            description="Merci de verifier si la commande est utilisée de manière valide (`/help Admin_command`)",
                            color= discord.Color.red()
                        )
                        return await send_embed(ctx, error_embed)
                    
                    
                    except IndexError :
                        if number - i > 1 :
                            error_embed = discord.Embed(
                                title=f"Vous avez demandé plus de Yo-kai que il n'y en a dans ce Médallium.",
                                description="Le nombre actuel dans le Médallium est : `1`",
                                color= discord.Color.red()
                            )
                            return await send_embed(ctx, error_embed)
                        one_more_author = False
                        
                    if one_more_author == True :
                        if number - i > inv[yokai][1] :
                            #return an error if the user want to remove more yokai than there is in the corespondign Medallium
                            error_embed = discord.Embed(
                                title=f"Vous avez demandé plus de Yo-kai que il n'y en a dans ce Médallium.",
                                description=f"Le nombre actuel dans le Médallium est : `{inv[yokai][1]}`",
                                color= discord.Color.red()
                            )
                            return await send_embed(ctx, error_embed)
                            
                            
                        #just remove the mention of several yokai if there are juste two
                        if inv[yokai][1] == 2:
                            inv[yokai].remove(inv[yokai][1])
                        else:
                            inv[yokai][1] -= 1
                                
                    else :
                        inv.pop(yokai)
                        inv[class_id] -= 1
                    await save_inv(data=inv, id=input_id)
                
            sucess_embed = discord.Embed(title=f"Le(s) Yo-Kai a été retiré du Médallium de {input_id}",
                                         color=discord.Color.green(),
                                         description=f"**{yokai}** de rang **{rang}** \n> quantité : {number} "
                                         )
            bot_logger.warning(msg=f"{ctx.author.name} a utilisé le /remove sur l'id {input_id}, le yokai {yokai}, la quantité {number}")
            return await ctx.send(embed=sucess_embed)
                
                
        #Main exception
        except Exception as e :
            error = await mk_error_file(e, ctx, command="remove")
            bot_logger.error(error)
        
        
        
        
        
        
        
#Medallium command cog
class Medallium(commands.Cog) :
    """
    Permet de voir votre Médallium (inventaire), tous les Yo-kai que vous avez eu avec le /yokai.
    """
    
    
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        
        
    @commands.hybrid_command(name="medallium")
    async def medallium(self, ctx, user : discord.User = None ):
        """
        Permet de voir votre Médallium (inventaire), tous les Yo-kai que vous avez eu avec le /yokai. 
        Utilisez */medallium {user}* pour voir le Médallium d'un autre utilisateur.
        """
        try :
            #log
            bot_logger.info(f"{ctx.author.name} a utilisé le /medallium dans {ctx.guild.name}")
            
            
            #define the user
            if user == None:
                user = ctx.author
                
            #Get inventory
            brute_inventory  = await get_inv(user.id)
            

            #try if the inv is empty
            if brute_inventory == {}:
                if user.id == ctx.author.id:
                    inv_embed = discord.Embed(title="Oops, votre Médallium est vide 😢!")
                else:
                    inv_embed = discord.Embed(title=f"Oops, le Médallium de {user.name} est vide 😢!")
                return await send_embed(ctx, inv_embed)
                

                
            
            #create the list :  
            yokai_per_class = {
                "E" : {},
                "D" : {},
                "C" : {},
                "B" : {},
                "A" : {},
                "S" : {},
                "treasureS" : {},
                "SpecialS" : {},
                "LegendaryS" : {},
                "DivinityS" : {},
                "Boss" : {}
                
            }
            
            #sort the Yo-kai by class
            for elements in brute_inventory:
                #Don't take any numbers
                if not type(brute_inventory[elements]) == int and not type(brute_inventory[elements]) == float :
                    categorie = brute_inventory[elements]
                    
                    #Check if it's stack
                    try :
                        count = brute_inventory[elements][1]
                    except :
                        count = 1
                    
                    #add it to the right list
                    # yokai_per_class[categorie[0]].append(elements)
                    yokai_per_class[categorie[0]][elements] = count
                    
            #sort the list alphabeticaly :
            for non_sorted_dicts in yokai_per_class :
                #get the key of teh dict and sort them
                list_key = list(yokai_per_class[non_sorted_dicts].keys())
                list_key.sort()
                
                #put the key in a dict
                sorted_dict = {i : yokai_per_class[non_sorted_dicts][i] for i in list_key}
                yokai_per_class[non_sorted_dicts] = sorted_dict
                    
            
            #Ask wich categorie the user want to show ?
            
            #Inv dropdown class

            class Inv_dropdown(discord.ui.Select):
                def __init__(self):
                    #set the options that will be in the dropdown
                    options = [
                        discord.SelectOption(label="Tout !", description="Affiche tout le Médallium si possible.", emoji="🌐"),
                        discord.SelectOption(label="E", emoji=emoji["E"]),
                        discord.SelectOption(label="D", emoji=emoji["D"]),
                        discord.SelectOption(label="C", emoji=emoji["C"]),
                        discord.SelectOption(label="B", emoji=emoji["B"]),
                        discord.SelectOption(label="A", emoji=emoji["A"]),
                        discord.SelectOption(label="S", emoji=emoji["S"]),
                        discord.SelectOption(label="Légendaire", emoji=emoji["LegendaryS"]),
                        discord.SelectOption(label="Trésor", emoji=emoji["treasureS"]),
                        discord.SelectOption(label="Spécial", emoji=emoji["SpecialS"]),
                        discord.SelectOption(label="Divinité / Enma", emoji=emoji["DivinityS"]),
                        discord.SelectOption(label="Boss", emoji=emoji["Boss"])
                    ]
                    
                    super().__init__(placeholder='Choisissez le rang que vous voulez...', min_values=1, max_values=1, options=options)
                    
                async def callback(self, interaction, ctx=ctx):
                    if self.values[0] == "Tout !" :
                        if user.id == ctx.author.id:
                            inv_embed = discord.Embed(title="Voici votre Médallium :")
                        else:
                            inv_embed = discord.Embed(title=f"Voici le Médallium de {user.name} :")

                        try :
                            for classes in yokai_per_class:
                                
                                #get the name of the class
                                yokai_list_brute = yokai_per_class[classes]
                                classes_name = classid_to_class(classes)
                                class_id = classes
                                

                                yokai_list_formated = ""
                                
                                if not yokai_list_brute == {}:
                                    for elements in  yokai_list_brute :
                                        if yokai_list_brute[elements] > 1 :
                                            yokai_list_formated += f"> {elements} **`(x{str(yokai_list_brute[elements])})`**\n"
                                        else:
                                            yokai_list_formated += f"> {elements} \n"
                                            
                                            
                                    inv_embed.add_field(name=f"Rang {classes_name} `{brute_inventory[class_id]}/{list_len[class_id]}`",
                                                        value=yokai_list_formated)
                                    inv_embed.set_author(name=f"Médallium de {user.name}")
                            return await interaction.response.send_message(embed=inv_embed)
                        except discord.errors.HTTPException as e:
                            error_embed =  discord.Embed(color=discord.Color.red(),
                                                        title="Oh non, une erreur s'est produite !",
                                                        description="> Un bug sur cette commande se produit quand le Médallium est trop grand pour être afficher. (C'est un peu un flex quand même 🙃)",
                                                        )
                            error_embed.add_field(name="Vous devez donc spécifier un rang pour que cela marche.", value="Vous pouvez utiliser le message ci-dessus.")
                            return await interaction.response.send_message(embed=error_embed)
                        
                    else :
                        asked_class = classid_to_class(self.values[0], True)
                        #get the name of the class
                        yokai_list_brute = yokai_per_class[asked_class]
                        classes_name = classid_to_class(asked_class)
                        class_id = asked_class
                              
                                
                        yokai_list_formated = ""
                                
                        if not yokai_list_brute == {}:
                            for elements in  yokai_list_brute :
                                if yokai_list_brute[elements] > 1 :
                                    yokai_list_formated += f"> {elements} **`(x{str(yokai_list_brute[elements])})`**\n"
                                else:
                                    yokai_list_formated += f"> {elements} \n"
                                            
                                            
                            inv_embed=discord.Embed(title=f"Yo-kai de Rang {classes_name} `{brute_inventory[class_id]}/{list_len[class_id]}`",
                                                description=yokai_list_formated,
                                                color=discord.Color.from_str(yokai_data[class_id]["color"])
                                                )
                            inv_embed.set_thumbnail(url=image_link[class_id])
                            inv_embed.set_author(name=f"Médallium de {user.name}")
                            return await interaction.response.send_message(embed=inv_embed)
                        else:
                            if user.id == ctx.author.id:
                                inv_embed = discord.Embed(title="Oops, votre Médallium ne contient pas de Yo-kai de ce rang 😢!")
                            else:
                                inv_embed = discord.Embed(title=f"Oops, le Médallium de {user.name} ne contient pas de Yo-kai de ce rang 😢!")
                            return await interaction.response.send_message(embed=inv_embed)
                        

            class Inv_dropdown_view(discord.ui.View):
                def __init__(self):
                    super().__init__()

                    # Adds the dropdown to our view object.
                    self.add_item(Inv_dropdown())
                    
            Dropdown = Inv_dropdown_view()
            #Create the main embed
            main_embed = discord.Embed(title="__Médallium -- Menu.__",
                      colour=0xf58f00)

            #Make the nerdy stats :
            yokai_claimed_count = ""
            for classes in yokai_per_class :

                if brute_inventory[classes] == 0 :
                    #Break if there's no yokai in the class
                    pass
                                
                elif  len(classes) == 1:
                    #If the class is only 1 letter, change the syntax
                    yokai_claimed_count += f"Yo-kai de rang **{classid_to_class(classes)}**: `{brute_inventory[classes]}/{list_len[classes]}`\n"
                    
                else :
                    yokai_claimed_count += f"Yo-kai **{classid_to_class(classes)}**: `{brute_inventory[classes]}/{list_len[classes]}`\n"
                    

            main_embed.add_field(name="Voici vos statistiques :",
                        value=yokai_claimed_count,
                        inline=True)



            main_embed.set_footer(text="Merci de choisir parmi les propositions ci-dessous pour afficher vos Yo-kai.")
            
            await ctx.send(embed=main_embed, view=Dropdown)
        
        #Main exception
        except Exception as e:
            error = await mk_error_file(e, ctx, command="medallium")
            bot_logger.error(error)

   
   
   
   
   
   
        
        
        

#Trade command cog
class Trade(commands.Cog):
    
    """
    Permet de trade un/des Yo-kai contre un/des Yo-kai avec un autre utilisateur
    """
    
    
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    
    
    @commands.hybrid_command(name="trade")
    async def trade(self, ctx, ton_yokai : str, destinataire : discord.User, son_yokai : str = ""):
        
        """
        
        **Cette commande permet d'échanger des Yo-kai entre deux utilisateurs. Elle s'utilise ainsi :**
        `/trade {Le Yo-kai que vous proposez}  {L'utilisateur avec qui vous voulez l'échanger}  {Le Yo-kai que vous voulez en retour}`

        - L'utilisateur qui exécute la commande peut annuler l'échange avant qu'il soit accepté en utilisant la réaction ❌.
        - L'utilisateur qui reçoit la proposition peut la refuser avec ❌ ou l'accepter avec ✅. Il dispose de 30 secondes avant que la demande soit annulée.
        - Vous pouvez trade plusieurs Yo-kai en les séparent par une virgule ; `/trade {Onisoi, Potache} {utilisateur} {Darabajoie, Espi}`
        
        **Si vous utilisez la commande sans spécifier de Yo-kai en échange :**
        `/trade {Le Yo-kai que vous proposez} {L'utilisateur avec qui vous voulez l'échanger}`
        Cela vous permet de donner un Yo-kai. Vous pouvez aussi en mettre plusieurs, mais la limite est de **2**.

        
        -# Note :
        -# L'équipe du support n'est en aucun cas responsable si vous échangez un Yo-kai par erreur. Aucun Yo-kai ne sera remboursé.
        """
        
        
        
        try :
            def dont_have_it_embed(who : str):
                if who == "a":
                    embed = discord.Embed(color=discord.Color.red(),
                                        title="Ce(s) Yo-kai n'est pas dans votre Médallium 🤔",
                                        description="Verifiez que l'orthographe est correct ou que vous le(s) possédez bien (`/medallium`)"
                                        )
                else:
                    embed = discord.Embed(color=discord.Color.red(),
                                        title=f"Ce(s) Yo-kai n'est pas dans le Médallium de {destinataire.name} 🤔",
                                        description=f"Verifiez que l'orthographe est correct ou que il le(s) possède bien (`/medallium {destinataire.name}`)"
                                        )
                return embed
            
            
            #Get what we need
            author_inv = await get_inv(ctx.author.id)
            recipient_inv = await get_inv(destinataire.id)
            
            #Format the yokai(s) in a tuple with separator ","
            if not son_yokai == "":
                son_yokai = tuple(son_yokai.split(sep=", "))
            ton_yokai = tuple(ton_yokai.split(sep=", "))
            
            
            
            #Do they have the yokai :
            author_have_it = False
            recipient_have_it = False
            give = False
            
            #First of all, is the command used to give ?
            if son_yokai == "" :
                give = True
                recipient_have_it = True
            
            #check if the give limit is exceed
            if give == True :
                if len(ton_yokai) > 2 :
                    error_embed = discord.Embed(color=discord.Color.red(),
                                        title="Vous ne pouvez pas donner plus de 2 Yo-kai en même temps ! 😒 (On est pas trop généreux quand même.)",
                                        description="Merci de demander un Yo-kai en retour pour se faire."
                                        )
                    return await ctx.send(embed = error_embed)
            
            #check for the author
            corect_yokai_number_author = 0
            if not author_inv == {} :
                for asked_yokai in ton_yokai:
                    for yokai in author_inv :
                        if yokai == asked_yokai:
                            corect_yokai_number_author += 1
                if len(ton_yokai) == corect_yokai_number_author:
                    author_have_it = True
                        
            
            #check for the recipient
            if give == False :
                corect_yokai_number_recipient = 0
                if not recipient_inv == {} :
                    for asked_yokai in son_yokai :
                        for yokai in recipient_inv :
                            if yokai == asked_yokai:
                                corect_yokai_number_recipient += 1
                    if len(son_yokai) == corect_yokai_number_recipient :
                        recipient_have_it = True
            else :
                if recipient_inv == {} :
                    error_embed = discord.Embed(color=discord.Color.red(),
                                        title=f"Le Medallium de {destinataire.name} est vide !",
                                        description="On va dire que j'avais la flemme de gérer ce cas, dcp dites lui de faire /yokai et relancez la commande svp."
                                        )
                    return await ctx.send(embed = error_embed)

            #if one of them don't have it 
            if not author_have_it:
                return await ctx.send(embed=dont_have_it_embed("a"))
            if not recipient_have_it :
                return await ctx.send(embed=dont_have_it_embed("r"))
            
            #format the asked yokai :
            if give == False :        
                asked_yokai_form = ""
                for asked_yokai in son_yokai :
                    asked_yokai_form += f"> Le Yo-kai **{asked_yokai}** de rang **{classid_to_class(recipient_inv[asked_yokai][0])}**\n "
            
            offered_yokai = ""
            for asked_yokai in ton_yokai :
                offered_yokai += f"> Le Yo-kai **{asked_yokai}** de rang **{classid_to_class(author_inv[asked_yokai][0])}**\n "
            
            
            if give == False :
                ask_embed = discord.Embed(color=discord.Color.green(),
                                        title=f"Demande de trade entre {ctx.author.display_name} et {destinataire.display_name} !",
                                        description="Merci de réagir avec ✅ pour accepter, ou ❌ pour annuler.\n **Vous pouvez voir les details du trade ci dessous.** \n -----------------------------------------------------"
                                        )
                ask_embed.add_field(name=f"Offre de {ctx.author.display_name} 🔀:",
                                    value=offered_yokai,
                                    inline=False
                                    )
                ask_embed.add_field(name="Contre 🔀:",
                                    value=asked_yokai_form,
                                    inline=False
                                    )
                ask_embed.set_author(name="🕰️ La demande timeout au bout de 1min.")
                
            else :
                ask_embed = discord.Embed(color=discord.Color.green(),
                                        title=f"{ctx.author.display_name} Fait un cadeau à {destinataire.display_name} !",
                                        description="Merci de réagir avec ✅ pour confirmez, ou ❌ pour annuler.\n **Vous pouvez voir les details ci dessous.** \n -----------------------------------------------------"
                                        )
                ask_embed.add_field(name=f"Offre de {ctx.author.display_name} 🔀:",
                                    value=offered_yokai,
                                    inline=False
                                    )
                ask_embed.set_author(name="🕰️ L'offre timeout au bout de 1min.")
            
            #Send the message to ask
            ask_message = await ctx.send(embed=ask_embed)
            await ask_message.add_reaction("✅")
            await ask_message.add_reaction("❌")
            if give == False :
                bot_logger.info(f"{ctx.author.name} a demandé un trade à {destinataire.name}, il demande {son_yokai} contre {ton_yokai}, dans {ctx.guild.name}")
            else :
                bot_logger.info(f"{ctx.author.name} a fait un cadeau à {destinataire.name}, il offre {ton_yokai}, dans {ctx.guild.name}")
                
            #How to check for the reaction
            if give == False:
                def reaction_check(reaction, user):
                    return ask_message.id == reaction.message.id and (ctx.author == user and str(reaction.emoji) == "❌") or (destinataire == user and (str(reaction.emoji) == "✅" or str(reaction.emoji) == "❌"))
                
            else :
                def reaction_check(reaction, user):
                    return ask_message.id == reaction.message.id and ctx.author == user and (str(reaction.emoji) == "✅" or str(reaction.emoji) == "❌")
                
                
                
            try :
                #wait fot reaction
                reaction, reaction_user = await bot.wait_for("reaction_add", timeout= 60, check=reaction_check)
            except TimeoutError:
                #what if no reaction after 30s
                if give == False :
                    denied_embed = discord.Embed(color=discord.Color.red(), title="🛑 Votre demande de trade a été annulée car aucune activité durant 1min.", description="Merci de relancer la commande")
                else:
                    denied_embed = discord.Embed(color=discord.Color.red(), title="🛑 Votre offre a été annulée car aucune activité durant 1min.", description="Merci de relancer la commande")
               
                return await ctx.send(embed=denied_embed)
            
            #What if the author cancel the request
            if reaction_user.id == ctx.author.id and reaction.emoji == "❌":
                if give == False:
                    denied_embed = discord.Embed(color=discord.Color.red(), title=" 🛑 Votre demande de trade a été annulée", description="Merci de relancer la commande si cela était une erreur.")
                    bot_logger.info(f"{ctx.author.name} a annulée sa demande de trade avec {destinataire.name}, dans {ctx.guild.name}")
                
                else :
                    denied_embed = discord.Embed(color=discord.Color.red(), title=" 🛑 Votre offre a été annulée", description="Merci de relancer la commande si cela était une erreur.")
                    bot_logger.info(f"{ctx.author.name} a annulée son cadeau pour {destinataire.name}, dans {ctx.guild.name}")
                
                return await ctx.send(embed=denied_embed)
            
            
            
            elif reaction_user.id == destinataire.id :
                if reaction.emoji == "❌":
                    denied_embed = discord.Embed(color=discord.Color.red(), title=" ❌ La demande de trade a été refusée", description="Merci de relancer la commande si cela était une erreur.")
                    bot_logger.info(f"{destinataire.name} a refusé la demande de trade de {ctx.author.name}, dans {ctx.guild.name}")
                    return await ctx.send(embed=denied_embed)
            
            
            #ADD the yokais in the invs
            #ADD to the author inv and +1 to the class count
            if give == False :
                for asked_yokai in son_yokai:
                    try:
                        author_inv[asked_yokai]
                        try:
                            #stack the yokai
                            author_inv[asked_yokai][1] += 1
                        except :
                            author_inv[asked_yokai].append(2)
                    except KeyError:
                        author_inv[asked_yokai] = [recipient_inv[asked_yokai][0]]
                        author_inv[author_inv[asked_yokai][0]] += 1
                    
            #ADD to the recipient inv
            for asked_yokai in ton_yokai :
                try :
                    recipient_inv[asked_yokai]
                    try :
                        #stack the Yo-kai
                        recipient_inv[asked_yokai][1] += 1
                    except :
                        recipient_inv[asked_yokai].append(2)
                except KeyError :
                    recipient_inv[asked_yokai] = [author_inv[asked_yokai][0]]
                    recipient_inv[author_inv[asked_yokai][0]] += 1
                
            
            #REMOVE the yokai from the invs
            # FIRST ; do they have more than one of this yokai ?
            for asked_yokai in ton_yokai:
                try :
                    one_more_author = author_inv[asked_yokai][1] > 1
                except :
                    one_more_author = False
                    
                
                
                if one_more_author == True :
                    #just remove the mention of several yokai if there are juste two
                    if author_inv[asked_yokai][1] == 2:
                        author_inv[asked_yokai].remove(author_inv[asked_yokai][1])
                    else:
                        author_inv[asked_yokai][1] -= 1
                        
                else :
                    author_inv.pop(asked_yokai)
                    author_inv[recipient_inv[asked_yokai][0]] -= 1
                
             
            # FIRST ; do they have more than one of this yokai ?
            if give == False :
                for asked_yokai in son_yokai :   
                    try :
                        one_more_recipient = recipient_inv[asked_yokai][1] > 1
                    except :
                        one_more_recipient = False
                    
                        
                    if one_more_recipient == True :
                        #just remove the mention of several yokai if there are juste two
                        if recipient_inv[asked_yokai][1] == 2:
                            recipient_inv[asked_yokai].remove(recipient_inv[asked_yokai][1])
                        else:
                            recipient_inv[asked_yokai][1] -= 1
                            
                    else :
                        recipient_inv.pop(asked_yokai)
                        recipient_inv[author_inv[asked_yokai][0]] -= 1
                    
            #Save the inv
            await save_inv(author_inv, ctx.author.id)
            await save_inv(recipient_inv, destinataire.id)
                
            #send the success embed
            if give == False :
                success_embed = discord.Embed(colour=discord.Color.green(),
                                            title="__**Le trade a été effectué**__ ✅",
                                            description="> Ci dessous vous pouvez vois le bilan du trade."
                                            )
                success_embed.add_field(name=f"{ctx.author.name} a eu le(s) Yo-kai :", value=asked_yokai_form, inline=False)
                success_embed.add_field(name=f"{destinataire.name} a eu le(s) Yo-kai :", value=offered_yokai, inline=False)
                
                bot_logger.info(f"{destinataire.name} a accepté le trade de {ctx.author.name}, il demandait {son_yokai} contre {ton_yokai}, dans {ctx.guild.name}")
            
            else :
                success_embed = discord.Embed(colour=discord.Color.green(),
                                            title="__**Le cadeau a bien été envoyé !**__ ✅",
                                            description="> Ci dessous vous pouvez vois le bilan."
                                            )
                success_embed.add_field(name=f"{destinataire.name} a eu le(s) Yo-kai :", value=offered_yokai, inline=False)
                bot_logger.info(f"{ctx.author.name} a offert {ton_yokai} à {destinataire.name}, dans {ctx.guild.name}")
                
            
            return await ctx.send(embed=success_embed)
            
            
        
        #Main exception
        except Exception as e:
            error = await mk_error_file(e, ctx, command="trade")
            bot_logger.error(error)










# Yokai command cog
class Yokai(commands.Cog):
    
    """
    Tire au sort un Yo-kai de manière aléatoire.
    """
    
    
    
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    @commands.hybrid_command(name="yokai")
    async def yokai(self, ctx):
        """
        **Tire au sort un Yo-kai de manière aléatoire.**
        La commande possède un cooldown de 1h30 (1h sur le serveur de support ;) )
        """
        try :
                #define the inv
                brute_inventory = await get_inv(ctx.author.id)
                
                
                #verify if the cooldown is bypassed ?
                iscooldown = True
                """for ids in team_member_id :
                    if ctx.author.id == ids :
                        iscooldown = False
                        break"""
                        
                #Verify if there is an claim in their inv
                try :
                    free_claim = brute_inventory["claim"]
                except :
                    free_claim = 0
                
                if free_claim > 0:
                    brute_inventory["claim"] -= 1
                    await save_inv(brute_inventory, ctx.author.id)
                    iscooldown = False
                    #Thx copilot for that one, i was to lasy to code it :->

                
                if iscooldown == True :
                    if brute_inventory == {}:
                        iscooldown = False
                    
                    if iscooldown == True :
                        #when is the last claim ?
                        last_claim = int(brute_inventory["last_claim"])
                        
                        #is 1h30 past last claim ?
                        #or is it 1h when executed in the support server ?
                        if ctx.guild.id == 1341432288562511914 :
                            cooldown = 3600
                            cooldown_str = "1h"
                            
                        else :
                            cooldown = 5400
                            cooldown_str = "1h30"
                        
                        
                        if not time.time() >= last_claim + cooldown :
                            
                            minimum_time_to_claim = last_claim + cooldown
                            remaining_time = time.gmtime( minimum_time_to_claim - time.time())
                            
                            yokai_embed = discord.Embed(title="Vous ne pouvez pas tirer de Yo-kai pour l'instant !",
                                                        description=f"🕰️ Merci d'attendre {cooldown_str} après votre dernier tirage. :/",
                                                        color=discord.Color.red()
                                                        )
                            yokai_embed.add_field(name="__Il vous reste :__",
                                                value=f"{remaining_time[3]}h {remaining_time[4]}min et {remaining_time[5]}s."
                                                )
                            return await send_embed(ctx, yokai_embed)
                
                
                #choose the class of the yokai
                class_choice = yokai_data[random.choices(Class_list, weights=Proba_list, k=1)[0]]
                
                #get the good name of the class and his id
                class_name = class_choice["class_name"]
                class_id = class_choice["class_id"]
                #choose the Yo-kai in the class
                Yokai_choice = random.choices(class_choice["yokai_list"])
                Yokai_choice = Yokai_choice[0]
                
                yokai_embed = discord.Embed(title=f"Vous avez eu le Yo-kai **{Yokai_choice}** ✨ ",
                                            description=f"Félicitations il est de rang **{class_name}**",
                                            color=discord.Color.from_str(yokai_data[class_id]["color"])
                                            )
                yokai_embed.set_thumbnail(url=image_link[class_id])
                bot_logger.info(f"{ctx.author.name} a utilisé le /yokai dans {ctx.guild.name}, il a eu {Yokai_choice}, de rang {class_name}")
                
                #is the Yo-kai in the inventory
                #try the inv

                if brute_inventory == {}:
                    brute_inventory = {
                    "last_claim" : time.time(),
                    "E" : 0,
                    "D" : 0,
                    "C" : 0,
                    "B" : 0,
                    "A" : 0,
                    "S" : 0,
                    "LegendaryS" : 0,
                    "treasureS" : 0,
                    "SpecialS" : 0,
                    "DivinityS" : 0,
                    "Boss" : 0,
                }
                    verification = False
                else :
                    verification = True
                        
                
                if verification == True :
                    #get all the yokais
                    for elements in brute_inventory.keys():
                        if elements == Yokai_choice:
                            try :
                                #stack the Yo-kai
                                brute_inventory[Yokai_choice][1] += 1
                            except :
                                brute_inventory[Yokai_choice].append(2)
                            
                            #Generate the embed
                            yokai_embed.add_field(name=f"Vous l'avez déjà eu. Vous en avez donc {brute_inventory[Yokai_choice][1]}", value="Faites `/medallium` pour voir votre Médallium.")
                            
                            #Set last claim
                            brute_inventory["last_claim"] = time.time()
                            #SAVE the inv
                            await save_inv(brute_inventory, ctx.author.id)
                            
                            #Send the embed
                            return await send_embed(ctx, yokai_embed)
                        
                        
                    
                    brute_inventory[Yokai_choice] = [class_id]
                    brute_inventory[class_id] += 1
                    brute_inventory["last_claim"] = time.time()
                    await save_inv(brute_inventory,  ctx.author.id)
                    yokai_embed.add_field(name="Vous ne l'avez jamais eu !", value="Il a été ajouté a votre Médallium. Faite `/medallium` pour le voir.")
                    
                else :
                    brute_inventory[Yokai_choice] = [class_id]
                    brute_inventory[class_id] += 1
                    await save_inv(brute_inventory,  ctx.author.id)
                    yokai_embed.add_field(name="Vous ne l'avez jamais eu !", value="Il a été ajouté a votre Médallium. Faite `/medallium` pour le voir.")

                #Futur update
                yokai_embed.set_author(name="Attention, cette commande sera renomée /bingo-kai.")
                          
                await send_embed(ctx, yokai_embed)
                
        #Main exception
        except Exception as e :
            error = await mk_error_file(e, ctx, command="yokai")
            bot_logger.error(error)












## create bot

class Yokai_bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix=prefix, intents=discord.Intents.all())
        
    async def setup_hook(self) -> None:
        #delete default help
        self.remove_command('help')
        #add cog
        await self.add_cog(Yokai(self))
        await self.add_cog(Medallium(self))
        await self.add_cog(Trade(self))
        await self.add_cog(Help(self))
        await self.add_cog(Admin_command(self))
        await self.tree.sync()
       
    async def on_ready(self):
        print(f"We have logged in as {bot.user}")
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name =f"/yokai || /help"))
        print(discord.__version__)
       
       
#here everythings start.
bot = Yokai_bot()

bot.run(token)