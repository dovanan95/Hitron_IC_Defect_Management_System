from django import forms
from PE.models import MasterData

class MasterForm(forms.ModelForm):
    class Meta:
        model = MasterData
        fields = "__all__"