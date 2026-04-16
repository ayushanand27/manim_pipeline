# Photosynthesis Animation - Educational Video Generator

An animated educational video about **Photosynthesis** created using **Manim** (Mathematical Animation Engine). This project is designed for Class 10 Science Chapter 6 and provides a visual, easy-to-understand explanation of the photosynthesis process.

---

## 📋 Project Overview

This project generates a professional animated video that explains the photosynthesis process through:
- ✅ Chemical equation visualization
- ✅ Color-coded reactants and products
- ✅ Interactive animations with labels and arrows
- ✅ Educational summary and key takeaways
- ✅ High-quality video output (480p at 15fps)

**Perfect for**: Students, teachers, educational content creators, and science educators.

---

## 🎯 What's Been Done

### Features Implemented:

1. **Animated Title & Subtitle**
   - Display of the topic with educational context
   - Smooth fade-in/fade-out animations

2. **Chemical Equation Display**
   - Photosynthesis equation: `6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂`
   - Color-coded elements (Blue, Teal, Yellow, Green)
   - Sequential appearance with smooth transitions

3. **Labeled Components**
   - Carbon Dioxide (Reactant)
   - Water (Reactant)
   - Glucose (Product)
   - Oxygen (Product)
   - Arrows connecting each term to its label

4. **Visual Highlighting**
   - Reactants box (blue highlight)
   - Products box (green highlight)
   - Clear categorization of inputs and outputs

5. **Summary & Key Takeaway**
   - Reinforces main learning points
   - Easy-to-remember conclusion

6. **Video Output**
   - Generated at 480p resolution (15fps)
   - Suitable for educational presentations
   - Multiple scene fragments with smooth transitions

---

## 📦 Project Structure

```
project_smartskale/
├── README.md                          # This file
├── photosynthesis_scene.py            # Main animation script
├── images/                            # Output images (if generated)
├── media/
│   ├── images/
│   │   └── photosynthesis_scene/      # Generated image frames
│   ├── videos/
│   │   └── photosynthesis_scene/
│   │       └── 480p15/
│   │           └── partial_movie_files/
│   │               └── PhotosynthesisScene/  # Generated video files
│   ├── Tex/                           # LaTeX equation files
│   └── texts/                         # Text rendering files
├── venv/                              # Python virtual environment
└── __pycache__/                       # Python cache files
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- FFmpeg (for video generation)
- LaTeX (for equation rendering)

### Installation Steps

#### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

#### 2. Create a Virtual Environment
```bash
# On Windows
python -m venv venv

# On macOS/Linux
python3 -m venv venv
```

#### 3. Activate Virtual Environment
```bash
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

#### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

Or install Manim directly:
```bash
pip install manim
```

#### 5. Install FFmpeg

**Windows** (using Chocolatey):
```bash
choco install ffmpeg
```

**macOS** (using Homebrew):
```bash
brew install ffmpeg
```

**Linux** (Ubuntu/Debian):
```bash
sudo apt-get install ffmpeg
```

#### 6. Install LaTeX

**Windows**:
- Download from [MiKTeX](https://miktex.org/) or [TeX Live](https://tug.org/texlive/)

**macOS**:
```bash
brew install basictex
```

**Linux** (Ubuntu/Debian):
```bash
sudo apt-get install texlive-latex-base texlive-latex-extra
```

---

## 💻 Usage

### Run the Animation

```bash
# Generate the video at 480p resolution, 15fps
manim -ql -so photosynthesis_scene.py PhotosynthesisScene

# For high-quality output (4K, 60fps) - takes longer
manim -qh -so photosynthesis_scene.py PhotosynthesisScene

# For preview mode (fast preview)
manim -ql photosynthesis_scene.py PhotosynthesisScene
```

### Manim Flags Explained:

| Flag | Description |
|------|-------------|
| `-ql` | Quality: Low (480p, 15fps) |
| `-qm` | Quality: Medium (720p, 30fps) |
| `-qh` | Quality: High (1080p, 60fps) |
| `-qk` | Quality: 4K (2160p, 60fps) |
| `-so` | Save output (renders the video file) |
| `-p` | Preview (plays video after rendering) |

### Output Location:
The generated video will be saved at:
```
media/videos/photosynthesis_scene/480p15/PhotosynthesisScene.mp4
```

---

## 📝 Customization

### Modify Animation Title:
Edit line 7 in `photosynthesis_scene.py`:
```python
title = Text("Your Title Here", font_size=48, color=GREEN_B)
```

### Change Colors:
Modify the color variables:
```python
r"6CO_2":        BLUE,          # Change to RED, YELLOW, etc.
r"6H_2O":        TEAL,
r"C_6H_{12}O_6": YELLOW,
r"6O_2":         GREEN,
```

### Adjust Animation Speed:
Modify `run_time` parameter in `self.play()` calls:
```python
self.play(Write(title), run_time=1.2)  # Increase for slower animation
```

---

## 🔧 Troubleshooting

### Issue: "ffmpeg not found"
**Solution**: Install FFmpeg using the steps above and add to PATH

### Issue: "LaTeX not found"
**Solution**: Install a LaTeX distribution (MiKTeX, TeX Live, or similar)

### Issue: "ModuleNotFoundError: No module named 'manim'"
**Solution**: Ensure virtual environment is activated and run:
```bash
pip install manim --upgrade
```

### Issue: Slow rendering
**Solution**: Use lower quality for faster preview:
```bash
manim -ql photosynthesis_scene.py PhotosynthesisScene
```

---

## 📚 Learning Resources

- **Manim Documentation**: [docs.manim.community](https://docs.manim.community/)
- **Manim Tutorial**: [Official Tutorials](https://docs.manim.community/en/stable/tutorials.html)
- **Photosynthesis Science**: [Khan Academy](https://www.khanacademy.org/)

---

## 📂 Files Description

| File | Purpose |
|------|---------|
| `photosynthesis_scene.py` | Main animation script containing the Scene class |
| `media/` | Output directory for generated videos and images |
| `venv/` | Python virtual environment with dependencies |

---

## 🎓 Educational Use

This animation is suitable for:
- ✅ Classroom presentations
- ✅ Online learning platforms
- ✅ Science YouTube channels
- ✅ Educational blogs
- ✅ Student projects
- ✅ Tuition centers

---

## 📄 License

This project is open source and available for educational purposes.

---

## 👤 Author

**Your Name**  
Gen AI Internship Project - SmartScale  
Date: 2026

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest improvements
- Add new educational animations
- Improve documentation

---

## 📧 Contact & Support

For questions or support, please reach out or open an issue in the repository.

---

## 🎬 Rendering Tips for Best Results

1. **For Web**: Use low/medium quality for faster loading
   ```bash
   manim -ql -so photosynthesis_scene.py PhotosynthesisScene
   ```

2. **For Presentations**: Use high quality
   ```bash
   manim -qh -so photosynthesis_scene.py PhotosynthesisScene
   ```

3. **For Thumbnails**: Use preview mode
   ```bash
   manim -ql -so -p photosynthesis_scene.py PhotosynthesisScene
   ```

---

**Happy Learning! 🌱**
