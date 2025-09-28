from src.core.file_generator import rotation_scheduler, generate_honeyfiles
from src.core.monitor import start_monitoring
from src.utils.logger import log_event, init_logging

def main():
    init_logging()
    log_event("🚀 Starting HoneyGuard Trap Tool...", "INFO")
    generate_honeyfiles()  # ensure initial set exists
    rotation_scheduler()   # schedule auto-rotation in background
    start_monitoring()     # blocking loop

if __name__ == "__main__":
    main()
