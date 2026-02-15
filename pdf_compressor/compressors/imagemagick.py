import subprocess
from pdf_compressor.utils import get_file_size_mb

def compress_with_imagemagick(input_path, output_path, quality=85):
    """ImageMagick compression"""
    print(f"Trying ImageMagick compression (quality: {quality})...")
    
    try:
        subprocess.run([
            'convert',
            '-density', '150',
            '-quality', str(quality),
            '-compress', 'jpeg',
            input_path,
            output_path
        ], check=True, capture_output=True, text=True)
        
        size = get_file_size_mb(output_path)
        print(f"✓ ImageMagick compression complete: {size:.2f} MB")
        return True, size
    except subprocess.CalledProcessError as e:
        print(f"✗ ImageMagick failed: {e.stderr}")
        return False, None
    except FileNotFoundError:
        print("✗ ImageMagick not found. Install it on your system to use this compression method.")
        return False, None