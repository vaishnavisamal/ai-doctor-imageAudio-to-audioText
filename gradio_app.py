import os
import gradio as gr
from dotenv import load_dotenv

from brain_of_dr import encode_image, analyze_image_with_query
from voice_of_patient import transcribe_with_groq
from voice_of_dr import text_to_speech_with_edge_tts

# Load environment variables
load_dotenv()

# Check API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found. Please add it to your .env file."
    )

system_prompt = """
You have to act as a professional doctor. I know you are not, but this is for learning purposes.
What's in this image? Do you find anything wrong with it medically?
If you make a differential diagnosis, suggest some remedies.
Do not add numbers or special characters in your response.
Respond in one concise paragraph (maximum two sentences).
Always respond as if speaking to a real patient.
Do not say "In the image I see"; instead say "With what I see, I think you have..."
Do not use markdown or mention that you are an AI.
"""

def process_inputs(audio_filepath, image_filepath):
    try:
        if audio_filepath is None:
            return (
                "No audio detected.",
                "Please record your question first.",
                None,
            )

        print("=" * 50)
        print("Audio File:", audio_filepath)
        print("Image File:", image_filepath)

        # Speech to Text
        speech_to_text_output = transcribe_with_groq(
            GROQ_API_KEY=GROQ_API_KEY,
            audio_filepath=audio_filepath,
            stt_model="whisper-large-v3"
        )

        print("Speech:", speech_to_text_output)

        # Vision Analysis
        if image_filepath:
            doctor_response = analyze_image_with_query(
                query=system_prompt + "\n\nPatient: " + speech_to_text_output,
                encoded_image=encode_image(image_filepath),
                model="qwen/qwen3.6-27b"
            )
        else:
            doctor_response = (
                "Please upload a medical image so I can analyze it."
            )

        print("Doctor Response:", doctor_response)

        # Text to Speech
        output_audio = "final.mp3"

        text_to_speech_with_edge_tts(
            input_text=doctor_response,
            output_filepath=output_audio
        )

        return (
            speech_to_text_output,
            doctor_response,
            output_audio,
        )

    except Exception as e:
        print("\nERROR:\n", e)
        return (
            "",
            f"Error: {str(e)}",
            None,
        )


iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(
            sources=["microphone"],
            type="filepath",
            label="Record your voice"
        ),
        gr.Image(
            type="filepath",
            label="Upload Medical Image"
        ),
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="Doctor's Diagnosis"),
        gr.Audio(label="Doctor's Voice"),
    ],
    title="🩺 AI Doctor with Vision + Voice",
    description="Upload a medical image and ask your question using your voice."
)

iface.launch(debug=True)