import os
import time
import textwrap
import logging
from typing import List, Tuple
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips
from pydub import AudioSegment
from .router import Router
import pathlib
from .utils import write_text_on_image
import shutil

logging.basicConfig(level=logging.INFO)

class Worker:
    def __init__(self, topic: str, num_lines: int, style: str, workspace: str = "My Workspace", delay: int = 10) -> None:
        self.topic = topic
        self.num_lines = num_lines
        self.style = style
        self.workspace = workspace
        self.delay = delay
        self.router = Router()
        self.output_dir = f"{self.workspace}_o"
        self.imgs_dir = os.path.join(self.workspace, "imgs")
        self.audio_dir = os.path.join(self.workspace, "audio")
        
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.workspace, exist_ok=True)
        os.makedirs(self.imgs_dir, exist_ok=True)
        os.makedirs(self.audio_dir, exist_ok=True)

    def generate_yt_script(self) -> Tuple[List[str], List[str]]:
        dialogue_template = textwrap.dedent(f"""\
            You are an enchanting poet with rhyming skills, whilst being a polymath.
            You only write the script and image descriptions of that frame and nothing else.
            Topic: {self.topic}
            You strictly follow this format:
            ||A Script Line of 12 words||An Image description||repeat again 
            Continue this format for {self.num_lines} lines, separated by the delimiter. 
            Dont add hashtags or any other text.
        """)
        response = self.router.generate_dialogue(prompt=dialogue_template).replace("*","")
        script_lines, image_descriptions = self._parse_dialogue(response)
        return script_lines, image_descriptions

    def _parse_dialogue(self, dialogue: str) -> Tuple[List[str], List[str]]:
        lines = dialogue.split("||")
        lines = [line.strip() for line in lines if line.strip()]
        return lines[::2], lines[1::2] 

    def add_subtitles_and_audio(self, script_line: str, img_path: str) -> Tuple[List[str], List[str]]:
        words = script_line.split()
        image_files = []
        audio_files = []
        base_name = os.path.splitext(os.path.basename(img_path))[0]
        subtitle_index = 0
        while words:
            chunk = " ".join(words[:12]) # had too much trouble so keeping 12 words as a safe option
            words = words[12:]
            subtitle_img_file = os.path.join(self.output_dir, f"{base_name}_subtitle_{subtitle_index}.jpeg")
            write_text_on_image(img_path, chunk, subtitle_img_file)
            image_files.append(subtitle_img_file)
            audio_file = os.path.join(self.audio_dir, f"{base_name}_subtitle_{subtitle_index}.mp3")
            self.router.generate_audio(chunk, audio_file)
            audio_files.append(audio_file)
            subtitle_index += 1

        return image_files, audio_files

    def process(self) -> None:
        script_lines, image_descriptions = self.generate_yt_script()
        for index, img_desc in enumerate(image_descriptions):
            file_name = os.path.join(self.imgs_dir, f"img_{index}.lol")
            full_img_desc = f"{img_desc} img style: {self.style}"
            self.router.generate_image(full_img_desc, file_name)
            logging.info(f"Generated image {index}: {file_name}")
            self.add_subtitles_and_audio(script_lines[index], file_name)
            time.sleep(self.delay)

    def flush(self) -> None:
        shutil.rmtree(self.workspace)
        shutil.rmtree(self.output_dir)
        print(f"Deleted Workspace {self.workspace}!!")

    def create_vid(self, output_path="output.mp4", fps=24):
        audio_dir = pathlib.Path(self.audio_dir)
        image_dir = pathlib.Path(self.output_dir)
        pairs = []
        for audio_file in audio_dir.glob("*"):
            if audio_file.suffix.lower() not in [".wav", ".mp3"]:
                continue
            stem = audio_file.stem
            image_files = list(image_dir.glob(f"{stem}.*"))
            if not image_files:
                print(f"No matching image found for {audio_file.name}")
                continue
            pairs.append((image_files[0], audio_file))
        if not pairs:
            raise ValueError("No valid audio-image pairs found")
        pairs.sort(key=lambda x: x[1].name)
        clips = []
        for img_path, audio_path in pairs:
            audio = AudioSegment.from_file(audio_path)
            duration = audio.duration_seconds
            img_clip = ImageClip(str(img_path)).with_duration(duration)
            audio_clip = AudioFileClip(str(audio_path))
            img_clip = img_clip.with_audio(audio_clip)
            clips.append(img_clip)
        final_video = concatenate_videoclips(clips, method="compose")
        # TODO: understand this part below
        # ffmpeg and ffmprobe were required
        final_video.write_videofile(
            output_path,
            fps=fps,
            codec="libx264",
            audio_codec="aac",
            threads=4)
        final_video.close()
        for clip in clips:
            clip.close()
