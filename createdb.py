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
 
import sys
import sqlalchemy
from sqlalchemy.exc import IntegrityError, ProgrammingError
from sqlalchemy.sql import text, bindparam
from Core.config import Config
from Core.db import Base, session
import shipstats

if len(sys.argv) > 2 and sys.argv[1] == "--migrate":
    round = sys.argv[2]
    if round.isdigit():
        round = "r"+round
else:
    round = None
    print "To migrate from an old round use: createdb.py --migrate <previous_round>"

if round:
    print "Moving tables to '%s' schema"%(round,)
    try:
        session.execute(text("ALTER SCHEMA public RENAME TO %s;" % (round,)))
    except ProgrammingError:
        print "Oops! It looks like you already have a backup called '%s'" % (round,)
        session.rollback()
        sys.exit()
    else:
        session.commit()
    finally:
        session.close()

print "Importing database models"
from Core.maps import Channel

print "Creating schema and tables"
try:
    session.execute(text("CREATE SCHEMA public;"))
except ProgrammingError:
    print "A public schema already exists, but this is completely normal"
    session.rollback()
else:
    session.commit()
finally:
    session.close()

Base.metadata.create_all()

## Remove # from this section to set up initial database ##
#print "Setting up default channels"
#userlevel = Config.get("Access", "member")
#maxlevel = Config.get("Access", "admin")
#for chan, name in Config.items("Channels"):
#    try:
#        session.add(Channel(name=name,userlevel=userlevel,maxlevel=maxlevel))
#        session.flush()
#    except IntegrityError:
#        print "Channel '%s' already exists" % (name,)
#        session.rollback()
#    else:
#        print "Created '%s' with access (%s|%s)" % (name, userlevel, maxlevel,)
#        session.commit()
#session.close()

if round:
    print "Migrating users/friends"
    session.execute(text("INSERT INTO users (id, name, alias, passwd, active, access, email, phone, pubphone, googlevoice, sponsor, fleetcount) SELECT id, name, alias, passwd, active, access, email, phone, pubphone, googlevoice, sponsor, 0 FROM %s.users;" % (round,)))
    session.execute(text("SELECT setval('users_id_seq',(SELECT max(id) FROM users));"))
    session.execute(text("INSERT INTO phonefriends (user_id, friend_id) SELECT user_id, friend_id FROM %s.phonefriends;" % (round,)))
    print "Migrating slogans/quotes"
    session.execute(text("INSERT INTO slogans (text) SELECT text FROM %s.slogans;" % (round,)))
    session.execute(text("INSERT INTO quotes (text) SELECT text FROM %s.quotes;" % (round,)))
#    print "Migrating props/votes/cookies"
#    session.execute(text("INSERT INTO invite_proposal (id,active,proposer_id,person,created,closed,vote_result,comment_text) SELECT id,active,proposer_id,person,created,closed,vote_result,comment_text FROM %s.invite_proposal;" % (round,)))
#    session.execute(text("INSERT INTO kick_proposal (id,active,proposer_id,person_id,created,closed,vote_result,comment_text) SELECT id,active,proposer_id,person_id,created,closed,vote_result,comment_text FROM %s.kick_proposal;" % (round,)))
#    session.execute(text("SELECT setval('proposal_id_seq',(SELECT max(id) FROM (SELECT id FROM invite_proposal UNION SELECT id FROM kick_proposal) AS proposals));"))
#    session.execute(text("INSERT INTO prop_vote (vote,carebears,prop_id,voter_id) SELECT vote,carebears,prop_id,voter_id FROM %s.prop_vote;" % (round,)))
#    session.execute(text("INSERT INTO cookie_log (log_time,year,week,howmany,giver_id,receiver_id) SELECT log_time,year,week,howmany,giver_id,receiver_id FROM %s.cookie_log;" % (round,)))
    print "Migrating smslog"
    session.execute(text("INSERT INTO sms_log (sender_id,receiver_id,phone,sms_text,mode) SELECT sender_id,receiver_id,phone,sms_text,mode FROM %s.sms_log;" % (round,)))
## Add # to the following 2 lines for initial database setup
    print "Migrating Channels"
    session.execute(text("INSERT INTO channels (id, name, userlevel, maxlevel) SELECT id, name, userlevel, maxlevel FROM %s.channels;" % (round,)))
    session.commit()
    session.close()


print "Inserting ship stats"
shipstats.main()
