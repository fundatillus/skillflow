# Skillflow — self-hosted certification tracker for IT and security professionals
# Copyright (C) 2026  Adam Clements
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from django.urls import path

from . import views

app_name = 'skillflow'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('certs/add/', views.cert_add, name='cert-add'),
    path('certs/<int:pk>/edit/', views.cert_edit, name='cert-edit'),
    path('certs/<int:pk>/delete/', views.cert_delete, name='cert-delete'),
    path('certs/<int:pk>/', views.cert_detail, name='cert-detail'),
    path('ce/add/', views.ce_add, name='ce-add'),
    path('ce/<int:pk>/edit/', views.ce_edit, name='ce-edit'),
    path('ce/<int:pk>/delete/', views.ce_delete, name='ce-delete'),
]
