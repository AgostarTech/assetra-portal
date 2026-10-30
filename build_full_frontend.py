import os

def build_frontend():
    # 1. Ensure all directories exist
    directories = [
        "static/css", 
        "static/js", 
        "templates/public/includes", 
        "templates/registration"
    ]
    for d in directories:
        os.makedirs(d, exist_ok=True)

    # ---------------------------------------------------------
    # 2. STATIC FILES (CSS & JS)
    # ---------------------------------------------------------
    # Tailwind Configuration (JS)
    tailwind_js = """tailwind.config = {
    theme: {
        extend: {
            colors: {
                brand: {
                    black: '#0a0a0a',
                    dark: '#1a1a1a',      // Primary Dark
                    gold: '#cfa76e',      // Primary Gold
                    goldlight: '#e8c99b', // Highlight Gold
                }
            }
        }
    }
}"""
    with open("static/js/tailwind-config.js", "w", encoding="utf-8") as f:
        f.write(tailwind_js)

    # Public Custom CSS
    public_css = """/* Custom overrides and animations for public site */
.glass-panel {
    background: rgba(26, 26, 26, 0.85);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(207, 167, 110, 0.3);
}
.gold-glow {
    box-shadow: 0 0 20px rgba(207, 167, 110, 0.4);
}
.hero-bg {
    background: radial-gradient(circle at center, #1a1a1a 0%, #0a0a0a 100%);
}
"""
    with open("static/css/public.css", "w", encoding="utf-8") as f:
        f.write(public_css)

    # ---------------------------------------------------------
    # 3. MODULAR COMPONENTS (Header & Footer)
    # ---------------------------------------------------------
    header_html = """{% load static %}
<header class="bg-brand-dark border-b border-brand-gold/30 sticky top-0 z-50 shadow-md">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-20">
            <!-- Logo & Brand -->
            <div class="flex-shrink-0 flex items-center gap-4">
                <img src="{% static 'images/asset_logo_3.jpg.jpg' %}" alt="Asset Portal Logo" class="h-14 w-14 rounded-full border-2 border-brand-gold gold-glow">
                <span class="font-bold text-2xl tracking-widest text-brand-gold uppercase">Asset Portal</span>
            </div>
            
            <!-- Main Navigation -->
            <nav class="hidden md:flex space-x-8">
                <a href="{% url 'home' %}" class="text-slate-300 hover:text-brand-gold font-medium transition tracking-wide">Home</a>
                <a href="{% url 'about' %}" class="text-slate-300 hover:text-brand-gold font-medium transition tracking-wide">About Us</a>
                <a href="{% url 'solutions' %}" class="text-slate-300 hover:text-brand-gold font-medium transition tracking-wide">Solutions</a>
                <a href="{% url 'contact' %}" class="text-slate-300 hover:text-brand-gold font-medium transition tracking-wide">Contact</a>
            </nav>

            <!-- Call to Actions -->
            <div class="flex items-center space-x-5">
                <a href="{% url 'login' %}" class="text-brand-gold hover:text-white font-semibold transition tracking-wide">Log In</a>
                <a href="{% url 'signup' %}" class="bg-brand-gold hover:bg-brand-goldlight text-brand-dark font-bold px-6 py-2.5 rounded shadow-lg transition tracking-wide uppercase text-sm">
                    Open Account
                </a>
            </div>
        </div>
    </div>
</header>"""
    with open("templates/public/includes/header.html", "w", encoding="utf-8") as f:
        f.write(header_html)

    footer_html = """<footer class="bg-brand-black text-slate-400 py-12 border-t border-brand-gold/30 mt-auto">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid grid-cols-1 md:grid-cols-4 gap-8">
        <div>
            <h3 class="text-brand-gold font-bold text-lg mb-4 uppercase tracking-widest">Asset Portal</h3>
            <p class="text-sm leading-relaxed">Institutional-grade portfolio tracking and compliance management for high-net-worth individuals.</p>
        </div>
        <div>
            <h4 class="text-white font-semibold mb-4 tracking-wide">Platform</h4>
            <ul class="space-y-2 text-sm">
                <li><a href="#" class="hover:text-brand-gold transition">Enterprise Security</a></li>
                <li><a href="#" class="hover:text-brand-gold transition">Compliance SLA</a></li>
            </ul>
        </div>
        <div>
            <h4 class="text-white font-semibold mb-4 tracking-wide">Legal</h4>
            <ul class="space-y-2 text-sm">
                <li><a href="#" class="hover:text-brand-gold transition">Terms of Service</a></li>
                <li><a href="#" class="hover:text-brand-gold transition">Privacy Policy</a></li>
            </ul>
        </div>
        <div class="flex flex-col justify-end">
            <p class="text-sm text-slate-500">&copy; {% now "Y" %} Enterprise Asset Portal.<br>All rights reserved.</p>
        </div>
    </div>
</footer>"""
    with open("templates/public/includes/footer.html", "w", encoding="utf-8") as f:
        f.write(footer_html)

    # ---------------------------------------------------------
    # 4. BASE PUBLIC TEMPLATE
    # ---------------------------------------------------------
    base_public_html = """{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Enterprise Asset Portfolio{% endblock %}</title>
    <!-- Tailwind CSS (CDN for development) -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Custom Tailwind Configuration -->
    <script src="{% static 'js/tailwind-config.js' %}"></script>
    <!-- Custom Public Styles -->
    <link rel="stylesheet" href="{% static 'css/public.css' %}">
</head>
<body class="bg-brand-black text-slate-200 font-sans antialiased flex flex-col min-h-screen">
    
    {% include 'public/includes/header.html' %}

    <main class="flex-grow">
        {% block content %}{% endblock %}
    </main>

    {% include 'public/includes/footer.html' %}
</body>
</html>"""
    with open("templates/base_public.html", "w", encoding="utf-8") as f:
        f.write(base_public_html)

    # ---------------------------------------------------------
    # 5. PUBLIC PAGES (Home, About, Solutions, Contact)
    # ---------------------------------------------------------
    pages = {
        "home.html": """{% extends 'base_public.html' %}
{% block content %}
<div class="hero-bg min-h-[80vh] flex items-center border-b border-brand-gold/20">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 flex flex-col lg:flex-row items-center gap-12">
        <div class="lg:w-1/2 text-center lg:text-left">
            <h1 class="text-4xl tracking-widest font-extrabold text-white sm:text-5xl md:text-6xl mb-6 uppercase">
                <span class="block">Institutional</span>
                <span class="block text-brand-gold mt-2">Private Wealth.</span>
            </h1>
            <p class="mt-4 text-lg text-slate-300 max-w-xl mx-auto lg:mx-0 mb-8 leading-relaxed">
                Consolidate your traditional assets, real estate, and equities into a single, highly secure environment.
            </p>
            <div class="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
                <a href="{% url 'signup' %}" class="bg-brand-gold hover:bg-brand-goldlight text-brand-dark font-bold px-8 py-3.5 rounded shadow-[0_0_15px_rgba(207,167,110,0.4)] transition text-center uppercase tracking-wide">
                    Start Application
                </a>
                <a href="{% url 'login' %}" class="bg-transparent hover:bg-white/5 text-brand-gold border border-brand-gold font-bold px-8 py-3.5 rounded transition text-center uppercase tracking-wide">
                    Client Access
                </a>
            </div>
        </div>
        <div class="lg:w-1/2 flex justify-center">
            <!-- Decorative Shield / Vault Graphic placeholder -->
            <div class="w-72 h-72 rounded-full border-4 border-brand-gold/20 flex items-center justify-center relative">
                <div class="w-56 h-56 rounded-full border-4 border-brand-gold/40 flex items-center justify-center animate-[spin_10s_linear_infinite]">
                    <div class="w-40 h-40 bg-brand-gold/10 rounded-full gold-glow"></div>
                </div>
                <div class="absolute inset-0 flex items-center justify-center">
                    <svg class="w-20 h-20 text-brand-gold" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path></svg>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}""",
        "about.html": """{% extends 'base_public.html' %}{% block content %}<div class="max-w-7xl mx-auto py-20 text-center"><h1 class="text-4xl font-bold text-brand-gold mb-6 uppercase tracking-widest">About Our Firm</h1></div>{% endblock %}""",
        "solutions.html": """{% extends 'base_public.html' %}{% block content %}<div class="max-w-7xl mx-auto py-20 text-center"><h1 class="text-4xl font-bold text-brand-gold mb-6 uppercase tracking-widest">Enterprise Solutions</h1></div>{% endblock %}""",
        "contact.html": """{% extends 'base_public.html' %}{% block content %}<div class="max-w-7xl mx-auto py-20 text-center"><h1 class="text-4xl font-bold text-brand-gold mb-6 uppercase tracking-widest">Contact Support</h1></div>{% endblock %}"""
    }
    for filename, html in pages.items():
        with open(f"templates/public/{filename}", "w", encoding="utf-8") as f:
            f.write(html)

    # ---------------------------------------------------------
    # 6. AUTHENTICATION PAGES (Login & Signup)
    # ---------------------------------------------------------
    login_html = """{% extends "base_public.html" %}
{% load static %}
{% block title %}Secure Login - Asset Portal{% endblock %}
{% block content %}
<div class="flex min-h-[calc(100vh-80px)] bg-brand-black">
    <!-- Left Side: Login Form -->
    <div class="w-full lg:w-1/2 flex items-center justify-center p-8">
        <div class="glass-panel p-10 rounded-lg w-full max-w-md shadow-2xl">
            <div class="text-center mb-8">
                <h2 class="text-2xl font-extrabold text-white tracking-widest uppercase">Access Portfolio</h2>
                <p class="mt-2 text-sm text-brand-gold">Secure Enterprise Gateway</p>
            </div>
            <form method="post" class="space-y-6">
                {% csrf_token %}
                <div class="space-y-4">
                    {% for field in form %}
                    <div>
                        <label class="block text-sm font-medium text-slate-300 mb-1">{{ field.label }}</label>
                        {{ field }}
                    </div>
                    {% endfor %}
                </div>
                <button type="submit" class="w-full py-3 px-4 rounded font-bold text-brand-dark bg-brand-gold hover:bg-brand-goldlight transition tracking-wide uppercase mt-4">
                    Authenticate
                </button>
            </form>
            <div class="text-center text-sm text-slate-400 mt-6">
                No account? <a href="{% url 'signup' %}" class="font-bold text-brand-gold hover:underline">Apply here</a>
            </div>
        </div>
    </div>
    <!-- Right Side: Graphic -->
    <div class="hidden lg:flex lg:w-1/2 items-center justify-center p-12 bg-black">
        <img src="{% static 'images/asset_logo_3.jpg.jpg' %}" alt="Enterprise Trust" class="max-w-md rounded-full border-4 border-brand-gold/30 gold-glow opacity-80">
    </div>
</div>

<script>
    document.addEventListener("DOMContentLoaded", function() {
        const inputs = document.querySelectorAll('input[type="text"], input[type="password"]');
        inputs.forEach(input => {
            input.className = "w-full px-4 py-3 bg-brand-dark border border-slate-700 rounded text-white focus:outline-none focus:border-brand-gold transition";
        });
    });
</script>
{% endblock %}"""
    with open("templates/registration/login.html", "w", encoding="utf-8") as f:
        f.write(login_html)

    signup_html = """{% extends "base_public.html" %}
{% block title %}Open Account - Asset Portal{% endblock %}
{% block content %}
<div class="max-w-3xl mx-auto px-4 py-16">
    <div class="text-center mb-10">
        <h2 class="text-3xl font-bold text-brand-gold uppercase tracking-widest">Application Portal</h2>
        <p class="mt-2 text-slate-400">Step 1: Secure Credentials</p>
    </div>
    <div class="glass-panel py-10 px-8 shadow-2xl rounded-lg">
        <form method="POST" class="space-y-6">
            {% csrf_token %}
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                    <label class="block text-sm text-slate-300 mb-1">First Name</label>
                    <input type="text" class="w-full px-4 py-3 bg-brand-dark border border-slate-700 rounded text-white focus:border-brand-gold outline-none">
                </div>
                <div>
                    <label class="block text-sm text-slate-300 mb-1">Last Name</label>
                    <input type="text" class="w-full px-4 py-3 bg-brand-dark border border-slate-700 rounded text-white focus:border-brand-gold outline-none">
                </div>
            </div>
            <div>
                <label class="block text-sm text-slate-300 mb-1">Email Address</label>
                <input type="email" class="w-full px-4 py-3 bg-brand-dark border border-slate-700 rounded text-white focus:border-brand-gold outline-none">
            </div>
            <div>
                <label class="block text-sm text-slate-300 mb-1">Secure Password</label>
                <input type="password" class="w-full px-4 py-3 bg-brand-dark border border-slate-700 rounded text-white focus:border-brand-gold outline-none">
            </div>
            <div class="pt-4">
                <button type="submit" class="w-full py-4 rounded font-bold text-brand-dark bg-brand-gold hover:bg-brand-goldlight transition tracking-widest uppercase">
                    Create Credentials & Continue
                </button>
            </div>
        </form>
    </div>
</div>
{% endblock %}"""
    with open("templates/registration/signup.html", "w", encoding="utf-8") as f:
        f.write(signup_html)

    # ---------------------------------------------------------
    # 7. ROUTING (urls.py)
    # ---------------------------------------------------------
    urls_path = "config/urls.py"
    if os.path.exists(urls_path):
        with open(urls_path, "r", encoding="utf-8") as f:
            urls_content = f.read()

        new_routes = """from django.views.generic import TemplateView

urlpatterns = [
    # Public Facing Website Routes
    path('', TemplateView.as_view(template_name='public/home.html'), name='home'),
    path('about/', TemplateView.as_view(template_name='public/about.html'), name='about'),
    path('solutions/', TemplateView.as_view(template_name='public/solutions.html'), name='solutions'),
    path('contact/', TemplateView.as_view(template_name='public/contact.html'), name='contact'),
    path('signup/', TemplateView.as_view(template_name='registration/signup.html'), name='signup'),"""
        
        if "path('', RedirectView" in urls_content:
            urls_content = urls_content.replace('path("", RedirectView.as_view(url="dashboard/router/", permanent=False)),', '')
        
        if "from django.views.generic import TemplateView" not in urls_content:
            urls_content = urls_content.replace("urlpatterns = [", new_routes)
            with open(urls_path, "w", encoding="utf-8") as f:
                f.write(urls_content)

    print("SUCCESS: Frontend architecture built securely with separate CSS, JS, and modular components!")

if __name__ == "__main__":
    build_frontend()