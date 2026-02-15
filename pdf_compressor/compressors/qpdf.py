import subprocess
from pdf_compressor.utils import get_file_size_mb

def compress_with_qpdf(input_path, output_path):
    """QPDF compression"""
    print("Trying QPDF compression...")
    try:
        subprocess.run([
            'qpdf',
            '--optimize-images',
            '--compression-level=9',
            input_path,
            output_path
        ], check=True, capture_output=True, text=True)
        
        size = get_file_size_mb(output_path)
        print(f"✓ QPDF compression complete: {size:.2f} MB")
        return True, size
    except subprocess.CalledProcessError as e:
        print(f"✗ QPDF failed: {e.stderr}")
        return False, None
    except FileNotFoundError:
        print("✗ QPDF not found (installing...)")
        try:
            subprocess.run(['sudo', 'apt-get', 'install', '-y', 'qpdf'], 
                         check=True, capture_output=True)
            return compress_with_qpdf(input_path, output_path)
        except:
            print("Could not install QPDF")
            return False, None