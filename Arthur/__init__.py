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
 
from django.conf.urls.defaults import include, patterns, url
from django.http import HttpResponseRedirect
from Core.config import Config
from Core.maps import Updates
from Arthur.context import menu, render
from Arthur.errors import page_not_found
from Arthur.loadable import loadable, load
bot = Config.get("Connection","nick")
name = Config.get("Alliance", "name")

handler404 = 'Arthur.errors.page_not_found'
handler500 = 'Arthur.errors.server_error'

urlpatterns = patterns('',
    (r'^(?:home/)?$', 'Arthur.home'),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'C:/merlin/Arthur/static/'}),
    (r'^guide/$', 'Arthur.guide'),
    (r'^links/(?P<link>\w+)/$', 'Arthur.links'),
    (r'', include('Arthur.lookup')),
    (r'', include('Arthur.alliance')),
    (r'', include('Arthur.rankings')),
)

@menu("Home")
@load
class home(loadable):
    def execute(self, request, user):
        if user.planet is not None:
            tick = Updates.midnight_tick()
            planets = (user.planet, user.planet.history(tick), None, None),
        else:
            planets = ()
        return render("index.tpl", request, planets=planets, title="Your planet")

@menu(name,                         suffix = name)
@menu("Planetarion", "Parser",      suffix = "parser")
@menu("Planetarion", "BCalc",       suffix = "bcalc")
@menu("Planetarion", "Sandmans",    suffix = "sandmans")
@menu("Planetarion", "PA Forums",      suffix = "forums")
@menu("Planetarion", "Game",        suffix = "game")
@menu(name, "DLR Forums",           suffix = "dlr_forums")
@load
class links(loadable):
    links = {"game"        : "http://game.planetarion.com",
             "forums"      : "http://pirate.planetarion.com",
             "sandmans"    : "http://sandmans.co.uk",
             "bcalc"       : "http://game.planetarion.com/bcalc.pl",
             "parser"      : "http://parser.5th-element.org/",
             name          : "/alliance/%s/" % (name,),
             "dlr_forums"  : "http://progression-uk.com/DLR/forum/index.php",
            }
    def execute(self, request, user, link):
        link = self.links.get(link)
        if link is None:
            return page_not_found(request)
        return HttpResponseRedirect(link)

@menu(bot, "Guide to %s"%(Config.get("Connection","nick"),))
@load
class guide(loadable):
    def execute(self, request, user):
        return render("guide.tpl", request, bot=Config.get("Connection","nick"), alliance=name)

#from Arthur import alliance
from Arthur import rankings
