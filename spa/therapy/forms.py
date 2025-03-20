from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from django.contrib.auth import get_user_model
from datetime import datetime
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordResetForm,
)
from django.utils.translation import gettext_lazy as _
from django import forms

from therapy.models import Bid

User = get_user_model()


# форма регистрации пользователя
class UserCreateForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Зарегистрироваться'))

    phone = forms.CharField(max_length=12, required=False)
    photo = forms.ImageField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "first_name", 'last_name', "phone", "password1", "password2", 'photo',
                  )
        widgets = {
            'sex': forms.RadioSelect(),
            'date_of_birth': forms.DateInput(attrs={'type': 'date',
                                                    'max': datetime.now().date()}),
        }


# форма редактирования данных пользователя
class ChangeUserlnfoForm(UserCreateForm):
    pass


# форма входа пользователя
class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                "Введите логин и пароль",
                'username',
                'password',

            ),
            Submit('submit', 'Войти'),
        )


# форма сброса пароля
class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                "Введите адрес электронной почты",
                'email',

            ),
            Submit('submit', 'отправить'),
        )


class AddBidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ('service', 'date', 'worker', 'is_chaild_bid', 'date_of_birth', 'sex', 'note')
