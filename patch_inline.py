import os

list_path = "templates/assets/asset_list.html"
os.makedirs("templates/assets", exist_ok=True)

html_content = """{% extends "base.html" %}
{% block title %}Asset List - Asset Portal{% endblock %}
{% block page_title %}Enterprise Asset Portfolio{% endblock %}

{% block content %}
<div style="background: #fff; padding: 25px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
    <h3 style="margin-top: 0; color: #1a1a1a;">Registered Assets</h3>
    <table style="width: 100%; border-collapse: collapse; margin-top: 15px;">
        <thead>
            <tr style="background: #f4f6f9; text-align: left; font-size: 13px; color: #555;">
                <th style="padding: 10px; border-bottom: 2px solid #ddd;">Asset Name</th>
                <th style="padding: 10px; border-bottom: 2px solid #ddd;">Category</th>
                <th style="padding: 10px; border-bottom: 2px solid #ddd;">Estimated Value</th>
                <th style="padding: 10px; border-bottom: 2px solid #ddd;">Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for asset in assets %}
            <tr style="border-bottom: 1px solid #eee; font-size: 14px;">
                <td style="padding: 10px;">{{ asset.name }}</td>
                <td style="padding: 10px;">{{ asset.category }}</td>
                <td style="padding: 10px;">
                    <span id="val-span-{{ asset.id }}" onclick="enableInlineEdit('{{ asset.id }}', '{{ asset.current_estimated_value }}')" style="cursor: pointer; border-bottom: 1px dashed #cfa76e;" title="Click to edit inline">${{ asset.current_estimated_value }}</span>
                </td>
                <td style="padding: 10px;">
                    <a href="{% url 'asset_update' asset.id %}" style="color: #cfa76e; text-decoration: none; font-weight: bold; font-size: 13px;">Full Edit</a>
                </td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="4" style="padding: 20px; text-align: center; color: #777;">No assets registered yet.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>

<script>
    function enableInlineEdit(id, currentVal) {
        const valSpan = document.getElementById("val-span-" + id);
        valSpan.innerHTML = "<input type=\"number\" id=\"input-val-" + id + "\" value=\"" + currentVal + "\" style=\"width: 100px; padding: 4px;\" onblur=\"saveAssetValue('" + id + "')\">";
        document.getElementById("input-val-" + id).focus();
    }

    function saveAssetValue(id) {
        const newVal = document.getElementById("input-val-" + id).value;
        const valSpan = document.getElementById("val-span-" + id);
        valSpan.innerHTML = "$" + parseFloat(newVal).toLocaleString();
    }
</script>
{% endblock %}
"""

with open(list_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("SUCCESS: Inline asset editing list template created successfully!")
