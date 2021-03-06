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
 
from Core.config import Config
from Core.maps import User
from Core.loadable import loadable, route

class whois(loadable):
    """Lookup a user's details"""
    usage = " <pnick>"
    
    @route(r"(\S+)", access = "member")
    def execute(self, message, user, params):

        # assign param variables 
        search=params.group(1)

        # do stuff here
        if search.lower() == Config.get("Connection","nick").lower():
            message.reply("I am %s. Hear me roar." % (Config.get("Connection","nick"),))
            return

        whore = User.load(name=search, exact=False, access="galmate")
        if whore is None:
            message.reply("No users matching '%s'"%(search,))
            return

        reply=""
        if whore == user:
            reply+="You are %s. Your access is %s. Your alias: is %s. Your planet id is: %s. Your Email is: %s. Your phone number is set to public: %s. Your number is sms'd through Google Voice: %s"
        else:
            reply+="Information about %s: Thier access is %s. Thier alias is: %s. Their planet id is: %s. Thier Email is: %s. Thier phone number is set to public: %s. Their number is sms'd through Google Voice: %s"
        reply=reply%(whore.name,whore.access,whore.alias,whore.planet_id,whore.email,whore.pubphone,whore._smsmode,)

        message.reply(reply)
