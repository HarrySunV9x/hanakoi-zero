import gradio as gr

from invoke import normal_invoke, chat_invoke

with gr.Blocks() as normal_invoke_gradio:
    with gr.Row():
        prompt = gr.Textbox(label="prompt")
        speaker = gr.Textbox(label="speaker")
        prompt_type = gr.Dropdown(choices=['hana', 'base'], label="type")
        model = gr.Dropdown(choices=['llama3.1', 'gemma2', 'qwen2.5'], label="model")
    with gr.Row():
        output = gr.Textbox(label="Greeting", lines=20)  # 设置为5行文本框

    gr.Button("Submit").click(fn=normal_invoke, inputs=[speaker, prompt_type, model, prompt], outputs=output)

with gr.Blocks() as chat_invoke_gradio:
    with gr.Row():
        prompt = gr.Textbox(label="prompt")
        speaker = gr.Textbox(label="speaker")
        context_id = gr.Textbox(label="context_id")
    with gr.Row():
        output = gr.Textbox(label="Greeting", lines=20)  # 设置为5行文本框

    gr.Button("Submit").click(fn=chat_invoke, inputs=[speaker, prompt, context_id], outputs=output)


def start_normal_invoke():
    normal_invoke_gradio.launch(server_port=3003)


def start_chat_invoke():
    chat_invoke_gradio.launch(server_port=3004)
