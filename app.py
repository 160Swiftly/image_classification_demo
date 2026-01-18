import streamlit as st
import numpy as np
import torch
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image

# Verify numpy is available
try:
    np.array([1, 2, 3])
except Exception as e:
    st.error(f"NumPy is not working properly: {e}")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Image Classification App",
    page_icon="🖼️",
    layout="wide"
)

# Title and description
st.title("🖼️ Image Classification App")
st.markdown("Upload an image to classify it using a pre-trained ResNet-50 model trained on ImageNet.")

# Load the model (cache it to avoid reloading on every interaction)
@st.cache_resource
def load_model():
    """Load pre-trained ResNet-50 model"""
    model = models.resnet50(pretrained=True)
    model.eval()
    return model

# Load ImageNet class labels
@st.cache_data
def load_imagenet_labels():
    """Load ImageNet class labels"""
    import urllib.request
    url = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
    try:
        urllib.request.urlretrieve(url, "imagenet_classes.txt")
    except:
        pass
    
    with open("imagenet_classes.txt", "r") as f:
        labels = [line.strip() for line in f.readlines()]
    return labels

# Image preprocessing
def preprocess_image(image):
    """Preprocess image for ResNet-50"""
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                           std=[0.229, 0.224, 0.225])
    ])
    return transform(image).unsqueeze(0)

# File uploader
uploaded_file = st.file_uploader(
    "Choose an image file",
    type=['jpg', 'jpeg', 'png'],
    help="Upload a JPG, JPEG, or PNG image"
)

if uploaded_file is not None:
    # Load model and labels (only when needed)
    status_container = st.empty()
    progress_bar = st.progress(0)
    status_container.info("🔄 Loading model (first time only - this may take a minute)...")
    
    progress_bar.progress(10)
    status_container.info("📥 Downloading model weights...")
    model = load_model()
    
    progress_bar.progress(60)
    status_container.info("📋 Loading ImageNet labels...")
    imagenet_labels = load_imagenet_labels()
    
    progress_bar.progress(100)
    status_container.success("✅ Model loaded successfully!")
    progress_bar.empty()
    status_container.empty()
    
    # Display uploaded image
    image = Image.open(uploaded_file).convert('RGB')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📤 Uploaded Image")
        st.image(image, use_container_width=True)
    
    with col2:
        st.subheader("🔍 Classification Results")
        
        # Preprocess and classify
        classify_status = st.empty()
        classify_progress = st.progress(0)
        
        classify_status.info("🔄 Processing image...")
        classify_progress.progress(20)
        input_tensor = preprocess_image(image)
        
        classify_status.info("🧠 Running classification...")
        classify_progress.progress(50)
        with torch.no_grad():
            outputs = model(input_tensor)
            probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
        
        classify_progress.progress(80)
        classify_status.info("📊 Calculating predictions...")
        # Get top 5 predictions
        top5_prob, top5_idx = torch.topk(probabilities, 5)
        
        classify_progress.progress(100)
        classify_status.success("✅ Classification complete!")
        classify_progress.empty()
        classify_status.empty()
        
        st.markdown("**Top 5 Predictions:**")
        st.markdown("---")
        
        for i in range(5):
            label = imagenet_labels[top5_idx[i]]
            prob = top5_prob[i].item() * 100
            
            # Display with progress bar
            st.write(f"**{i+1}. {label}**")
            st.progress(prob / 100)
            st.write(f"   Confidence: {prob:.2f}%")
            st.markdown("---")
    
    # Show top prediction prominently
    top_label = imagenet_labels[top5_idx[0]]
    top_prob = top5_prob[0].item() * 100
    
    st.success(f"🎯 **Most likely:** {top_label} ({top_prob:.2f}% confidence)")

else:
    st.info("👆 Please upload an image file to get started!")
    st.markdown("---")
    st.markdown("**Note:** The model will load automatically when you upload your first image.")

# Sidebar with information
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    This app uses a pre-trained **ResNet-50** model 
    trained on the **ImageNet** dataset.
    
    **Features:**
    - Supports JPG, JPEG, and PNG formats
    - Shows top 5 predictions
    - Displays confidence scores
    
    **Model:** ResNet-50  
    **Dataset:** ImageNet (1000 classes)
    """)
    
    st.header("📝 Instructions")
    st.markdown("""
    1. Click "Browse files" or drag and drop an image
    2. Wait for the classification to complete
    3. View the top 5 predictions with confidence scores
    """)
