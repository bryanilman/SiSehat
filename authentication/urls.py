from django.urls import path
from authentication.views import dokter_login, logout_user, pasien_login, registrasi_dokter, registrasi_pasien

app_name = 'authentication'

urlpatterns = [
    path('dokter-login/', dokter_login, name='dokter_login'),
    path('pasien-login/', pasien_login, name='pasien_login'),    
    path('dokter-signup/', registrasi_dokter, name='dokter_signup'),    
    path('pasien-signup/', registrasi_pasien, name='pasien_signup'),    
    path('logout/', logout_user, name='logout'),    
]
