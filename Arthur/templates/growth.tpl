{% extends "base.tpl" %}
{% block content %}
{% load humanize %}
<table cellspacing="0" cellpadding="0" width="100%" class="black">
<tr>
<td>
<table cellspacing="1" cellpadding="3" width="100%">
    <tr class="datahigh">
        <th colspan="4">
            Growth
        </th>
    </tr>
    <tr class="header">
        <th width="100">Rank</th>
        <th width="100">User (Alias)</th>
        <th width="100">Planet</th>
        <th width="100">Growth</th>
    </tr>
    {% for member, planet, epenis in queens %}
    <tr class="{% cycle 'odd' 'even' %}">
        <td>{{ epenis.rank }}</td>
        <td>{{ member.name }}{% if member.alias %} ({{ member.alias }}){% endif %}</td>
        <td>{{ planet.x }}:{{ planet.y }}:{{ planet.z }}</td>
        <td>{{ epenis.penis|intcomma }}</td>
    </tr>
    {% endfor %}
</table>
</td>
</tr>
</table>
{% endblock %}


