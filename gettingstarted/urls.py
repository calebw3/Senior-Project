from django.urls import path, include

from django.contrib import admin

admin.autodiscover()

import hello.views

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("", hello.views.index, name="index"),
    path("admin/", admin.site.urls),
    path("explore/", hello.views.explore),
    path("groups/", hello.views.groups, name="groups"),
    path("groups/<str:name>", hello.views.group),
    #login urlpatterns
    path('login/', hello.views.signIn),
    path('home/', hello.views.home),
    path('postsignIn/', hello.views.postsignIn),
    path('signUp/', hello.views.signUp, name="signup"),
    path('logout/', hello.views.logout, name="log"),
    path('postsignUp/', hello.views.postsignUp),
    path('filter/', hello.views.filter),
    path('postcreateGroup/', hello.views.postcreateGroup),

]
