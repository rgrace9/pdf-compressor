import subprocess
from pdf_compressor.utils import get_file_size_mb
from pdf_compressor.config import GHOSTSCRIPT_QUALITY_SETTINGS

def compress_with_ghostscript(input_path, output_path, quality='screen'):
    """
    Ghostscript compression
    Quality levels:
    - screen: 72 dpi (smallest, lowest quality)
    - ebook: 150 dpi (good for most uses)
    - printer: 300 dpi (high quality)
    - prepress: 300 dpi (highest quality)
    """
    
    dpi_setting = GHOSTSCRIPT_QUALITY_SETTINGS.get(quality, '/ebook')
    print(f"Trying Ghostscript compression (quality: {quality})...")
    
    try:
        subprocess.run([
            'gs',
            '-sDEVICE=pdfwrite',
            '-dCompatibilityLevel=1.4',
            '-sColorConversionStrategy=Gray',
            '-dProcessColorModel=/DeviceGray',
            f'-dPDFSETTINGS={dpi_setting}',
            '-dColorImageResolution=30',
            '-dGrayImageResolution=30',
            '-dMonoImageResolution=30',
            '-dJPEGQ=30',
            '-dColorImageDownsampleType=/Bicubic',
            '-dGrayImageDownsampleType=/Bicubic',
            '-dNOPAUSE',
            '-dQUIET',
            '-dBATCH',
            f'-sOutputFile={output_path}',
            input_path
        ], check=True, capture_output=True, text=True)
        
        size = get_file_size_mb(output_path)
        print(f"✓ Ghostscript compression complete: {size:.2f} MB")
        return True, size
    except subprocess.CalledProcessError as e:
        print(f"✗ Ghostscript failed: {e.stderr}")
        return False, None
    except FileNotFoundError:
        print("✗ Ghostscript not found (installing...)")
        try:
            subprocess.run(['sudo', 'apt-get', 'install', '-y', 'ghostscript'], 
                         check=True, capture_output=True)
            return compress_with_ghostscript(input_path, output_path, quality)
        except:
            print("Could not install Ghostscript")
            return False, None