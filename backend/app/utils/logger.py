import sys
from loguru import logger
from pathlib import Path

# Configure Logger
log_path = Path("logs")
log_path.mkdir(exist_ok=True)

logger.remove()  # Remove default handler

# Console Handler (Colorized, Info Level)
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO",
    colorize=True
)

# File Handler (Rotation, Debug Level)
logger.add(
    log_path / "kuno_app.log",
    rotation="10 MB",
    retention="1 week",
    compression="zip",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
)

# Export logger
log = logger

def get_logger(name: str):
    return log.bind(name=name)
