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
from django.contrib import admin

from .models import Certification, CertificationRecord, CertificationVendor, ContinuingEducationRecord


@admin.register(CertificationVendor)
class CertificationVendorAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_name']
    search_fields = ['name', 'short_name']


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ['short_name', 'name', 'vendor_id_fk', 'valid_term_months', 'units_required']
    list_filter = ['vendor_id_fk']
    search_fields = ['name', 'short_name']


@admin.register(CertificationRecord)
class CertificationRecordAdmin(admin.ModelAdmin):
    list_display = ['user', 'cert_id_fk', 'cert_number', 'eff_date']
    list_filter = ['cert_id_fk']
    search_fields = ['user__username', 'cert_number']


@admin.register(ContinuingEducationRecord)
class ContinuingEducationRecordAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'presenter', 'date', 'hours']
    list_filter = ['date']
    search_fields = ['user__username', 'title', 'presenter']
    filter_horizontal = ['applicable_certs']
