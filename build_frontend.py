import os

def build_frontend():
    # Ensure directories exist
    os.makedirs("templates/public", exist_ok=True)
    os.makedirs("templates/registration", exist_ok=True)
    os.makedirs("templates/includes", exist_ok=True)

    # ---------------------------------------------------------
    # 1. BASE PUBLIC TEMPLATE (With Header Navigation)
    # ---------------------------------------------------------
    base_public_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Enterprise Asset Portfolio{% endblock %}</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 text-slate-900 font-sans antialiased flex flex-col min-h-screen">
    
    <!-- Public Header Navigation -->
    <header class="bg-white border-b border-slate-200 sticky top-0 z-50 shadow-sm">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-20">
                <!-- Logo & Brand -->
                <div class="flex-shrink-0 flex items-center gap-3">
                    <div class="w-10 h-10 bg-emerald-700 rounded-lg flex items-center justify-center shadow-md">
                        <span class="text-white font-bold text-xl">AP</span>
                    </div>
                    <span class="font-bold text-xl tracking-tight text-slate-900">Asset Portal</span>
                </div>
                
                <!-- Main Navigation -->
                <nav class="hidden md:flex space-x-8">
                    <a href="/" class="text-slate-600 hover:text-emerald-700 font-medium transition">Home</a>
                    <a href="#" class="text-slate-600 hover:text-emerald-700 font-medium transition">About Us</a>
                    <a href="#" class="text-slate-600 hover:text-emerald-700 font-medium transition">Solutions</a>
                    <a href="#" class="text-slate-600 hover:text-emerald-700 font-medium transition">Contact</a>
                </nav>

                <!-- Call to Actions -->
                <div class="flex items-center space-x-4">
                    <a href="{% url 'login' %}" class="text-slate-600 hover:text-slate-900 font-semibold transition">Log In</a>
                    <a href="#" class="bg-slate-900 hover:bg-slate-800 text-white font-medium px-5 py-2.5 rounded-xl shadow-md transition">
                        Open an Account
                    </a>
                </div>
            </div>
        </div>
    </header>

    <!-- Main Content Area -->
    <main class="flex-grow">
        {% block content %}{% endblock %}
    </main>

    <!-- Public Footer -->
    <footer class="bg-slate-950 text-slate-400 py-12 border-t border-slate-900">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center md:text-left grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
                <h3 class="text-white font-bold text-lg mb-4">Asset Portal</h3>
                <p class="text-sm">Institutional-grade portfolio tracking and compliance management for high-net-worth individuals.</p>
            </div>
            <div>
                <h4 class="text-white font-semibold mb-4">Platform</h4>
                <ul class="space-y-2 text-sm">
                    <li><a href="#" class="hover:text-emerald-400 transition">Security</a></li>
                    <li><a href="#" class="hover:text-emerald-400 transition">Compliance SLA</a></li>
                </ul>
            </div>
            <div>
                <h4 class="text-white font-semibold mb-4">Legal</h4>
                <ul class="space-y-2 text-sm">
                    <li><a href="#" class="hover:text-emerald-400 transition">Terms of Service</a></li>
                    <li><a href="#" class="hover:text-emerald-400 transition">Privacy Policy</a></li>
                </ul>
            </div>
            <div>
                <p class="text-sm">&copy; {% now "Y" %} Enterprise Asset Portfolio. All rights reserved.</p>
            </div>
        </div>
    </footer>
