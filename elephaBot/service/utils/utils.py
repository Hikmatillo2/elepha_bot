import re


def check_user_message(data: str, email: bool = False) -> bool:
    pattern = "[A-Za-zА-Яа-я-'@.]"

    if email:
        pattern = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if re.fullmatch(pattern, data):
            return True
    else:
        result = re.findall(pattern, data)
        if len(result) == len(data):
            return True

    return False
