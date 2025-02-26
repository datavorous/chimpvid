# ChimpVid

Simple and minimal short video generator with voice-over. Uses gemini, flux and elevenlabs. 
Download `ffmpeg` beforehand.

## Demo

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/datavorous/chimpvid.git
   cd chimpvid
   ```

2. **Set Up Environment Variables:**

   Create a `.env` file in the root directory with the following keys:

   ```
   ELEVENLABS_API_KEY=your_elevenlabs_api_key
   GEMINI_API_KEY=your_gemini_api_key
   CLOUDFLARE_ACCOUNT_ID=your_cloudflare_account_id
   CLOUDFLARE_API_KEY=your_cloudflare_api_key
   ```
   Refer to [Cloudflare AI worker docs](https://developers.cloudflare.com/workers-ai/models/).

3. **Use uv:**

   ```bash
   pip install uv
   uv install
   uv run main.py
   ```

## Example

Open `main.py`.

```python
from chimp.worker import Worker

worker = Worker(
    workspace="Pointers",
    topic="Write a ...",
    num_lines=10,  
    style="Vintage Anime ..."  
)

worker.process()
worker.create_vid(output_path="pointers.mp4", fps=10)
worker.flush()
```

## Dependencies

**ElevenLabs:** For text-to-speech conversion.
**Gemini AI:** For generating viral script content.
**Cloudflare API:** For generating stylized images.
**Pillow:** For image processing.
**MoviePy & Pydub:** For video and audio processing.
**python-dotenv:** For managing environment variables.



