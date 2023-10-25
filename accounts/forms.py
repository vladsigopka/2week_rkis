from .models import Application, User, Category
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, EmailValidator


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=255, label="Логин")

    full_name = forms.CharField(max_length=255, label="ФИО")

    password = forms.CharField(widget=forms.PasswordInput(), label="Пароль")
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Подтвердите пароль")
    email = forms.EmailField(label="Email")
    checkbox = forms.CharField(label='Согласие на обработку персональных данных', widget=forms.CheckboxInput,
                               required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'full_name')

    def clean_full_name(self):
        full_name = self.cleaned_data['full_name']
        if not all(char.isalpha() or char.isspace() or char == '-' for char in full_name):
            raise forms.ValidationError("ФИО должно содержать только кириллические буквы, дефис и пробелы.")
        return full_name

    def clean_username(self):
        username = self.cleaned_data['username']
        if not all(char.isalpha() or char == '-' for char in username):
            raise forms.ValidationError("Логин может содержать только латинские буквы и дефис.")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Логин уже занят.")
        return username

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['confirm_password']
        if password != password2:
            raise forms.ValidationError("Пароли не совпадают.")
        return password2

    def clean_checkbox(self):
        cd = self.cleaned_data
        print(cd['checkbox'])
        if cd['checkbox'] == False:
            raise forms.ValidationError('Подтвердите обработку персональных данных')
        return cd['checkbox']


class ApplicationCreateForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['title', 'desc', 'img']

    def clean_photo(self):
        img = self.cleaned_data.get('img')
        if img:
            if img.size > 2 * 1024 * 1024:
                raise ValidationError("Размер фото должен быть не более 2Мб.")
            if not img.name.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                raise ValidationError("Фото должно быть в формате jpg, jpeg, png или bmp.")
        return img

    # class Meta:
    #     model = Application
    #     fields = ('title', 'desc', 'img')


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
