import os

os.makedirs("templates/dashboards", exist_ok=True)
template_path = "templates/dashboards/client_dashboard.html"

html_content = """{% extends 'base.html' %}
{% block content %}
<div class="min-h-screen bg-slate-950 text-slate-100 p-6 lg:p-10">
    
    <!-- Top Bar & Net Worth Toggle -->
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
        <div>
            <h1 class="text-3xl font-bold tracking-tight text-white">Private Wealth Portal: {{ request.user.get_full_name }}</h1>
            <p class="text-slate-400 text-sm">Traditional Asset Portfolio & Institutional Oversight</p>
        </div>
        <div class="flex items-center gap-4 bg-slate-900 border border-slate-800 p-2 rounded-xl">
            <span class="text-xs uppercase tracking-wider text-slate-400 font-semibold px-2">Valuation Mode:</span>
            <button id="toggleNetWorth" class="bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-medium px-4 py-2 rounded-lg transition shadow-md">
                Net Value (Post-Liabilities)
            </button>
        </div>
    </div>

    <!-- KPI Metric Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div class="bg-slate-900/80 border border-slate-800/80 rounded-2xl p-6 shadow-xl backdrop-blur-md">
            <p class="text-xs font-medium text-slate-400 uppercase">Total Portfolio Valuation</p>
            <h3 class="text-2xl font-bold text-white mt-2">$4,850,200.00</h3>
            <span class="text-emerald-400 text-xs font-semibold flex items-center mt-1">↑ +3.8% this quarter</span>
        </div>
        <div class="bg-slate-900/80 border border-slate-800/80 rounded-2xl p-6 shadow-xl backdrop-blur-md">
            <p class="text-xs font-medium text-slate-400 uppercase">Real Estate & Land</p>
            <h3 class="text-2xl font-bold text-white mt-2">$2,600,000.00</h3>
            <span class="text-slate-400 text-xs mt-1 block">Custom Tag: Estate Planning</span>
        </div>
        <div class="bg-slate-900/80 border border-slate-800/80 rounded-2xl p-6 shadow-xl backdrop-blur-md">
            <p class="text-xs font-medium text-slate-400 uppercase">Equities & Government Bonds</p>
            <h3 class="text-2xl font-bold text-white mt-2">$1,750,200.00</h3>
            <span class="text-emerald-400 text-xs font-semibold flex items-center mt-1">Fixed Coupon Yield Active</span>
        </div>
        <div class="bg-slate-900/80 border border-slate-800/80 rounded-2xl p-6 shadow-xl backdrop-blur-md">
            <p class="text-xs font-medium text-slate-400 uppercase">Secured Liabilities</p>
            <h3 class="text-2xl font-bold text-amber-400 mt-2">$500,000.00</h3>
            <span class="text-slate-400 text-xs mt-1 block">Commercial Mortgage Facility</span>
        </div>
    </div>

    <!-- Charts Section -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
        <!-- Asset Distribution Donut Chart -->
        <div class="bg-slate-900/80 border border-slate-800/80 rounded-2xl p-6 shadow-xl lg:col-span-1">
            <h2 class="text-lg font-semibold text-white mb-4">Traditional Asset Allocation</h2>
            <div class="relative h-64 flex items-center justify-center">
                <canvas id="assetDonutChart"></canvas>
            </div>
        </div>
        <!-- 12-Month Performance Line Graph -->
        <div class="bg-slate-900/80 border border-slate-800/80 rounded-2xl p-6 shadow-xl lg:col-span-2">
            <div class="flex justify-between items-center mb-4">
                <h2 class="text-lg font-semibold text-white">Historical Performance (12 Months)</h2>
                <a href="#" class="bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium px-3 py-1.5 rounded-lg border border-slate-700 transition">
                    Download Statement PDF
                </a>
            </div>
            <div class="relative h-64">
                <canvas id="performanceLineChart"></canvas>
            </div>
        </div>
    </div>

    <!-- Asset List Table with Inline Editing -->
    <div class="bg-slate-900/80 border border-slate-800/80 rounded-2xl p-6 shadow-xl mb-8">
        <h2 class="text-lg font-semibold text-white mb-4">Registered Holdings & Wealth Goals</h2>
        <div class="overflow-x-auto">
            <table class="w-full text-left text-sm text-slate-300">
                <thead class="bg-slate-800/50 text-xs uppercase text-slate-400">
                    <tr>
                        <th class="p-3">Asset / Property Name</th>
                        <th class="p-3">Category</th>
                        <th class="p-3">Portfolio Goal Tag</th>
                        <th class="p-3">Estimated Value (Inline Editable)</th>
                        <th class="p-3">Last Verified</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-slate-800">
                    <tr>
                        <td class="p-3 font-medium text-white">Commercial Office Complex (Plot 42)</td>
                        <td class="p-3">Real Estate (Land/House)</td>
                        <td class="p-3"><span class="bg-blue-950 text-blue-300 border border-blue-800 text-xs px-2.5 py-1 rounded-full">Retirement Fund</span></td>
                        <td class="p-3 cursor-pointer hover:text-emerald-400 transition" contenteditable="true">$2,100,000.00</td>
                        <td class="p-3 text-slate-400">2026-09-14</td>
                    </tr>
                    <tr>
                        <td class="p-3 font-medium text-white">Global Industrial Equities Index</td>
                        <td class="p-3">Stocks</td>
                        <td class="p-3"><span class="bg-purple-950 text-purple-300 border border-purple-800 text-xs px-2.5 py-1 rounded-full">Growth Portfolio</span></td>
                        <td class="p-3 cursor-pointer hover:text-emerald-400 transition" contenteditable="true">$950,000.00</td>
                        <td class="p-3 text-slate-400">2026-10-02</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

</div>

<!-- Chart.js Script Integration -->
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    const ctxDonut = document.getElementById('assetDonutChart').getContext('2d');
    new Chart(ctxDonut, {
        type: 'doughnut',
        data: {
            labels: ['Real Estate', 'Equities', 'Gov Bonds', 'Vehicles'],
            datasets: [{
                data: [55, 25, 14, 6],
                backgroundColor: ['#10b981', '#6366f1', '#f59e0b', '#3b82f6'],
                borderWidth: 0
            }]
        },
        options: { responsive: true, maintainAspectRatio: false }
    });

    const ctxLine = document.getElementById('performanceLineChart').getContext('2d');
    new Chart(ctxLine, {
        type: 'line',
        data: {
            labels: ['Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'],
            datasets: [{
                label: 'Portfolio Valuation ($)',
                data: [3800000, 3900000, 4100000, 4000000, 4300000, 4400000, 4200000, 4500000, 4600000, 4700000, 4800000, 4850200],
                borderColor: '#10b981',
                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                fill: true,
                tension: 0.3
            }]
        },
        options: { responsive: true, maintainAspectRatio: false }
    });
</script>
{% endblock %}
"""

with open(template_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("SUCCESS: Client Dashboard frontend template generated successfully!")
