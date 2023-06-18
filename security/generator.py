from datetime import datetime, timedelta
import random


def code_confirm_generator():
    expire = datetime.now() + timedelta(
        seconds=600
    )
    code = random.randint(10000, 99999)
    return expire, code


