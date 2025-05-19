- # 赛博女儿零号机——hanakoi  

构建AI的  

* 眼——图像识别
* 耳——语音识别
* 口——TTS
* 手——Agent
* 脑——LLM

的能力。

## 环境搭建
1️⃣ clone 项目
2️⃣ 安装python环境：

1. git clone https://github.com/pyenv-win/pyenv-win 并配置环境变量：

   ```
   F:\pyenv-win-master\pyenv-win\bin
   F:\pyenv-win-master\pyenv-win\shims
   ```

2. 查看支持的python版本列表

   ```
   pyenv install -l
   ```

3. 安装一个版本

   ```
   pyenv install 3.11.9
   ```

4. 将python版本设置为全局版本

   ```
   pyenv global 3.11.9
   ```

5. 查看安装的所有python版本

   ```
   pyenv versions
   ```

6. 查看使用的python版本及其路径

   ```
   pyenv version
   ```

7. 卸载python版本

   ```
   pyenv uninstall 3.11.9
   ```

3️⃣ 修改pip源（可选）：

```
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip config set install.trusted-host pypi.tuna.tsinghua.edu.cn
```

4️⃣ 创建python虚拟环境与依赖：

```
python -m venv .venv
.\.venv\Scripts\activate
pip install -r .\requirements.txt
```

5️⃣ 运行：

```
python main.py
```

## 脑

历史版本曾用过LangChain，放弃的原因有：
* LangChain每次更新，库依赖差距过大，经常导致各种不兼容，难以定制化自己想要用的LLM相关技术栈
* LangChain过度抽象化，简单的语句无需过度抽象，代码阅读和维护困难。
* 提升自己造轮子的能力。  

后面尝试用过过dify这种更全面的框架，最后决定放弃，理由与LangChain差不多。最后还是决定自己编写LLM的实现。