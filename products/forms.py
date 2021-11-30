from django import forms
from django.utils.translation import gettext_lazy as _

from products.models import Category, Product


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


class ProductForm(forms.ModelForm):
    features_excel = forms.FileField(required=False)

    class Meta:
        model = Product
        fields = '__all__'

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.cleaned_data['features_excel']:
            csv = self.cleaned_data.get('features_excel')
            file_content = csv.readlines()
            line_lists = []
            for line in file_content:
                line = line.decode('windows-1252').strip().replace("\"", '')
                line_lists.append(line.split(',', 2))
            result = {}
            for items in line_lists:
                line_dict = self.dictionary_export(items)
                key, value = line_dict.popitem()
                value2 = result.get(key, None)
                if value2:
                    value.update(value2)
                    result[key] = value
                else:
                    result[key] = value

            instance.features = [{i: result[i]} for i in result]
        if commit:
            instance = instance.save()
        return instance

    def dictionary_export(self, items):
        key = items[0]
        value = items[1:]
        if len(value) == 1:
            value = value[0]
        elif len(value) > 1:
            value = self.dictionary_export(items[1:])
        return {key: value}
