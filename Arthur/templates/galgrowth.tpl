{% extends "base.tpl" %}
{% block content %}
<table cellspacing="1" cellpadding="3" class="black">
    <tr class="datahigh">
        <th colspan="4">
            Galaxy 72hr Growth
        </th>
    </tr>
    <tr class="header">
        <th width="20">#</th>
        <th width="20">X:Y</th>
        <th width="200">Galaxy</th>
        <th width="75">Growth</th>
    </tr>
    {% for galaxy, galpenis in gqueens %}
    <tr class="{{ loop.cycle('odd', 'even') }}">
        <td class="right">{{ galpenis.rank }}</td>
        <td align="right"><a href="{% url "galaxy", galaxy.x, galaxy.y %}">{{ galaxy.x }}:{{ galaxy.y }}</a></td>
        <td><a class="{% if galaxy == user.planet.galaxy %}myplanet{% else %}gray{% endif %}" href="{% url "galaxy", galaxy.x, galaxy.y %}">
                {{ galaxy.name }}
        </a></td>
        <td class="right">{{ galpenis.penis|intcomma }}</td>
    </tr>
    {% endfor %}
</table>
{% endblock %}
