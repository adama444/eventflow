import gradio as gr
import requests

API_URL = "http://127.0.0.1:8000/api/v1/chat/"  # adjust to your endpoint


def chat_fn(message, history):
    """
    Send user message to FastAPI backend and return assistant reply.
    history: [(user, bot), ...]
    """
    try:
        # Build files payload dynamically
        files = [("files", (f.split("/")[-1], open(f, "rb"))) for f in message["files"]]

        # For testing, we use a fixed user_id
        response = requests.post(
            API_URL, data={"user_id": 3, "message": message["text"]}, files=files
        )
        response.raise_for_status()

        # Close files
        for _, (filename, file_obj) in files:
            file_obj.close()

        return response.json()["response"]
    except Exception as e:
        return f"⚠️ Error: {str(e)}"


# Build Gradio chat UI
demo = gr.ChatInterface(
    fn=chat_fn,
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

demo.launch(server_name="127.0.0.1", server_port=7860)
