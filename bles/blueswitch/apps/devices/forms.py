from django import forms
from django.utils.translation import ugettext as _


class UploadFileForm(forms.Form):
    """
    """
    file = forms.FileField(label='Choose excel to upload')
