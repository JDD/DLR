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
import time
from urllib import urlencode
from urllib2 import urlopen, URLError
from Core.exceptions_ import LoadableError
from Core.config import Config
from Core.db import session
from Core.maps import User, SMS
from Core.loadable import loadable

@loadable.module("member")
class sms(loadable):
    """Sends an SMS to the specified user. Your username will be appended to the end of each sms. The user must have their phone correctly added and you must have access to their number."""
    usage = " <nick> <message>"
    paramre = re.compile(r"\s+(\S+)\s+(.+)")
    
    @loadable.require_user
    def execute(self, message, user, params):
        
        rec = params.group(1)
        public_text = params.group(2) + ' - %s' % (user.name,)
        text = public_text.encode('latin-1') + '/%s' %(user.phone,)
        receiver=User.load(name=rec,exact=False)
        if not receiver:
            message.reply("Who exactly is %s?" % (rec,))
            return
        if receiver.name.lower() == 'cybdev':
            message.reply("I refuse to talk to that Norwegian clown. Use !phone show CybDev and send it using your own phone.")
            return
        if receiver.name.lower() == 'zeb':
            message.reply("FOR EMERGENCY ONLY!!!! Zeb only has a land line so only rings will work.  Use !phone show Zeb to get his phone number.")
            return

        if not receiver.pubphone and user not in receiver.phonefriends:
            message.reply("%s's phone number is private or they have not chosen to share their number with you. Supersecret message not sent." % (receiver.name,))
            return

        phone = self.prepare_phone_number(receiver.phone)
        if not phone or len(phone) <= 6:
            message.reply("%s has no phone number or their phone number is too short to be valid (under 6 digits). Super secret message not sent." % (receiver.name,))
            return

        if len(text) >= 160:
            message.reply("Max length for a text is 160 characters. Your text was %i characters long. Super secret message not sent." % (len(text),))
            return

        mode = Config.get("Misc", "sms")
        error = ""

        if mode == "googlevoice" or mode == "combined":
            error = self.send_googlevoice(user, receiver, public_text, phone, text)
            sent = "Google Voice"
        if mode == "clickatell" or (mode == "combined" and error is not None):
            error = self.send_clickatell(user, receiver, public_text, phone, text)
            sent = "Clickatell"

        if error is None:
            message.reply("%s successfully processed message to: %s saying: %s" % (sent,receiver.name,text))
        else:
            message.reply(error or "That wasn't supposed to happen. I don't really know what went wrong. Maybe your mother dropped you.")

    def send_clickatell(self, user, receiver, public_text, phone, message):
        try:
            post = urlencode({"user"        : Config.get("clickatell", "user"),
                              "password"    : Config.get("clickatell", "pass"),
                              "api_id"      : Config.get("clickatell", "api"),
                              "to"          : phone,
                              "text"        : message,
                            })
            status, msg = urlopen("https://api.clickatell.com/http/sendmsg", post, 5).read().split(":")
            if status in ("OK","ID",):
                self.log_message(user, receiver, phone, public_text, "clickatell")
                return None
            elif status in ("ERR",):
                raise SMSError(msg.strip())
            else:
                return ""
        except (URLError, SMSError) as e:
            return "Error sending message: %s" % (str(e),)

    def send_googlevoice(self, user, receiver, public_text, phone, message):
        try:
            post = urlencode({"accountType" : "GOOGLE",
                              "Email"       : Config.get("googlevoice", "user"),
                              "Passwd"      : Config.get("googlevoice", "pass"),
                              "service"     : "grandcentral",
                              "source"      : "Merlin",
                            })
            text = urlopen("https://www.google.com/accounts/ClientLogin", post, 5).read()
            m = re.search(r"^Auth=(.+?)$", text, re.M)
            if m is None:
                raise SMSError("unable to authenticate")
            auth = m.group(1)

            post = urlencode({"id"          : '',
                              "phoneNumber" : '+'+phone,
                              "text"        : message,
                              "auth"        : auth,
                              "_rnr_se"     : Config.get("googlevoice", "api"),
                            })
            text = urlopen("https://www.google.com/voice/sms/send/", post, 5).read()
            if text != '{"ok":true,"data":{"code":0}}':
                raise SMSError("success code not returned")

            time.sleep(5)

            get = urlencode({"auth"         : auth,
                           })
            text = urlopen("https://www.google.com/voice/inbox/recent/sms/?"+get, None, 5).read()
            m = re.search(self.googlevoice_regex(message), text)
            if m is None:
                raise SMSError("message not found in SMS history")
            if m.group(4) is None:
                self.log_message(user, receiver, phone, public_text, "googlevoice")
                return None
            else:
                return m.group(4)
        except (URLError, SMSError) as e:
            return "Error sending message: %s" % (str(e),)

    def googlevoice_regex(self, message):
        message = re.escape(message)
        regex = r'<div class="gc-message-sms-row">\s*'
        regex+= r'<span class="gc-message-sms-from">\s*'
        regex+= r'Me:\s*'
        regex+= r'</span>\s*'
        regex+= r'<span class="gc-message-sms-text">\s*'
        regex+= r'('+message+')'
        regex+= r'</span>\s*'
        regex+= r'<span class="gc-message-sms-time">\s*'
        regex+= r'(.*?)'
        regex+= r'</span>\s*'
        regex+= r'</div>\s*'
        regex+= r'(?:'
        regex+= r'<div class="gc-message-sms-row">\s*'
        regex+= r'<span class="gc-message-sms-from">\s*'
        regex+= r'(.*?):\s*'
        regex+= r'</span>\s*'
        regex+= r'<span class="gc-message-sms-text">\s*'
        regex+= r'(Error: this message was not successfully delivered.)'
        regex+= r'</span>\s*'
        regex+= r'<span class="gc-message-sms-time">\s*'
        regex+= r'(.*?)'
        regex+= r'</span>\s*'
        regex+= r'</div>\s*'
        regex+= r')?'
        return regex

    def prepare_phone_number(self,text):
        if not text:
            return text
        s = "".join([c for c in text if c.isdigit()])
        return s.lstrip("00")

    def log_message(self,sender,receiver,phone,text,mode):
        session.add(SMS(sender=sender,receiver=receiver,phone=phone,sms_text=text,mode=mode))
        session.commit()

class SMSError(LoadableError):
    pass