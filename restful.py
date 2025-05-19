import glob
import os
import time

import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rich import print
from starlette.responses import FileResponse

from brain.comfyui import queue_prompt_text
from brain.config import llm_config
from brain.invoke import normal_invoke, chat_invoke

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头
)


class PromptRequest(BaseModel):
    prompt: str


@app.get("/")
def root_api():
    return "root"


@app.post("/invoke")
def invoke_api(request: PromptRequest):
    return normal_invoke(request.speaker, request.type, request.prompt)


@app.post("/hana_chat_invoke")
def invoke_api(request: PromptRequest):
    if request.context_id:
        return chat_invoke(request.speaker, request.prompt, request.context_id)
    else:
        return chat_invoke(request.speaker, request.prompt)


@app.post("/painter")
def painter_api(file: UploadFile = File(...)):
    with open(llm_config.get("PAINT_INPUT_IMAGE"), "wb") as f:
        f.write(file.file.read())

    # 1. 删除文件
    print(":smiley:[bold magenta]painter_api[/bold magenta]", "remove origin file")
    file_pattern = llm_config.get("PAINT_OUTPUT_IMAGE")
    file_paths = glob.glob(file_pattern)

    # 删除所有匹配的文件
    for file_path in file_paths:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"删除文件失败: {e}")

    # 2. 执行 queue_prompt_text (替换成实际的命令或函数)
    print(":smiley:[bold magenta]painter_api[/bold magenta]", "queue_prompt_text")
    queue_prompt_text("")

    # 3. 轮询文件是否存在
    timeout = 60  # 设置超时时间，比如 60 秒
    start_time = time.time()
    while time.time() - start_time < timeout:
        print(":smiley:[bold magenta]painter_api[/bold magenta]", "check output")
        file_paths = glob.glob(file_pattern)
        if len(file_paths) != 0:
            file_path = file_paths[0]
            print(f"File generated and ready for download: {file_path}")
            return FileResponse(file_path, media_type='image/png', filename=os.path.basename(file_path))
        time.sleep(1)  # 每秒检查一次

    print(":smiley:[bold magenta]painter_api[/bold magenta]", "ok")
    # 超时后抛出异常
    raise HTTPException(status_code=408, detail="文件生成超时")


def start_uvicorn():
    uvicorn.run(app, host="0.0.0.0", port=3002)
