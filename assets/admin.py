from django.contrib import admin
from .models import Asset, Vehicle, Land, House, Stock, GovernmentBond

class AssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'owner', 'current_estimated_value', 'currency', 'status')
    list_filter = ('category', 'status', 'currency')
    search_fields = ('name', 'unique_reference', 'owner__username')

admin.site.register(Asset, AssetAdmin)
admin.site.register(Vehicle)
admin.site.register(Land)
admin.site.register(House)
admin.site.register(Stock)
admin.site.register(GovernmentBond)
