from django import forms
from .models import *


class BotUserForm(forms.ModelForm):
    class Meta:
        model = BotUser
        fields = ('telegram_id',
                  'nickname',
                  'full_name',
                  'email',
                  'notify'
                  )

        widgets = {
            'first_name': forms.NumberInput,
            'nickname': forms.TextInput,
            'full_name': forms.TextInput,
            'email': forms.TextInput,
        }
