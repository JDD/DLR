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

from Core.paconf import PA
from Core.loadable import loadable, route

class roidsave(loadable):
    """Tells you how much value will be mined by a number of roids in that many ticks."""
    usage = " <roids> <ticks> [mining_bonus]"

    @route(r"(\d+)\s+(\d+)(?:\s+(\d+))?")
    def execute(self, message, user, params):
        
        roids=int(params.group(1))
        ticks=int(params.group(2))
        bonus=int(params.group(3) or 0)
        mining = PA.getint("roids","mining")

        mining = mining *(float(bonus+100)/100)

        cost=self.num2short(ticks*roids*mining/100)
        reply="In %s ticks (%s days) %s roids with %s%% bonus will mine %s value" % (ticks,ticks/24,roids,bonus,cost)

        costdemo=self.num2short(ticks*roids*mining/100*(1/(1+PA.getfloat("demo","prodcost"))))
        costtotal=self.num2short(ticks*roids*mining/100*(1/(1+PA.getfloat("total","prodcost"))))
        reply+=" Democracy: %s value" % (costdemo)
        reply+=" Totalitarianism: %s value" % (costtotal)

        message.reply(reply)
