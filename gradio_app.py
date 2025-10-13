import gradio as gr
import requests

from app.core.config import settings


def chat_fn(message, history, session_id):
    """
    Send user message + files to FastAPI backend and return assistant reply.
    history: [(user, bot), ...]
    session_id: the conversation thread identifier
    """
    if not session_id:
        return "⚠️ Please enter a Session ID first."

    try:
        # Build files payload dynamically
        files = []
        if "files" in message and message["files"]:
            files = [("files", (f.split("/")[-1], open(f, "rb"))) for f in message["files"]]

        # Send request to API
        response = requests.post(
            settings.api_url, data={"user_id": session_id, "message": message["text"]}, files=files
        )
        response.raise_for_status()

        # Close files
        for _, (_, file_obj) in files:
            file_obj.close()

        return response.json()["response"]
    except Exception as e:
        return f"⚠️ Error: {str(e)}"


# Build Gradio chat UI
with gr.Blocks() as demo:
    gr.Markdown("## 🗂 EventFlow Test Chatbot")
    gr.Markdown("Enter a **Session ID** (number) to start/resume your conversation.")

    session_id_box = gr.Textbox(label="Session ID", placeholder="e.g. 123 or 7", lines=1)

    chat_ui = gr.ChatInterface(
        fn=chat_fn,
        additional_inputs=[session_id_box],
        multimodal=True,
        type="messages",
        chatbot=gr.Chatbot(height=400),
        textbox=gr.MultimodalTextbox(
            interactive=True,
            file_count="multiple",
            placeholder="Enter message or upload file...",
            show_label=False,
            file_types=["image"],
            sources=["upload"],
        ),
        title="EventFlow Test Chatbot",
        description="Quick test interface for EventFlow API",
        theme="ocean",
    )

demo.launch(server_name="127.0.0.1", server_port=settings.gradio_app_port)
