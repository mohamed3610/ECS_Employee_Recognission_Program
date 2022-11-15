from django.urls import path
from . import views

urlpatterns = [
    path("home",views.index , name = "users-home"),
    path("api/announcements",views.get_announcements , name = "get_announcements"),
    path("index/<int:anouncement_id>", views.announcement_view, name = "anouncement"),
    path("<int:anouncement_id>/index", views.delete_announcements_view , name = "delete_announcements"),
    path("add_Notification",views.add_notifications , name = "Announcement"),
    path("archive/<str:model_name>",views.view_archive, name = "archive"),
    path("archive/",views.view_archive, name = "archive", kwargs={'model_name':'Users'}),
    # path("leaderboard/",views.leaderboard, name = "leaderboard"),
]
