import os

risk_path = "templates/portfolios/risk_assessment.html"
os.makedirs("templates/portfolios", exist_ok=True)

html_content = """{% extends "base.html" %}
{% block title %}Risk Tolerance Assessment - Asset Portal{% endblock %}
{% block page_title %}Client Risk Tolerance & Investment Profiling{% endblock %}

{% block content %}
<div style="max-width: 700px; margin: 30px auto; background: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
    <h3 style="margin-top: 0; color: #1a1a1a;">Investment Risk Profiling Questionnaire</h3>
    <p style="color: #666; font-size: 14px; margin-bottom: 25px;">Complete this questionnaire to determine your official wealth management risk category and asset allocation strategy.</p>

    <form id="risk-form" onsubmit="calculateRiskProfile(event)">
        <!-- Question 1 -->
        <div style="margin-bottom: 20px;">
            <label style="font-weight: bold; display: block; margin-bottom: 8px; color: #333;">1. What is your primary investment time horizon?</label>
            <select name="q1" style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px;" required>
                <option value="1">Less than 3 years (Short-term)</option>
                <option value="2">3 to 7 years (Medium-term)</option>
                <option value="3">More than 7 years (Long-term growth)</option>
            </select>
        </div>

        <!-- Question 2 -->
        <div style="margin-bottom: 20px;">
            <label style="font-weight: bold; display: block; margin-bottom: 8px; color: #333;">2. How would you react to a temporary 15% market drawdown in your portfolio value?</label>
            <select name="q2" style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px;" required>
                <option value="1">Sell assets immediately to prevent further losses</option>
                <option value="2">Hold position and wait for market recovery</option>
                <option value="3">View it as a buying opportunity and allocate more capital</option>
            </select>
        </div>

        <!-- Question 3 -->
        <div style="margin-bottom: 25px;">
            <label style="font-weight: bold; display: block; margin-bottom: 8px; color: #333;">3. What is your primary portfolio objective?</label>
            <select name="q3" style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px;" required>
                <option value="1">Capital Preservation & Stable Income</option>
                <option value="2">Balanced Growth & Capital Appreciation</option>
                <option value="3">Aggressive Capital Growth (High Risk / High Return)</option>
            </select>
        </div>

        <button type="submit" style="width: 100%; background: #1a1a1a; color: #cfa76e; border: none; padding: 12px; font-weight: bold; border-radius: 4px; cursor: pointer;">Calculate Risk Profile</button>
    </form>

    <div id="result-box" style="display: none; margin-top: 25px; padding: 20px; background: #fdfbf7; border: 1px solid #cfa76e; border-radius: 6px; text-align: center;">
        <h4 style="margin: 0 0 10px 0; color: #1a1a1a;">Assigned Risk Classification:</h4>
        <span id="profile-result" style="font-size: 20px; font-weight: bold; color: #cfa76e;"></span>
    </div>
</div>

<script>
    function calculateRiskProfile(e) {
        e.preventDefault();
        const q1 = parseInt(document.querySelector('[name="q1"]').value);
        const q2 = parseInt(document.querySelector('[name="q2"]').value);
        const q3 = parseInt(document.querySelector('[name="q3"]').value);
        
        const totalScore = q1 + q2 + q3;
        let profile = "Moderate Growth Strategy";
        
        if (totalScore <= 4) {
            profile = "Conservative / Capital Preservation (Low Risk)";
        } else if (totalScore >= 7) {
            profile = "Aggressive Growth / Equity Focus (High Risk)";
        }

        document.getElementById("profile-result").innerText = profile;
        document.getElementById("result-box").style.display = "block";
    }
</script>
{% endblock %}
"""

with open(risk_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("SUCCESS: Client Risk Tolerance Assessment template created successfully!")
