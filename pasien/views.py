from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import HttpResponse, render
from django.urls import reverse
from dokter.models import Penyakit

from pasien.forms import RincianKeluhan
from pasien.models import Keluhan
from registrasi.models import Dokter, Pasien

def menentukanTipePengguna(request):
    if request.user != "AnonymousUser" and request.COOKIES.get("user_type") == "pasien":
        if request.COOKIES.get("user_type") == "pasien":
            pasien = True
            dokter = False
        else:
            pasien = False
            dokter = True
    else:
        pasien = False
        dokter = False

    return {'pasien':pasien, 'dokter':dokter, "rincian_keluhan":RincianKeluhan()}

def riwayat(request):
    return render(request, "riwayat.html", menentukanTipePengguna(request))

@login_required(login_url='/registrasi/halaman-masuk/')
def keluhan(request):
    return render(request, "keluhan.html", menentukanTipePengguna(request))

@login_required(login_url='/registrasi/halaman-masuk/')
def mengeluh(request):
    try:
        pasien = Pasien.objects.get(user=request.user)
    except Pasien.DoesNotExist:
        pasien = None

    if request.method == "POST" and RincianKeluhan(request.POST).is_valid():
        nama_dokter = request.POST.get("dokter")

        try:
            user = User.objects.filter(username=nama_dokter)
        except User.DoesNotExist:
            user = None

        if user != None:
            try:
                dokter = Dokter.objects.filter(user=user[0])
            except Dokter.DoesNotExist:
                dokter = None

        tanggal = request.POST.get("tanggal")
        tema = request.POST.get("tema")
        deskripsi = request.POST.get("deskripsi")

        if user != None and dokter != None:
            # membuat keluhan
            keluhan = Keluhan.objects.create(
                pasien=pasien,
                dokter=dokter[0],

                tanggal=tanggal,
                tema=tema,
                deskripsi=deskripsi
            )

            # menyimpan keluhan
            keluhan.save()

            return HttpResponseRedirect(reverse("pasien:keluhan"))
        else:
            return HttpResponseRedirect(reverse("pasien:keluhan"))
    else:
        context = {"pasien":pasien, "rincian_keluhan":RincianKeluhan()}
        return render(request, "keluhan.html", context)

@login_required(login_url='/registrasi/halaman-masuk/')
def daftar_keluhan(request, nilai):
    if nilai == "kosong":
        nilai = ""

    if request.COOKIES.get("user_type") == "pasien":
        try:
            pasien = Pasien.objects.get(user=request.user)
        except Pasien.DoesNotExist:
            pasien = None
            
        daftar_keluhan = Keluhan.objects.filter(pasien=pasien)

    if request.COOKIES.get("user_type") == "dokter":
        try:
            dokter = Dokter.objects.get(user=request.user)
        except Dokter.DoesNotExist:
            dokter = None
            
        daftar_keluhan = Keluhan.objects.filter(dokter=dokter)

    daftar_keluhan_terpilih = set()
    for keluhan in daftar_keluhan:
        if nilai.lower().strip() in keluhan.tema.lower().strip():
            daftar_keluhan_terpilih.add(keluhan)
    
    return HttpResponse(serializers.serialize("json", daftar_keluhan_terpilih), content_type="application/json")

def daftar_dokter(request):
    try:
        dokter = Dokter.objects.all()
    except Dokter.DoesNotExist:
        dokter = None
    
    return HttpResponse(serializers.serialize("json", dokter), content_type="application/json")

def riwayat_penyakit(request):
    try:
        pengguna = User.objects.filter(username=request.COOKIES.get("username"))[0]
    except (IndexError, User.DoesNotExist):
        pengguna = None

    try:
        pasien = Pasien.objects.filter(user=pengguna)[0]
    except (IndexError, NameError, Pasien.DoesNotExist):
        pasien = None
    
    try:
        riwayat_penyakit = Penyakit.objects.filter(pasien=pasien)
    except (IndexError, NameError, Penyakit.DoesNotExist):
        riwayat_penyakit = None
    
    return HttpResponse(serializers.serialize("json", riwayat_penyakit), content_type="application/json")

def riwayat_penyakit_pasien(request, nama):
    try:
        pengguna = User.objects.filter(username=nama)[0]
    except (IndexError, User.DoesNotExist):
        pengguna = None

    try:
        dokter = Dokter.objects.filter(user=pengguna)[0]
    except (IndexError, NameError, Dokter.DoesNotExist):
        dokter = None
    
    try:
        riwayat_penyakit = Penyakit.objects.filter(dokter=dokter)
    except (IndexError, NameError, Penyakit.DoesNotExist):
        riwayat_penyakit = None
    
    return HttpResponse(serializers.serialize("json", riwayat_penyakit), content_type="application/json")

def cari_pengguna(request, id):
    try:
        pasien = Pasien.objects.filter(pk=id)
        nama_pengguna = pasien[0].user.username
    except (IndexError, Pasien.DoesNotExist):
        nama_pengguna = None

    if nama_pengguna == None:
        try:
            dokter = Dokter.objects.filter(pk=id)
            nama_pengguna = dokter[0].user.username
        except (IndexError, Dokter.DoesNotExist):
            nama_pengguna = None

    paket = {"nama_pengguna": nama_pengguna}

    return JsonResponse(paket)

def cari_identitas(request, nama):
    try:
        pengguna = User.objects.filter(username=nama)[0]
    except (IndexError, User.DoesNotExist):
        pengguna = None

    if pengguna != None:
        try:
            pasien = Pasien.objects.filter(user=pengguna)
            identitas = pasien[0].pk
        except (IndexError, Pasien.DoesNotExist):
            identitas = None

        if identitas == None:
            try:
                dokter = Dokter.objects.filter(user=pengguna)
                identitas = dokter[0].pk
            except (IndexError, Dokter.DoesNotExist):
                identitas = None

    paket = {"identitas": identitas}

    return JsonResponse(paket)

@login_required(login_url='/registrasi/halaman-masuk/')
def log_out(request):
    response = HttpResponseRedirect('/registrasi/halaman-masuk/')

    response.delete_cookie('username')
    response.delete_cookie('user_type')
    response.delete_cookie('last_login')

    logout(request)
    return response

def riwayat_terbuka(request):
    penyakit = list(Penyakit.objects.values())
    return JsonResponse({'penyakit': penyakit})
