from django.db import models


class BotUser(models.Model):
    telegram_id = models.BigIntegerField(
        primary_key=True,
        verbose_name='ID в телеграм',
        null=False,
        blank=False,
    )

    nickname = models.TextField(
        verbose_name='Никнейм',
        null=False,
        blank=False,
    )

    first_name = models.TextField(
        verbose_name='Имя',
        null=True,
        blank=False,
    )

    second_name = models.TextField(
        verbose_name='Фамилия',
        null=True,
        blank=False,
    )

    email = models.TextField(
        verbose_name='Почта',
        null=True,
        blank=False,
    )

    phone_number = models.TextField(
        verbose_name='Номер телефона',
        null=True,
        blank=False,
    )

    completed = models.BooleanField(
        default=False,
    )

    objects = models.Manager()

    def __str__(self):
        return f'@{self.nickname}'

    class Meta:
        verbose_name = 'Пользователь бота'
        verbose_name_plural = 'Пользователи бота'


class BotUserCondition(models.Model):
    user = models.OneToOneField(
        to=BotUser,
        on_delete=models.CASCADE,
    )

    on_first_name_input = models.BooleanField(
        verbose_name='Ввод имени',
        default=False,
        null=True,
        blank=False,
    )

    on_second_name_input = models.BooleanField(
        verbose_name='Ввод фамилии',
        default=False,
        null=True,
        blank=False,
    )

    on_email_input = models.BooleanField(
        verbose_name='Ввод почты',
        default=False,
        null=True,
        blank=False,
    )

    on_phone_number_input = models.BooleanField(
        verbose_name='Ввод номера телефона',
        default=False,
        null=True,
        blank=False,
    )

    def __str__(self):
        return f'Состояние для @{self.user.nickname}'

    class Meta:
        verbose_name = 'Состояние пользователя'
        verbose_name_plural = 'Состояния пользователей'


class File(models.Model):
    title = models.TextField(
        verbose_name='Название файла',
        blank=False,
        null=False,
    )
    file = models.FileField(
        upload_to='files/',
        verbose_name='Файл',
        blank=False,
        null=False,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
