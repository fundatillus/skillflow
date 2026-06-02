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
from datetime import date

from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.db import models


class CertificationVendor(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.short_name}"


class Certification(models.Model):
    """Template added by admin"""
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=20)
    vendor_id_fk = models.ForeignKey(CertificationVendor,
                                     on_delete=models.PROTECT,
                                     null=True)
    valid_term_months = models.IntegerField()
    units_required = models.IntegerField()

    def __str__(self):
        return f"{self.short_name}"


class CertificationRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cert_id_fk = models.ForeignKey(Certification,
                                   on_delete=models.PROTECT,
                                   null=True)
    cert_number = models.CharField(max_length=50, null=True, blank=True)
    eff_date = models.DateField()

    @property
    def exp_date(self):
        if self.eff_date and self.cert_id_fk:
            return self.eff_date + relativedelta(months=self.cert_id_fk.valid_term_months)
        return None

    @property
    def status(self):
        today = date.today()
        if self.exp_date is None:
            return 'unknown'
        if self.exp_date < today:
            return 'expired'
        if (self.exp_date - today).days <= 90:
            return 'expiring'
        return 'active'

    def __str__(self):
        return f"{self.cert_id_fk} ({self.user.username})"


class ContinuingEducationRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    presenter = models.CharField(max_length=100)
    date = models.DateField()
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    certificate_file = models.FileField(
        upload_to='ce_certificates/',
        null=True,
        blank=True,
    )
    applicable_certs = models.ManyToManyField(CertificationRecord)

    def __str__(self):
        return f"{self.presenter} - {self.title}"
