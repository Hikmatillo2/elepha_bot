from django.contrib import admin

from .forms import *

@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ['telegram_id',
                    'nickname',
                    'full_name',
                    'email',
                    'notify'
                    ]

    form = BotUserForm
