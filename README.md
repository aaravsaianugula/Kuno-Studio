# Kuno Studio - AI Music Production Suite

Kuno Studio is a powerful, locally-hosted AI music generation application combining a FastAPI backend with a modern React/Next.js frontend. It leverages the HeartMuLa model for generation and HeartCodec for decoding, optimized for consumer hardware including AMD GPUs via DirectML.

## Features

- **Text-to-Music Generation**: Create tracks from text prompts.
- **Dynamic Lyrics**: Generate songs with specific lyrics and styles.
- **Hardware Acceleration**: 
  - Optimized for AMD GPUs (DirectML)
  - Fallbacks for CPU execution
  - Layer streaming for low-VRAM environments
- **Modern UI**: Sleek, responsive interface for managing projects and generations.

## Prerequisites

- **Python 3.10+**
- **Node.js 18+**
- **FFmpeg** (must be in system PATH)
- **Git**

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/aaravsaianugula/Kuno-Studio.git
    cd Kuno-Studio
    ```

2.  **Backend Setup:**
    ```bash
    cd backend
    python -m venv env
    .\env\Scripts\activate
    pip install -r requirements.txt
    ```
    *(Note: You may need specific versions of torch-directml depending on your hardware)*

3.  **Frontend Setup:**
    ```bash
    cd frontend
    npm install
    ```

## Usage

### Easy Start (Windows)
Double-click the `start_kuno.bat` file in the root directory. This will launch both servers and open your web browser.

### Manual Start
**Backend:**
```bash
cd backend
python -m app.main
```

**Frontend:**
```bash
cd frontend
npm run dev
```

Visit `http://localhost:3000` to use the studio.

## Project Structure

- `/backend`: FastAPI application, AI engine, and audio processing logic.
- `/frontend`: Next.js React application for the user interface.
- `/models`: Directory for AI model checkpoints (not included in repo, auto-downloaded on first run).
