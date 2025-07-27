
# 🐶 Pix2Pix GAN for Image Generation from Edge Maps

This project implements a **Pix2Pix Conditional GAN** that generates realistic images from edge outlines, using object masks from the **COCO 2017 dataset**. The model learns to translate binary edge maps into colored, high-resolution dog/object images using a U-Net-based generator and a PatchGAN discriminator.

---

## 🧠 Project Summary

- **Dataset:** COCO 2017 via TensorFlow Datasets (TFDS)
- **Input:** Edge maps (generated using OpenCV's Canny filter on segmentation masks)
- **Output:** 256×256 RGB images of objects (e.g., dogs)
- **Model:** Pix2Pix GAN with U-Net generator + PatchGAN discriminator
- **Loss Function:** GAN loss + L1 loss (`total = GAN + λ * L1`)
- **Frameworks:** TensorFlow 2.x, OpenCV, Matplotlib

---

## 🚀 Highlights

- 🧩 End-to-end edge-to-photo translation using paired image data
- 🖼️ Real-time image generation visualization
- 📦 Custom training loop with TensorBoard support
- 🧪 Includes data preprocessing, augmentation, batching, and shuffling
- 💾 Checkpoint saving for long training runs

---

## 📂 Directory Structure

```
📁 pix2pix-gan-coco/
│
├── ai_project_ares.py         # Full training & model definition
├── checkpoints/               # Saved model weights
├── logs/                      # TensorBoard logs
├── samples/                   # Example predictions
├── README.md                  # You are here
```

---

## 🔧 How It Works

1. **Data Preprocessing:**
   - Loads COCO 2017 images using TFDS
   - Extracts segmentation masks and applies edge detection (Canny)
   - Resizes and normalizes both edge maps and original images

2. **Model Architecture:**
   - **Generator:** U-Net-style encoder-decoder with skip connections
   - **Discriminator:** PatchGAN to classify real/fake (image, outline) pairs

3. **Training Loop:**
   - Uses `tf.GradientTape` for manual backpropagation
   - Logs losses (GAN, L1, Discriminator) with TensorBoard
   - Saves model checkpoints every 5000 steps
   - Generates preview outputs during training

---

## 📊 Sample Outputs

| Input Edge Map | Ground Truth | Generated Image |
|----------------|--------------|------------------|
| ![Edge](samples/edge.png) | ![GT](samples/real.png) | ![Gen](samples/fake.png) |

---

## 🛠️ Tech Stack

- Python 3.10+
- TensorFlow 2.14+
- OpenCV
- Matplotlib
- COCO Dataset (via `tensorflow_datasets`)

---

## 📈 To Train the Model

```bash
# Clone the repo
git clone https://github.com/your-username/pix2pix-gan-coco.git
cd pix2pix-gan-coco

# Install dependencies
pip install tensorflow opencv-python matplotlib tensorflow-datasets

# Run training script
python ai_project_ares.py
```

---

## 📌 Future Improvements

- Add FID and SSIM metrics for evaluation
- Support for custom datasets (e.g., Stanford Dogs)
- Streamlit or Gradio UI for demo
- Export model for real-time inference

---

## 📄 License

This project is released under the MIT License.

---

## 🙋‍♂️ Author

**Anurag Pradhan**  
📧 [anuragpradhancb@gmail.com](mailto:anuragpradhancb@gmail.com)  
🔗 [LinkedIn](https://linkedin.com/in/anurag-pradhan-0340bb288) • [GitHub](https://github.com/anurag965)

---
