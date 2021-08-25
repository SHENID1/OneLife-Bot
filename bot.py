from datetime import datetime
import traceback
import requests
import asyncio
import sqlite3
import discord
import math
from Cybernator import Paginator as pag
from discord.ext import commands
from random import randint
from discord.ext.commands import MissingPermissions
intents = discord.Intents.default()
intents.members = True
content_error = '<Response [204]>'
client = commands.Bot( command_prefix = '!', intents=intents)

guild = 1234567890 #id сервера
role_personal_id = 1234567890 #id роли персонала
channel_ver = 1234567890  #id канала верификации
channel_log_id = 1234567890 #id канала логи
channel_OL_main = 1234567890 #id канала мессенджер
ver_role_id = 1234567890 #id роли верификации
OL_role_id = 1234567890 #id роли Игрок OneLife

client.remove_command( 'help' )
person = 'Персонал'
db = sqlite3.connect('data.db')
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS deletevercod(
    code TEXT,
    nik TEXT,
    reason TEXT
    )""")
db.commit()

sql.execute("""CREATE TABLE IF NOT EXISTS usersuuid(
    uuid TEXT,
    code TEXT
    )""")
db.commit()
sql.execute("""CREATE TABLE IF NOT EXISTS users(
    nik TEXT,
    ver TEXT
    )""")
db.commit()

sql.execute("""CREATE TABLE IF NOT EXISTS nickname(
    id TEXT,
    name TEXT,
    mine_id TEXT
    )""")
db.commit()

@client.event
async def on_ready():
 print("Бот запущен!")
 try:   
    gl = client.get_guild(guild)
    while True:
            await asyncio.sleep(5)
            for i in sql.execute(f"SELECT mine_id, name, id FROM nickname"):
                url = f'https://sessionserver.mojang.com/session/minecraft/profile/{i[0]}'
                response = requests.get(url)
                try:
                        member1 = await gl.fetch_member(i[2])
                        c = (response.json())["name"]
                        n5 = member1.display_name
                        if n5 != c:
                         await member1.edit(nick = c)
                         p = datetime.now()
                         channel_log = client.get_channel(channel_log_id)
                         embl = discord.Embed( description = f'Никнейм **`{n5}`** был изменен на **`{c}`** у игрока **<@{i[2]}>**.', color = 0x0EE829 )
                         await channel_log.send(embed = embl)
                         continue

                        elif (str(response) == content_error):
                         p = datetime.now()
                         channel_log = client.get_channel(channel_log_id)
                         embl = discord.Embed( description = f'Ошибка, ник `{i[1]}` не существует. {p}', color = 0x0EE829 )
                         await channel_log.send(embed = embl)
                         sql.execute(f"DELETE FROM nickname WHERE name = '{i[1]}'")
                         db.commit()
                         continue
                except:
                        role = discord.utils.get( gl.roles, id = OL_role_id)
                        if role in member1.roles:
                         p = datetime.now()
                         channel_log = client.get_channel(channel_log_id)
                         sql.execute(f"DELETE FROM nickname WHERE name = '{i[1]}'")
                         db.commit()
                         p = datetime.now()
                         channel_log = client.get_channel(channel_log_id)
                         embl = discord.Embed( description = f'||<@&{role_personal_id}>|| Ник **`{i[1]}`** был удален из базы данных, по причине: бот не может поменять ник.', color = 0x0EE829 )
                         await channel_log.send(embed = embl)
                         continue
                        
                else:
                    continue
 except Exception:
  embl = discord.Embed( description = f'error\n>>> {traceback.format_exc()}', color = 0x0EE829 )
  channel_log = client.get_channel(channel_log_id)
  await channel_log.send(embed = embl)

@client.command(pass_context = True)
@commands.has_permissions( administrator = True)
async def addbd(ctx, player: discord.User, nick):
 try: 
    id = player.id
    url = f"https://api.mojang.com/users/profiles/minecraft/{nick}"
    response = requests.get(url)
    sql.execute(f"SELECT name FROM nickname WHERE name = '{nick}'",)
    if(str(response)==content_error):
          emb = discord.Embed( title = f'**:negative_squared_cross_mark: Ошибка, ник `{nick}` не существует.**', color = 0x0EE829 )
          await ctx.send(embed = emb)
    elif sql.fetchone() is None:
       for ids in sql.execute(f"SELECT id FROM nickname"):    
            if str(ids[0]) == str(id):
                emb = discord.Embed( title = f'**:negative_squared_cross_mark: Ошибка, пользователь уже есть в базе данных.**', color = 0x0EE829 )
                await ctx.send(embed = emb)
                return
       mineid = (response.json())['id']
       sql.execute("INSERT INTO nickname VALUES (?, ?, ?)", (id, nick, mineid))
       db.commit()
       emb = discord.Embed( title = f'✅ Игрок **`{nick}`** был добавлен в базу данных.', color = 0x0EE829 )
       emb.set_footer(text=f'Запросил {ctx.author.name}', icon_url=ctx.author.avatar_url)
       await ctx.send(embed = emb)
       c = datetime.now()
       channel_log = client.get_channel(channel_log_id)
       embl = discord.Embed( description = f'✅ Ник - **{nick}** был добавлен в базу данных для игрока {player.mention} в {c}', color = 0x0EE829 )
       embl.set_footer(text=f'Запросил {ctx.author.name}', icon_url=ctx.author.avatar_url)
       await channel_log.send(embed = embl)

    else:
        emb = discord.Embed( title = f'**:negative_squared_cross_mark: Ошибка, ник `{nick}` уже есть в базе данных**', color = 0x0EE829 )
        await ctx.send(embed = emb)
 except Exception:
  embl = discord.Embed( description = f'error\n>>> {traceback.format_exc()}', color = 0x0EE829 )
  channel_log = client.get_channel(channel_log_id)
  await channel_log.send(embed = embl)



@client.event
async def on_member_join(member):
 try:   
    emb = discord.Embed(color = 0x0EE829 )
    emb.set_image(url = 'https://cdn.discordapp.com/attachments/283934314675306496/672873027783884830/1380ddbbd531bfa4.jpg')
    await member.send('**:wave: Хей, приветствуем тебя на сервере OneLife!\n:bulb: Для получение доступа ко всем каналам, введите верификационный код в канале - <#1234567890>\n:point_right: Получить верификационный код можно в ЛС сообщества - __https://vk.me/onelifeminemc__\n:thinking: OneLife - Это ванильный сервер по игре майнкрафт, который представляет собой RP (RolePlay) составляющие сервера. :gem:\n:cityscape: Обосновывайте города, вступайте в города, стройте, развивайтесь, выживайте - всё в ваших руках! :star2:\n:tada: Приятного времяпровождения на сервере! :zap:**', embed = emb)
 except Exception:
  embl = discord.Embed( description = f'error\n>>> {traceback.format_exc()}', color = 0x0EE829 )
  channel_log = client.get_channel(channel_log_id)
  await channel_log.send(embed = embl)

@client.command(pass_context = True)
@commands.has_permissions( administrator = True)
async def addverifycode(ctx, nik1: str):
 try:
    url = f"https://api.mojang.com/users/profiles/minecraft/{nik1}"
    response = requests.get(url)
    if(str(response)==content_error):
         id = ctx.author
         emb = discord.Embed( title = f'**:negative_squared_cross_mark: Ошибка, ник `{nik1}` не существует.**', color = 0x0EE829 )
         emb.set_footer(text=f'Запросил {ctx.author.name}', icon_url=ctx.author.avatar_url)
         await ctx.send(embed = emb)
         return
    
    else:
        list = ['a', 'b' ,'c' ,'d' ,'e' ,'f' ,'g' ,'h' ,'j' ,'k' ,'m' ,'n' ,'p' ,'q' ,'r' ,'s' ,'t' ,'u' ,'v' ,'w' ,'x' ,'y' ,'z' ,'A' ,'B' ,'C' ,'D' ,'E' ,'F' ,'G' ,'H' ,'J' ,'K' ,'M' ,'N' ,'P' ,'Q' ,'R' ,'S' ,'T' ,'U','V','W','X','Y','Z','2','3','4','5','6','7','8','9','0','1']
        sql.execute(f"SELECT nik FROM users WHERE nik = '{nik1}'",)
        if sql.fetchone() is None:
          l = []
          for i in range(6):
           value = randint(0, 55)
           l.append(list[value])
          val = "".join(l)
          try:
              mineid = (response.json())['id']
          except:
              id = ctx.author
              emb = discord.Embed( title = f'**:negative_squared_cross_mark: Ошибка, ник `{nik1}` не существует.**', color = 0x0EE829 )
              emb.set_footer(text=f'Запросил {ctx.author.name}', icon_url=ctx.author.avatar_url)
              await ctx.send(embed = emb)
              return
          sql.execute("INSERT INTO usersuuid VALUES (?, ?)", (mineid, val))
          db.commit()
          sql.execute("INSERT INTO users VALUES (?, ?)", (nik1, val))
          db.commit()
          id = ctx.author
          emb = discord.Embed( title = f'✅ Верификационный код был создан для игрока - **`{nik1}`.**', color = 0x0EE829 )
          emb.set_footer(text=f'Запросил {ctx.author.name}', icon_url=ctx.author.avatar_url)
          emb1 = discord.Embed( title = f':detective: Верификационный код для игрока - **`{nik1}`.**\n\nОтправьте игроку следующий код: **`{val}`.**', color = 0x0EE829 )
          try:
                await ctx.author.send(embed = emb1)
          except:
              await ctx.send(embed = discord.Embed( title = f'Ошибка, бот не может вам написать!\nКод можно посмотреть по команде: !bdlistVU', color = 0x0EE829 ))
          await ctx.send(embed = emb)
          p = datetime.now()
          channel_log = client.get_channel(channel_log_id)
          embl = discord.Embed( description = f'Верификационный код - ||{val}|| был создан для ника - **{nik1}** в {p}', color = 0x0EE829 )
          embl.set_footer(text=f'Запросил {ctx.author.name}', icon_url=ctx.author.avatar_url)
          await channel_log.send(embed = embl)
          await asyncio.sleep(86400)#86400
          sql.execute(f"SELECT nik FROM users WHERE nik = '{nik1}'",)
          if sql.fetchone() is None:
              return
          else:
            sql.execute("INSERT INTO deletevercod VALUES (?, ?, ?)", (val, nik1, '2'))
            db.commit()
            sql.execute(f"DELETE FROM users WHERE nik ='{nik1}'")
            db.commit()
            sql.execute(f"DELETE FROM usersuuid WHERE code ='{val}'")
            db.commit()
            p1 = datetime.now()
            channel_log = client.get_channel(channel_log_id)
            embl = discord.Embed( description = f'Срок действия верификационного кода для игрока - **`{nik1}`** истек в {p1}.', color = 0x0EE829 )
            embl.set_footer(text=f'Запросил {ctx.author.name}', icon_url=ctx.author.avatar_url)
            await channel_log.send(embed = embl)
        else:
           emb6 = discord.Embed( title = f'**:negative_squared_cross_mark: Ошибка, ник `{nik1}` уже добавлен в базу данных.**' , color = 0x0EE829 )
           emb6.set_footer(text=f'Запросил {ctx.author.name}', icon_url=ctx.author.avatar_url)
           await ctx.send(embed = emb6)
 except Exception:
        embl = discord.Embed( description = f'error\n>>> {traceback.format_exc()}', color = 0x0EE829 )
        channel_log = client.get_channel(channel_log_id)
        await channel_log.send(embed = embl)

@client.event
async def on_member_remove(member):
    member_id = member.id
    for i in sql.execute("SELECT id FROM nickname"):
     if str(i[0])==str(member_id):
      sql.execute(f"DELETE FROM nickname WHERE id ='{member_id}'")
      db.commit()
      p = datetime.now()
      channel_log = client.get_channel(channel_log_id)
      embl = discord.Embed( description = f'Пользователь {member.name} был удален из базы данных, по причине: покинул дискорд сервер.', color = 0x0EE829 )
      await channel_log.send(embed = embl)
     else:
        continue
        

@client.event
async def on_message(message):
 try:
    await client.process_commands( message )
    if (message.channel.id == channel_ver):
       await message.channel.purge( limit = 1 )
       msg = message.content
       for i in sql.execute("SELECT ver FROM users"):
           id = message.author
           if msg == i[0]:
            ver = discord.utils.get( message.guild.roles, id =ver_role_id)
            await message.author.remove_roles( ver)
            role = discord.utils.get( message.guild.roles, id = OL_role_id)
            await message.author.add_roles( role)
            emb = discord.Embed( title = ':white_check_mark: Верификационный код был активирован,\nтеперь Вам открыт доступ ко всем каналам!', color = 0x0EE829 )
            emb1 = discord.Embed( description = f'**:partying_face: {id.mention}, ввёл верификационный код и открыл доступ ко всем каналам.**', color = 0x0EE829 )
            emb1.set_author( name = f'Приветствуем новенького - {id}', icon_url = id.avatar_url )
            channel_OL = client.get_channel(channel_OL_main)
            await channel_OL.send(embed = emb1)
            try:
                await message.author.send(embed = emb)
            except:
                pass
            p1 = datetime.now()
            channel_log = client.get_channel(channel_log_id)
            embl = discord.Embed( description = f'**Игрок {message.author.mention} активировал верификационный код.**', color = 0x0EE829 )
            embl.set_footer(text=f'Ввел код {message.author.name}', icon_url=message.author.avatar_url)
            await channel_log.send(embed = embl)
            for m in sql.execute(f"SELECT uuid FROM usersuuid WHERE code ='{msg}'"):
                url = f"https://sessionserver.mojang.com/session/minecraft/profile/{m[0]}"
                response = requests.get(url)
                id2 = message.author.id
                name = (response.json())['name']
                sql.execute("INSERT INTO nickname VALUES (?, ?, ?)", (id2, name, m[0]))
                db.commit()
                await id.edit(nick = name)
                p = datetime.now()
                channel_log = client.get_channel(channel_log_id)
                embl = discord.Embed( description = f'**Данные игрока {message.author.mention} были добавлены в базу данных.**', color = 0x0EE829 )
                embl.set_footer(text=f'Запросил {message.author.name}', icon_url=message.author.avatar_url)
                await channel_log.send(embed = embl)
                sql.execute("INSERT INTO deletevercod VALUES (?, ?, ?)", (msg, name, '1'))
                db.commit()
                sql.execute(f"DELETE FROM users WHERE ver ='{msg}'")
                db.commit()
                return
       for bl in sql.execute("SELECT * FROM deletevercod"): 
            for bl in sql.execute("SELECT * FROM deletevercod"): 
             if(msg == bl[0]):
              if '1' == bl[2]:
                 emb = discord.Embed( title = '❎ Верификационный код был активирован\nПожалуйста запросите новый в ЛС сообщества', color = 0x0EE829 )   
                 try:
                    await message.author.send(embed = emb)
                 except:
                     pass
              elif '2' == bl[2]:
                 emb = discord.Embed( title = '❎ Срок действия кода истек!\nПожалуйста запросите новый в ЛС сообщества', color = 0x0EE829 )   
                 try:
                    await message.author.send(embed = emb)
                 except:
                     pass
 except Exception:
  embl = discord.Embed( description = f'error\n>>> {traceback.format_exc()}', color = 0x0EE829 )
  channel_log = client.get_channel(channel_log_id)
  await channel_log.send(embed = embl)

    
@client.command(pass_context = True)
@commands.has_permissions( administrator = True)
async def deleteallbd(ctx):
 try:
    await ctx.message.add_reaction('✅')
    await ctx.message.add_reaction('❎')
    def check(reaction, user):
            return user == ctx.author and (str(reaction.emoji) == '✅' or str(reaction.emoji) == '❎')

    try:
            reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
    except asyncio.TimeoutError:
            await ctx.send(embed=discord.Embed(description='❎ Операция была отменена.', color=0xdb0000))

    else:
            if (str(reaction) == '✅'):
                await ctx.send(
                    embed=discord.Embed(description='**:white_check_mark: Все данные игроков были удалены.**', color=0x38f433))
                sql.execute("DELETE FROM nickname")
                db.commit()
                sql.execute("DELETE FROM users")
                db.commit()
                sql.execute(f"DELETE FROM usersuuid")
                db.commit()
                p1 = datetime.now()
                channel_log = client.get_channel(channel_log_id)
                embl = discord.Embed( description = f'**Все данные в базе данных были удалены!**', color = 0x0EE829 )
                embl.set_footer(text=f'Запросил {ctx.author.name}', icon_url=ctx.author.avatar_url)
                await channel_log.send(embed = embl)
            else:
                await ctx.send(embed=discord.Embed(description='**❎ Операция была отменена.**', color=0xdb0000))
 except Exception:
  embl = discord.Embed( description = f'error\n>>> {traceback.format_exc()}', color = 0x0EE829 )
  channel_log = client.get_channel(channel_log_id)
  await channel_log.send(embed = embl)

@client.command(pass_context = True)
@commands.has_permissions( administrator = True)
async def deletebd(ctx, user):
 try:   
    sql.execute(f"SELECT name FROM nickname WHERE name = '{user}'",)
    if sql.fetchone() is None:
        emb = discord.Embed(description = f'**❎ Ошибка, ник `{user}` не найден.**', color = 0x0EE829 )
        await ctx.send(embed = emb)
    else:
        await ctx.message.add_reaction('✅')
        await ctx.message.add_reaction('❎')
        def check(reaction, userm):
            return userm == ctx.author and (str(reaction.emoji) == '✅' or str(reaction.emoji) == '❎')

        try:
            reaction, userm = await client.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send(embed=discord.Embed(description='**❎ Операция была отменена.**', color=0xdb0000))

        else:
            if (str(reaction) == '✅'):
                await ctx.send(
                    embed=discord.Embed(description=f'**:white_check_mark: Ник `{user}` был удален из базы данных**', color=0x38f433))
                p1 = datetime.now()
                channel_log = client.get_channel(channel_log_id)
                embl = discord.Embed( description = f'**Ник `{user}` был удален из базы данных.**', color = 0x0EE829 )
                embl.set_footer(text=f'Запросил {ctx.author.name}', icon_url=ctx.author.avatar_url)
                await channel_log.send(embed = embl)
                sql.execute(f"DELETE FROM nickname WHERE name = '{user}'")
                db.commit()
            else:
                await ctx.send(embed=discord.Embed(description='**❎ Операция была отменена.**', color=0xdb0000))
 except Exception:
  embl = discord.Embed( description = f'error\n>>> {traceback.format_exc()}', color = 0x0EE829 )
  channel_log = client.get_channel(channel_log_id)
  await channel_log.send(embed = embl)


@client.command(pass_context = True)
@commands.has_permissions( administrator = True)
async def bdlistMU(ctx):
 try:   
    fc = 0
    for i in sql.execute("SELECT * FROM nickname"):
        fc += 1
        continue
    fcx = math.ceil(fc/24)
    
    embed1 = discord.Embed(title="Аккаунты майнкрафт\nСтраница 1", color=0x38f433)
    embed2 = discord.Embed(title="Страница 2", color=0x38f433)
    embed3 = discord.Embed(title="Страница 3", color=0x38f433)
    embed4 = discord.Embed(title="Страница 4", color=0x38f433)
    embed5 = discord.Embed(title="Страница 5", color=0x38f433)
    embed6 = discord.Embed(title="Страница 6", color=0x38f433)
    embed7 = discord.Embed(title="Страница 7", color=0x38f433)
    embed8 = discord.Embed(title="Страница 8", color=0x38f433)
    embed9 = discord.Embed(title="Страница 9", color=0x38f433)
    embed10 = discord.Embed(title="Страница 10", color=0x38f433)
    embed11 = discord.Embed(title="Страница 11", color=0x38f433)
    embed12 = discord.Embed(title="Страница 12", color=0x38f433)
    embed13 = discord.Embed(title="Страница 13", color=0x38f433)
    embed14 = discord.Embed(title="Страница 14", color=0x38f433)
    embed15 = discord.Embed(title="Страница 15", color=0x38f433)
    embed16 = discord.Embed(title="Страница 16", color=0x38f433)
    embed17 = discord.Embed(title="Страница 17", color=0x38f433)
    embed18 = discord.Embed(title="Страница 18", color=0x38f433)
    embed19 = discord.Embed(title="Страница 19", color=0x38f433)
    embed20 = discord.Embed(title="Страница 20", color=0x38f433)
    embed21 = discord.Embed(title="Страница 21", color=0x38f433)
    embed22 = discord.Embed(title="Страница 22", color=0x38f433)
    embed23 = discord.Embed(title="Страница 23", color=0x38f433)
    embed24 = discord.Embed(title="Страница 24", color=0x38f433)
    embed25 = discord.Embed(title="Страница 25", color=0x38f433)
    embed26 = discord.Embed(title="Страница 26", color=0x38f433)
    embed27 = discord.Embed(title="Страница 27", color=0x38f433)
    embed28 = discord.Embed(title="Страница 28", color=0x38f433)
    embed29 = discord.Embed(title="Страница 29", color=0x38f433)
    embed30 = discord.Embed(title="Страница 30", color=0x38f433)
    embed31 = discord.Embed(title="Страница 31", color=0x38f433)
    embed32 = discord.Embed(title="Страница 32", color=0x38f433)
    embeds = [embed1, embed2, embed3, embed4, embed5, embed6, embed7, embed8, embed9, embed10, embed11, embed12, embed13, embed14, embed15, embed16, embed17, embed18, embed19, embed20, embed21, embed22, embed23, embed24, embed25, embed26, embed27, embed28, embed29, embed30, embed31, embed32]
    if fcx == 0:
        del embeds[1:32]
    else:
        del embeds[fcx:32]
    
    t = 0
    g1 = 1
    
    l1 = 24
    
    
    for i in sql.execute("SELECT id, name FROM nickname"):
        
        embeds[t].add_field( name = g1, value = f'Ник `{i[1]}` пользователя <@{i[0]}>' )
        
        g1 += 1
        l1 -= 1
        if l1 == 0:
            t += 1
            l1 = 24
    
    try:
        h = await ctx.author.send(embed = embed1)
        exreaction = ["⏹"]
        reactions = ["⏪", "⏩"]
            
        page = pag(client, h, only=ctx.author, use_more=False, embeds=embeds, reactions=reactions, use_exit=True, delete_message=True)
        await page.start()
    except:
        bed1 = discord.Embed(description="Бот вам не может написать!\nПожалуйста проверьте настройки конфидициальности!", color=0x38f433)
        await ctx.send(embed = bed1)
 except Exception:
  embl = discord.Embed( description = f'error\n>>> {traceback.format_exc()}', color = 0x0EE829 )
  channel_log = client.get_channel(channel_log_id)
  await channel_log.send(embed = embl)

@client.command(pass_context = True)
@commands.has_permissions( administrator = True)
async def bdlistVU(ctx):
 try:   
    g2 = 1
    l2 = 24
    
    
    lembed1 = discord.Embed(title="Аккаунты для верификации\nСтраница 1", color=0x38f433)
    lembed2 = discord.Embed(title="Страница 2", color=0x38f433)
    lembed3 = discord.Embed(title="Страница 3", color=0x38f433)
    lembed4 = discord.Embed(title="Страница 4", color=0x38f433)
    lembed5 = discord.Embed(title="Страница 5", color=0x38f433)
    lembed6 = discord.Embed(title="Страница 6", color=0x38f433)
    lembed7 = discord.Embed(title="Страница 7", color=0x38f433)
    lembed8 = discord.Embed(title="Страница 8", color=0x38f433)
    lembed9 = discord.Embed(title="Страница 9", color=0x38f433)
    lembed10 = discord.Embed(title="Страница 10", color=0x38f433)
    lembed11 = discord.Embed(title="Страница 11", color=0x38f433)
    lembed12 = discord.Embed(title="Страница 12", color=0x38f433)
    lembed13 = discord.Embed(title="Страница 13", color=0x38f433)
    lembed14 = discord.Embed(title="Страница 14", color=0x38f433)
    lembed15 = discord.Embed(title="Страница 15", color=0x38f433)
    lembed16 = discord.Embed(title="Страница 16", color=0x38f433)
    lembed17 = discord.Embed(title="Страница 17", color=0x38f433)
    lembed18 = discord.Embed(title="Страница 18", color=0x38f433) 
    lembed19 = discord.Embed(title="Страница 19", color=0x38f433)
    lembed20 = discord.Embed(title="Страница 20", color=0x38f433)
    lembed21 = discord.Embed(title="Страница 21", color=0x38f433)
    lembed22 = discord.Embed(title="Страница 22", color=0x38f433)
    lembed23 = discord.Embed(title="Страница 23", color=0x38f433)
    lembed24 = discord.Embed(title="Страница 24", color=0x38f433)
    lembed25 = discord.Embed(title="Страница 25", color=0x38f433)
    lembed26 = discord.Embed(title="Страница 26", color=0x38f433)
    lembed27 = discord.Embed(title="Страница 27", color=0x38f433)
    lembed28 = discord.Embed(title="Страница 28", color=0x38f433)
    lembed29 = discord.Embed(title="Страница 29", color=0x38f433)
    lembed30 = discord.Embed(title="Страница 30", color=0x38f433)
    lembed31 = discord.Embed(title="Страница 31", color=0x38f433)
    lembed32 = discord.Embed(title="Страница 32", color=0x38f433)
    lembeds = [lembed1, lembed2, lembed3, lembed4, lembed5, lembed6, lembed7, lembed8, lembed9, lembed10, lembed11, lembed12, lembed13, lembed14, lembed15, lembed16, lembed17, lembed18, lembed19, lembed20, lembed21, lembed22, lembed23, lembed24, lembed25, lembed26, lembed27, lembed28, lembed29, lembed30, lembed31, lembed32]
    
    j = 0
    fc = 0
    for i in sql.execute("SELECT * FROM users"):
        fc += 1
        continue
    fcx = math.ceil(fc/24)
    if fcx == 0:
        del lembeds[1:32]
    else:
        del lembeds[fcx:32]
    
    
    for i in sql.execute("SELECT nik, ver FROM users"):
        
        lembeds[j].add_field(  name = g2, value = f'Ник {i[0]}, ||{i[1]}||'  )
        
        g2 += 1
        l2 -= 1
        if l2 == 0:
            j += 1
            l2 = 24
    
    try:
        y = await ctx.author.send(embed = lembed1)
        exreaction = ["⏹"]
        reactions = ["⏪", "⏩"]
        
        page = pag(client, y, only=ctx.author, use_more=False, embeds=lembeds, reactions=reactions, use_exit=True, delete_message=True)
        await page.start()
    except:
        bed1 = discord.Embed(description="Бот вам не может написать!\nПожалуйста проверьте настройки конфидициальности!", color=0x38f433)
        await ctx.send(embed = bed1)
 except Exception:
  embl = discord.Embed( description = f'error\n>>> {traceback.format_exc()}', color = 0x0EE829 )
  channel_log = client.get_channel(channel_log_id)
  await channel_log.send(embed = embl)

@client.command(pass_context = True)
@commands.has_permissions( administrator = True)
async def verifycodecheck(ctx):
 try:   
    g2 = 1
    l2 = 24
    
    
    lembed1 = discord.Embed(title="Нерабочие коды\nСтраница 1", color=0x38f433)
    lembed2 = discord.Embed(title="Страница 2", color=0x38f433)
    lembed3 = discord.Embed(title="Страница 3", color=0x38f433)
    lembed4 = discord.Embed(title="Страница 4", color=0x38f433)
    lembed5 = discord.Embed(title="Страница 5", color=0x38f433)
    lembed6 = discord.Embed(title="Страница 6", color=0x38f433)
    lembed7 = discord.Embed(title="Страница 7", color=0x38f433)
    lembed8 = discord.Embed(title="Страница 8", color=0x38f433)
    lembed9 = discord.Embed(title="Страница 9", color=0x38f433)
    lembed10 = discord.Embed(title="Страница 10", color=0x38f433)
    lembed11 = discord.Embed(title="Страница 11", color=0x38f433)
    lembed12 = discord.Embed(title="Страница 12", color=0x38f433)
    lembed13 = discord.Embed(title="Страница 13", color=0x38f433)
    lembed14 = discord.Embed(title="Страница 14", color=0x38f433)
    lembed15 = discord.Embed(title="Страница 15", color=0x38f433)
    lembed16 = discord.Embed(title="Страница 16", color=0x38f433)
    lembed17 = discord.Embed(title="Страница 17", color=0x38f433)
    lembed18 = discord.Embed(title="Страница 18", color=0x38f433) 
    lembed19 = discord.Embed(title="Страница 19", color=0x38f433)
    lembed20 = discord.Embed(title="Страница 20", color=0x38f433)
    lembed21 = discord.Embed(title="Страница 21", color=0x38f433)
    lembed22 = discord.Embed(title="Страница 22", color=0x38f433)
    lembed23 = discord.Embed(title="Страница 23", color=0x38f433)
    lembed24 = discord.Embed(title="Страница 24", color=0x38f433)
    lembed25 = discord.Embed(title="Страница 25", color=0x38f433)
    lembed26 = discord.Embed(title="Страница 26", color=0x38f433)
    lembed27 = discord.Embed(title="Страница 27", color=0x38f433)
    lembed28 = discord.Embed(title="Страница 28", color=0x38f433)
    lembed29 = discord.Embed(title="Страница 29", color=0x38f433)
    lembed30 = discord.Embed(title="Страница 30", color=0x38f433)
    lembed31 = discord.Embed(title="Страница 31", color=0x38f433)
    lembed32 = discord.Embed(title="Страница 32", color=0x38f433)
    lembeds = [lembed1, lembed2, lembed3, lembed4, lembed5, lembed6, lembed7, lembed8, lembed9, lembed10, lembed11, lembed12, lembed13, lembed14, lembed15, lembed16, lembed17, lembed18, lembed19, lembed20, lembed21, lembed22, lembed23, lembed24, lembed25, lembed26, lembed27, lembed28, lembed29, lembed30, lembed31, lembed32]
    
    j = 0
    fc = 0
    for i in sql.execute("SELECT * FROM deletevercod"):
        fc += 1
        continue
    fcx = math.ceil(fc/24)
    if fcx == 0:
        del lembeds[1:32]
    else:
        del lembeds[fcx:32]
    
    
    for i in sql.execute("SELECT * FROM deletevercod"):
        
        lembeds[j].add_field(  name = g2, value = f'Код - `{i[0]}`\nНик - `{i[1]}`\nСлучай - `{i[2]}`'  )
        
        g2 += 1
        l2 -= 1
        if l2 == 0:
            j += 1
            l2 = 24
    
    try:
        y = await ctx.author.send(embed = lembed1)
        exreaction = ["⏹"]
        reactions = ["⏪", "⏩"]
        
        page = pag(client, y, only=ctx.author, use_more=False, embeds=lembeds, reactions=reactions, use_exit=True, delete_message=True)
        await page.start()
    except:
        bed1 = discord.Embed(description="Бот вам не может написать!\nПожалуйста проверьте настройки конфидициальности!", color=0x38f433)
        await ctx.send(embed = bed1)
 except Exception:
  embl = discord.Embed( description = f'error\n>>> {traceback.format_exc()}', color = 0x0EE829 )
  channel_log = client.get_channel(channel_log_id)
  await channel_log.send(embed = embl)

@client.command(pass_context = True)
@commands.has_permissions( administrator = True)
async def help( ctx ):
 try:   
        await ctx.message.add_reaction('❓')
        def check(reaction, userm):
            return userm == ctx.author and (str(reaction.emoji) == '❓')

        try:
            reaction, userm = await client.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            pass

        else:
            if (str(reaction) == '❓'):
                    emb = discord.Embed( title = 'Команды', description = '**!bdlistMU**\nПоказывает Базу данных данных игроков в ЛС\n\n**!bdlistVU**\nПоказывает Базу данных данных игроков для верификации в ЛС\n\n**!verifycodecheck**\nПоказывает Базу данных нерабочих кодов верификации в ЛС.\n\n**!addverifycode [ник]**\nСоздает код игроку для верификации (действует в течении 24 часов).\n\n**!addbd [@ник дс] [ник]**\nДобавить игрока в базу данных.\n\n**!deletebd [Ник]**\nУдалить пользователя из базы данных.\n\n**!deleteallbd**\nОчистить всю базу данных.'  ,color = 0x0EE829 )
                    emb.set_footer(text=f'Запросил {ctx.author.name}', icon_url=ctx.author.avatar_url)
                    await ctx.send( embed = emb)
            else:
                pass
 except Exception:
  embl = discord.Embed( description = f'error\n>>> {traceback.format_exc()}', color = 0x0EE829 )
  channel_log = client.get_channel(channel_log_id)
  await channel_log.send(embed = embl)
    
@bdlistVU.error
async def bdlistVU_error(ctx,error):

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(embed=discord.Embed(color=0xdb0000,description=':x: У вас нету прав!'))
        return

@bdlistMU.error
async def bdlistMU_error(ctx,error):

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(embed=discord.Embed(color=0xdb0000,description=':x: У вас нету прав!'))
        return

@verifycodecheck.error
async def verifycodecheck_error(ctx,error):

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(embed=discord.Embed(color=0xdb0000,description=':x: У вас нету прав!'))
        return
    
@addverifycode.error
async def addverifycode_error(ctx,error):
    
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=discord.Embed(color=0xdb0000,description=':x: Отсутсвует аргумент!'))
        return
    if isinstance(error, commands.BadArgument):
        await ctx.send(embed=discord.Embed(color=0xdb0000,description=':x: Введен неверный аргумен!'))
        return
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(embed=discord.Embed(color=0xdb0000,description=':x: У вас нету прав!'))
        return

@addbd.error
async def addbd_error(ctx,error):
    
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=discord.Embed(color=0xdb0000,description=':x: Отсутсвует аргумент!'))
        return
    if isinstance(error, commands.BadArgument):
        await ctx.send(embed=discord.Embed(color=0xdb0000,description=':x: Введен неверный аргумен!'))
        return
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(embed=discord.Embed(color=0xdb0000,description=':x: У вас нету прав!'))
        return

@deletebd.error
async def deletebd_error(ctx,error):
    
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=discord.Embed(color=0xdb0000,description=':x: Отсутсвует аргумент!'))
        return
    if isinstance(error, commands.BadArgument):
        await ctx.send(embed=discord.Embed(color=0xdb0000,description=':x: Введен неверный аргумен!'))
        return
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(embed=discord.Embed(color=0xdb0000,description=':x: У вас нету прав!'))
        return

@deleteallbd.error
async def deleteallbd_error(ctx,error):

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(embed=discord.Embed(color=0xdb0000,description=':x: У вас нету прав!'))
        return


client.run("TOKEN")