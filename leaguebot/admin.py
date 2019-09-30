from django.contrib import admin
from .models import Player, FlexMatch, SoloMatch, Rank, Champion

admin.site.register(Champion)
admin.site.register(Player)
admin.site.register(Rank)
admin.site.register(SoloMatch)
admin.site.register(FlexMatch)
