from django import forms
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.crypto import get_random_string

User = get_user_model()


def send_activation_mail(email, activation_code):
    message = f'http://127.0.0.1:8000/accounts/activation/?u={activation_code}'
    send_mail('Активация кода', message, 'test@gmail.com', [email])


class RegistrationForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(min_length=8, widget=forms.PasswordInput, required=True)
    password_confirm = forms.CharField(min_length=8, widget=forms.PasswordInput, required=True)
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)

    class Meta:
        model = User
        fields = ['email', 'password', 'password_confirm', 'first_name', 'last_name']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользовать с таким именем уже существует')
        return email

    def clean(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.pop('password_confirm')
        if password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают')
        return self.cleaned_data

    def save(self):
        user = User.objects.create(**self.cleaned_data)
        user.create_activation_code()
        send_activation_mail(user.email, user.activation_code)
        return user


class ChangePasswordForm(forms.Form):
    old_pass = forms.CharField(min_length=1, widget=forms.PasswordInput)
    new_pass = forms.CharField(min_length=2, widget=forms.PasswordInput)
    new_pass_confirm = forms.CharField(min_length=2, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

    def clean_old_pass(self):
        old_pass = self.cleaned_data.get('old_pass')
        user = self.request.user
        if not user.check_password(old_pass):
            raise forms.ValidationError('Input correct password ')
        return old_pass

    def clean(self):
        new_pass = self.cleaned_data.get('new_pass')
        new_pass_confirm = self.cleaned_data.get('new_pass_confirm')
        if new_pass != new_pass_confirm:
            raise forms.ValidationError('Wrong  old or new  password')
        return self.cleaned_data

    def save(self):
        new_pass = self.cleaned_data.get('new_pass')
        user = self.request.user
        user.set_password(new_pass)
        user.save()


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Unknown user')
        return email

    def send_new_password(self):
        email = self.cleaned_data.get('email')
        new_pass = get_random_string(length=8)
        user = User.objects.get(email=email)
        user.set_password(new_pass)
        user.save()
        send_mail('Восстановление пароля', f'Ваш новый пароль: {new_pass}', 'test@gmail.com', [email])





