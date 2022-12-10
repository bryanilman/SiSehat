from django.shortcuts import render
from dokter.forms import PenyakitForm
from dokter.models import Penyakit

from django.shortcuts import render, redirect

from django.contrib import messages

from django.contrib.auth.models import User
from registrasi.models import Pasien, Dokter
from pasien.models import Keluhan

from django.contrib.auth.decorators import login_required

from django.core import serializers

from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse

from django.views.decorators.csrf import csrf_exempt


# Create your views here.

@login_required(login_url='/registrasi/halaman-masuk/')
def show_penyakit(request):
    if request.COOKIES.get('user_type') == 'dokter':
        pasien = Pasien.objects.all()
        data_penyakit = Penyakit.objects.all()
        form = PenyakitForm(request.POST)
        context = {
            'list_penyakit': data_penyakit,
            'list_pasien': pasien,
            'form': form,
        }
        return render(request, 'riwayat_penyakit.html', context)
    else:
        return redirect('registrasi:halaman_registrasi')

@login_required(login_url='/registrasi/halaman-masuk/')
def get_penyakit_pasien(request, pasien):
    if request.COOKIES.get('user_type') == 'dokter':
        pasien = Pasien.objects.get(nomor_induk_kependudukan=pasien)
        data_penyakit = serializers.serialize("json", Penyakit.objects.filter(pasien=pasien))
        return HttpResponse(data_penyakit, content_type="application/json")
    else:
        return redirect('registrasi:halaman_registrasi')

@login_required(login_url='/registrasi/halaman-masuk/')
def add_penyakit(request, pasien):
    if request.COOKIES.get('user_type') == 'dokter':
        form = PenyakitForm(request.POST)

        if request.method == 'POST':
            if form.is_valid():
                penyakit = form.save(commit=False)
                penyakit.pasien = Pasien.objects.get(nomor_induk_kependudukan=pasien)
                penyakit.dokter = Dokter.objects.get(user=request.user)
                penyakit.save()
                return show_penyakit(request)

            return HttpResponseNotFound()        
        return HttpResponseNotFound()
    else:
        return redirect('registrasi:halaman_registrasi')

@login_required(login_url='/registrasi/halaman-masuk/')
def toggle_penyakit(request, id):
    if request.COOKIES.get('user_type') == 'dokter':
        penyakit = Penyakit.objects.get(id=id)
        if penyakit.sembuh:
            penyakit.sembuh = False
        else:
            penyakit.sembuh = True
        penyakit.save()
        return show_penyakit(request)
    else:
        return redirect('registrasi:halaman_registrasi')

@login_required(login_url='/registrasi/halaman-masuk/')
def get_keluhan_pasien(request, pasien):
    if request.COOKIES.get('user_type') == 'dokter':
        pasien = Pasien.objects.get(nomor_induk_kependudukan=pasien)
        dokter = Dokter.objects.get(user=request.user)
        data_keluhan = serializers.serialize("json", Keluhan.objects.filter(pasien=pasien, dokter=dokter))
        return HttpResponse(data_keluhan, content_type="application/json")
    else:
        return redirect('registrasi:halaman_registrasi')

def redirect_home(request):
    return HttpResponseRedirect(reverse('halaman_utama:landing_page'))

# @login_required(login_url='/registrasi/halaman-masuk/')
def show_penyakit_json(request):
    # print(f'active?: {request.user.is_active}')
    data = Penyakit.objects.all()
    return HttpResponse(serializers.serialize("json", data),
                        content_type="application/json")

# @login_required(login_url='/registrasi/halaman-masuk/')
def show_keluhan_json(request):
    # print(f'active?: {request.user.is_active}')
    data = Keluhan.objects.all()
    return HttpResponse(serializers.serialize("json", data),
                        content_type="application/json")

# @login_required(login_url='/registrasi/halaman-masuk/')
def show_pasien_json(request):
    # print(f'active?: {request.user.is_active}')
    data = Pasien.objects.all()
    return HttpResponse(serializers.serialize("json", data),
                        content_type="application/json")

# @login_required(login_url='/registrasi/halaman-masuk/')
def toggle_penyakit_mobile(request, id):
        # print(f'active?: {request.user.is_active}')
        penyakit = Penyakit.objects.get(id=id)
        if penyakit.sembuh:
            penyakit.sembuh = False
        else:
            penyakit.sembuh = True
        penyakit.save()
        return show_penyakit(request)

# @login_required(login_url='/registrasi/halaman-masuk/')
@csrf_exempt
def add_penyakit_mobile(request, pasien):
    # print(f'active?: {request.user.is_active}')
    form = PenyakitForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            penyakit = form.save(commit=False)
            penyakit.pasien = Pasien.objects.get(nomor_induk_kependudukan=pasien)
            user = User.objects.get(username=request.POST["username"])
            dokter = Dokter.objects.get(user=user)
            penyakit.dokter = dokter
            penyakit.save()
            print('a')
            return show_penyakit(request)
        print('b')
        return HttpResponseNotFound()   
    print('c')     
    return HttpResponseNotFound()