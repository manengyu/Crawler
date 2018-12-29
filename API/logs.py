import os
import sys
import logging
import logging.handlers
from raven import Client
from flask import session
from functools import reduce


class Logs:
    PATH = os.path.join(os.path.dirname(sys.path[0]), "logs")
    LEVELS = ('INFO', 'ERROR', "WARNING")
    LOG_INSTANCE = None
    SENTRY_INSTANCE = None
    ARGS_CONFIG = ""

    def __init__(self, *args):
        print('init Logs,sys.path:', sys.path)
        Logs.ARGS_CONFIG = args[1]
        if not os.path.isdir(Logs.PATH):
            os.makedirs(Logs.PATH, 0o777, True)

        logs_instance = dict()
        for i in Logs.LEVELS:
            lower = i.lower()
            logger_name = lower + '_logger'

            logs_instance[logger_name] = logging.getLogger(i)
            handler = logging.handlers.TimedRotatingFileHandler(
                os.path.join(Logs.PATH, lower + '.log'),
                when='MIDNIGHT',
                interval=1,
                backupCount=15,
                encoding="utf-8"
            )
            handler.setFormatter(
                logging.Formatter('%(asctime)s%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
            )
            console = logging.StreamHandler()  # add console print
            console.setLevel(logging.INFO)
            logs_instance[logger_name].addHandler(console)
            logs_instance[logger_name].addHandler(handler)
            logs_instance[logger_name].setLevel(i)
        Logs.LOG_INSTANCE = logs_instance

        dsn = args[0] if len(args) > 0 else None
        if Logs.SENTRY_INSTANCE is None and dsn:
            Logs.SENTRY_INSTANCE = Client(dsn)
            Logs.SENTRY_INSTANCE.logger = Logs.LOG_INSTANCE['error_logger']
            # Logs.SENTRY_INSTANCE = Logs.LOG_INSTANCE.__getattribute__('error_logger')


def logs(fn):
    name = getattr(fn, '__name__')

    def wrapper(*args, **kwargs):
        session_flag, args_c = "", ""
        try:
            result = fn(*args, **kwargs)
            if "SESSION_COOKIE_NAME" in Logs.ARGS_CONFIG:
                session_flag = id(session.__getattr__("on_update"))

            if "create_app" == name:
                args_c = dict(result.config)
                if Logs.LOG_INSTANCE is None:
                    Logs(args_c["DSN"], args_c)
                if Logs.SENTRY_INSTANCE:
                    Logs.SENTRY_INSTANCE.captureMessage(
                        format_msg("启动参数:", get_nopwd(dict(result.config))).replace("'", "\""), level='warning')
                Logs.LOG_INSTANCE['warning_logger'].warning(format_msg("启动参数:", get_nopwd(args_c)).replace("'", "\""))
                return result

            Logs.LOG_INSTANCE['info_logger'].info(
                format_msg(session_flag, name, result, args, kwargs))
            return result
        except Exception as e:
            if Logs.SENTRY_INSTANCE is not None:
                Logs.SENTRY_INSTANCE.captureException(exc_info=True, message=format_msg(  # 异常捕获,上传traceback
                    id(session.__getattr__("on_update")), name, e.args, args, kwargs))
                Logs.LOG_INSTANCE['error_logger'].error(format_msg(session_flag, name, e.args, args, kwargs))
                # Logs.SENTRY_INSTANCE.captureMessage(format_msg(name, e))  # sentry由消息合并事件,因此需去除参数 msg
            raise e

    setattr(wrapper, '__name__', name)
    return wrapper


def format_msg(*args):
    return reduce(lambda x, y: "{} {}".format(x, y), args, "")


def get_nopwd(data_dic):
    rnt_dic = {}
    for k, v in data_dic.items():
        rnt_dic[k] = "*" if "_PWD" in k else "{}".format(v)
    rnt_dic["start_file_name"] = sys.argv[0]
    return rnt_dic


# @logs
# def create_app():
#     report_app = Flask(__name__)
#     report_app.config.from_object(config)
#     report_app.url_map.strict_slashes = False
#     report_app.register_blueprint(grant_blueprint)
#     return report_app
#
#
# @logs
# def create_app():
#     class App(object):
#         config = config.__dict__
#     return App
#
#
# app = create_app()
#
#
# def run_flask():
#     app.run(host=config.HOST, port=config.PORT)
