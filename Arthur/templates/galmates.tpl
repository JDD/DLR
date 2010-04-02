{% extends "base.tpl" %}
{% block content %}
<table cellspacing="0" cellpadding="0" width="100%" class="black">
<tr>
<td>
<table cellspacing="1" cellpadding="3" width="100%">
    <tr class="datahigh">
        <th colspan="5">
            Galmates
        </th>
    </tr>
    <tr class="header">
        <th width="100"><a href="{% url galmates "name" %}">User (Alias)</a></th>
        <th width="100"><a href="{% url galmates "access" %}">Access</a></th>
        <th width="100"><a href="{% url galmates "planet" %}">Planet</a></th>
        <th width="100">Phone</th>
    </tr>
    {% for member, alias, access, planet, phone, pubphone, phonefriend in members %}
    <tr class="{% cycle 'odd' 'even' %}">
        <td>{{ member }}{% if alias %} ({{ alias }}){% endif %}</td>
        <td>{{ access }}</td>
        <td>{% if planet %}{{ planet.x }}:{{ planet.y }}:{{ planet.z }}{% endif %}</td>
        <td>{% if pubphone or phonefriend %}{{ phone }}{% else %}Hidden{% endif %}</td>
    </tr>
    {% endfor %}
</table>
</td>
</tr>
</table>
{% endblock %}
