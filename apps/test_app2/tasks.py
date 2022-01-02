from libs import settings
from apps.test_app2 import models

@settings.background_scheduler.scheduled_job('interval', seconds=60, max_instances=1)
def offline_task():
    model = models.TOfflineTask
    undo_tasks = model.objects().filter(model.process=='未完成').all()
    for undo_task in undo_tasks:
        # 处理离线任务逻辑
        pass
    print("test_app2:处理离线任务逻辑")
