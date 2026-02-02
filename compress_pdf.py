#!/usr/bin/env python3
"""
PDF Compression Script
Uses multiple strategies to compress large PDFs
"""

import subprocess
import os
import sys
from pathlib import Path

def get_file_size_mb(filepath):
    """Get file size in MB"""
    size_bytes = os.path.getsize(filepath)
    return size_bytes / (1024 * 1024)

def compress_with_qpdf(input_path, output_path):
    """Method 1: QPDF compression"""
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

def compress_with_ghostscript(input_path, output_path, quality='screen'):
    """
    Method 2: Ghostscript compression
    Quality levels:
    - screen: 72 dpi (smallest, lowest quality)
    - ebook: 150 dpi (good for most uses)
    - printer: 300 dpi (high quality)
    - prepress: 300 dpi (highest quality)
    """
    quality_settings = {
        'screen': '/screen',
        'ebook': '/ebook',
        'printer': '/printer',
        'low': '/screen'
    }
    
    dpi_setting = quality_settings.get(quality, '/ebook')
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

def compress_with_imagemagick(input_path, output_path, quality=85):
    """Method 3: ImageMagick compression"""
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
        print("✗ ImageMagick not found")
        return False, None

def main():
    if len(sys.argv) != 2:
        print("Usage: python compress_pdf.py <input_pdf_path>")
        print("\nOr place your PDF in /mnt/user-data/uploads/ and just provide the filename")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # Try to find the file in various locations
    if os.path.exists(input_file):
        # File exists at given path (relative or absolute)
        input_path = input_file
    elif os.path.exists(f"/mnt/user-data/uploads/{input_file}"):
        # File is in uploads folder
        input_path = f"/mnt/user-data/uploads/{input_file}"
    else:
        print(f"Error: File not found: {input_file}")
        print(f"Current directory: {os.getcwd()}")
        print(f"Looking for: {os.path.abspath(input_file)}")
        sys.exit(1)
    
    original_size = get_file_size_mb(input_path)
    print(f"\n📄 Original file: {Path(input_path).name}")
    print(f"📊 Original size: {original_size:.2f} MB")
    print(f"🎯 Target: < 31 MB\n")
    
    base_name = Path(input_path).stem
    output_dir = os.path.join(os.getcwd(), "outputs")
    os.makedirs(output_dir, exist_ok=True)
    
    results = []
    
    # Strategy 1: QPDF (lossless optimization)
    output1 = f"{output_dir}/{base_name}_qpdf.pdf"
    success, size = compress_with_qpdf(input_path, output1)
    if success:
        results.append(('QPDF', output1, size))
    
    # Strategy 2: Ghostscript with 'ebook' quality (good balance)
    output2 = f"{output_dir}/{base_name}_ebook.pdf"
    success, size = compress_with_ghostscript(input_path, output2, 'ebook')
    if success:
        results.append(('Ghostscript (ebook)', output2, size))
    
    # Strategy 3: Ghostscript with 'screen' quality (more aggressive)
    output3 = f"{output_dir}/{base_name}_screen.pdf"
    success, size = compress_with_ghostscript(input_path, output3, 'screen')
    if success:
        results.append(('Ghostscript (screen)', output3, size))
    
    # Strategy 4: ImageMagick with reduced quality
    output4 = f"{output_dir}/{base_name}_imagemagick.pdf"
    success, size = compress_with_imagemagick(input_path, output4, quality=75)
    if success:
        results.append(('ImageMagick (q75)', output4, size))
    
    # Print summary
    print("\n" + "="*60)
    print("COMPRESSION RESULTS")
    print("="*60)
    
    if not results:
        print("❌ No compression methods succeeded")
        return
    
    # Sort by file size
    results.sort(key=lambda x: x[2])
    
    print(f"\n{'Method':<25} {'Size (MB)':<12} {'Status'}")
    print("-" * 60)
    
    best_under_31 = None
    for method, path, size in results:
        status = "✓ Under 31MB!" if size < 31 else "Still too large"
        print(f"{method:<25} {size:>8.2f} MB   {status}")
        
        if size < 31 and best_under_31 is None:
            best_under_31 = (method, path, size)
    
    if best_under_31:
        method, path, size = best_under_31
        print(f"\n🎉 SUCCESS! Best result: {method} ({size:.2f} MB)")
        print(f"📁 File saved to: {path}")
    else:
        print(f"\n⚠️  All files still exceed 31 MB")
        print(f"💡 Smallest achieved: {results[0][2]:.2f} MB with {results[0][0]}")
        print("\nTips to reduce further:")
        print("  - Use the 'screen' quality setting (72 DPI)")
        print("  - Reduce image DPI/quality in the source document")
        print("  - Remove unnecessary images or graphics")
        print("  - Split into multiple PDFs")
        print("  - Try even lower quality: gs -dPDFSETTINGS=/screen")

if __name__ == "__main__":
    main()