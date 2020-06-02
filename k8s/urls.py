"""k8s URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url
from credit_k8s import views as iviews
from manage_k8s import views as mviews

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^index$', iviews.index, name='index'),
    url(r'^init$', iviews.init, name='init'),
    url(r'^init_2$', iviews.init_2, name='init_2'),
    url(r'^init_api$', iviews.init_api, name='init_api'),
    url(r'^install_packet$', iviews.install_packet, name='install_packet'),
    url(r'^update$', mviews.update, name='update'),
    url(r'^update_api$', mviews.update_api, name='update_api'),
    url(r'^add_node$', mviews.add_node, name='add_node'),
    url(r'^add_node_api$', mviews.add_node_api, name='add_node_api')
]
