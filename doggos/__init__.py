from .doggos import Doggos

def setup(bot):
    bot.add_cog(Doggos(bot))