 <div align="center">

# 🌱 GreenBuddy AI

### 🌿 Less Scrolling. More Exploring. More Living.

**Your AI-powered companion for discovering activities beyond the screen.**

<p>
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/Ollama-Local%20AI-111111?style=for-the-badge" alt="Ollama"/>
  <img src="https://img.shields.io/badge/Open%20Source-Community-2EA44F?style=for-the-badge&logo=github&logoColor=white" alt="Open Source"/>
</p>

**Discover nature. Build better habits. Make every break count.** 🍃

</div>

---

## 🍀 About the Project

**GreenBuddy AI** is a local AI-powered outdoor activity companion that recommends personalised nature-related and screen-free activities based on your available time, interests, and surroundings.

Whether you have 15 minutes for a quick nature break or a couple of hours for exploration, GreenBuddy helps you discover meaningful ways to spend your time.

Instead of endlessly scrolling, take a break, explore your surroundings, and reconnect with the world outside your screen. 🌎

> 💚 **Our mission:** Turn screen breaks into opportunities for exploration, creativity, and connection with nature.

## ✨ Features

| Feature | Description |
|---|---|
| 🎯 Personalised Recommendations | Suggests activities based on available time, interests, and location. |
| 🧠 Local AI Generation | Uses Ollama with the Qwen2.5:3b model to generate activity ideas locally. |
| ⏱️ Time-Aware Suggestions | Checks the duration reported by the AI against the selected time. |
| 🔄 Repeat Reduction | Uses recently completed activity names to reduce repeated recommendations. |
| ✅ Activity Tracking | Lets users mark activities as completed. |
| 📚 Activity History | Saves completed activities in a local JSON file. |
| 🔐 Privacy-Conscious Design | Keeps activity history on the user's device. |
| 🌿 Simple User Interface | Provides an interactive interface built with Streamlit. |

## 🛠️ Tech Stack

<div align="center">

| Technology | Purpose |
|---|---|
| 🐍 Python | Core application logic |
| 🎨 Streamlit | Interactive web interface |
| 🦙 Ollama | Local model runtime |
| 🤖 Qwen2.5:3b | AI-powered activity generation |
| 🔌 Requests | Communicating with the local Ollama API |
| 📄 JSON | Local activity-history storage |
| 🔧 Git & GitHub | Version control and project hosting |

</div>

## ⚙️ Getting Started

Follow these steps to run GreenBuddy AI on your computer.

### 📋 Prerequisites

Make sure you have:

- Python installed
- Git installed
- Ollama installed
- The Qwen2.5:3b model downloaded

Download Ollama from [ollama.com](https://ollama.com/).

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/kavin553/GreenBuddy-AI.git
cd GreenBuddyAI
```

Replace `kavin553` with your GitHub username.

### 2️⃣ Create a Virtual Environment

**Windows — PowerShell**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks virtual-environment activation, follow the Python documentation for your environment or activate the environment using Command Prompt instead.

### 3️⃣ Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4️⃣ Download the AI Model

```bash
ollama pull qwen2.5:3b
```

Make sure the Ollama application or service is running on your computer.

### 5️⃣ Launch GreenBuddy AI 🚀

```bash
python -m streamlit run app.py
```

Open the local address shown in your terminal. It is usually:

**http://localhost:8501**

🎉 You're ready to discover your next activity!

## 🧭 How It Works

```text
       👤 User Preferences
                |
                v
    ⏱️ Available Time
    🌱 Interests
    📍 Available Location
                |
                v
       🧠 GreenBuddy AI
                |
                v
       🤖 Local Ollama Model
                |
                v
      ✨ Activity Recommendation
                |
                v
        ✅ Complete Activity
                |
                v
       📚 Save Local History
```

*The flow above illustrates the intended application workflow.*

## 🌼 How to Use

1. 🚀 Launch the Streamlit application.
2. ⏱️ Select how much time you have available.
3. 🌿 Choose your interests, such as nature, gardening, walking, birdwatching, or photography.
4. 📍 Select your available location.
5. ✨ Click **Plan My Outdoor Activity**.
6. 📝 Read your personalised activity recommendation.
7. ✅ After actually completing the activity, click **Mark Activity as Completed**.
8. 📚 View your saved activity history.

**Tip:** Start small. Even a short break away from your screen can be an opportunity to explore something new. 🌳

## 📂 Project Structure

```text
GreenBuddyAI/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── .gitignore              # Files excluded from Git
│
└── activity_history.json   # Local activity data, created at runtime
```

> 🔒 `activity_history.json` is local application data and should not be committed to the public repository.

## 🔐 Privacy & Data Handling

Privacy is an important part of GreenBuddy AI.

- 🖥️ **Local inference:** Activity generation uses the Ollama model running on your computer.
- 📁 **Local history:** Completed activities are stored in a local JSON file.
- 🔑 **No cloud AI key required:** The core activity-generation workflow does not require a cloud AI API key.
- 🚫 **Git exclusions:** The `.gitignore` file excludes the virtual environment, local history, and secret configuration files.

**Note:** Local model inference does not automatically guarantee that every part of a computer or network is offline. Keep Ollama and other software appropriately configured.

## ⚠️ Current Limitations

- AI-generated suggestions can sometimes be inaccurate or repetitive.
- Duration validation checks the duration stated in the generated text; it does not measure actual completion time.
- Weather conditions and outdoor safety are not automatically verified.
- GPS and live location services are not currently integrated.
- Ollama must be installed and running locally for AI generation.

## 🚀 Future Improvements

Potential directions for future development include:

- 🌦️ Weather-aware outdoor activity recommendations
- 🗺️ Optional nearby nature-spot discovery
- 📊 Activity streaks and progress visualisation
- 🎨 A more personalised and animated interface
- 🌍 Multilingual recommendations
- 🧩 Improved activity diversity and recommendation validation
- 📱 A responsive mobile-friendly experience

*These are potential enhancements, not features currently guaranteed to be implemented.*

## 🤝 Contributing

Contributions, ideas, bug reports, and suggestions are welcome!

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Test the application locally.
5. Submit a pull request describing your improvements.

Please avoid including private data, local activity history, or secret configuration files in contributions.

## 💚 Project Philosophy

GreenBuddy AI is built around one simple idea:

> 🌎 **Technology should help us live better — not keep us glued to a screen.**

Take a break. Step outside. Explore your surroundings. Discover something new.

<div align="center">

### 🌱 GreenBuddy AI

**Less scrolling. More exploring. More living.**

Made with 💚 and Python.

</div>

---

## 📄 License

No open-source license has been selected yet. Choose an appropriate license and add a `LICENSE` file before formally distributing the project under an open-source license.
