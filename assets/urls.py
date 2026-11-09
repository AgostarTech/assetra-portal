from django.urls import path
from . import views

app_name = "assets"

urlpatterns = [
    # All assets list
    path("", views.asset_list, name="asset_list"),

    # Dedicated Category Views
    path("vehicles/", views.vehicle_list, name="vehicle_list"),
    path("land/", views.land_list, name="land_list"),
    path("houses/", views.house_list, name="house_list"),
    path("stocks/", views.stock_list, name="stock_list"),
    path("bonds/", views.bond_list, name="bond_list"),
    path("others/", views.other_list, name="other_list"),

    # Add assets
    path("add/vehicle/", views.create_vehicle, name="create_vehicle"),
    path("add/land/", views.create_land, name="create_land"),
    path("add/house/", views.create_house, name="create_house"),
    path("add/stock/", views.create_stock, name="create_stock"),
    path("add/bond/", views.create_bond, name="create_bond"),
    path("add/other/", views.create_other, name="create_other"),

    # Supporting documents & Intelligence Vault
    path("documents/", views.asset_documents, name="asset_documents"),
    path("map/", views.asset_map, name="asset_map"),
    path("timeline/", views.asset_timeline, name="asset_timeline"),

    # Individual asset actions
    path("<int:asset_id>/", views.asset_detail, name="asset_detail"),
    path("<int:asset_id>/edit/", views.asset_update, name="asset_update"),
    path("<int:asset_id>/delete/", views.asset_delete, name="asset_delete"),
    path("<int:asset_id>/report/", views.asset_report_pdf, name="asset_report_pdf"),
]