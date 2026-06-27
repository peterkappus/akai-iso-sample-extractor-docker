# AKAI ISO Sample Extractor

This project provides a containerized environment to parse proprietary AKAI (S1000/S3000 format) ISO disc images and automatically convert and extract their audio samples into standard stereo WAV files.

It bundles `akaiutil` inside a lightweight Docker container and uses a Python script to automate the extraction process without requiring manual interactive commands.

### Key Features
* **Multi-Stage Build:** The Docker image compiles `akaiutil` from source but discards heavy build tools afterward, keeping the final image lightweight.
* **Flexible File Paths:** Accept any ISO file name dynamically via command-line flags.
* **Secure Extraction:** Uses Python's secure tar filtering to prevent path traversal vulnerabilities.

---

### How to Use It

#### 1. Directory Structure
Place your AKAI ISO files into a local folder (e.g., `data/`) on your host machine:
```text
├── Dockerfile
├── extractor.py
└── data/
    ├── drum_samples.iso
    └── synth_sounds.iso
```

#### 2. Build the Docker Image
Run the following command to build the optimized container image:

`docker build -t akai-extractor .`

#### 3. Run the Extractor
Mount your local data directory to /data inside the container, and pass the input (-i) and output (-o) flags.

```docker run --rm -v "$(pwd)/data:/data" akai-extractor \
  -i /data/drum_samples.iso \
  -o /data/extracted_drums
  ```

Command Flags
-i, --input (Required): The path to the ISO file inside the container directory.

-o, --output (Optional): The directory inside the container where files will be extracted. Defaults to /data/extracted.