import discord
from discord.ext import commands
from .utils import checks
from random import randint
from random import choice, shuffle
import json
import urllib.request
import requests

class RoleTools:
    """Commands for assigning roles, self assigned roles, and default roles."""

    def __init__(self, bot):
        self.bot = bot

    
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
        
def setup(bot):
    bot.add_cog(RoleTools(bot))
