from django import forms
from .models import Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'

    def save(self, commit=True):
        instance = super(ClientForm, self).save(commit=commit)
        if commit:
            instance.action_on_save = True
            instance.save()
        return instance
