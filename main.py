import os
import platform

from application import app
from application.config.ServerConfig import ServerConfig
from application.middleware.TimedTaskMiddleware import TimedTaskMiddleware
from application.middleware.global_vars import global_timed_task
from application.util.WorkFlowUtil import start_deque

# 定义启动命令
command: str = f"python -m gunicorn --log-level debug application:app -b {ServerConfig.host}:{ServerConfig.port} -w {ServerConfig.workers}"
# 获取系统类型
system: str = platform.system()
# 实例化定时任务类
timed_task: TimedTaskMiddleware = global_timed_task

if __name__ == "__main__":
    # 启动定时任务调度器
    timed_task.start_scheduler()
    # 启动任务进度扫描
    timed_task.start_scan_progress()
    # 启动任务队列
    start_deque()

    # 启动Flask服务器
    if system == "Linux":
        os.system(command=command)
    elif system == "Windows":
        app.run(host=ServerConfig.host, port=ServerConfig.port, debug=False)
    else:
        print("无法识别当前系统")
