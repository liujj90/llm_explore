from pathlib import Path
import gradio as gr
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from scripts.pdfquery import QApipeline

app = FastAPI()

# create a static directory to store the static files
static_dir = Path('./static')
static_dir.mkdir(parents=True, exist_ok=True)

# mount FastAPI StaticFiles server
app.mount("/static", StaticFiles(directory=static_dir), name="static")


def upload_file(files):
    file_paths = [file.name for file in files]
    result = pdfbot(file_paths)
    return result


def pdfbot(input):
    for i in input:
        global qa_model
        qa_model = QApipeline(i)
        result = qa_model.run("give me a concise summary of this document.")
        return result
    
def pdfchat(input_text, history):
    result = qa_model.run(input_text)
    history.append((input_text, result))
    return "", history

with gr.Blocks() as demo:
    with gr.Column():
        text_output = gr.Textbox(label="Summary")
        upload_button = gr.UploadButton("Click to Upload a File", file_types=[".pdf"], file_count="multiple")
        upload_button.upload(upload_file, upload_button, text_output)
        
        chatbot = gr.Chatbot()
        msg = gr.Textbox()
        clear = gr.Button("Clear")
        
        msg.submit(pdfchat, [msg, chatbot], [msg, chatbot])
        clear.click(lambda: None, None, chatbot, queue=False)
        
# mount Gradio app to FastAPI app
app = gr.mount_gradio_app(app, demo, path="/")

if __name__ == "__main__":
    import uvicorn
    # demo.launch() 
    uvicorn.run(app, host="0.0.0.0", port=7860)      