from sqlalchemy.sql import asc
from Core.config import Config
from Core.db import session
from Core.maps import Alliance, apenis
from Arthur.context import menu, render
from Arthur.loadable import loadable, load
name = Config.get("Alliance", "name")

@menu("72hr Growth", "Alliance Growth")
@load
class agrowth(loadable):
    def execute(self, request, user):
        
        Q = session.query(Alliance, apenis)
        Q = Q.join(Alliance.apenis)
        Q = Q.order_by(asc(apenis.rank))
        return render("AGrowth.tpl", request, aqueens=Q.all())
