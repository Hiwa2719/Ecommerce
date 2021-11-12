from django import forms
from django.utils.translation import gettext_lazy as _

from products.models import Category, Feature


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

    def clean_parent(self):
        parent = self.cleaned_data.get('parent')
        if self.instance:
            if parent == self.instance:
                raise forms.ValidationError(_('You cann\'t add same category to it\'s parent'), code='invalid parent')
        return parent


class FeatureForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['name'] = cleaned_data.get('name').lower()
        cleaned_data['value'] = cleaned_data.get('value').lower()
        return cleaned_data