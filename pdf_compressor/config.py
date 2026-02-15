# LLM-optimized defaults (very aggressive)
LLM_OPTIMIZED_SETTINGS = {
    'convert_to_grayscale': True,
    'max_image_dpi': 72,
    'jpeg_quality': 30,
    'strip_metadata': True
}


# Default target size for LLM attachments (MB)
DEFAULT_TARGET_SIZE = 31

# LLM size limits for convenience (MB)
LLM_LIMITS = {
    'claude': 30,
    'gpt4': 512,
    'gemini': 20,
    'copilot': 50
}


# Ghostscript quality settings
GHOSTSCRIPT_QUALITY_SETTINGS = {
    'screen': '/screen',
    'ebook': '/ebook', 
    'printer': '/printer',
    'low': '/screen'
}

# LLM-optimized compression settings (very aggressive for text extraction)
LLM_OPTIMIZED = {
    'color_image_resolution': 30,
    'gray_image_resolution': 30,
    'mono_image_resolution': 30,
    'jpeg_quality': 30,
    'imagemagick_quality': 75,
    'imagemagick_density': 150
}