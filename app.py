from __future__ import annotations

import json
import re
from pathlib import Path

import requests
import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="GreenBuddy AI | Nature Companion",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------- DESIGN SYSTEM ----------------
st.markdown(
    """
<style>
:root {
    --gb-forest: #164b35;
    --gb-forest-dark: #103c2b;
    --gb-leaf: #2f8753;
    --gb-mint: #e5f6eb;
    --gb-mint-light: #f3fbf5;
    --gb-ink: #20392b;
    --gb-muted: #647d6c;
    --gb-border: #d9eadd;
    --gb-white: #ffffff;
}

.stApp {
    background:
      radial-gradient(ellipse at 4% 8%, rgba(191, 237, 207, .55), transparent 31%),
      radial-gradient(ellipse at 96% 24%, rgba(204, 241, 214, .48), transparent 29%),
      linear-gradient(160deg, #f6fcf7 0%, #edf8f0 58%, #f8fcf8 100%);
    color: var(--gb-ink);
}

.block-container {
    max-width: 1120px;
    padding-top: 1.6rem;
    padding-bottom: 3.2rem;
}

/* Gentle floating leaves on the page edges */
.stApp::before, .stApp::after {
    position: fixed;
    z-index: 0;
    pointer-events: none;
    opacity: .13;
    font-size: 2.25rem;
    animation: gb-leaf-drift 9s ease-in-out infinite;
}
.stApp::before { content: "🍃"; left: 2.2%; top: 22%; }
.stApp::after { content: "🌿"; right: 2.2%; bottom: 16%; animation-delay: -4.5s; }
@keyframes gb-leaf-drift {
    0%, 100% { transform: translateY(0) rotate(-8deg); }
    50% { transform: translateY(-13px) rotate(8deg); }
}

/* General typography and readable contrast */
.stApp, .stApp p, .stApp label, .stApp li,
.stApp [data-testid="stMarkdownContainer"] {
    color: var(--gb-ink);
}
.stApp h1, .stApp h2, .stApp h3, .stApp h4 {
    color: var(--gb-forest) !important;
    letter-spacing: -.35px;
}
.stApp [data-testid="stCaptionContainer"],
.stApp [data-testid="stCaptionContainer"] * {
    color: var(--gb-muted) !important;
}
.stApp [data-testid="stWidgetLabel"],
.stApp [data-testid="stWidgetLabel"] * {
    color: #315c40 !important;
    -webkit-text-fill-color: #315c40 !important;
    font-weight: 600;
}

/* Hero */
.gb-hero {
    position: relative;
    overflow: hidden;
    padding: clamp(1.5rem, 4vw, 2.8rem);
    border-radius: 28px;
    background: linear-gradient(125deg, #123f2d 0%, #1d6442 58%, #4e8d59 100%);
    box-shadow: 0 18px 45px rgba(26, 81, 48, .17);
    margin-bottom: 1rem;
}
.gb-hero::after {
    content: "🌿";
    position: absolute;
    right: 4%;
    bottom: 4%;
    font-size: clamp(3.5rem, 8vw, 7rem);
    opacity: .15;
    transform: rotate(-18deg);
    pointer-events: none;
}
.gb-eyebrow {
    color: #d5f2bd !important;
    -webkit-text-fill-color: #d5f2bd !important;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: .76rem;
    font-weight: 800;
}
.gb-hero-title {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    font-size: clamp(2.15rem, 5vw, 3.65rem);
    font-weight: 850;
    line-height: 1.08;
    letter-spacing: -1.5px;
    margin: .8rem 0 .75rem;
}
.gb-hero-copy {
    color: #f1fbf2 !important;
    -webkit-text-fill-color: #f1fbf2 !important;
    font-size: 1.06rem;
    line-height: 1.65;
    max-width: 690px;
    margin: 0 0 1.25rem;
}
.gb-tagline {
    display: inline-block;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    background: rgba(255,255,255,.13);
    border: 1px solid rgba(255,255,255,.28);
    border-radius: 999px;
    padding: .62rem .95rem;
    font-size: .91rem;
    font-weight: 600;
}
.gb-trust {
    margin: .65rem 0 1.4rem;
    color: #668571 !important;
    font-size: .88rem;
}

/* White cards and planner */
div[data-testid="stForm"],
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255,255,255,.88);
    border: 1px solid var(--gb-border);
    border-radius: 22px;
    box-shadow: 0 10px 30px rgba(31, 79, 47, .055);
}
div[data-testid="stForm"] { padding: 1.1rem 1.25rem .9rem; }
div[data-testid="stVerticalBlockBorderWrapper"] { padding: 1rem; }

/* Streamlit select and multiselect controls */
.stSelectbox [data-baseweb="select"],
.stMultiSelect [data-baseweb="select"] {
    background: #ffffff !important;
    border-radius: 12px !important;
    border-color: #cfe2d3 !important;
}
.stSelectbox [data-baseweb="select"] *,
.stMultiSelect [data-baseweb="select"] * {
    color: #20392b;
}
div[data-baseweb="popover"], div[data-baseweb="menu"] {
    background: #ffffff !important;
}
div[data-baseweb="popover"] *, div[data-baseweb="menu"] * {
    color: #20392b !important;
}

/* Buttons */
.stButton > button, .stFormSubmitButton > button {
    border: 0;
    border-radius: 12px;
    min-height: 2.8rem;
    padding: .55rem 1rem;
    color: #ffffff !important;
    background: linear-gradient(120deg, #2f8753, #1b603e);
    font-weight: 700;
    box-shadow: 0 5px 14px rgba(39, 112, 67, .13);
    transition: transform .18s ease, box-shadow .18s ease;
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
    color: #ffffff !important;
    border: 0;
    transform: translateY(-2px);
    box-shadow: 0 9px 20px rgba(39, 112, 67, .22);
}

/* Activity content */
.gb-card-kicker {
    color: #4d805b !important;
    font-size: .74rem;
    letter-spacing: 1.6px;
    text-transform: uppercase;
    font-weight: 850;
}
.gb-duration {
    display: inline-block;
    background: #e6f6e8;
    color: #245c39 !important;
    -webkit-text-fill-color: #245c39 !important;
    border: 1px solid #cce8d0;
    border-radius: 999px;
    padding: .4rem .75rem;
    font-weight: 750;
    font-size: .86rem;
}
.gb-mini-label {
    color: #2e7047 !important;
    font-weight: 750;
    margin: .45rem 0 .15rem;
}
.gb-stat-label {
    color: #62816b !important;
    font-size: .82rem;
    font-weight: 650;
}
.gb-stat-value {
    color: #164b35 !important;
    font-size: 1.8rem;
    font-weight: 850;
    line-height: 1.2;
}

/* Metric contrast */
.stApp [data-testid="stMetricLabel"],
.stApp [data-testid="stMetricLabel"] * {
    color: #54745d !important;
    -webkit-text-fill-color: #54745d !important;
}
.stApp [data-testid="stMetricValue"],
.stApp [data-testid="stMetricValue"] * {
    color: #164b35 !important;
    -webkit-text-fill-color: #164b35 !important;
    font-weight: 800;
}

/* Expanders and dividers */
div[data-testid="stExpander"] {
    border: 1px solid #d7e8d9;
    border-radius: 14px;
    background: rgba(255,255,255,.75);
}
hr { border-color: rgba(72, 125, 83, .17); }

@media (max-width: 700px) {
    .block-container { padding-left: 1rem; padding-right: 1rem; }
    .gb-hero { border-radius: 21px; }
    div[data-testid="stForm"] { padding: .7rem; }
}
@media (prefers-reduced-motion: reduce) {
    .stApp::before, .stApp::after { animation: none; }
    .stButton > button, .stFormSubmitButton > button { transition: none; }
}
</style>
""",
    unsafe_allow_html=True,
)

