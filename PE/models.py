from django.db import models


# Create your models here.
class MasterData(models.Model):
    Cus_name = models.CharField(max_length=250, null=True)
    PE = models.CharField(max_length=250, null=True)
    PN = models.CharField(max_length=250, null=True)
    Model = models.CharField(max_length=250, null=True)
    ICPN = models.CharField(max_length=250, null=True)
    ICSpec = models.CharField(max_length=250, null=True)
    Part_burn = models.CharField(max_length=250, null=True)
    FwVer = models.CharField(max_length=250, null=True)
    ICPos = models.CharField(max_length=250, null=True)
    CheckSum = models.CharField(max_length=250, null=True)
    Prog_name = models.CharField(max_length=250, null=True)
    dot_color = models.CharField(max_length=250, null=True)
    dot_pos = models.ImageField(upload_to='templates/images/')
    Change_date = models.DateField(auto_now=False)
    Fw_note = models.CharField(max_length=250, null=True)
      

