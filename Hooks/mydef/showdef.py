# This file is part of Merlin.
# Merlin is the Copyright (C)2008,2009,2010 of Robin K. Hansen, Elliot Rosemarine, Andreas Jacobsen.

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
 
from Core.maps import Updates, User
from Core.loadable import loadable, route, require_user

class showdef(loadable):
    usage = " <pnick>"
    access = "member"
    
    @route(r"(\S+)")
    def user(self, message, user, params):
        name=params.group(1)
        u = User.load(name=name, exact=False, access="member")
        if u is None:
            message.reply("No members matching %s found"%(name,))
        else:
            self.execute(message, u)
    
    @route(r"")
    @require_user
    def me(self, message, user, params):
        self.execute(message, user)
    
    def execute(self, message, u):
        tick = Updates.current_tick()
        ships = u.fleets.all()
        
        if len(ships) < 1:
            message.reply("%s hasn't updated their def since tick %s. (comment: %s)"%(u.name,u.fleetupdated,u.fleetcomment))
        else:
            reply = "%s def info: fleetcount %s, updated: %s (%s), ships: " %(u.name,u.fleetcount,u.fleetupdated,u.fleetupdated-tick)
            reply+= ", ".join(map(lambda x:"%s %s" %(self.num2short(x.ship_count),x.ship.name),ships))
            reply+= " comment: %s"%(u.fleetcomment,)
            message.reply(reply)
