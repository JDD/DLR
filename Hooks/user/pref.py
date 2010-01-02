# This file is part of Merlin.
# Merlin is the Copyright (C)2008-2009 of Robin K. Hansen, Elliot Rosemarine, Andreas Jacobsen.

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
 
import re
from Core.config import Config
from Core.db import session
from Core.maps import Planet, Alliance, User, Intel
from Core.loadable import loadable

@loadable.module()
class pref(loadable):
    """Set your planet, password for the webby, email and phone number; order doesn't matter"""
    usage = " [planet=x:y:z] [password=pass] [email=my.email@address.com] [phone=999] [pubphone=T|F]"
    paramre = re.compile(r"\s(.+)")
    
    @loadable.require_user
    def execute(self, message, user, params):
        
        params = self.split_opts(params.group(1))
        reply = ""
        for opt, val in params.items():
            if opt == "planet":
                m = self.planet_coordre.match(val)
                if m:
                    planet = Planet.load(*m.groups())
                    if planet is None:
                        continue
                    user.planet = planet
                    reply += " planet=%s:%s:%s"%(planet.x,planet.y,planet.z)
                    if user.is_member():
                        alliance = Alliance.load(Config.get("Alliance","name"))
                        if planet.intel is None:
                            planet.intel = Intel(nick=user.name, alliance=alliance)
                        else:
                            planet.intel.nick = user.name
                            planet.intel.alliance = alliance
            if opt == "password":
                user.passwd = val
                reply += " password=%s"%(val)
            if opt == "email":
                try:
                    user.email = val
                except AssertionError:
                    pass
                else:
                    reply += " email=%s"%(val)
            if opt == "phone":
                user.phone = val
                reply += " phone=%s"%(val)
            if opt == "pubphone":
                if val.lower() in self.true:
                    user.pubphone = True
                    reply += " pubphone=%s"%(True)
                elif val.lower() in self.false:
                    user.pubphone = False
                    reply += " pubphone=%s"%(False)
        session.commit()
        message.reply("Updated your preferences:"+reply)
