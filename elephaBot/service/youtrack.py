from .bot import bot
from .database import get_user_by_email, get_users_to_notify


def assignee_alert(data: dict) -> bool:
    try:
        email = data['email']
        description = data['description']
        summary = data['summary']
        issue_link = data['link']
        project = data['project']
    except KeyError:
        return False

    assignee = get_user_by_email(email)

    if assignee is not None:
        bot.send_message(assignee.telegram_id,
                         "На вас назначена новая задача!\n\n"
                         f"Проект: <b>{project}</b>\n"
                         f"Название: <a href='{issue_link}'>{summary}</a>\n"
                         f"Описание: <b>{description}</b>",
                         parse_mode='html')
        return True

    return False


def notify(data: dict) -> bool:
    try:
        summary = data['summary']
        issue_link = data['link']
        state = data['state']
        project = data['project']
    except KeyError:
        return False

    users = get_users_to_notify()

    if users is not None:
        for user in users:
            bot.send_message(user.telegram_id,
                             f"Новый статус задачи!\n\n"
                             f"Проект: <b>{project}</b>\n"
                             f"Задача: <a href='{issue_link}'>{summary}</a>\n"
                             f"Статус: <b>{state}</b>",
                             parse_mode='html')
        return True

    return False
