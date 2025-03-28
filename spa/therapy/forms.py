from cProfile import label
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

from therapy.models import Bid, BidStatus

User = get_user_model()


# форма регистрации пользователя
class UserCreateForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.add_input(Submit("submit", "Зарегистрироваться"))

    phone = forms.CharField(max_length=12, required=False)
    photo = forms.ImageField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "password1",
            "password2",
            "photo",
        )
        widgets = {
            "sex": forms.RadioSelect(),
            "date_of_birth": forms.DateInput(
                attrs={"type": "date", "max": datetime.now().date()}
            ),
        }


# форма редактирования данных пользователя
class ChangeUserlnfoForm(UserCreateForm):
    pass


# форма входа пользователя
class UserLoginForm(AuthenticationForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     self.helper = FormHelper(self)
    #     self.helper.layout = Layout(
    #         Fieldset(
    #             "Введите логин и пароль",
    #             "username",
    #             "password",
    #         ),
    #         Submit("submit", "Войти"),
        # )
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'input'}), )
    password = forms.CharField(label=_("password"), widget=forms.PasswordInput(attrs={'class': 'input'}), )   


# форма сброса пароля
class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                "Введите адрес электронной почты",
                "email",
            ),
            Submit("submit", "отправить"),
        )


class AddBidForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["service"].empty_label = "выберите услугу"
        self.fields["worker"].empty_label = "выберите специалиста"
        self.helper = FormHelper(self)
        self.helper.add_input(Submit("submit", "Создать заявку"))

    def save(self, commit=True):
        # Сначала сохраняем объект, чтобы у него появился id
        instance = super().save(commit=commit)

        # Затем устанавливаем связи many-to-many
        if commit:
            instance.statuses.set([1])  # Устанавливаем статус с id=1
        return instance

    class Meta:
        model = Bid
        fields = (
            "service",
            "date",
            "worker",
            "is_chaild_bid",
            "date_of_birth",
            "sex",
            "note",
        )
        widgets = {
            "sex": forms.RadioSelect(),
            "date": forms.DateInput(
                attrs={"type": "date", "min": datetime.now().date()}
            ),
            "date_of_birth": forms.DateInput(
                attrs={"type": "date", "max": datetime.now().date()}
            ),
            
        }
        help_texts = {
            "date": _("Выберите дату в формате ДД-ММ-ГГГГ"),
            "date_of_birth": _("Выберите дату в формате ДД-ММ-ГГГГ"),
        }
        labels = {
            "note": _("Дополнительная информация (если есть)"),
        }
        
