from sqlalchemy.sql import asc
from Core.config import Config
from Core.db import session
from Core.maps import Galaxy, galpenis
from Arthur.context import menu, render
from Arthur.loadable import loadable, load
name = Config.get("Alliance", "name")

@menu("72hr Growth", "Galaxy Growth")
@load
class galgrowth(loadable):
    def execute(self, request, user):
        
        Q = session.query(Galaxy, galpenis)
        Q = Q.join(Galaxy.galpenis)
        Q = Q.order_by(asc(galpenis.rank))
        return render("galgrowth.tpl", request, gqueens=Q.all())
