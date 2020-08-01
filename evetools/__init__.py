import logging
import importlib.util
from .evetools import EveTools

from redbot.core.errors import CogLoadError
from laggron_utils import init_logger

# Setup file to read in the cog


if not importlib.util.find_spec("laggron_utils"):
    raise CogLoadError(
        "You need the `laggron_utils` package for the loggin to properly function "
        "Use the command `[p]pipinstall git+https://github.com/retke/Laggron-utils.git` "
        "or type `pip3 install -U git+https://github.com/retke/Laggron-utils.git` in the "
        "terminal to install the library."
    )

log = logging.getLogger("red.xsv-cogs.evetools")


async def setup(bot):
    init_logger(log, EveTools.__class__.__name__)
    n = EveTools(bot)
    bot.add_cog(n)
    log.debug("Cog successfully loaded on the instance.")