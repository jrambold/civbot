from django.contrib import admin
from .models import Player, FlexMatch, SoloMatch

admin.site.register(Player)
admin.site.register(SoloMatch)
admin.site.register(FlexMatch)
