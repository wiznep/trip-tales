#### filepath: backend/test_video_generation.py
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from app.utils.video_processor import create_video_from_images

# Test image paths (replace with your actual test images)
image_paths = [
    "uploads/1.jpg",
    "uploads/2.jpg",
    "uploads/3.jpg",
]

output_path = "uploads/test_output.mp4"

print("Starting video generation...")
success = create_video_from_images(
    image_paths=image_paths,
    output_path=output_path,
    title="My Test Travel Story",
    fps=30,
    resolution=(1920, 1080)
)

if success:
    print(f"✅ Video created successfully: {output_path}")
else:
    print("❌ Video generation failed")