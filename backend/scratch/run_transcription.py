import sys
import os
from pathlib import Path
import logging

# Add the backend/src directory to sys.path so we can import modules
# Script is in backend/scratch/run_transcription.py
# backend/src/video_utils.py is the target
current_dir = Path(__file__).parent
backend_dir = current_dir.parent
sys.path.append(str(backend_dir))

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import the function
try:
    from src.video_utils import get_video_transcript
    logger.info("Successfully imported get_video_transcript from src.video_utils")
except ImportError as e:
    logger.error(f"Failed to import get_video_transcript: {e}")
    sys.exit(1)

def main():
    # The video path is relative to the backend directory
    video_path = backend_dir / "kaPKwrOKD6E_5m.mp4"
    
    if not video_path.exists():
        logger.error(f"Video file not found at {video_path}")
        return

    logger.info(f"🚀 Starting standalone transcription for: {video_path}")
    
    try:
        # Call the transcription function
        transcript = get_video_transcript(video_path)
        
        print("\n" + "="*50)
        print("TRANSCRIPTION RESULT")
        print("="*50)
        print(transcript)
        print("="*50 + "\n")
        
        # Check if cache was created
        cache_path = video_path.with_suffix(".transcript_cache.json")
        if cache_path.exists():
            logger.info(f"✅ Transcript cache created at: {cache_path}")
        else:
            logger.warning("⚠️ Transcript cache was not created.")
            
    except Exception as e:
        logger.error(f"❌ Error during transcription: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
