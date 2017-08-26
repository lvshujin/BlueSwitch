from django import forms
from django.utils.translation import ugettext_lazy as _, ugettext

from django.core.exceptions import ValidationError

from blueswitch.libs.accounts.models import User
from blueswitch.apps.devices.models import TwinDevice


class DeviceUpdateForm(forms.ModelForm):
    """
    Class Based Device Form required to update the Device.
    """
    def __init__(self, *args, **kwargs):
        try:
            if 'instance' in kwargs:
                self.id = kwargs['instance'].id
        except Exception as e:
            pass

        super(DeviceUpdateForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        """
        Meta Information required to generate model form, and to mention the fields, widgets and fieldsets
        information required to render for the form.
        """
        model = TwinDevice
        exclude = ()

    def clean(self):
        cleaned_data = super(DeviceUpdateForm, self).clean()
        mac1 = cleaned_data.get('mac1', None)
        mac2 = cleaned_data.get('mac2', None)

        if mac1:
            if (mac1 == mac2):
                raise ValidationError("mac1 & mac2 should not same.")
        return cleaned_data


class ProfileForm(forms.ModelForm):
    """
    Class Based Profile Form required to update the admin profile.
    """
    def __init__(self, *args, **kwargs):
        try:
            if 'instance' in kwargs:
                self.id = kwargs['instance'].id
        except Exception as e:
            pass

        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password1'].label = 'Password'
        self.fields['confirm_password'].widget.attrs.update({'placeholder': 'Confirm Password'})
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

    password1 = forms.CharField(max_length=128, required=False)
    confirm_password = forms.CharField(max_length=128, required=False, widget=forms.PasswordInput)

    class Meta:
        """
        Meta Information required to generate model form, and to mention the fields, widgets and fieldsets
        information required to render for the form.
        """
        model = User
        fields = ('name', 'email',  'password1', 'confirm_password')

    def clean_confirm_password(self):
        password = self.cleaned_data['password1']
        confirm_password = self.cleaned_data.pop('confirm_password')
        if password != confirm_password:
            raise ValidationError("password does not match.")

        return confirm_password
