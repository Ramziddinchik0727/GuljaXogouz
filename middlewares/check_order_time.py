from datetime import time
from loader import types

import pytz

class CheckOrderTime:
    async def check_order_time(self, message: types.Message, user):
        server_time = message.date
        tashkent_tz = pytz.timezone('Asia/Tashkent')
        local_time = server_time.astimezone(tashkent_tz).time()

        start_time = time(11, 0)
        end_time = time(23, 0)

        if start_time <= local_time <= end_time:
            return True
        else:
            return False
