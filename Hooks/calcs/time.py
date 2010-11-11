import datetime
from Core.maps import Updates
from Core.loadable import loadable, route

class time(loadable):
    """Calculate tick time in specified timezone."""
    usage = " <tick> <timezone>"
    class_timezone = {"adt": -3,
                      "akdt": -8,
                      "akst": -9,
                      "ast": -4,
                      "cdt": -5,
                      "cst": -6,
                      "edt": -4,
                      "est": -5,
                      "hadt": -9,
                      "hast": -10,
                      "mdt": -6,
                      "mst": -7,
                      "pdt": -7,
                      "pst": -8,
                      "aedt": 11,
                      "aest": 10,
                      "awdt": 9,
                      "awst": 8,
                      "cxt": 7,
                      "wdt": 9,
                      "wst": 8,
                      "bst": 1,
                      "cedt": 2,
                      "cest": 2,
                      "cet": 1,
                      "eedt": 3,
                      "eest": 3,
                      "eet": 2,
                      "gmt": 0,
                      "est": 1,
                      "msd": 4,
                      "msk": 3,
                      "wedt": 1,
                      "west": 1}

    @route(r"(\d+)\s+(\S+)")
    def execute(self, message, user, params):

        tick, timezone = params.groups()
        tick = int(tick)
        
        if timezone.lower() in self.class_timezone.keys():
             timezone = self.class_timezone[timezone.lower()]   
        else:
            try:
                timezone = int(timezone)
            except ValueError:
                message.alert("Invalid timezone '%s'" % (timezone,))
                return

        current_tick=Updates.current_tick()

        current_time = datetime.datetime.utcnow()
        tzajust = tick + timezone
        tztime = current_time + datetime.timedelta(hours=(tzajust-current_tick))

        message.reply("Time at tick %s, timezone %s : %s" % (tick, params.group(2), (tztime.strftime("%m-%d %H:55"))))