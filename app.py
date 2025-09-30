import os
import gradio as gr
from dotenv import load_dotenv
from elevenlabs import ElevenLabs
from blog_summarizer import summarize_blog

load_dotenv()

# Function stays the same
def process_url(url):
    summary = summarize_blog(url)
    print("Blog Summary:", summary)
    client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
    response = client.text_to_speech.convert(
        text=summary,
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        model_id="eleven_v3",
        output_format="mp3_44100_128"
    )

    audio_file = "audio_output.mp3"
    with open(audio_file, "wb") as f:
        for chunk in response:
            f.write(chunk)

    print("Vocals generated successfully")
    return "Vocals generated successfully", summary, audio_file


# Modern UI with Gradio
with gr.Blocks(
    title="🎙️Orris",
    theme=gr.themes.Default(primary_hue="red", secondary_hue="gray")
) as demo:

    # Header
    gr.Markdown(
        """
        <h1 style='text-align:center; color:#ff0000; font-family:Arial Black; font-size:72px; margin-top:50px;'>
            🎙️ Orris
        </h1>
        <p style='text-align:center; color:#4b5563; font-family:Arial; font-size:18px; margin-bottom:40px;'>
            Enter a blog URL and generate a podcast episode in seconds!
        </p>
        """,
        elem_id="header"
    )

    with gr.Column(scale=1, min_width=600, elem_id="main-column"):
        # Input
        url_input = gr.Textbox(
            placeholder="https://example.com/blog-post",
            label="Blog URL",
            interactive=True,
            elem_id="url-input"
        )

        # Generate Button
        generate_btn = gr.Button(
            "🎧 Generate Podcast",
            elem_id="generate-btn",
            variant="primary"
        )

        # Status
        status_output = gr.Textbox(
            label="Status",
            interactive=False,
            lines=1,
            elem_id="status-output"
        )

        # Summary
        summary_output = gr.Textbox(
            label="Blog Summary",
            placeholder="Summary will appear here...",
            lines=15,
            interactive=False,
            elem_id="summary-output"
        )

        # Audio output
        audio_output = gr.Audio(
            label="Generated Podcast",
            elem_id="audio-output"
        )

    # Connect button
    generate_btn.click(
        fn=process_url,
        inputs=url_input,
        outputs=[status_output, summary_output, audio_output]
    )

# Launch app
if __name__ == "__main__":
    demo.launch(server_port=2222)