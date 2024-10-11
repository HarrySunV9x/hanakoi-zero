import json


# 加载配置文件的函数
def load_config():
    with open('config.json', 'r') as config_file:
        return json.load(config_file)


# 在模块加载时读取配置，只执行一次
llm_config = load_config()
