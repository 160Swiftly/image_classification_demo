# Image Classification Web App

A Python-based web application for image classification using a pre-trained ResNet-50 model. Built with Streamlit for an easy-to-use web GUI.

## Features

- 🖼️ Upload images (JPG, JPEG, PNG)
- 🔍 Classify images using ResNet-50 model
- 📊 Display top 5 predictions with confidence scores
- 🎯 Clean and intuitive web interface

## Requirements

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd image_classification_app
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser:**
   - The app will automatically open in your default browser
   - If not, navigate to `http://localhost:8501`

3. **Upload an image:**
   - Click "Browse files" or drag and drop an image
   - Supported formats: JPG, JPEG, PNG

4. **View results:**
   - The app will display the uploaded image
   - Top 5 predictions with confidence scores will be shown

## Model Information

- **Model:** ResNet-50
- **Dataset:** ImageNet (1000 classes)
- **Framework:** PyTorch

## Project Structure

```
image_classification_app/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Notes

- The model will be downloaded automatically on first run (may take a few minutes)
- ImageNet class labels will be downloaded automatically
- The app uses CPU by default (GPU support available if CUDA is installed)

## Troubleshooting

- **Import errors:** Make sure all dependencies are installed (`pip install -r requirements.txt`)
- **Port already in use:** Streamlit will try to use port 8501. If busy, it will use the next available port
- **Model download issues:** Ensure you have an internet connection for the first run

## Docker Instructions

Prerequisites
- Docker installed (Docker Desktop or Docker Engine)
- Build the Docker image

From the project root (where the Dockerfile is located):
```bash
docker build -t streamlit-app .
```

Run the container
```bash
docker run -p 8501:8501 streamlit-app
```

Once running, open your browser and navigate to:

http://localhost:8501

Notes
- Streamlit runs on port 8501 by default.
- The container maps port 8501 inside the container to 8501 on the host.
- Ensure your Streamlit app is configured to bind to 0.0.0.0, not localhost, when running in Docker.

Example (if specified explicitly):
```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

Optional: Run in detached mode
```bash
docker run -d -p 8501:8501 streamlit-app
```

To stop the container:
```bash
docker ps
docker stop <container_id>
```