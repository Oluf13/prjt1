from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Veille, Article
from .models import Req

admin.site.register(Req)
admin.site.register(Veille)
admin.site.register(Article)
