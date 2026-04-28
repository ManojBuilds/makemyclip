import argparse
import sys
import os
from pathlib import Path
import logging

# Add the current directory to sys.path to allow importing 'src' as a package
sys.path.append(os.getcwd())

try:
    from src.video_utils import create_optimized_clip, parse_timestamp_to_seconds
    from src.caption_templates import get_template_names
except ImportError as e:
    print(f"Error importing modules: {e}")
    print(f"Make sure you are running this script from the 'backend' directory.")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Iterate on video captions without re-transcribing."
    )
    parser.add_argument("video_path", type=str, help="Path to the source video file")
    parser.add_argument(
        "--start", type=str, default="00:00", help="Start time (MM:SS or seconds)"
    )
    parser.add_argument(
        "--end", type=str, default="00:10", help="End time (MM:SS or seconds)"
    )
    parser.add_argument(
        "--template",
        type=str,
        default="default",
        choices=get_template_names(),
        help="Caption template to use",
    )
    parser.add_argument(
        "--font-size", type=int, default=None, help="Override font size"
    )
    parser.add_argument(
        "--font-family", type=str, default=None, help="Override font family"
    )
    parser.add_argument(
        "--font-color",
        type=str,
        default=None,
        help="Override font color (e.g. #FFFFFF)",
    )
    parser.add_argument(
        "--output", type=str, default="test_clip.mp4", help="Output filename"
    )
    parser.add_argument(
        "--original-size",
        action="store_true",
        help="Keep original video size (no vertical crop)",
    )
    parser.add_argument(
        "--no-dynamic", action="store_true", help="Disable dynamic face tracking"
    )
    parser.add_argument(
        "--hook", type=str, default=None, help="Hook title text (for roylee style)"
    )

    args = parser.parse_args()

    video_path = Path(args.video_path)
    if not video_path.exists():
        logger.error(f"Video file not found: {video_path}")
        return

    # Check for transcript cache
    cache_path = video_path.with_suffix(".transcript_cache.json")
    if not cache_path.exists():
        logger.error(
            f"Transcript cache not found at {cache_path}. You must run the full pipeline at least once to generate this cache."
        )
        return

    logger.info(f"Using video: {video_path}")
    logger.info(f"Using cache: {cache_path}")

    start_seconds = parse_timestamp_to_seconds(args.start)
    end_seconds = parse_timestamp_to_seconds(args.end)

    output_path = Path(args.output)
    output_format = "original" if args.original_size else "vertical"
    dynamic_tracking = not args.no_dynamic

    logger.info(
        f"Rendering clip: {args.start} -> {args.end} ({output_format}, dynamic_tracking={dynamic_tracking})"
    )

    success = create_optimized_clip(
        video_path=video_path,
        start_time=start_seconds,
        end_time=end_seconds,
        output_path=output_path,
        add_subtitles=True,
        caption_template=args.template,
        font_size=args.font_size,
        font_family=args.font_family,
        font_color=args.font_color,
        output_format=output_format,
    )

    if success:
        logger.info(f"Successfully created test clip: {output_path}")
        logger.info(f"Preview the result in {output_path.absolute()}")
    else:
        import traceback

        traceback.print_exc()
        logger.error("Failed to create test clip.")


if __name__ == "__main__":
    main()
