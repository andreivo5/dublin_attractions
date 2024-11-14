from django.contrib.gis import admin
from .models import WorldBorder, Profile, TouristAttraction

class TouristAttractionAdmin(admin.ModelAdmin):
    search_fields = ('name', 'description')

admin.site.register(WorldBorder, admin.ModelAdmin)
admin.site.register(Profile, admin.ModelAdmin)
admin.site.register(TouristAttraction, TouristAttractionAdmin)
