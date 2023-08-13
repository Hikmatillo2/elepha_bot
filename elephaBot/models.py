from django.db import models


class BotUser(models.Model):
    telegram_id = models.BigIntegerField(primary_key=True,
                                         verbose_name='ID в телеграм',
                                         null=False,
                                         blank=False
                                         )

    nickname = models.TextField(verbose_name='Никнейм',
                                null=False,
                                blank=False
                                )

    full_name = models.TextField(verbose_name='ФИО',
                                 null=False,
                                 blank=False
                                 )

    email = models.TextField(verbose_name='Почта',
                             null=False,
                             blank=False
                             )

    notify = models.BooleanField(verbose_name="Уведомление о статусе задач",
                                 null=False,
                                 blank=False,
                                 default=False)

    objects = models.Manager()

    def __str__(self):
        return f'#{self.telegram_id} {self.full_name} @{self.nickname}'

    class Meta:
        verbose_name = 'Админ бота'
        verbose_name_plural = 'Админы бота'
