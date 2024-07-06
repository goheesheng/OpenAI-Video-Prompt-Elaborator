import whisper
import openai
import os
from pytube import YouTube
from pathlib import Path

openai.api_key = os.getenv('OPENAI_API_KEY') # Replace your OpenAI key here
OPENAI_MODEL = 'text-davinci-003'
WHISPER_MODEL = 'large-v3'
YOUTUBE_VIDEO_URL = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
OUTPUT_AUDIO = Path(__file__).resolve().parent.parent.joinpath('data', 'summary.mp4')

def download_youtube_video(url, output_audio):
    # youtube video object
    youtube_video = YouTube(url)
    streams = youtube_video.streams.filter(only_audio=True)
    # taking first object of lowest quality
    stream = streams.first()
    stream.download(filename=output_audio)

def summarize_text(transcript):
    #
    system_prompt = "I would like for you to assume the role of a tech savvy individual who understand how to rick roll"
    user_prompt = f"""Generate a concise summary of the text below.
    Text: {transcript}
    """
    #
    print('summarizing ... ')
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo-16k',
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt}
        ],
        max_tokens=4096,
        temperature=1
    )
    #
    summary = response['choices'][0]['message']['content']
    return summary

    
def boot():
    #
    download_youtube_video(YOUTUBE_VIDEO_URL, OUTPUT_AUDIO)
    #
    model = whisper.load_model(WHISPER_MODEL)
    transcript = model.transcribe(OUTPUT_AUDIO.as_posix())
    transcript = transcript['text']
    print(f'Transcript generated: \n{transcript}')
    #
    summary = summarize_text(transcript)
    print(f'Summary for the Youtube Video:\n{summary}')


if __name__ == '__main__':
    #
    boot()
    
