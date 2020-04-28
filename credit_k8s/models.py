from django.db import models

# Create your models here.
class packet_install(models.Model):
    packet_name=models.CharField(max_length=255, verbose_name=u"包名")
    packet_url=models.CharField(max_length=255, verbose_name=u"url")
    install_id=models.IntegerField(verbose_name=u"步骤", default=1)

