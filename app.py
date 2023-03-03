import gradio as gr
from llama_index import GPTSimpleVectorIndex
import os

css_style = """
.gradio-container {
    font-family: "IBM Plex Mono";
}
"""

# Load the pre-created index
index_filename =  'indices/index_vector_2100.json'
index = GPTSimpleVectorIndex.load_from_disk(index_filename)


def ask_question(question, openai_api_key):
    if len(openai_api_key) > 0:
        os.environ['OPENAI_API_KEY'] = openai_api_key.strip()
        prompt_template = "Provide references to sections in the MPEP"
        response = index.query(question + " " + prompt_template )
        return response.response
    return "Enter your OpenAI API key to use MPEP-QA"

with gr.Blocks(css=css_style) as demo:
    openai_api_key = gr.State('')
    gr.Markdown(f"""
    # 📑 MPEP Question-Answering System
    *By Vasanth Sarathy ([@vasanthsarathy](https://twitter.com/vasanthsarathy))*

    This tool aims to make the [MPEP](https://www.uspto.gov/web/offices/pac/mpep/index.html) (Manual of Patent Examination and Procedure) more accessible to everyone. The MPEP is what guides patent examiners at the US Patent and Trademark Office ([USPTO](https://www.uspto.gov/)) when they examine patent applications. It is also what guides patent lawyers and patent agents when preparing patent applications for their clients.

    MPEP-QA uses OpenAI's GPT models and thus you must enter your API key below. The tool is under active development and costs some money if you run it - About $0.10 - $0.20 per question.

    **DISCLAIMER:** Please note that the answers provided by MPEP-QA are not legally binding and do not constitute legal advice. It provides a starting point for your queries about the patent system. Any followups, deeper dives and advice relating to your specific situation should be done in consultation with someone (human) who is registered to practice in front of the USPTO.

    * [mpep-qa](https://github.com/vasanthsarathy/mpep-qa) contains the code behind the tool.
    * [llamaIndex](https://github.com/jerryjliu/gpt_index/blob/main/docs/index.rst) is the main library this tool uses, and is just awesome!

    How to use:
    1. Enter API Key ([What is that?](https://platform.openai.com/account/api-keys))
    2. Ask your question! (Currently can only answer questions about Patentability (chapter 2100))
    """)

    openai_api_key = gr.Textbox(
        label="OpenAI API Key", placeholder="sk-...", type="password")

    question = gr.Textbox(placeholder="Enter your question here...",
                          label="Question")
    gr.Examples(["Can I patent a new recipe for pancakes?",
                 "What is the difference between novelty and non-obviousness",
                 "Why does a patent need to have claims?"],
                question)
    ask = gr.Button("Ask Question")
    answer = gr.Markdown(label="Answer")

    ask.click(fn=ask_question,
              inputs=[question, openai_api_key],
              outputs=[answer])

demo.queue(concurrency_count=20)
demo.launch(show_error=True)

