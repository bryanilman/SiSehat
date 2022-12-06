from django.urls import path
from dokter.views import add_penyakit_mobile, show_penyakit, get_penyakit_pasien, add_penyakit, toggle_penyakit, get_keluhan_pasien, redirect_home, show_keluhan_json, show_penyakit_json, show_pasien_json, toggle_penyakit_mobile

app_name = 'dokter'

urlpatterns = [
    path('riwayat-penyakit/', show_penyakit, name='show_riwayat_penyakit'),
    path('riwayat-penyakit/<str:pasien>', get_penyakit_pasien, name='get_penyakit_pasien'),
    path('add-penyakit/<str:pasien>', add_penyakit, name='add_penyakit'),
    path('toggle-penyakit/<int:id>', toggle_penyakit, name='toggle-penyakit'),
    path('riwayat-keluhan/<str:pasien>', get_keluhan_pasien, name='get_keluhan_pasien'),
    path('home/', redirect_home, name='home'),
    path('penyakit/', show_penyakit_json, name='penyakit'),
    path('keluhan/', show_keluhan_json, name='keluhan'),
    path('pasien/', show_pasien_json, name='pasien'),
    path('toggle-mobile/<int:id>', toggle_penyakit_mobile, name='toggle_mob'),
    path('add-penyakit-mobile/<str:pasien>', add_penyakit_mobile, name='add_mob'),
]
