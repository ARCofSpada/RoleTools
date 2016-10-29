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
        if not os.path.isfile(self.rolePath):
            print("Creating new selfrole database.")
            dataIO.save_json(self.rolePath, "{}")
        self.selfrole_list = dataIO.load_json(self.rolePath)

    #@commands.command()
    #async def rolehelp(self):
        
    
    @commands.command(no_pm=True, pass_context=True)
    @checks.admin_or_permissions(manage_roles=True)
    #async def setrole(self, ctx, user : discord.Member, *, role : discord.Role):
    async def setrole(self, ctx, user : discord.Member, *, roles):
        """Adds roles to users.\nExample: setrole (@)User \"Role 1, Role 2, Role 3\" """
        roles = roles.replace("\"", "")
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
    async def assignme(self, ctx):
        """Assign default roles to yourself."""
        rolesList = ["role 1", "role 2", "role 3"]
        user = ctx.message.author #get user that typed the command
        error = False
        errormsg = "There was a problem setting the following roles: "
        for roleName in rolesList:
            for role in server.roles:
                if roleName == role.name:
                    try:
                        await self.bot.add_roles(user, role)
                    except discord.Forbidden:
                        error = True
                        errormsg += role.name
        if error == True:
            await self.bot.say(errormsg)
                        
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
    async def _selfrole_add(self, role : discord.Role):
        """Adds a self assignable role"""
        if role.id not in self.selfrole_list:
            self.selfrole_list.append(role.id)
            fileIO("data/roles/selfroles.json", "save", self.selfrole_list)
            await self.bot.say("The role is now self assignable.")
        else:
            await self.bot.say("this role is already on the list.")

    @selfrole.command(name="remove")
    async def _selfrole_remove(self, role : discord.Role):
        """Removes a self assignable role from the list."""
        await self.bot.say("placeholder")

    @selfrole.command(name="list")
    async def _selfrole_list(self):
        """Lists all self assignable roles in this server."""
        await self.bot.say("Placeholder")
    
def setup(bot):
    bot.add_cog(RoleTools(bot))
