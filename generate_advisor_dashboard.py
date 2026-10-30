import os

os.makedirs("templates/dashboards", exist_ok=True)
template_path = "templates/dashboards/wealth_advisor_dashboard.html"

html_content = """{% extends 'base.html' %}
{% block content %}
<div class="min-h-screen bg-slate-950 text-slate-100 p-6 lg:p-10">
    
    <!-- Top Bar & Advisor Greeting -->
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
        <div>
            <h1 class="text-3xl font-bold tracking-tight text-white">Wealth Advisor Console: {{ request.user.get_full_name }}</h1>
            <p class="text-slate-400 text-sm">Client Portfolio Oversight & Compliance Review Center</p>
        </div>
        <div class="flex items-center gap-3">
            <a href="#" class="bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-medium px-4 py-2.5 rounded-xl transition shadow-lg">
                Export Audit Report (PDF)[cite: 1]
            </a>
        </div>
    </div>

    <!-- Manager KPI Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div class="bg-slate-900/80 border border-slate-800/80 rounded-2xl p-6 shadow-xl backdrop-blur-md">
            <p class="text-xs font-medium text-slate-400 uppercase">Assigned Roster AUM[cite: 1]</p>
            <h3 class="text-2xl font-bold text-white mt-2">$24,650,000.00</h3>
            <span class="text-emerald-400 text-xs font-semibold flex items-center mt-1">12 Active Client Portfolios</span>
        </div>
        <div class="bg-slate-900/80 border border-slate-800/80 rounded-2xl p-6 shadow-xl backdrop-blur-md">
            <p class="text-xs font-medium text-slate-400 uppercase">Pending Document Reviews[cite: 1]</p>
            <h3 class="text-2xl font-bold text-amber-400 mt-2">7 Items</h3>
            <span class="text-slate-400 text-xs mt-1 block">Requires KYC Verification[cite: 1]</span>
        </div>
        <div class="bg-slate-900/80 border border-slate-800/80 rounded-2xl p-6 shadow-xl backdrop-blur-md">
            <p class="text-xs font-medium text-slate-400 uppercase">Stale Valuations Alert[cite: 1]</p>
            <h3 class="text-2xl font-bold text-rose-400 mt-2">3 Assets</h3>
            <span class="text-slate-400 text-xs mt-1 block">> 12 Months Unvalued[cite: 1]</span>
        </div>
        <div class="bg-slate-900/80 border border-slate-800/80 rounded-2xl p-6 shadow-xl backdrop-blur-md">
            <p class="text-xs font-medium text-slate-400 uppercase">SLA Compliance Rate</p>
            <h3 class="text-2xl font-bold text-emerald-400 mt-2">98.4%</h3>
            <span class="text-slate-400 text-xs mt-1 block">Reviewed within 48h SLA[cite: 1]</span>
        </div>
    </div>

    <!-- Client Overview Matrix Table -->
    <div class="bg-slate-900/80 border border-slate-800/80 rounded-2xl p-6 shadow-xl mb-8">
        <div class="flex justify-between items-center mb-4">
            <h2 class="text-lg font-semibold text-white">Assigned Client Roster & Compliance Matrix[cite: 1]</h2>
            <input type="text" placeholder="Search clients..." class="bg-slate-950 border border-slate-800 text-xs text-slate-200 px-4 py-2 rounded-xl focus:outline-none focus:border-indigo-500">
        </div>
        <div class="overflow-x-auto">
            <table class="w-full text-left text-sm text-slate-300">
                <thead class="bg-slate-800/50 text-xs uppercase text-slate-400">
                    <tr>
                        <th class="p-3">Client Name</th>
                        <th class="p-3">Total AUM[cite: 1]</th>
                        <th class="p-3">Primary Asset Class</th>
                        <th class="p-3">KYC Status[cite: 1]</th>
                        <th class="p-3">Actions</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-slate-800">
                    <tr>
                        <td class="p-3 font-medium text-white">Arthur Pendelton</td>
                        <td class="p-3">$4,850,200.00</td>
                        <td class="p-3">Real Estate / Equities</td>
                        <td class="p-3"><span class="bg-emerald-950 text-emerald-300 border border-emerald-800 text-xs px-2.5 py-1 rounded-full">Verified</span></td>
                        <td class="p-3">
                            <a href="#" class="text-indigo-400 hover:text-indigo-300 font-medium text-xs">View Dossier</a>
                        </td>
                    </tr>
                    <tr>
                        <td class="p-3 font-medium text-white">Eleanor Vance</td>
                        <td class="p-3">$6,120,000.00</td>
                        <td class="p-3">Commercial Land & Bonds</td>
                        <td class="p-3"><span class="bg-amber-950 text-amber-300 border border-amber-800 text-xs px-2.5 py-1 rounded-full">Pending Review[cite: 1]</span></td>
                        <td class="p-3">
                            <a href="#" class="text-indigo-400 hover:text-indigo-300 font-medium text-xs">Review Queue[cite: 1]</a>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

    <!-- Document Verification Queue with SLA Timers -->
    <div class="bg-slate-900/80 border border-slate-800/80 rounded-2xl p-6 shadow-xl mb-8">
        <h2 class="text-lg font-semibold text-white mb-4">Document Verification Queue (SLA Monitoring)[cite: 1]</h2>
        <div class="overflow-x-auto">
            <table class="w-full text-left text-sm text-slate-300">
                <thead class="bg-slate-800/50 text-xs uppercase text-slate-400">
                    <tr>
                        <th class="p-3"><input type="checkbox" class="rounded bg-slate-900 border-slate-700"></th>
                        <th class="p-3">Document Title</th>
                        <th class="p-3">Client</th>
                        <th class="p-3">Uploaded Time</th>
                        <th class="p-3">SLA Status[cite: 1]</th>
                        <th class="p-3">Review Action[cite: 1]</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-slate-800">
                    <tr class="bg-rose-950/20 border-l-4 border-rose-500">
                        <td class="p-3"><input type="checkbox" class="rounded bg-slate-900 border-slate-700"></td>
                        <td class="p-3 font-medium text-white">Title Deed - Plot 88 (Commercial)</td>
                        <td class="p-3">Eleanor Vance</td>
                        <td class="p-3 text-slate-400">52 hours ago</td>
                        <td class="p-3"><span class="text-rose-400 font-semibold text-xs">SLA Breached (>48h)[cite: 1]</span></td>
                        <td class="p-3 flex gap-2">
                            <button class="bg-emerald-600 hover:bg-emerald-500 text-white text-xs px-3 py-1 rounded-lg transition">Approve[cite: 1]</button>
                            <button class="bg-rose-600 hover:bg-rose-500 text-white text-xs px-3 py-1 rounded-lg transition">Reject[cite: 1]</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

</div>
{% endblock %}
"""

with open(template_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("SUCCESS: Wealth Advisor Dashboard frontend template generated successfully!")
