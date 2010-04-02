# This file is part of Merlin/Arthur.
# Merlin/Arthur is the Copyright (C)2009,2010 of Elliot Rosemarine.

# Individual portions may be copyright by individual contributors, and
# are included in this collective work with permission of the copyright
# owners.

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA
 
from sqlalchemy.sql import asc, desc
from Core.config import Config
from Core.db import session
from Core.maps import Updates, Planet, User, PhoneFriend, Channel
from Arthur.context import menu, render
from Arthur.loadable import loadable, load
bot = Config.get("Connection","nick")

@menu(bot, "Members")
@load
class members(loadable):
    access = "admin"
    def execute(self, request, user, sort=None):

        levels = sorted(Config.items("Access"), key=lambda acc: int(acc[1]), reverse=True)
        if sort is not None:
            levels = [("All member", levels[-1][1],),]

        order =  {"name"  : (asc(User.name),),
                  "access" : (desc(User.access),),
                  "planet" : (asc(Planet.x),asc(Planet.y),asc(Planet.z),),
                  "mydef" : (asc(User.fleetupdated),),
                  "phone" : (asc(User.phone),),
                  }
        if sort not in order.keys():
            sort = "name"
        order = order.get(sort)

        members = []
        for level in levels:
            Q = session.query(User.name, User.alias, User.access, Planet, User.fleetupdated,
                              User.phone, User.pubphone, User.id.in_(session.query(PhoneFriend.user_id).filter_by(friend=user)))
            Q = Q.outerjoin(User.planet)
            Q = Q.filter(User.active == True)
            Q = Q.filter(User.access >= level[1])
            Q = Q.filter(User.access < levels[levels.index(level)-1][1]) if levels.index(level) > 0 else Q
            for o in order:
                Q = Q.order_by(o)

            members.append((level[0], Q.all(),))
        
        return render("members.tpl", request, accesslist=members, tick=Updates.current_tick()*-1)

@menu(bot, "Galmates")
@load
class galmates(loadable):
    access = "admin"
    def execute(self, request, user, sort=None):
        
        levels = sorted(Config.items("Access"), key=lambda acc: int(acc[1]), reverse=True)
        
        order =  {"name"  : (asc(User.name),),
                  "access" : (desc(User.access),),
                  "planet" : (asc(Planet.x),asc(Planet.y),asc(Planet.z),),
                  }
        if sort not in order.keys():
            sort = "name"
        order = order.get(sort)
        
        members = []
        Q = session.query(User.name, User.alias, User.access, Planet,
                          User.phone, User.pubphone, User.id.in_(session.query(PhoneFriend.user_id).filter_by(friend=user)))
        Q = Q.outerjoin(User.planet)
        Q = Q.filter(User.active == True)
        Q = Q.filter(User.access == 0)
        for o in order:
            Q = Q.order_by(o)
        
        return render("galmates.tpl", request, members=Q.all())

@menu(bot, "Channels")
@load
class channels(loadable):
    access = "member"
    def execute(self, request, user, sort=None):
        
        levels = sorted(Config.items("Access"), key=lambda acc: int(acc[1]), reverse=True)
        if sort is not None:
            levels = [("All", 0,),]
        else:
            levels.append(("Galaxy", 0,))
        
        order =  {"name"  : (asc(Channel.name),),
                  "userlevel" : (asc(Channel.userlevel),),
                  "maxlevel" : (desc(Channel.maxlevel),),
                  }
        if sort not in order.keys():
            sort = "name"
        order = order.get(sort)
        
        channels = []
        for level in levels:
            Q = session.query(Channel.name, Channel.userlevel, Channel.maxlevel)
            Q = Q.filter(Channel.userlevel >= level[1])
            Q = Q.filter(Channel.userlevel < levels[levels.index(level)-1][1]) if levels.index(level) > 0 else Q
            for o in order:
                Q = Q.order_by(o)
            
            channels.append((level[0], Q.all(),))
        
        return render("channels.tpl", request, accesslist=channels)
