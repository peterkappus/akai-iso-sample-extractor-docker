import os
import subprocess
import tarfile
import argparse

def extract_akai_iso(iso_path, output_dir):
    if not os.path.exists(iso_path):
        print(f"[-] Error: ISO file not found at {iso_path}")
        return

    os.makedirs(output_dir, exist_ok=True)
    tar_output = os.path.join(output_dir, "extracted_samples.tar")
    
    print(f"[*] Parsing AKAI image: {iso_path}...")

    # We provide the ISO path via the command line -r flag.
    # The stdin string tells akaiutil to export the wav tarball and then quit.
    commands = f"targetwav {tar_output}\nq\n"

    try:
        process = subprocess.Popen(
            ['akaiutil', '-r', iso_path],  # Passing file directly here
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(input=commands)
        
        if process.returncode != 0:
            print(f"[-] akaiutil error:\n{stderr}")
            return
            
        print("[+] Conversion to WAV package complete.")
        
        if os.path.exists(tar_output):
            print("[*] Unpacking audio files to destination...")
            with tarfile.open(tar_output, "r:") as tar:
                tar.extractall(path=output_dir, filter='data')
            os.remove(tar_output) 
            print(f"[+] Success! Samples extracted to: {output_dir}")
        else:
            print("[-] Error: Tar file was not generated. Check if the ISO is a valid S1000/S3000 image.")

    except Exception as e:
        print(f"[-] An exception occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract audio samples from an AKAI S1000/S3000 ISO.")
    parser.add_argument("-i", "--input", required=True, help="Path to the input AKAI ISO file inside the container.")
    parser.add_argument("-o", "--output", default="/data/extracted", help="Path to the output folder inside the container.")
    
    args = parser.parse_args()
    
    extract_akai_iso(args.input, args.output)