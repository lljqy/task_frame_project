import os
import sys
import warnings
import importlib

# 消除告警
warnings.filterwarnings('ignore')

# 根据需要修改下面配置文件dev或者prod
os.environ.setdefault("GLOBAL_SETTINGS", "settings.dev")


def main():
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
    # 启动任务
    # config.background_scheduler.start()
    # config.background_scheduler.shutdown()
    # config.asyncio_scheduler.start()
    # config.asyncio_scheduler.shutdown()
    print("开始启动")
    config.scheduler.start()
    print("启动成功")


if __name__ == '__main__':
    main()
    print("开始了")
