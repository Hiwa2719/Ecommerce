from django import forms
from django.utils.translation import gettext_lazy as _
from products.models import Category


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
