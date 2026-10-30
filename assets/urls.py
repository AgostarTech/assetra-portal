
from django.urls import path

from . import views

app_name = "assets"

urlpatterns = [
    # All assets and category filtering
    path("", views.asset_list, name="asset_list"),

    # Add assets
    path("add/vehicle/", views.create_vehicle, name="create_vehicle"),
    path("add/land/", views.create_land, name="create_land"),
    path("add/house/", views.create_house, name="create_house"),
    path("add/stock/", views.create_stock, name="create_stock"),
    path("add/bond/", views.create_bond, name="create_bond"),

    # Supporting documents
    path("documents/", views.asset_documents, name="asset_documents"),

    # Edit an existing asset
    path("<int:asset_id>/edit/", views.asset_update, name="asset_update"),
]
