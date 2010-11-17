{% extends "base.tpl" %}
{% block content %}
<table cellspacing="1" cellpadding="3" class="black">
    <tr class="datahigh">
        <th colspan="3">
            Alliance 72hr Growth
        </th>
    </tr>
    <tr class="header">
        <th width="20">#</th>
        <th width="150">Alliance</th>
        <th width="75">Growth</th>
    </tr>
    {% for alliance, apenis in aqueens %}
    <tr class="{{ loop.cycle('odd', 'even') }}">
        <td class="right">{{ apenis.rank }}</td>
        <td><a class="{% if user|intel and alliance.name == name %}myplanet{% else %}gray{% endif %}" href="{% url "alliance_members", alliance.name %}">
            {{ alliance.name }}
        </a></td>
        <td class="right">{{ apenis.penis|intcomma }}</td>
    </tr>
    {% endfor %}
</table>
{% endblock %}
