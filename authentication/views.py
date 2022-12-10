from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from registrasi.forms import MendaftarDokter, MendaftarPasien

from registrasi.models import Dokter, Pasien
import re

@csrf_exempt
def dokter_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            # Redirect to a success page.
            return JsonResponse({
            "status": True,
            "message": "Successfully Logged In!",
            "username:": username,
            "user_type": "dokter"
            # Insert any extra data if you want to pass data to Flutter
            }, status=200)
        else:
            return JsonResponse({
            "status": False,
            "message": "Failed to Login, Account Disabled."
            }, status=401)
    else:
        return JsonResponse({
        "status": False,
        "message": "Failed to Login, check your email/password."
        }, status=401)

@csrf_exempt
def pasien_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            # Redirect to a success page.
            print(f'active?: {request.user.is_active}')
            return JsonResponse({
            "status": True,
            "message": "Successfully Logged In!",
            "username:": username,
            "user_type": "pasien"
            # Insert any extra data if you want to pass data to Flutter
            }, status=200)
        else:
            return JsonResponse({
            "status": False,
            "message": "Failed to Login, Account Disabled."
            }, status=401)
    else:
        return JsonResponse({
        "status": False,
        "message": "Failed to Login, check your email/password."
        }, status=401)

@csrf_exempt
def registrasi_dokter(request):
    form_mendaftar_dokter = MendaftarDokter()

    if request.method == "POST":
        user = UserCreationForm(request.POST)

        nomor_induk_kependudukan = request.POST["nomor_induk_kependudukan"]
        
        nama_rumah_sakit = request.POST["nama_rumah_sakit"]

        angka_16_digit = "^\d{16}$"
        keabsahan_pengguna = re.search(angka_16_digit, nomor_induk_kependudukan)

        print(user.errors)
        if user.is_valid() and keabsahan_pengguna != None:
            user = user.save()

            dokter = Dokter.objects.create(
                user = user,
                nomor_induk_kependudukan = nomor_induk_kependudukan,
                nama_rumah_sakit = nama_rumah_sakit
            )

            dokter.save()

            return JsonResponse({
                "status": True,
                "message": "Successfully Signed Up!",
                "NIK": nomor_induk_kependudukan,
                "user_type": "dokter"
                # Insert any extra data if you want to pass data to Flutter
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Failed to Sign Up, Account Disabled."
            }, status=401)
    else:
         return JsonResponse({
            "status": False,
            "message": "Failed to Sign Up, check your username/password."
        }, status=401)

@csrf_exempt
def registrasi_pasien(request):
    form_mendaftar_pasien = MendaftarPasien()

    if request.method == "POST":
        user = UserCreationForm(request.POST)

        nomor_induk_kependudukan = request.POST["nomor_induk_kependudukan"]

        angka_16_digit = "^\d{16}$"
        keabsahan_pengguna = re.search(angka_16_digit, nomor_induk_kependudukan)

        if user.is_valid() and keabsahan_pengguna != None:
            user = user.save()

            pasien = Pasien.objects.create(
                user = user,
                nomor_induk_kependudukan = nomor_induk_kependudukan
            )

            pasien.save()

            return JsonResponse({
                "status": True,
                "message": "Successfully Signed Up!",
                "NIK": nomor_induk_kependudukan,
                "user_type": "pasien"
                # Insert any extra data if you want to pass data to Flutter
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Failed to Sign Up, Account Disabled."
            }, status=401)
    else:
         return JsonResponse({
            "status": False,
            "message": "Failed to Sign Up, check your username/password."
        }, status=401)

@csrf_exempt
def logout_user(request):
    print(f'active?: {request.user.is_active}')
    logout(request)
    print(f'AFTLGOUTactive?: {request.user.is_active}')
    return JsonResponse({
            "status": True,
            "message": "Successfully logged out."
        }, status=401)
    