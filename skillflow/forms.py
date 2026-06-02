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
from django import forms

from .models import CertificationRecord, ContinuingEducationRecord


class CertificationRecordForm(forms.ModelForm):
    class Meta:
        model = CertificationRecord
        fields = ['cert_id_fk', 'cert_number', 'eff_date']
        widgets = {
            'eff_date': forms.DateInput(attrs={'type': 'date'}),
        }


class ContinuingEducationRecordForm(forms.ModelForm):
    class Meta:
        model = ContinuingEducationRecord
        fields = ['title', 'presenter', 'date', 'hours', 'certificate_file', 'applicable_certs']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'applicable_certs': forms.CheckboxSelectMultiple(),
        }
