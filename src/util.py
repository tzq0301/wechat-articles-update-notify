import logging


def log_around(f):
    def func(*args, **kwargs):
        logging.info(f"{f.__name__} 开始执行")
        f(*args, **kwargs)
        logging.info(f"{f.__name__} 结束执行")

    return func
