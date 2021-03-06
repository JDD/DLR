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
 
from traceback import format_exc
from Core.config import Config

CRLF = "\r\n"
encoding = "latin1"

def decode(text):
    # Converts strings to Unicode
    if type(text) is unicode:
        return text
    elif type(text) is str:
        return text.decode(encoding)
    else:
        raise UnicodeError

def encode(text):
    # Converts Unicode to strings
    if type(text) is str:
        return text
    elif type(text) is unicode:
        return text.encode(encoding)
    else:
        raise UnicodeError

def log(file, log, traceback=True, spacing=True):
    with open(file, "a") as file:
        file.write(encode(log) + "\n")
        if traceback is True:
            file.write(format_exc() + "\n")
        if spacing is True:
            file.write("\n\n")

errorlog = lambda text, traceback=True: log(Config.get("Misc","errorlog"), text, traceback=traceback)
scanlog = lambda text, traceback=False, spacing=False: log(Config.get("Misc","scanlog"), text, traceback=traceback, spacing=spacing or traceback)
arthurlog = lambda text, traceback=True: log(Config.get("Misc","arthurlog"), text, traceback=traceback)
