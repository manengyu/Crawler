# -*- coding:utf-8 -*-


def retry_request(num):  # 总计尝试num次
    def wrapper(func):
        def to_do(*args, **kwargs):
            is_true, values = False, u""
            n = 0
            while n < num:
                n += 1
                is_true, values = func(*args, **kwargs)
                if not is_true:
                    break
                if is_true:
                    break
            return is_true, values
        return to_do
    return wrapper
    