</body>
</html>"""
    with open("templates/base_public.html", "w", encoding="utf-8") as f:
        f.write(base_public_html)
    print("[1/4] Created base_public.html with top navigation.")

    # ---------------------------------------------------------
    # 2. PUBLIC HOME PAGE (Landing)
    # ---------------------------------------------------------
    home_html = """{% extends 'base_public.html' %}
{% block content %}
<!-- Hero Section -->
<div class="relative bg-white overflow-hidden">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 lg:py-32 flex flex-col lg:flex-row items-center gap-12">
        <div class="lg:w-1/2 text-center lg:text-left">
            <h1 class="text-4xl tracking-tight font-extrabold text-slate-900 sm:text-5xl md:text-6xl mb-6">
                <span class="block">Institutional Oversight.</span>
                <span class="block text-emerald-700">Private Wealth.</span>
            </h1>
            <p class="mt-3 text-base text-slate-500 sm:mt-5 sm:text-lg sm:max-w-xl mx-auto lg:mx-0 mb-8">
                Consolidate your traditional assets, real estate, and equities into a single, highly secure environment. Backed by enterprise-grade compliance and dedicated wealth advisors.
            </p>
            <div class="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
                <a href="#" class="bg-emerald-700 hover:bg-emerald-600 text-white font-bold px-8 py-3.5 rounded-xl shadow-lg transition text-center">
                    Start Your Application
                </a>
                <a href="{% url 'login' %}" class="bg-white hover:bg-slate-50 text-slate-900 border border-slate-300 font-bold px-8 py-3.5 rounded-xl shadow-sm transition text-center">
                    Client Access
                </a>
            </div>
        </div>
        <div class="lg:w-1/2">
            <div class="bg-slate-900 rounded-2xl shadow-2xl p-8 transform rotate-1 hover:rotate-0 transition duration-300">
                <!-- Abstract Dashboard Graphic -->
                <div class="flex items-center justify-between mb-6 border-b border-slate-700 pb-4">
                    <div class="w-1/3 h-4 bg-slate-700 rounded"></div>
                    <div class="w-12 h-12 bg-emerald-500 rounded-full opacity-80"></div>
                </div>
                <div class="space-y-4">
                    <div class="h-8 bg-slate-800 rounded w-3/4"></div>
                    <div class="h-24 bg-slate-800 rounded w-full"></div>
                    <div class="flex gap-4">
                        <div class="h-16 bg-slate-800 rounded w-1/2"></div>
                        <div class="h-16 bg-emerald-900/50 border border-emerald-700 rounded w-1/2"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}"""
    with open("templates/public/home.html", "w", encoding="utf-8") as f:
        f.write(home_html)
    print("[2/4] Created public/home.html (Landing Page).")

    # ---------------------------------------------------------
    # 3. SPLIT-SCREEN LOGIN PAGE
    # ---------------------------------------------------------
    login_html = """{% extends "base_public.html" %}
{% block title %}Secure Login - Asset Portal{% endblock %}

{% block content %}
<div class="flex min-h-[calc(100vh-80px)] bg-white">
    <!-- Left Side: Login Form -->
    <div class="w-full lg:w-1/2 flex items-center justify-center p-8 sm:p-12 lg:p-24">
        <div class="w-full max-w-md space-y-8">
            <div>
                <h2 class="text-3xl font-extrabold text-slate-900 tracking-tight">Access Your Portfolio</h2>
                <p class="mt-2 text-sm text-slate-500">Secure entry to your enterprise wealth management environment.</p>
            </div>
            
            <form method="post" class="mt-8 space-y-6">
                {% csrf_token %}
                <div class="space-y-4">
                    <!-- Standard Django form rendering with Tailwind classes -->
                    {% for field in form %}
                    <div>
                        <label for="{{ field.id_for_label }}" class="block text-sm font-medium text-slate-700 mb-1">{{ field.label }}</label>
                        {{ field }}
                        {% if field.errors %}
                            <p class="text-rose-500 text-xs mt-1">{{ field.errors.0 }}</p>
                        {% endif %}
                    </div>
                    {% endfor %}
                </div>

                <div class="flex items-center justify-between">
                    <div class="flex items-center">
                        <input id="remember-me" name="remember-me" type="checkbox" class="h-4 w-4 text-emerald-600 focus:ring-emerald-500 border-slate-300 rounded">
                        <label for="remember-me" class="ml-2 block text-sm text-slate-700">Remember me for 30 days</label>
                    </div>
                    <div class="text-sm">
                        <a href="#" class="font-medium text-emerald-700 hover:text-emerald-600">Forgot password?</a>
                    </div>
                </div>

                <button type="submit" class="w-full flex justify-center py-3.5 px-4 border border-transparent rounded-xl shadow-sm text-sm font-bold text-white bg-slate-900 hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-slate-900 transition">
                    Authenticate & Enter
                </button>
            </form>
            
            <div class="text-center text-sm text-slate-500 mt-6">
                Don't have an account? <a href="#" class="font-bold text-emerald-700 hover:text-emerald-600">Apply for access</a>
            </div>
        </div>
    </div>

    <!-- Right Side: Graphic / Value Prop -->
    <div class="hidden lg:flex lg:w-1/2 bg-slate-950 items-center justify-center p-12 relative overflow-hidden">
        <!-- Background decorative elements -->
        <div class="absolute inset-0 opacity-10 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-emerald-500 via-slate-900 to-slate-950"></div>
        
        <div class="relative z-10 max-w-lg text-center">
            <div class="inline-flex items-center justify-center w-20 h-20 rounded-full bg-emerald-900/30 border border-emerald-700/50 mb-8">
                <svg class="w-10 h-10 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path></svg>
            </div>
            <h3 class="text-3xl font-bold text-white mb-4">Enterprise-Grade Security</h3>
            <p class="text-slate-400 text-lg leading-relaxed mb-8">
                Your data is protected by strict Multi-Factor Authentication, end-to-end encryption, and rigorous compliance Service Level Agreements.
            </p>
            <div class="flex items-center justify-center gap-4 text-sm font-medium text-slate-300">
                <span class="flex items-center gap-2"><svg class="w-4 h-4 text-emerald-500" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path></svg> Immutable Audits</span>
                <span class="flex items-center gap-2"><svg class="w-4 h-4 text-emerald-500" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path></svg> KYC Compliant</span>
            </div>
        </div>
    </div>
