#!/usr/bin/env python3
"""
PDF Compression Script
Uses multiple strategies to compress large PDFs
"""

import subprocess
import os
import sys
from pathlib import Path
from pdf_compressor.utils import get_file_size_mb
from pdf_compressor.config import DEFAULT_TARGET_SIZE, LLM_OPTIMIZED
from pdf_compressor.compressors.qpdf import compress_with_qpdf
from pdf_compressor.compressors.ghostscript import compress_with_ghostscript
from pdf_compressor.compressors.imagemagick import compress_with_imagemagick

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
    print(f"🎯 Target: < {DEFAULT_TARGET_SIZE} MB\n")

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