import os
import subprocess
from pathlib import Path
import sys

# Add src to path to get template names
sys.path.append(str(Path(__file__).parent / "src"))
from caption_templates import get_template_names


def main():
    video_file = "kaPKwrOKD6E_30s.mp4"
    if not os.path.exists(video_file):
        print(f"Error: {video_file} not found in the current directory.")
        return

    templates = get_template_names()
    print(f"Found {len(templates)} templates: {', '.join(templates)}")

    output_dir = Path("style_samples")
    output_dir.mkdir(exist_ok=True)

    for template in templates:
        output_file = output_dir / f"sample_{template}.mp4"
        print(f"\n--- Generating clip with style: {template} ---")

        cmd = [
            "uv",
            "run",
            "python",
            "iterate_captions.py",
            video_file,
            "--start",
            "00:05",
            "--end",
            "00:15",
            "--template",
            template,
            "--output",
            str(output_file),
        ]

        try:
            subprocess.run(cmd, check=True)
            print(f"Successfully generated: {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to generate {template}: {e}")


if __name__ == "__main__":
    main()
