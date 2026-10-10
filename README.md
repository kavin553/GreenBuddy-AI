# 🌱 GreenBuddy AI

### Your AI-Powered Outdoor Activity Companion

**Less scrolling. More exploring. More living.**

GreenBuddy AI is a local AI-powered application that recommends personalised outdoor and nature-related activities based on a user's available time, interests, and location.

It encourages people to spend less time on screens and more time enjoying their surroundings.

## ✨ Features

- **Personalised activity planning** based on time, interests, and location.
- **Local AI generation** using Ollama and the Qwen2.5:3b model.
- **Activity memory** to store completed activities locally.
- **Repeat reduction** by providing recent activity names to the AI and retrying repeated suggestions.
- **Duration checking** to reject suggestions whose reported duration does not fit the selected time.
- **Simple interface** built with Streamlit.
- **Privacy-conscious storage** with activity history kept in a local JSON file.

## 🛠️ Tech Stack

- Python
- Streamlit
- Ollama
- Qwen2.5:3b
- Requests
- JSON

## ⚙️ Prerequisites

Install the following before running GreenBuddy AI:

1. Python
2. Ollama
3. The Qwen2.5:3b model

Download Ollama from https://ollama.com/.

Pull the model using:

```bash
ollama pull qwen2.5:3b
```

## 🚀 Installation and Setup

Clone this repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd GreenBuddyAI
```

Create and activate a virtual environment on Windows:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install Python dependencies:

```bash
python -m pip install -r requirements.txt
```

Make sure Ollama is running and the model is available:

```bash
ollama run qwen2.5:3b
```

In another terminal, start the application:

```bash
python -m streamlit run app.py
```

Open the local URL displayed in the terminal, usually:

http://localhost:8501

## 🧭 How to Use

1. Choose your available time.
2. Select one or more interests.
3. Choose your available location.
4. Click **Plan My Outdoor Activity**.
5. Review the generated activity.
6. Click **Mark Activity as Completed** when you have actually completed it.
7. Explore your saved activity history.

## 📂 Project Structure

```text
GreenBuddyAI/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── activity_history.json  # Local data; not committed
```

## 🔒 Privacy

GreenBuddy AI uses a local Ollama model for activity generation. Completed activities are stored in `activity_history.json` on the local device.

The application does not need a cloud AI API key for its core activity-generation workflow. Avoid committing personal activity history or secret configuration files to a public repository.

## ⚠️ Limitations

- AI suggestions may sometimes be repetitive or inaccurate.
- Duration checking relies on the duration reported in the generated text; it does not measure actual activity time.
- The application does not automatically verify live weather, GPS, or location safety.
- Ollama must be installed and running locally.

## 🌿 Project Goal

GreenBuddy AI aims to encourage healthier screen habits through practical, personalised activities that connect people with nature.

**Less scrolling. More exploring. More living.**

## 📄 License

A license has not yet been selected. Add an appropriate open-source license before distributing the project under one.
