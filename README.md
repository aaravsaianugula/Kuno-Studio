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

## Installation

### Easiest Method (Recommended)
1.  **Download the Installer Code:**
    Create a new file on your computer named `install.bat`, paste the code below into it, and save.
    
    ```batch
    @echo off
    echo Installing Kuno Studio...
    where git >nul 2>nul || (echo Git not found. Install Git first! & pause & exit /b)
    if exist "Kuno-Studio" (cd Kuno-Studio && git pull) else (git clone https://github.com/aaravsaianugula/Kuno-Studio.git && cd Kuno-Studio)
    call setup_kuno.bat
    ```
2.  **Run it:** Double-click your `install.bat`. It will do everything for you.

### Manual Method
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/aaravsaianugula/Kuno-Studio.git
    cd Kuno-Studio
    ```

2.  **One-Click Setup / Update:**
    Double-click `setup_kuno.bat`. **Run this script anytime to update the app.**
    
    This script will:
    - **Pull the latest updates from GitHub**
    - Create/Update the Python virtual environment
    - Install all backend and frontend dependencies
    - **Create a Desktop Shortcut for you**

## Usage

### Easy Start
- **Native App:** Run `start_native.bat` (Recommended). This opens a dedicated window and manages everything.
- **Legacy:** Double-click the **Kuno Studio** shortcut on your Desktop (created by the setup script), or run `start_kuno.bat` in the folder.

### Manual Start
**Backend:**
```bash
cd backend
python -m app.main
```

**Frontend:**
```bash
cd frontend
npm run dev # for browser version
# OR
npm run electron-dev # for native app version
```

Visit `http://localhost:3000` to use the studio.

## Project Structure

- `/backend`: FastAPI application, AI engine, and audio processing logic.
- `/frontend`: Next.js React application for the user interface.
- `/models`: Directory for AI model checkpoints (not included in repo, auto-downloaded on first run).
