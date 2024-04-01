from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.index, name="index"),
    path("left-sidebar/", views.left_sidebar_view, name="left_sidebar_view"),
    path("right-sidebar/", views.right_sidebar_view, name="right_sidebar_view"),
    path("no-sidebar/", views.no_sidebar_view, name="no_sidebar_view")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


