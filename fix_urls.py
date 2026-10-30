import os

url_path = "portfolios/urls.py"
if os.path.exists(url_path):
    with open(url_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    if "from django.urls import path, include" not in content:
        content = content.replace("from django.urls import path", "from django.urls import path, include")
        with open(url_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("SUCCESS: Added 'include' import to portfolios/urls.py!")
else:
    print("Creating portfolios/urls.py with correct imports...")
    os.makedirs("portfolios", exist_ok=True)
    with open(url_path, "w", encoding="utf-8") as f:
        f.write("from django.urls import path, include\n\nurlpatterns = [\n    path('compliance/report/export/', include('portfolios.reports')),\n]\n")
