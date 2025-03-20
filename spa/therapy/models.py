from django.contrib.auth.models import AbstractUser
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


class User(AbstractUser):
    class Role(models.IntegerChoices):
        Boss = 0, 'Босс'
        Customer = 1, 'Пользователь'
        Worker = 2, 'Специалист'
        Receptionist = 3, 'Администратор'

    role = models.PositiveSmallIntegerField(choices=Role.choices, default=Role.Customer, verbose_name='кто по жизни')
    phone = models.CharField(max_length=12, blank=True, null=True, verbose_name='Телефон')
    photo = models.ImageField(upload_to='user.photos', blank=True, null=True, verbose_name='Фото')
    registration_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['id']


class ServicesCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True)
    is_public = models.BooleanField(default=True, verbose_name='Публикация')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория услуг'
        verbose_name_plural = 'Категории услуг'


class Services(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True)
    category = models.ForeignKey(ServicesCategory, on_delete=models.CASCADE, related_name='services',
                                 verbose_name='Категория')
    duration = models.PositiveIntegerField(verbose_name='Длительность приема в минутах')
    price = models.PositiveIntegerField(verbose_name='Цена')
    woker_reward = models.PositiveIntegerField(verbose_name='Вознаграждение специалиста')
    discription = CKEditor5Field('Описание', config_name='extends', blank=True, null=True)
    is_public = models.BooleanField(default=True, verbose_name='Публикация')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'


class BidStatus(models.TextChoices):
    RAW = 'CREATED', 'Создана'
    ADMINCONFIRMED = 'CONFIRMED1', 'Подтверждена администратором'
    WORKERCONFIRMED = 'CONFIRMED2', 'Подтверждена специалистом'
    REJECTED = 'REJECTED', 'Отклонена'
    PAID = 'PAID', 'Оплачена'
    COMLETED = 'COMPLETED', 'Завершена'


class Bid(models.Model):
    SEX = (
        ('male', 'Мужской'),
        ('female', 'Женский'),)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bid_user', verbose_name='Пользователь')
    service = models.ForeignKey(Services, on_delete=models.CASCADE, related_name='bid_services', verbose_name='Услуга')
    date = models.DateTimeField(verbose_name='Дата')
    worker = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 2}, related_name='bid_worker',
                               verbose_name='специалист')
    is_chaild_bid = models.BooleanField(default=False, verbose_name='заявка для ребенка')
    date_of_birth = models.DateField(verbose_name='Дата рождения клиента', blank=True, null=True)
    sex = models.CharField(max_length=10, choices=SEX, default='male', verbose_name='Пол')
    status = models.CharField(max_length=50, choices=BidStatus.choices, default=BidStatus.RAW,
                              verbose_name='статус заказа')
    note = CKEditor5Field('Примечание', config_name='extends', blank=True, null=True)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'


class Abonements(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    servise = models.ForeignKey(Services, on_delete=models.CASCADE, related_name='abonements_services', verbose_name='Услуга')
    price = models.PositiveIntegerField(verbose_name='Цена')
    number_of_visits = models.PositiveIntegerField(verbose_name='Количество посещений')
    days_limit = models.PositiveIntegerField(verbose_name='Лимит дней')
    description = CKEditor5Field('Описание', config_name='extends', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Абонемент'
        verbose_name_plural = 'Абонементы'


class AbonementBid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='abo_user',
                             limit_choices_to={'role': 1}, verbose_name='Пользователь')
    worker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='abo_worker',
                                 limit_choices_to={'role': 2}, verbose_name='специалист')
    abonement = models.ForeignKey(Abonements, on_delete=models.CASCADE, related_name='abo_bid',
                                  verbose_name='Абонемент')
    start_day = models.DateField(auto_now_add=True)
    rest_of_visits = models.PositiveIntegerField(verbose_name='Оставшийся лимит посещений')

    class Meta:
        verbose_name = 'Заявка на абонемент'
        verbose_name_plural = 'Заявки на абонементы'


class WorkerSchedule(models.Model):
    class WeekDays(models.IntegerChoices):
        MONDAY = 0, "Понедельник"
        TUESDAY = 1, "Вторник"
        WEDNESDAY = 2, "Среда"
        THURSDAY = 3, "Четверг"
        FRIDAY = 4, "Пятница"
        SATURDAY = 5, "Суббота"
        SUNDAY = 6, "Воскресенье"

    worker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='worker_schedule',
                               limit_choices_to={'role': 2}, verbose_name='Специалист')
    day_of_week = models.SmallIntegerField(choices=WeekDays.choices, verbose_name='День недели')
    start_time = models.TimeField(verbose_name='Начало рабочего дня')
    end_time = models.TimeField(verbose_name='Конец рабочего дня')
    pre_entry_days = models.PositiveIntegerField(default=14,
                                                 verbose_name="предварительная запись на прием (кол-во дней)")

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписание'
