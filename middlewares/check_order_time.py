from datetime import time
from loader import types

class CheckOrderTime:
    async def check_order_time(self, message: types.Message, user):
        date = message.date
        local_time = date.time()

        start_time = time(11, 0)
        end_time = time(23, 0)

        if start_time <= local_time <= end_time:
            return True
        else:
            return False
