#### filepath: backend/app/utils/video_styles.py
import cv2
import numpy as np


class VideoStyles:
    """Apply different artistic styles to video frames"""
    
    @staticmethod
    def cinematic(frame: np.ndarray) -> np.ndarray:
        """Apply cinematic color grading (teal and orange)"""
        # Convert to LAB color space
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Increase contrast
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        
        # Shift colors toward teal-orange
        a = cv2.add(a, 10)  # More orange
        b = cv2.subtract(b, 10)  # More teal
        
        # Merge and convert back
        lab = cv2.merge([l, a, b])
        result = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        
        # Add slight vignette
        return VideoStyles.add_vignette(result)
    
    @staticmethod
    def vintage(frame: np.ndarray) -> np.ndarray:
        """Apply vintage/retro effect"""
        # Sepia tone
        kernel = np.array([[0.272, 0.534, 0.131],
                          [0.349, 0.686, 0.168],
                          [0.393, 0.769, 0.189]])
        result = cv2.transform(frame, kernel)
        
        # Add grain
        noise = np.random.normal(0, 15, frame.shape).astype(np.uint8)
        result = cv2.add(result, noise)
        
        # Reduce saturation
        hsv = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)
        hsv[:, :, 1] = hsv[:, :, 1] * 0.6
        result = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        
        return VideoStyles.add_vignette(result, intensity=0.4)
    
    @staticmethod
    def vibrant(frame: np.ndarray) -> np.ndarray:
        """Increase saturation and vibrance"""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype(np.float32)
        
        # Increase saturation
        hsv[:, :, 1] = hsv[:, :, 1] * 1.5
        hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)
        
        # Slightly increase value
        hsv[:, :, 2] = hsv[:, :, 2] * 1.1
        hsv[:, :, 2] = np.clip(hsv[:, :, 2], 0, 255)
        
        result = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
        return result
    
    @staticmethod
    def black_and_white(frame: np.ndarray) -> np.ndarray:
        """Convert to dramatic black and white"""
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Increase contrast
        clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        
        # Convert back to BGR
        result = cv2.cvtColor(enhanced, cv2.COLOR_GRAY2BGR)
        
        return VideoStyles.add_vignette(result, intensity=0.3)
    
    @staticmethod
    def add_vignette(frame: np.ndarray, intensity: float = 0.3) -> np.ndarray:
        """Add vignette effect"""
        rows, cols = frame.shape[:2]
        
        # Create radial gradient
        X = np.linspace(-1, 1, cols)
        Y = np.linspace(-1, 1, rows)
        X, Y = np.meshgrid(X, Y)
        
        # Calculate distance from center
        radius = np.sqrt(X**2 + Y**2)
        
        # Create vignette mask
        vignette = 1 - np.clip(radius * intensity, 0, 1)
        vignette = vignette[:, :, np.newaxis]
        
        # Apply vignette
        result = (frame * vignette).astype(np.uint8)
        
        return result
    
    @staticmethod
    def apply_style(frame: np.ndarray, style: str) -> np.ndarray:
        """Apply style based on name"""
        styles = {
            'cinematic': VideoStyles.cinematic,
            'vintage': VideoStyles.vintage,
            'vibrant': VideoStyles.vibrant,
            'black_and_white': VideoStyles.black_and_white,
            'memory_lane': VideoStyles.vintage,  # Alias
            'instagram': VideoStyles.vibrant,  # Alias
        }
        
        style_func = styles.get(style.lower())
        if style_func:
            return style_func(frame)
        
        return frame  # Return original if style not found