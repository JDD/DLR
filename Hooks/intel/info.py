# This file is part of Merlin.
# Merlin is the Copyright (C)2008, 2009, 2010 of Robin K. Hansen, Elliot Rosemarine, Andreas Jacobsen.

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

from sqlalchemy.sql import desc
from sqlalchemy.sql.functions import count, sum
from Core.db import session
from Core.maps import Planet, Alliance, Intel
from Core.loadable import loadable, route

class info(loadable):
    """Alliance information (All information taken from intel, for tag information use the lookup command)"""
    usage = " [alliance]"

    @route(r"(\S+)", access = "member")
    def execute(self, message, user, params):
        
        alliance = Alliance.load(params.group(1))
        if alliance is None:
            message.reply("No alliance matching '%s' found"%(params.group(1),))
            return
        
        Q = session.query(sum(Planet.value), sum(Planet.score),
                          sum(Planet.size), sum(Planet.xp),
                          count())
        Q = Q.join(Planet.intel)
        Q = Q.filter(Planet.active == True)
        Q = Q.filter(Intel.alliance==alliance)
        Q = Q.group_by(Intel.alliance_id)
        result = Q.first()
        if result is None:
            message.reply("No planets in intel match alliance %s"%(alliance.name,))
            return
        
        value, score, size, xp, members = result
        if members <= 60:
            reply="%s Members: %s, Value: %s, Avg: %s," % (alliance.name,members,self.num2short(value),self.num2short(value/members))
            reply+=" Score: %s, Avg: %s," % (self.num2short(score),self.num2short(score/members))
            reply+=" Size: %s, Avg: %s, XP: %s, Avg: %s" % (self.num2short(size),self.num2short(size/members),self.num2short(xp),self.num2short(xp/members))
            message.reply(reply)
            return
        
        Q = session.query(Planet.value, Planet.score, 
                          Planet.size, Planet.xp, 
                          Intel.alliance_id)
        Q = Q.join(Planet.intel)
        Q = Q.filter(Planet.active == True)
        Q = Q.filter(Intel.alliance==alliance)
        Q = Q.order_by(desc(Planet.score))
        Q = Q.limit(60)
        Q = Q.from_self(sum(Planet.value), sum(Planet.score),
                        sum(Planet.size), sum(Planet.xp),
                        count())
        Q = Q.group_by(Intel.alliance_id)
        ts_result = Q.first()
        
        ts_value, ts_score, ts_size, ts_xp, ts_members = ts_result
        reply="%s Members: %s (%s)" % (alliance.name,members,ts_members)
        reply+=", Value: %s (%s), Avg: %s (%s)" % (self.num2short(value),self.num2short(ts_value),self.num2short(value/members),self.num2short(ts_value/ts_members))
        reply+=", Score: %s (%s), Avg: %s (%s)" % (self.num2short(score),self.num2short(ts_score),self.num2short(score/members),self.num2short(ts_score/ts_members))
        reply+=", Size: %s (%s), Avg: %s (%s)" % (self.num2short(size),self.num2short(ts_size),self.num2short(size/members),self.num2short(ts_size/ts_members))
        reply+=", XP: %s (%s), Avg: %s (%s)" % (self.num2short(xp),self.num2short(ts_xp),self.num2short(xp/members),self.num2short(ts_xp/ts_members))
        message.reply(reply)