# ---------------- HERO ----------------
st.markdown(
    """
<div class="gb-hero">
  <div class="gb-eyebrow">🌍 Your personal nature companion</div>
  <div class="gb-hero-title">GreenBuddy AI 🌱</div>
  <p class="gb-hero-copy">Discover simple activities. Reconnect with nature. Make every break count.</p>
  <div class="gb-tagline">🍃 Less scrolling. More exploring. More living.</div>
</div>
<div class="gb-trust">🛡️ Powered by local AI · Your activity history stays on your device</div>
""",
    unsafe_allow_html=True,
)

# ---------------- CONFIG ----------------
HISTORY_FILE = Path(__file__).parent / "activity_history.json"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:3b"
MAX_ATTEMPTS = 3


def load_history():
    if HISTORY_FILE.exists():
        try:
            data = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
            if isinstance(data, list):
                return [item for item in data if isinstance(item, dict)]
        except (json.JSONDecodeError, OSError):
            pass
    return []


def save_history(history):
    HISTORY_FILE.write_text(
        json.dumps(history, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def extract_activity_name(text):
    match = re.search(
        r"Activity\s*Name\s*:\s*\**([^*\n]+)", text, flags=re.IGNORECASE
    )
    if match:
        return match.group(1).strip(" *:-")
    for line in text.splitlines():
        line = line.strip().strip("*# ")
        if line:
            return line[:100]
    return ""


def extract_duration_line(text):
    match = re.search(
        r"(?:approximate\s+)?duration\s*:\s*([^\n]+)",
        text,
        flags=re.IGNORECASE,
    )
    return match.group(1).strip() if match else ""


def parse_activity_sections(text):
    labels = {
        "why": r"Why it fits\s*:",
        "steps": r"Simple Steps\s*:",
        "duration": r"(?:Approximate )?Duration\s*:",
        "materials": r"Materials Needed\s*:",
        "encouragement": r"Less Screen Time\s*:",
    }
    all_labels = "|".join(f"(?:{pattern})" for pattern in labels.values())
    sections = {}
    for key, pattern in labels.items():
        match = re.search(
            pattern + rf"\s*(.*?)(?=\n\s*(?:{all_labels})|\Z)",
            text,
            flags=re.IGNORECASE | re.DOTALL,
        )
        if match:
            sections[key] = match.group(1).strip()

    steps = []
    for line in sections.get("steps", "").splitlines():
        cleaned = re.sub(r"^\s*(?:[-*]|\d+[.)])\s*", "", line).strip()
        if cleaned:
            steps.append(cleaned)

    return {
        "name": extract_activity_name(text) or "Your nature activity",
        "duration": extract_duration_line(text) or "See activity details",
        "why": sections.get("why", "A simple activity tailored to your preferences."),
        "steps": steps,
        "materials": sections.get("materials", "Not specified"),
        "encouragement": sections.get(
            "encouragement", "Take a break and enjoy the world around you."
        ),
    }


def duration_fits(text, available_time):
    duration_line = extract_duration_line(text)
    if not duration_line:
        return False
    matches = re.findall(
        r"(\d+(?:\.\d+)?)\s*(minutes?|mins?|hours?|hrs?)",
        duration_line,
        flags=re.IGNORECASE,
    )
    if not matches:
        return False

    values = []
    for number, unit in matches:
        value = float(number)
        values.append(value * 60 if unit.lower().startswith(("hour", "hr")) else value)
    duration_minutes = max(values)
    limits = {"15 minutes": 15, "30 minutes": 30, "1 hour": 60}
    if available_time == "2+ hours":
        return duration_minutes >= 120
    limit = limits.get(available_time)
    return limit is not None and duration_minutes <= limit


def get_recent_activity_names(history, limit=10):
    names = []
    for item in reversed(history):
        activity_text = str(item.get("activity", "")).strip()
        if activity_text:
            name = extract_activity_name(activity_text)
            if name:
                names.append(name)
        if len(names) >= limit:
            break
    return names


if "history" not in st.session_state:
    st.session_state.history = load_history()
if "current_activity" not in st.session_state:
    st.session_state.current_activity = None
if "current_details" not in st.session_state:
    st.session_state.current_details = None

# ---------------- PLANNER ----------------
st.markdown("## 🌿 Plan your next little adventure")
st.markdown(
    "Choose your time, interests, and surroundings. GreenBuddy will suggest one practical activity."
)

with st.form("activity_form"):
    form_col1, form_col2 = st.columns(2)
    with form_col1:
        available_time = st.selectbox(
            "⏱️ How much free time do you have?",
            ["15 minutes", "30 minutes", "1 hour", "2+ hours"],
        )
    with form_col2:
        location = st.selectbox(
            "📍 Where can you go?",
            ["Garden or park", "Neighbourhood", "Outdoor trail", "At home"],
        )
    interests = st.multiselect(
        "🌼 What do you enjoy?",
        ["Nature", "Walking", "Gardening", "Birdwatching", "Photography"],
        placeholder="Choose one or more interests",
    )
    submitted = st.form_submit_button(
        "🌿 Plan My Outdoor Activity", use_container_width=True
    )

# ---------------- GENERATE ACTIVITY ----------------
if submitted:
    st.session_state.current_activity = None
    st.session_state.current_details = None

    if not interests:
        st.warning("Please select at least one interest so GreenBuddy can personalise your activity.")
    else:
        recent_names = get_recent_activity_names(st.session_state.history, limit=10)
        history_context = (
            "\n".join(f"- {name}" for name in recent_names)
            if recent_names
            else "No activities completed yet."
        )
        rejected_suggestions = []
        base_prompt = f"""
You are GreenBuddy, an AI assistant that helps people spend less time on screens and enjoy safe outdoor activities.

USER PREFERENCES
Available time: {available_time}
Interests: {", ".join(interests)}
Available location: {location}

RECENTLY COMPLETED ACTIVITY NAMES
{history_context}

YOUR TASK
Recommend exactly ONE practical, personalised activity.

STRICT TIME RULES
- 15 minutes: total activity must take 15 minutes or less.
- 30 minutes: total activity must take 30 minutes or less.
- 1 hour: total activity must take 60 minutes or less.
- 2+ hours: suggest an activity lasting at least 2 hours.
- Include preparation and travel time when relevant.
- Give a realistic duration and never knowingly exceed the time limit.

AVOID REPETITION
- Do not reuse a recent activity name.
- Avoid activities that are substantially similar to recent activities.
- Choose a different activity type where practical.
- Do not simply rename a previously completed activity.

PERSONALISATION
- Match the selected interests and location.
- If location is At home, suggest an activity suitable for home.
- Prefer common materials or no special equipment.
- Make sure the activity can realistically be completed in the selected time.

SAFETY
- Suggest age-appropriate, low-risk activities.
- Prefer familiar, accessible places and daylight outdoor activities.
- Do not suggest isolated places, trespassing, or travelling far alone.
- Do not invent live weather, GPS, or location information.

OUTPUT FORMAT
Activity Name: [short, specific name]

Why it fits:
[Explain in 1-2 sentences.]

Simple Steps:
1. [First action]
2. [Second action]
3. [Third action]

Approximate Duration: [duration in minutes or hours]
Materials Needed: [short list, or None]
Less Screen Time:
[One short encouraging sentence.]

Keep the response friendly, practical, and concise. Return only the activity plan.
"""
        accepted_activity = None
        last_error = None

        with st.spinner("🌱 GreenBuddy is growing a plan for you..."):
            for _attempt in range(MAX_ATTEMPTS):
                retry_context = ""
                if rejected_suggestions:
                    retry_context = (
                        "\nIMPORTANT: Do not suggest any of these rejected activities:\n"
                        + "\n".join(f"- {name}" for name in rejected_suggestions)
                        + "\nGenerate a different activity following every rule.\n"
                    )
                try:
                    response = requests.post(
                        OLLAMA_URL,
                        json={"model": MODEL_NAME, "prompt": base_prompt + retry_context, "stream": False},
                        timeout=180,
                    )
                    response.raise_for_status()
                    activity = str(response.json().get("response", "")).strip()
                    if not activity:
                        last_error = "The AI returned an empty response."
                        continue

                    activity_name = extract_activity_name(activity)
                    if not activity_name:
                        last_error = "Could not identify the activity name."
                        continue

                    previous_names = {name.casefold() for name in recent_names}
                    if activity_name.casefold() in previous_names:
                        rejected_suggestions.append(activity_name)
                        last_error = "The AI repeated a recent activity."
                        continue

                    if not duration_fits(activity, available_time):
                        rejected_suggestions.append(activity_name)
                        last_error = "The activity duration was missing or did not match the selected time."
                        continue

                    accepted_activity = activity
                    break
                except requests.exceptions.ConnectionError:
                    last_error = "Cannot connect to Ollama. Make sure Ollama is running."
                    break
                except requests.exceptions.Timeout:
                    last_error = "The AI took too long to respond. Please try again."
                    break
                except requests.exceptions.RequestException as error:
                    last_error = f"AI request failed: {error}"
                    break
                except (ValueError, TypeError, KeyError):
                    last_error = "The AI returned an unexpected response."
                    break

        if accepted_activity:
            st.session_state.current_activity = accepted_activity
            st.session_state.current_details = {
                "time": available_time,
                "interests": interests,
                "location": location,
            }
        else:
            st.warning("GreenBuddy couldn't create a suitable new activity after a few attempts. Please try again.")
            if last_error:
                st.caption(f"Reason: {last_error}")

# ---------------- RECOMMENDATION CARD ----------------
if st.session_state.current_activity:
    activity_text = st.session_state.current_activity
    activity_card = parse_activity_sections(activity_text)
    st.markdown("## ✨ Your personalised activity")

    with st.container(border=True):
        st.markdown(
            '<div class="gb-card-kicker">🌿 YOUR NEXT LITTLE ADVENTURE</div>',
            unsafe_allow_html=True,
        )
        st.markdown(f"### {activity_card['name']}")
        st.markdown(
            f'<span class="gb-duration">⏱️ {activity_card["duration"]}</span>',
            unsafe_allow_html=True,
        )
        st.markdown(" ")

        reason_col, materials_col = st.columns(2)
        with reason_col:
            st.markdown("**🌱 Why it fits**")
            st.write(activity_card["why"])
        with materials_col:
            st.markdown("**🎒 Materials needed**")
            st.write(activity_card["materials"])

        st.markdown("**🧭 Your simple steps**")
        if activity_card["steps"]:
            for index, step in enumerate(activity_card["steps"], start=1):
                st.markdown(f"**{index}.** {step}")
        else:
            st.info("Open the complete AI response below to view the suggested steps.")

        st.info(f"💚 {activity_card['encouragement']}")
        with st.expander("Read the complete AI response"):
            st.markdown(activity_text)

        if st.button("✅ Mark Activity as Completed", key="complete_activity", use_container_width=True):
            details = st.session_state.current_details
            if not details:
                st.error("Activity details are missing. Generate a new plan.")
            else:
                entry = {**details, "activity": activity_text}
                updated_history = [*st.session_state.history, entry]
                try:
                    save_history(updated_history)
                    st.session_state.history = updated_history
                    st.session_state.current_activity = None
                    st.session_state.current_details = None
                    st.success("Activity saved to your local history!")
                    st.rerun()
                except OSError:
                    st.error("Could not save history. Check folder permissions.")

# ---------------- ACTIVITY MEMORY DASHBOARD ----------------
st.markdown("## 📚 Your activity memory")
st.markdown("Your completed activities, saved locally on this device.")

valid_history = [
    item for item in st.session_state.history
    if isinstance(item, dict) and str(item.get("activity", "")).strip()
]
latest_history = list(reversed(valid_history))

total_completed = len(valid_history)
unique_names = {
    extract_activity_name(str(item.get("activity", ""))).casefold()
    for item in valid_history
    if extract_activity_name(str(item.get("activity", "")))
}

metric1, metric2, metric3 = st.columns(3)
with metric1:
    st.metric("🌿 Activities completed", total_completed)
with metric2:
    st.metric("✨ Different activities", len(unique_names))
with metric3:
    st.metric("🗓️ Latest activity", "Today" if latest_history else "—")

if latest_history:
    latest = latest_history[0]
    latest_name = extract_activity_name(str(latest.get("activity", ""))) or "Completed activity"
    st.markdown("### 🌱 Latest completed activity")
    with st.container(border=True):
        st.markdown(f"#### {latest_name}")
        info1, info2 = st.columns(2)
        with info1:
            st.caption(f"⏱️ Time: {latest.get('time', 'N/A')}")
        with info2:
            st.caption(f"📍 Location: {latest.get('location', 'N/A')}")
        latest_interests = latest.get("interests", [])
        if isinstance(latest_interests, list):
            latest_interests = ", ".join(latest_interests)
        st.write(f"**Interests:** {latest_interests or 'N/A'}")
        with st.expander("View latest activity details"):
            st.markdown(str(latest.get("activity", "")).strip())

    st.markdown("### 📖 Previous activities")
    if len(latest_history) > 1:
        for number, item in enumerate(latest_history[1:], start=1):
            activity_text = str(item.get("activity", "")).strip()
            activity_name = extract_activity_name(activity_text) or "Completed activity"
            with st.expander(f"{number}. {activity_name}"):
                st.write("**Available time:**", item.get("time", "N/A"))
                interests_value = item.get("interests", [])
                if isinstance(interests_value, list):
                    interests_value = ", ".join(interests_value)
                st.write("**Interests:**", interests_value or "N/A")
                st.write("**Location:**", item.get("location", "N/A"))
                st.markdown(activity_text)
    else:
        st.caption("Your previous activities will appear here after you complete more activities.")
else:
    st.info("No completed activities yet. Generate an activity and mark it as completed to start building your history.")

st.divider()
st.markdown(
    '<div style="text-align:center;color:#668571;font-size:.86rem;padding:.5rem 0 1rem;">Made with 💚 and local AI · Take a break, step outside, and explore.</div>',
    unsafe_allow_html=True,
)
