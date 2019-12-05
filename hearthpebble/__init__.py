from .hearthpebble import Hearthpebble

def setup(bot):
    bot.add_cog(Hearthpebble(bot))