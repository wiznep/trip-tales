#### filepath: backend/app/utils/video_processor.py
import cv2
import numpy as np
from pathlib import Path
from typing import List
import logging
from PIL import Image
from app.utils.video_styles import VideoStyles

logger = logging.getLogger(__name__)


class VideoProcessor:
    """Process images and videos into a compiled video story"""
    
    def __init__(
        self,
        output_path: str,
        fps: int = 30,
        resolution: tuple = (1920, 1080),
        codec: str = "mp4v",
        style: str = "cinematic"  # Add style parameter
    ):
        self.output_path = output_path
        self.fps = fps
        self.resolution = resolution
        self.codec = codec
        self.style = style  # Store style
        self.fourcc = cv2.VideoWriter_fourcc(*codec)
        
    def resize_and_pad(self, image: np.ndarray) -> np.ndarray:
        """Resize image to fit resolution while maintaining aspect ratio"""
        target_width, target_height = self.resolution
        height, width = image.shape[:2]
        
        # Calculate aspect ratios
        target_aspect = target_width / target_height
        image_aspect = width / height
        
        if image_aspect > target_aspect:
            # Image is wider than target
            new_width = target_width
            new_height = int(target_width / image_aspect)
        else:
            # Image is taller than target
            new_height = target_height
            new_width = int(target_height * image_aspect)
        
        # Resize image
        resized = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)
        
        # Create black canvas and center the image
        canvas = np.zeros((target_height, target_width, 3), dtype=np.uint8)
        y_offset = (target_height - new_height) // 2
        x_offset = (target_width - new_width) // 2
        canvas[y_offset:y_offset + new_height, x_offset:x_offset + new_width] = resized
        
        return canvas
    
    def apply_fade_in(self, frame: np.ndarray, alpha: float) -> np.ndarray:
        """Apply fade-in effect to frame"""
        return cv2.addWeighted(frame, alpha, np.zeros_like(frame), 1 - alpha, 0)
    
    def apply_fade_out(self, frame: np.ndarray, alpha: float) -> np.ndarray:
        """Apply fade-out effect to frame"""
        return cv2.addWeighted(frame, 1 - alpha, np.zeros_like(frame), alpha, 0)
    
    def add_text_overlay(
        self, 
        frame: np.ndarray, 
        text: str, 
        position: str = "bottom"
    ) -> np.ndarray:
        """Add text overlay to frame"""
        height, width = frame.shape[:2]
        
        # Configure text
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.5
        thickness = 3
        color = (255, 255, 255)  # White
        
        # Get text size
        (text_width, text_height), baseline = cv2.getTextSize(
            text, font, font_scale, thickness
        )
        
        # Calculate position
        if position == "bottom":
            x = (width - text_width) // 2
            y = height - 100
        elif position == "top":
            x = (width - text_width) // 2
            y = 100
        else:  # center
            x = (width - text_width) // 2
            y = (height + text_height) // 2
        
        # Add semi-transparent background
        overlay = frame.copy()
        cv2.rectangle(
            overlay,
            (x - 20, y - text_height - 20),
            (x + text_width + 20, y + baseline + 20),
            (0, 0, 0),
            -1
        )
        frame = cv2.addWeighted(frame, 0.7, overlay, 0.3, 0)
        
        # Add text
        cv2.putText(
            frame,
            text,
            (x, y),
            font,
            font_scale,
            color,
            thickness,
            cv2.LINE_AA
        )
        
        return frame
    
    def process_image(
        self,
        image_path: str,
        duration: int = 1,
        transition_frames: int = 15,
        add_text: str = None
    ) -> List[np.ndarray]:
        """Process a single image into video frames"""
        try:
            # Read image using PIL first (better format support)
            pil_image = Image.open(image_path)
            
            # Convert to RGB if necessary
            if pil_image.mode != 'RGB':
                pil_image = pil_image.convert('RGB')
            
            # Convert PIL to OpenCV format
            image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            
            # Resize and pad to target resolution
            processed = self.resize_and_pad(image)
            
            # Apply artistic style
            processed = VideoStyles.apply_style(processed, self.style)
            
            # Add text overlay if provided
            if add_text:
                processed = self.add_text_overlay(processed, add_text)
            
            # Calculate total frames
            total_frames = duration * self.fps
            frames = []
            
            # Generate frames with transitions
            for i in range(total_frames):
                frame = processed.copy()
                
                # Fade in at start
                if i < transition_frames:
                    alpha = i / transition_frames
                    frame = self.apply_fade_in(frame, alpha)
                
                # Fade out at end
                elif i > total_frames - transition_frames:
                    alpha = (total_frames - i) / transition_frames
                    frame = self.apply_fade_out(frame, 1 - alpha)
                
                frames.append(frame)
            
            logger.info(f"Processed image: {image_path} -> {len(frames)} frames")
            return frames
            
        except Exception as e:
            logger.error(f"Error processing image {image_path}: {str(e)}")
            return []
    
    def process_video_clip(
        self,
        video_path: str,
        max_duration: int = 5
    ) -> List[np.ndarray]:
        """Process a video clip (limit duration and resize)"""
        try:
            cap = cv2.VideoCapture(video_path)
            frames = []
            max_frames = max_duration * self.fps
            frame_count = 0
            
            while cap.isOpened() and frame_count < max_frames:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Resize to target resolution
                processed = self.resize_and_pad(frame)
                frames.append(processed)
                frame_count += 1
            
            cap.release()
            logger.info(f"Processed video: {video_path} -> {len(frames)} frames")
            return frames
            
        except Exception as e:
            logger.error(f"Error processing video {video_path}: {str(e)}")
            return []
    
    def create_video_from_media(
        self,
        media_files: List[dict],
        title: str = None,
        add_intro: bool = True,
        add_outro: bool = True
    ) -> bool:
        """
        Create video from list of media files
        
        Args:
            media_files: List of dicts with 'path', 'type', 'filename'
            title: Optional title for intro
            add_intro: Add title intro screen
            add_outro: Add outro screen
        
        Returns:
            bool: Success status
        """
        try:
            # Initialize video writer
            writer = cv2.VideoWriter(
                self.output_path,
                self.fourcc,
                self.fps,
                self.resolution
            )
            
            if not writer.isOpened():
                logger.error("Failed to open video writer")
                return False
            
            all_frames = []
            
            # Add intro if requested
            if add_intro and title:
                intro_frames = self.create_title_screen(title, duration=3)
                all_frames.extend(intro_frames)
            
            # Process each media file
            for idx, media in enumerate(media_files):
                logger.info(f"Processing media {idx + 1}/{len(media_files)}: {media['filename']}")
                
                if media['type'] == 'image':
                    frames = self.process_image(
                        media['path'],
                        duration=1,  # 1 second per photo
                        transition_frames=15,
                        add_text=f"{idx + 1}/{len(media_files)}"
                    )
                elif media['type'] == 'video':
                    frames = self.process_video_clip(
                        media['path'],
                        max_duration=5
                    )
                else:
                    logger.warning(f"Unknown media type: {media['type']}")
                    continue
                
                all_frames.extend(frames)
            
            # Add outro if requested
            if add_outro:
                outro_frames = self.create_title_screen(
                    "Thank you for watching!",
                    duration=2
                )
                all_frames.extend(outro_frames)
            
            # Write all frames to video
            logger.info(f"Writing {len(all_frames)} frames to video...")
            for frame in all_frames:
                writer.write(frame)
            
            writer.release()
            logger.info(f"Video created successfully: {self.output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating video: {str(e)}")
            return False
    
    def create_title_screen(self, text: str, duration: int = 3) -> List[np.ndarray]:
        """Create a title screen with text"""
        frames = []
        total_frames = duration * self.fps
        
        for i in range(total_frames):
            # Create black background
            frame = np.zeros((self.resolution[1], self.resolution[0], 3), dtype=np.uint8)
            
            # Add gradient background
            gradient = np.linspace(0, 100, self.resolution[1], dtype=np.uint8)
            frame[:, :, 0] = gradient[:, None]  # Blue channel
            frame[:, :, 1] = gradient[:, None] * 0.5  # Green channel
            
            # Add text
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 2.5
            thickness = 4
            color = (255, 255, 255)
            
            # Get text size
            (text_width, text_height), _ = cv2.getTextSize(
                text, font, font_scale, thickness
            )
            
            # Center text
            x = (self.resolution[0] - text_width) // 2
            y = (self.resolution[1] + text_height) // 2
            
            cv2.putText(
                frame,
                text,
                (x, y),
                font,
                font_scale,
                color,
                thickness,
                cv2.LINE_AA
            )
            
            # Apply fade in/out
            if i < 15:  # Fade in
                alpha = i / 15
                frame = self.apply_fade_in(frame, alpha)
            elif i > total_frames - 15:  # Fade out
                alpha = (total_frames - i) / 15
                frame = self.apply_fade_out(frame, 1 - alpha)
            
            frames.append(frame)
        
        return frames


def create_video_from_images(
    image_paths: List[str],
    output_path: str,
    title: str = None,
    fps: int = 30,
    resolution: tuple = (1920, 1080)
) -> bool:
    """
    Convenience function to create video from images
    
    Args:
        image_paths: List of image file paths
        output_path: Output video file path
        title: Optional title for intro
        fps: Frames per second
        resolution: Video resolution (width, height)
    
    Returns:
        bool: Success status
    """
    processor = VideoProcessor(output_path, fps, resolution)
    
    media_files = [
        {
            'path': path,
            'type': 'image',
            'filename': Path(path).name
        }
        for path in image_paths
    ]
    
    return processor.create_video_from_media(
        media_files,
        title=title,
        add_intro=True,
        add_outro=True
    )