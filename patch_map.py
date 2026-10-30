import os

map_path = "templates/assets/asset_map.html"
os.makedirs("templates/assets", exist_ok=True)

html_content = """{% extends "base.html" %}
{% block title %}Asset Geographic Map - Asset Portal{% endblock %}
{% block page_title %}Real Estate & Land Map Integration{% endblock %}

{% block content %}
<div style="background: #fff; padding: 25px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
    <h3 style="margin-top: 0; color: #1a1a1a;">Geographic Pin Drop Visualization</h3>
    <p style="color: #666; font-size: 14px; margin-bottom: 20px;">Visually drop geographic pins for land and house assets based on their location fields[cite: 1].</p>

    <div style="width: 100%; height: 400px; background: #eef2f5; border-radius: 6px; display: flex; align-items: center; justify-content: center; border: 1px solid #ddd;">
        <div style="text-align: center; color: #555;">
            <h4 style="margin: 0 0 5px 0; color: #1a1a1a;">Interactive Map Viewer (Google Maps / Mapbox API)[cite: 1]</h4>
            <p style="font-size: 13px; margin: 0;">Pins loaded: Commercial Estate (Dar es Salaam), Residential Villa (Arusha)</p>
        </div>
    </div>
</div>
{% endblock %}
"""

with open(map_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("SUCCESS: Map Integration template created successfully!")
