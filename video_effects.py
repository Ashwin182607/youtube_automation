from moviepy.video.fx.all import *
from moviepy.editor import *

class VideoEffects:
    @staticmethod
    def apply_fade(clip, duration=1.0):
        """Add fade in and fade out effect"""
        return fade_in(fade_out(clip, duration), duration)
    
    @staticmethod
    def apply_zoom(clip, zoom_factor=1.3):
        """Add slow zoom effect"""
        def zoom(t):
            return 1 + (zoom_factor - 1) * t / clip.duration
        return clip.resize(zoom)
    
    @staticmethod
    def apply_blur(clip, sigma=3):
        """Add blur effect"""
        return blur(clip, sigma)
    
    @staticmethod
    def apply_brightness(clip, factor=1.2):
        """Adjust brightness"""
        return multiply_color(clip, factor)
    
    @staticmethod
    def apply_vignette(clip, size=0.8):
        """Add vignette effect"""
        def vignette_filter(gf, t):
            im = gf(t)
            mask = np.zeros(im.shape)
            h, w = mask.shape[:2]
            center = (int(w/2), int(h/2))
            radius = min(center[0], center[1])
            x, y = np.ogrid[:h, :w]
            mask_area = (x - center[0])**2 + (y - center[1])**2 <= radius**2
            mask[mask_area] = 1
            mask = mask * size + (1-size)
            return im * np.dstack([mask] * 3)
        return clip.fl(vignette_filter)
    
    @staticmethod
    def apply_mirror_effect(clip):
        """Add mirror effect"""
        return mirror_x(clip)
    
    @staticmethod
    def apply_color_effect(clip, color="blue", intensity=0.3):
        """Add color tint effect"""
        color_clip = ColorClip(clip.size, col=color).set_duration(clip.duration)
        return CompositeVideoClip([clip, color_clip.set_opacity(intensity)])
    
    @staticmethod
    def apply_wave_effect(clip, wavelength=20, amplitude=10):
        """Add wave distortion effect"""
        def distort(gf, t):
            im = gf(t)
            h, w = im.shape[:2]
            x = np.arange(w)
            y = np.arange(h)
            X, Y = np.meshgrid(x, y)
            offset = amplitude * np.sin(2 * np.pi * X / wavelength + 2 * np.pi * t / clip.duration)
            return np.array([[[im[int(np.clip(y + offset[int(y), int(x)], 0, h-1)), int(x), c]
                             for c in range(3)]
                            for x in range(w)]
                           for y in range(h)])
        return clip.fl(distort)

    @classmethod
    def get_available_effects(cls):
        """Return a list of available effects and their descriptions"""
        return {
            'fade': 'Add fade in/out effect',
            'zoom': 'Slow zoom effect',
            'blur': 'Blur effect',
            'brightness': 'Adjust brightness',
            'vignette': 'Vignette effect',
            'mirror': 'Mirror effect',
            'color': 'Color tint effect',
            'wave': 'Wave distortion effect'
        }

    @classmethod
    def apply_effects(cls, clip, effects_config):
        """
        Apply multiple effects to a clip based on configuration
        effects_config: dict of effect names and their parameters
        """
        result = clip
        
        for effect, params in effects_config.items():
            if effect == 'fade' and params.get('enabled', False):
                result = cls.apply_fade(result, params.get('duration', 1.0))
            elif effect == 'zoom' and params.get('enabled', False):
                result = cls.apply_zoom(result, params.get('factor', 1.3))
            elif effect == 'blur' and params.get('enabled', False):
                result = cls.apply_blur(result, params.get('sigma', 3))
            elif effect == 'brightness' and params.get('enabled', False):
                result = cls.apply_brightness(result, params.get('factor', 1.2))
            elif effect == 'vignette' and params.get('enabled', False):
                result = cls.apply_vignette(result, params.get('size', 0.8))
            elif effect == 'mirror' and params.get('enabled', False):
                result = cls.apply_mirror_effect(result)
            elif effect == 'color' and params.get('enabled', False):
                result = cls.apply_color_effect(result, 
                                             params.get('color', 'blue'),
                                             params.get('intensity', 0.3))
            elif effect == 'wave' and params.get('enabled', False):
                result = cls.apply_wave_effect(result,
                                            params.get('wavelength', 20),
                                            params.get('amplitude', 10))
                
        return result
