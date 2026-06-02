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
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CertificationRecordForm, ContinuingEducationRecordForm
from .models import CertificationRecord, ContinuingEducationRecord


@login_required
def dashboard(request):
    records = CertificationRecord.objects.filter(
        user=request.user
    ).select_related('cert_id_fk')
    ce_hours = {}
    ce_progress = {}
    for rec in records:
        total = rec.continuingeducationrecord_set.aggregate(Sum('hours'))['hours__sum'] or 0
        ce_hours[rec.pk] = total
        required = rec.cert_id_fk.units_required if rec.cert_id_fk else 0
        ce_progress[rec.pk] = min(100, int(total / required * 100)) if required else 0
    return render(request, 'skillflow/dashboard.html', {
        'records': records,
        'ce_hours': ce_hours,
        'ce_progress': ce_progress,
    })


@login_required
def cert_add(request):
    if request.method == 'POST':
        form = CertificationRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.user = request.user
            record.save()
            messages.success(request, 'Certification added.')
            return redirect('skillflow:dashboard')
    else:
        form = CertificationRecordForm()
    return render(request, 'skillflow/cert_form.html', {'form': form, 'action': 'Add'})


@login_required
def cert_edit(request, pk):
    record = get_object_or_404(CertificationRecord, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CertificationRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Certification updated.')
            return redirect('skillflow:cert-detail', pk=pk)
    else:
        form = CertificationRecordForm(instance=record)
    return render(request, 'skillflow/cert_form.html', {'form': form, 'action': 'Edit'})


@login_required
def cert_delete(request, pk):
    record = get_object_or_404(CertificationRecord, pk=pk, user=request.user)
    if request.method == 'POST':
        record.delete()
        messages.success(request, 'Certification removed.')
        return redirect('skillflow:dashboard')
    return render(request, 'skillflow/cert_confirm_delete.html', {'record': record})


@login_required
def cert_detail(request, pk):
    record = get_object_or_404(CertificationRecord, pk=pk, user=request.user)
    ce_records = ContinuingEducationRecord.objects.filter(applicable_certs=record)
    total_ce = ce_records.aggregate(Sum('hours'))['hours__sum'] or 0
    return render(request, 'skillflow/cert_detail.html', {
        'record': record,
        'ce_records': ce_records,
        'total_ce': total_ce,
    })


@login_required
def ce_add(request):
    if request.method == 'POST':
        form = ContinuingEducationRecordForm(request.POST, request.FILES)
        form.fields['applicable_certs'].queryset = CertificationRecord.objects.filter(user=request.user)
        if form.is_valid():
            ce = form.save(commit=False)
            ce.user = request.user
            ce.save()
            form.save_m2m()
            messages.success(request, 'CE record added.')
            return redirect('skillflow:dashboard')
    else:
        form = ContinuingEducationRecordForm()
        form.fields['applicable_certs'].queryset = CertificationRecord.objects.filter(user=request.user)
    return render(request, 'skillflow/ce_form.html', {'form': form, 'action': 'Add'})


@login_required
def ce_edit(request, pk):
    ce = get_object_or_404(ContinuingEducationRecord, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ContinuingEducationRecordForm(request.POST, request.FILES, instance=ce)
        form.fields['applicable_certs'].queryset = CertificationRecord.objects.filter(user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'CE record updated.')
            return redirect('skillflow:dashboard')
    else:
        form = ContinuingEducationRecordForm(instance=ce)
        form.fields['applicable_certs'].queryset = CertificationRecord.objects.filter(user=request.user)
    return render(request, 'skillflow/ce_form.html', {'form': form, 'action': 'Edit'})


@login_required
def ce_delete(request, pk):
    ce = get_object_or_404(ContinuingEducationRecord, pk=pk, user=request.user)
    if request.method == 'POST':
        ce.delete()
        messages.success(request, 'CE record deleted.')
        return redirect('skillflow:dashboard')
    return render(request, 'skillflow/ce_confirm_delete.html', {'ce': ce})
