from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("veille.urls")),

]
handler400='prjt.views.handler400'
handler403='prjt.views.handler403'
handler404='prjt.views.handler404'
handler500='prjt.views.handler500'