</div>

<!-- Script to automatically style Django form inputs to match Tailwind -->
<script>
    document.addEventListener("DOMContentLoaded", function() {
        const inputs = document.querySelectorAll('input[type="text"], input[type="password"]');
        inputs.forEach(input => {
            input.className = "appearance-none block w-full px-4 py-3 border border-slate-300 rounded-xl shadow-sm placeholder-slate-400 focus:outline-none focus:ring-emerald-500 focus:border-emerald-500 sm:text-sm transition";
        });
    });
</script>
{% endblock %}"""
    with open("templates/registration/login.html", "w", encoding="utf-8") as f:
        f.write(login_html)
    print("[3/4] Replaced basic login with split-screen login.html.")

    # ---------------------------------------------------------
    # 4. MULTI-STEP SIGNUP TEMPLATE
    # ---------------------------------------------------------
    signup_html = """{% extends "base_public.html" %}
{% block title %}Open an Account - Asset Portal{% endblock %}

{% block content %}
<div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
    <div class="text-center mb-12">
        <h2 class="text-3xl font-extrabold text-slate-900">Application for Private Wealth Portal</h2>
        <p class="mt-4 text-slate-500">Complete the initial credentials phase. Multi-Factor setup and KYC document upload will be required upon first login.</p>
    </div>

    <!-- Stepper UI -->
    <div class="flex items-center justify-center mb-12">
        <div class="flex items-center">
            <div class="w-8 h-8 bg-slate-900 text-white rounded-full flex items-center justify-center font-bold shadow-md">1</div>
            <div class="w-16 h-1 bg-slate-200 mx-2 rounded"></div>
            <div class="w-8 h-8 bg-white border-2 border-slate-300 text-slate-400 rounded-full flex items-center justify-center font-bold">2</div>
            <div class="w-16 h-1 bg-slate-200 mx-2 rounded"></div>
            <div class="w-8 h-8 bg-white border-2 border-slate-300 text-slate-400 rounded-full flex items-center justify-center font-bold">3</div>
        </div>
    </div>
    <div class="flex justify-center mb-8 text-xs text-slate-500 font-medium space-x-12">
        <span class="text-slate-900">Credentials</span>
        <span>MFA Setup</span>
        <span>KYC Upload</span>
    </div>

    <!-- Form Container -->
    <div class="bg-white py-10 px-6 shadow-xl rounded-2xl sm:px-12 border border-slate-100">
        <form method="POST" class="space-y-6">
            {% csrf_token %}
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                    <label class="block text-sm font-medium text-slate-700 mb-1">First Name</label>
                    <input type="text" class="block w-full px-4 py-3 border border-slate-300 rounded-xl shadow-sm focus:ring-emerald-500 focus:border-emerald-500 sm:text-sm">
                </div>
                <div>
                    <label class="block text-sm font-medium text-slate-700 mb-1">Last Name</label>
                    <input type="text" class="block w-full px-4 py-3 border border-slate-300 rounded-xl shadow-sm focus:ring-emerald-500 focus:border-emerald-500 sm:text-sm">
                </div>
            </div>

            <div>
                <label class="block text-sm font-medium text-slate-700 mb-1">Email Address</label>
                <input type="email" class="block w-full px-4 py-3 border border-slate-300 rounded-xl shadow-sm focus:ring-emerald-500 focus:border-emerald-500 sm:text-sm">
            </div>

            <div>
                <label class="block text-sm font-medium text-slate-700 mb-1">Secure Password</label>
                <input type="password" class="block w-full px-4 py-3 border border-slate-300 rounded-xl shadow-sm focus:ring-emerald-500 focus:border-emerald-500 sm:text-sm">
                <p class="text-xs text-slate-500 mt-2">Must be at least 12 characters and include a symbol.</p>
            </div>

            <div class="pt-4">
                <button type="submit" class="w-full flex justify-center py-4 px-4 border border-transparent rounded-xl shadow-md text-sm font-bold text-white bg-slate-900 hover:bg-slate-800 transition">
                    Create Account & Continue to MFA
                </button>
            </div>
        </form>
    </div>
</div>
{% endblock %}"""
    with open("templates/registration/signup.html", "w", encoding="utf-8") as f:
        f.write(signup_html)
    print("[4/4] Created multi-step signup.html form.")

if __name__ == "__main__":
    build_frontend()