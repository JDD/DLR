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
from sqlalchemy.sql import desc
from Core.db import session
from Core.maps import SMS
from Core.loadable import loadable

@loadable.module("member")
class smslog(loadable):
    """Show the last ten SMS sent, or the text of a specific SMS sender."""
    usage = " [id]"
    paramre = re.compile(r"\s*(\d+)?")
    
    def execute(self, message, user, params):
        
        id=params.group(1)
        
        if id:
            sms = self.get_sms(id)
            if sms:
                reply = "SMS with ID %s (%s) sent by %s to %s with text: %s"%(sms.id,sms.mode.upper(),sms.sender.name,sms.receiver.name,sms.sms_text)
            else:
                reply = "There was no SMS sent with ID %s"%(id,)
            message.reply(reply)
        else:
            last_ten = self.get_last_ten()
            reply="Last 10 SMSes: "
            reply+=", ".join(map(lambda x: "id: %s (%s -> %s)"%(x.id,x.sender.name,x.receiver.name),last_ten))
            message.reply(reply)
    
    def get_sms(self, id):
        return session.query(SMS).filter_by(id=id).first()
        
    def get_last_ten(self):
        return session.query(SMS).order_by(desc(SMS.id))[:10]
