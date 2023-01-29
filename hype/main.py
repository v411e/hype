from hype import Hype
from config import Config

bot = Hype(Config())
bot.login()
bot.update_profile()
bot.start()