# Badriprasad: Autonomous Multimodal Desktop Voice Agent

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![LLM](https://img.shields.io/badge/LLM-Google%20Gemini%20API-orange)](https://ai.google.dev/)
[![Speech](https://img.shields.io/badge/TTS-Microsoft%20Edge%20Neural-green)](https://github.com/rany2/edge-tts)

An asynchronous personal desktop assistant capable of natural conversational reasoning, dynamic intent decoding, and autonomous system tool execution powered by Google Gemini and Microsoft Edge Neural TTS.

---

## Architecture Overview

```text
[ Microphone Input ]
         │
         ▼
[ SoundDevice (16kHz Mono Stream) ]
         │
         ▼
[ SpeechRecognition (Google STT Engine) ]
         │ (Transcribed Text)
         ▼
[ Google Gemini Agent (gemini-3.8-flash) ]
         │
         ├─── Tool Calling Needed? ──► [ Function Runner ]
         │                                   ├── open_website()
         │                                   ├── play_youtube_video()
         │                                   └── get_current_time()
         ▼
[ Natural Response Generation ]
         │
         ▼
[ Microsoft Edge Neural TTS (edge-tts) ]
         │
         ▼
[ Pygame Non-Blocking Audio Stream ]
         │
         ▼
[ Spoken Audio Output ]
''' 
Key FeaturesTool-Augmented Intelligence: Utilizes Gemini's native Function Calling schema to run local system and web utilities dynamically without rigid if-elif regex or keyword ladders.Studio-Quality Neural Speech: Replaces robotic SAPI5 engines with Microsoft Edge Neural TTS (en-IN-PrabhatNeural) streamed asynchronously through Pygame.Lightweight Audio Capture: Directly interfaces with system audio via sounddevice into raw NumPy memory buffers, removing native PortAudio/PyAudio driver compilation issues.Fail-Safe & Secure Runtime: Encapsulates API secrets using python-dotenv and provides structured error handling for STT mismatches, network drops, and rate limits.Tools & IntegrationsTool FunctionDescriptionImplementationopen_website(url)Sanitizes and opens target URLs in default web browserwebbrowserplay_youtube_video(query)Searches and streams music/video content on YouTubepywhatkitget_current_time()Queries local machine clock for formatted time responsesdatetimeGetting Started1. PrerequisitesPython 3.10 or higher.A free Google Gemini API key from Google AI Studio.2. Clone the RepositoryBashgit clone https://github.com/Deepansh-panchal/Badriprasad-voice-agent-.git
cd Badriprasad-voice-agent-
3. Install DependenciesBashpip install google-generativeai edge-tts sounddevice speechrecognition pygame pywhatkit numpy python-dotenv
4. Configure API KeyCreate a .env file in the root directory:Code snippetGEMINI_API_KEY=your_gemini_api_key_here
5. Run the AgentBashpython main.py
LicenseDistributed under the MIT License.
---

### Step 2: VS Code mein Paste Karo
1. `README.md` file mein **`Ctrl + A`** daba kar puraana text select karo.
2. **`Ctrl + V`** daba kar naya text paste kar do.
3. **`Ctrl + S`** daba kar save karo.

---

### Step 3: Terminal Commands
File save hone ke baad terminal mein bas yeh 3 lines chala do:

```bash
git add README.md
git commit -m "docs: finalize full README documentation"
git push origin main