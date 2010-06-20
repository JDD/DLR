{% extends "base.tpl" %}
{% block content %}
{% for level, members in accesslist %}
<table cellspacing="0" cellpadding="0" width="100%" class="black">
<tr>
<td>
<table cellspacing="1" cellpadding="3" width="100%">
    <tr class="datahigh">
        <th colspan="5">
            {{ level|capfirst }}s
        </th>
    </tr>
    <tr class="header">
        <th width="100"><a href="{% url members "name" %}">User (Alias)</a></th>
        <th width="100"><a href="{% url members "access" %}">Access</a></th>
        <th width="100"><a href="{% url members "planet" %}">Planet</a></th>
        <th width="100"><a href="{% url members "mydef" %}"><a href="{% url members "defage" %}">MyDef Age</a></th>
        <th width="100"><a href="{% url members "phone" %}">Phone</th>
    </tr>
    {% for member, alias, access, planet, fleetupdated, phone, pubphone, phonefriend in members %}
    <tr class="{% cycle 'odd' 'even' %}">
        <td>{{ member }}{% if alias %} ({{ alias }}){% endif %}</td>
        <td>{{ access }}</td>
        <td>{% if planet %}{{ planet.x }}:{{ planet.y }}:{{ planet.z }}{% endif %}</td>
        <td>{% if fleetupdated %}{{ tick|add:fleetupdated }}{% endif %}</td>
        <td>{% if pubphone or phonefriend %}{{ phone }}{% else %}Hidden{% endif %}</td>
    </tr>
    {% endfor %}
</table>
</td>
</tr>
</table>
{% if forloop.last %}
{% else %}
<p />
{% endif %}
{% endfor %}
{% endblock %}
