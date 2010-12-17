<?xml version="1.0" encoding="iso-8859-1"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
    <title>{{ name }}</title>
    <link rel="stylesheet" href="/static/style.css" />

    {% if menu %}
    <!-- FreeStyle Menu v1.0RC by Angus Turnbull http://www.twinhelix.com -->
    <script type="text/javascript" src="/static/fsmenu.js"></script>
    <link rel="stylesheet" type="text/css" href="/static/listmenu_h.css" id="listmenu-h" title="Horizontal 'Earth'" />
    <!-- Fallback CSS menu file allows list menu operation when JS is disabled. -->
    <noscript><link rel="stylesheet" type="text/css" href="/static/listmenu_fallback.css" /></noscript>
    <script type="text/javascript" src="/static/anim.js"></script>
    {% endif %}

    <script type="text/javascript">
        function linkshift(event, link) {
            if (event.ctrlKey==1 || event.shiftKey==1 || event.altKey==1) {
                window.location.assign(link);
                return false;
            }
            else {
              return true;
            }
        }
        
        var cssRules = document.styleSheets[0].cssRules || document.styleSheets[0].rules;
        function getStyle(name) {
            for(var i = 0;i < cssRules.length;i++)
                if(cssRules[i].selectorText == name)
                    return cssRules[i].style;
        }
        function toggleGrowth() {
            var growth_pc = getStyle('.growth_pc');
            var growth_diff = getStyle('.growth_diff');
            
            if(!growth_pc || !growth_diff)
                return;
            
            growth_pc.display = growth_pc.display == 'none' ? 'inline' : 'none';
            growth_diff.display = growth_diff.display == 'none' ? 'inline' : 'none';
        }
    </script>

</head>

<body>
<div id="wrapper">
    {% if menu %}
    <table cellspacing="1" cellpadding="3">
        <tr class="header">
            <td>
    <ul class="menulist" id="listMenuRoot">
        {% for drop in menu %}
        <li>
            <a href="{{ drop.1 }}"{% if drop.2 %} target="_blank"{% endif %}>{{ drop.0 }}</a>
            <ul>
            {% if drop.3 %}
                {% for sub in drop.3 %}
                <li><a href="{{ sub.1 }}"{% if sub.2 %} target="_blank"{% endif %}>{{ sub.0 }}</a></li>
                {% endfor%}
            {% endif %}
            </ul>
        </li>
        {% endfor %}
    </ul>
            </td>
            <td>PT: {{ tick }}</td>
<form method="post" action="/lookup/">
            <th>Lookup:</th>
            <td><input type="text" name="lookup" size="8" onkeyup="var val=this.value;this.value=val+' ';this.value=val; var tl=val.length; if(tl<8){this.size=8;return;} if(tl>80){ this.size=100;return;} this.size=tl+(tl/4);"/></td>
            <td><input type="submit" value="!"/></td>
</form>
        </tr>
    </table>
    {% endif %}
{% block headerbar %}{% include "headerbar.tpl" %}{% endblock%}    

    <div style="clear: both; height: 2em"></div>
    <table cellspacing="1" cellpadding="3" width="100%"><tr><td><center>
    {% block content %}{% endblock %}
    <p>&nbsp;</p>
    </center></td></tr></table>
    <div id="push"></div>
</div>
<div id="footer" align="center">
    Free Domain Hosting from <a href="http://www.freedomain.co.nr/">http://www.freedomain.co.nr/</a>
    <br />
    Uses <a href="http://www.twinhelix.com/">DHTML / JavaScript Menu &copy; by TwinHelix Designs</a>
    <br />
    All your base are belong to us. Codez &copy; 2009-2010 Elliot Rosemarine.
</div>
</body>
</html>
