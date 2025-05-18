from django import forms
from .models import Tutor
import re

class TutorForm(forms.ModelForm):
    class Meta:
        model = Tutor
        fields = ['nome', 'sobrenome', 'rua', 'bairro', 'telefone', 'cidade', 'estado', 'cep', 'email', 'cpf']
        labels = {
            'nome': 'Nome',
            'sobrenome': 'Sobrenome',
            'rua': 'Rua',
            'bairro': 'Bairro',
            'telefone': 'Telefone',
            'cidade': 'Cidade',
            'estado': 'Estado',
            'cep': 'CEP',
            'email': 'E-mail',
            'cpf': 'CPF',
        }

    def clean_telefone(self):
        telefone = self.cleaned_data['telefone']
        if not re.match(r'^\(\d{2}\)\s9\d{4}-\d{4}$', telefone):
            raise forms.ValidationError('Telefone deve estar no formato (XX) 9XXXX-XXXX, como (11) 91234-5678.')
        return telefone

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        cpf_clean = re.sub(r'[^0-9]', '', cpf)
        if len(cpf_clean) != 11:
            raise forms.ValidationError('CPF deve conter 11 dígitos.')
        return cpf_clean

    def clean_cep(self):
        cep = self.cleaned_data['cep']
        if not re.match(r'^\d{5}-\d{3}$', cep):
            raise forms.ValidationError('CEP deve estar no formato XXXXX-XXX, como 12345-678.')
        return cep

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['telefone'].widget.attrs.update({
            'class': 'telefone-mask',
            'placeholder': '(11) 91234-5678',
            'type': 'text',
            'maxlength': '15'
        })
        self.fields['cpf'].widget.attrs.update({
            'class': 'cpf-mask',
            'placeholder': '123.456.789-09',
            'type': 'text',
            'maxlength': '14'
        })
        self.fields['cep'].widget.attrs.update({
            'class': 'cep-mask',
            'placeholder': '12345-678',
            'type': 'text',
            'maxlength': '9'
        })