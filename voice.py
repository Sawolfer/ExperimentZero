import os 
import torch
from TTS.api import TTS
import gradio as gr


device = "cuda" if torch.cuda.is_available() else "cpu"

# tts = TTS(TTS.list_models()[0])
# wav = tts.tts("This is a test! This is also a test!!", speaker=tts.speakers[0], language=tts.languages[0])
# tts.tts_to_file(text="Hello world!", speaker=tts.speakers[0], language=tts.languages[0], file_path="output.wav")

def generate_audio(text, language="ru"):
    try:
        # tts = TTS(model_name="xtts_v2", model_path=)
        # speakers = torch.load("female.wav")
        tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=True, gpu=False)
        # tts = TTS(model_name=' tts_models/multilingual/multi-dataset/xtts_v2').to(device)
        current_dir = os.path.dirname(__file__)
        output_file = os.path.join(current_dir, "output.ogg")
        speaker_file = os.path.join(current_dir, "female.wav")
        if not os.path.exists(speaker_file):
            print("Speaker file not found!")
            return
        tts.tts_to_file(
            text=text, 
            file_path=output_file,
            language=language, 
            speaker_wav=speaker_file
            )
        return
    except Exception as e:
        print(f"Error: {e}")

demo = gr.Interface(
    fn=generate_audio, 
    inputs=[gr.Text(label="input"),]
    ,outputs=[gr.Audio(label="audio")],
    )

# demo.launch(
#     share=True
# )

# generate_audio("пенис пенис")