"""
URL configuration for octopus project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from graphene_django.views import AsyncGraphQLView

from api.schema_sync import schema_sync
from api.schema_async import schema_async

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "graphql_async/",
        csrf_exempt(AsyncGraphQLView.as_view(schema=schema_async, graphiql=True)),
    ),
    path("graphql_sync/", csrf_exempt(GraphQLView.as_view(schema=schema_sync, graphiql=True))),

]
