import discord
import time


from redbot.core import commands, checks
from redbot.core.utils.chat_formatting import pagify
from redbot.core.utils.chat_formatting import box
from redbot.core.utils import chat_formatting as chat
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS

listener = getattr(commands.Cog, "listener", lambda: lambda x: x)



class Information