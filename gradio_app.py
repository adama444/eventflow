import gradio as gr
import requests

API_URL = "http://127.0.0.1:8000/api/v1/chat/"  # adjust to your endpoint


def chat_fn(message, history):
    """
    Send user message to FastAPI backend and return assistant reply.
    history: [(user, bot), ...]
    """
    try:
        # For testing, we use a fixed user_id
        response = requests.post(
            API_URL, data={"user_id": 3, "message": message}, files={}
        )
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        return f"⚠️ Error: {str(e)}"


# Build Gradio chat UI
demo = gr.ChatInterface(
    fn=chat_fn,
    multimodal=True,
    type="messages",
    chatbot=gr.Chatbot(height=400),
    textbox=gr.Textbox(placeholder="Type your message..."),
    title="EventFlow Test Chatbot",
    description="Quick test interface for EventFlow API",
    theme="ocean",
)

demo.launch(server_name="127.0.0.1", server_port=7860)
