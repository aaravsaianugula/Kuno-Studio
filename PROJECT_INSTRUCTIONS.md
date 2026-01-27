# Kuno Project Instructions

## Overview
Kuno is an AI-powered Audio OS designed for generative music creation. It features a modern, glassmorphic UI built with Next.js and a backend driven by Python (FastAPI) and PyTorch models (HeartMuLa, HeartCodec).

## Architecture

### Frontend (`/frontend`)
- **Framework**: Next.js 14 (App Router)
- **Styling**: Tailwind CSS 4 + Custom Glassmorphism
- **Key Components**:
    - `GlassPanel`: Core UI container with blur effects.
    - `SongSequencer`: Timeline visualization and control.
    - `MonitorWidget`: Visualizer for system status.
    - `CommandInterface`: JSON-based generative control (Cmd+K style).
    - `MixerView`, `LibraryView`, `RecordingView`: Functional tabs.

### Backend (`/backend`)
- **Server**: FastAPI (`app.main`)
- **Engine**:
    - `StudioEnhancer`: Semantic understanding of audio.
    - `HeartMuLaService`: Generative audio model service (HeartMuLa-RL-oss-3B).
- **Data storage**: `generated_songs/` (WAV output), `current_project.json` (State).

## Usage Guide

1.  **AI Generation**:
    - Click the **Command** icon (⌘) or the **Add** button in the timeline.
    - Paste a valid JSON Song Structure (e.g., `{"title": "My Song", "structure": [...]}`).
    - **Note**: Ensure `genre` uses comma-separated tags with NO spaces (e.g., `kpop,upbeat`).
    - **Tip**: Use `CLAUDE_PROMPT.md` to generate valid JSONs with Claude.
    - Click **Generate**. The backend will process this and update the timeline.

2.  **Audio Recording**:
    - Go to the **Mic** tab.
    - Click the red microphone to record vocal/beatbox ideas.
    - Recording automatically uploads to the backend for potential "audio-to-audio" conditioning (future feature).

3.  **Library**:
    - The **Music** tab lists all generated songs (WAV files).
    - Click **Play** to listen to your creations.

4.  **Mixing**:
    - The **Layers** tab offers a functional mixer.
    - Adjust levels for different stems (simulated for now, can be wired to real stem separation).

## Development
- **Run Frontend**: `npm run dev` (Port 3000)
- **Run Backend**: `python -m app.main` (Port 8000)
- **Configuration**: Edit `backend/app/config.py` for model paths and hardware settings.
