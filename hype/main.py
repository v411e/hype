from .config import Config
from .hype import Hype

bot = Hype(Config())
bot.login()
bot.update_profile()
bot.start()
