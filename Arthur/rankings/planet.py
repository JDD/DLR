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
 
from django.http import HttpResponseRedirect
from Core.maps import Updates, Planet
from Arthur.context import render
from Arthur.loadable import loadable, load

@load
class planet(loadable):
    access = "member"
    def execute(self, request, user, x, y, z):
        tick = Updates.midnight_tick()
        
        planet = Planet.load(x,y,z)
        if planet is None:
            return HttpResponseRedirect("/planets/")
        ph = planet.history(tick)
        if planet.intel and planet.alliance:
            planets = (planet, ph, planet.intel.nick, planet.alliance.name),
        elif planet.intel:
            planets = (planet, ph, planet.intel.nick, None),
        else:
            planets = (planet, ph, None, None),
        
        return render("planet.tpl", request, planets=planets, title="%s:%s:%s"%(planet.x, planet.y, planet.z), intel=user.is_member())
