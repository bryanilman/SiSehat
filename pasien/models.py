from datetime import datetime
from django.db import models

from accounts.models import Dokter, Pasien

class Keluhan(models.Model):
    pasien = models.ForeignKey(Pasien, on_delete=models.DO_NOTHING)
    dokter = models.ForeignKey(Dokter, on_delete=models.DO_NOTHING)
    tanggal = models.DateField(primary_key=True)
    tema = models.CharField(max_length=120)
    deskripsi = models.TextField()
