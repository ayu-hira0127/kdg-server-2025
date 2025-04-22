from django import forms
from django.forms.widgets import ClearableFileInput
from .models import Product, ProductImage

class SearchForm(forms.Form):
    query = forms.CharField(
        label='検索キーワード',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': '検索したいキーワードを入力'})
    )

class CustomClearableFileInput(ClearableFileInput):
    allow_multiple_selected = True

# forms.py の修正部分
class ProductForm(forms.ModelForm):
    images = forms.FileField(
        widget=CustomClearableFileInput(attrs={'multiple': True}),
        required=True,
        label='画像ファイル'
    )

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category']
        labels = {
            'name': '商品名',
            'description': '商品説明',
            'price': '価格',
            'category': 'カテゴリ',
        }

    def clean_images(self):
        images = self.cleaned_data.get('images')  # 修正点
        if not images:
            raise forms.ValidationError('少なくとも1つの画像をアップロードする必要があります。')
        if len(images) > 10:
            raise forms.ValidationError('画像は最大10枚までアップロード可能です。')
        for image in images:
            if image.size > 5 * 1024 * 1024:  # 5MB以上の画像を弾く
                raise forms.ValidationError('画像サイズは5MB以下である必要があります。')
        return images

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        images = self.cleaned_data.get('images', [])
        for image in images:
            ProductImage.objects.create(product=instance, image=image)
        if commit:
            self.save_m2m()  # Save many-to-many relationships after saving the instance
        return instance

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']