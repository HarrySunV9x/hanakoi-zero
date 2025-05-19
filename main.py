"""
main.py

启动fastapi服务
"""

import threading

from restful import start_uvicorn
from web import start_normal_invoke, start_chat_invoke

if __name__ == "__main__":
    thread1 = threading.Thread(target=start_normal_invoke)
    thread2 = threading.Thread(target=start_chat_invoke)
    thread3 = threading.Thread(target=start_uvicorn)

    thread1.start()
    thread2.start()
    thread3.start()

    thread1.join()
    thread2.join()
    thread3.join()
