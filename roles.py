import discord
from discord.ext import commands
from .utils.dataIO import fileIO, dataIO
from .utils import checks
from __main__ import send_cmd_help, settings
from random import randint
from random import choice, shuffle
import json
import urllib.request
import requests
import os

class RoleTools:
    """Commands for assigning roles, self assigned roles, and default roles."""

    def __init__(self, bot):
        self.bot = bot
        self.rolePath = "data/roles/selfroles.json"
        self.selfrole_list = dataIO.load_json(self.rolePath)

    
    @commands.command(pass_context=True)
    async def channelid(self, ctx):
        await self.bot.say(ctx.message.channel.id)

    @commands.command(no_pm=True, pass_context=True)
    @checks.admin_or_permissions(manage_roles=True)
    #async def setrole(self, ctx, user : discord.Member, *, role : discord.Role):
    async def setrole(self, ctx, user : discord.Member, *, roles):
        """Adds roles to users.\nExample: setrole (@)User \"Role 1, Role 2, Role 3\" """
        #roles = roles.replace("\"", "")
        roles = roles.strip()
        print(roles)
        rolesList = roles.split(", ")
        server = ctx.message.server
        
        #debugging
        for roleName in rolesList:
            print(roleName)
            
        message = "Roles added to **" + user.name + "**: "
        error = False
        for roleName in rolesList:
            for role in server.roles:
                if roleName == role.name:
                    try:
                        await self.bot.add_roles(user, role)
                        message += role.name + ", "
                        #await self.bot.say("Role **" + role.name + "** added to **" + user.name + "**")
                    except discord.Forbidden:
                        #await self.bot.say("There was a problem setting this role: " + role.name)
                        error = True
                        message += "~~" + role.name + "~~"
        if error == True:
            message += "\nIf a role has a line through it, the bot lacks the permissions to add that role."
        await self.bot.say(message)
        
        
    @commands.command(no_pm=True, pass_context=True)
    async def assignme(self, ctx, role : discord.Role):
        """Add self assignable roles to yourself."""
        user = ctx.message.author #get user that typed the command
        error = False
        for srole in ctx.message.server.roles:
            if srole.name == role.name:
              if role.id in self.selfrole_list:
                try:
                    await self.bot.add_roles(user, role)
                    await self.bot.say("You now have the " + role.name + " role.")
                except discord.Forbidden:
                    await self.bot.say("There was an error setting that role.")
              else:
                await self.bot.say("That's not in the list of self assignable roles.")
                        
    @commands.command(no_pm=True, pass_context=True)
    async def listroles(self, ctx):
        """Lists all the roles in a server."""
        server = ctx.message.server
        role_list = "**List of Roles by ID & Name:**\n```perl\n"
        for role in server.roles:
            role_list += str(role.id) + " | " + str(role.name) + "\n"
        role_list += "```"
        await self.bot.say(role_list)
        
    @commands.group(no_pm=True, pass_context=True)
    async def selfrole(self, ctx):
        """Manages self assignable roles"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
    
    @selfrole.command(name="add")
    @checks.admin_or_permissions(manage_roles=True)
    async def _selfrole_add(self, role : discord.Role):
        """Adds a self assignable role"""
        if role.id not in self.selfrole_list:
            self.selfrole_list.append(role.id)
            fileIO("data/roles/selfroles.json", "save", self.selfrole_list)
            await self.bot.say("The role is now self assignable.")
        else:
            await self.bot.say("this role is already on the list.")

    @selfrole.command(name="remove")
    @checks.admin_or_permissions(manage_roles=True)
    async def _selfrole_remove(self, role : discord.Role):
        """Removes a self assignable role from the list."""
        if role in self.selfrole_list:
            self.selfrole_list.remove(role)
            fileIO("data/roles/selfroles.json", "save", self.selfrole_list)
            await self.bot.say("role removed from selfrole list.")
        else:
            await self.bot.say("This role isn't in the list.")

    @selfrole.command(name="list")
    async def _selfrole_list(self):
        """Lists all self assignable roles in this server."""
        await self.bot.say("Placeholder")
    
def setup(bot):
    bot.add_cog(RoleTools(bot))
