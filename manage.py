import os
import sys
import warnings
import importlib

# 消除告警
warnings.filterwarnings('ignore')

# 根据需要修改下面配置文件dev或者prod
os.environ.setdefault("GLOBAL_SETTINGS", "settings.dev")


def start_scheduler():
    # 将项目加载到python包搜索路径中
    BASE_PATH = os.path.dirname(__file__)
    sys.path.append(BASE_PATH)
    for dir_or_file in os.listdir(BASE_PATH):
        if os.path.isdir(dir_or_file):
            sys.path.append(os.path.join(BASE_PATH, dir_or_file))
    config = importlib.import_module(os.environ.get("GLOBAL_SETTINGS"))
    # 读取任务
    for app in config.INSTALL_APPS:
        importlib.import_module(app + '.tasks')
    # 启动任务（顺序启动后台任务, 协程任务，阻塞任务）
    config.background_scheduler.start()
    config.asyncio_scheduler.start()
    config.scheduler.start()


def main():
    if not sys.platform.startswith("win32"):
        import atexit
        import fcntl
        f = open("scheduler.lock", "wb")
        try:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
            start_scheduler()
        except:
            pass

        def unlock():
            fcntl.flock(f, fcntl.LOCK_UN)
            f.close()

        atexit.register(unlock())
    else:
        start_scheduler()


if __name__ == '__main__':
    main()
