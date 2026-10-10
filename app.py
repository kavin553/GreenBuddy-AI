
import json
import re
from pathlib import Path

import requests
import streamlit as st


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="GreenBuddy AI",
    page_icon="🌱",
    layout="centered",
)


st.title("🌱 GreenBuddy AI")

st.markdown(
    """
    ### Your personal outdoor activity companion

    Discover simple activities that fit your interests,
    free time, and available location.

    **Less scrolling. More exploring. More living.** 🌿
    """
)

st.caption("Powered by local AI · Your activity history stays on your device")
st.divider()



# ---------------- LOCAL HISTORY ----------------
HISTORY_FILE = Path(__file__).parent / "activity_history.json"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:3b"
MAX_ATTEMPTS = 3


def load_history():
    if HISTORY_FILE.exists():
        try:
            data = json.loads(
                HISTORY_FILE.read_text(encoding="utf-8")
            )
            if isinstance(data, list):
                return [
                    item for item in data
                    if isinstance(item, dict)
                ]
        except (json.JSONDecodeError, OSError):
            pass

    return []


def save_history(history):
    HISTORY_FILE.write_text(
        json.dumps(history, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def extract_activity_name(text):
    """Extract the activity name from an AI response."""
    match = re.search(
        r"Activity\s*Name\s*:\s*\**([^\n*]+)",
        text,
        flags=re.IGNORECASE,
    )

    if match:
        return match.group(1).strip(" *:-")

    # Fallback: use the first non-empty line.
    for line in text.splitlines():
        line = line.strip().strip("*# ")
        if line:
            return line[:100]

    return ""


def extract_duration_line(text):
    """Find the approximate duration line."""
    match = re.search(
        r"(?:approximate\s+)?duration\s*:\s*([^\n]+)",
        text,
        flags=re.IGNORECASE,
    )

    return match.group(1).strip() if match else ""


def duration_fits(text, available_time):
    """
    Best-effort duration check.
    Returns True when the reported duration appears to fit.
    """
    duration_line = extract_duration_line(text)

    # Ask the model to retry if it omitted the duration.
    if not duration_line:
        return False

    matches = re.findall(
        r"(\d+(?:\.\d+)?)\s*(minutes?|mins?|hours?|hrs?)",
        duration_line,
        flags=re.IGNORECASE,
    )

    if not matches:
        return False

    reported_minutes = []

    for number, unit in matches:
        value = float(number)

        if unit.lower().startswith(("hour", "hr")):
            reported_minutes.append(value * 60)
        else:
            reported_minutes.append(value)

    # For a range such as "30-45 minutes", check the upper value.
    duration_minutes = max(reported_minutes)

    limits = {
        "15 minutes": 15,
        "30 minutes": 30,
        "1 hour": 60,
    }

    if available_time == "2+ hours":
        return duration_minutes >= 120

    limit = limits.get(available_time)

    if limit is None:
        return False

    return duration_minutes <= limit


def get_recent_activity_names(history, limit=10):
    """Return recent activity names, newest first."""
    names = []

    for item in reversed(history):
        activity_text = str(item.get("activity", "")).strip()

        if not activity_text:
            continue

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


# ---------------- ACTIVITY PLANNER ----------------
with st.form("activity_form"):
    available_time = st.selectbox(
        "How much free time do you have?",
        ["15 minutes", "30 minutes", "1 hour", "2+ hours"],
    )

    interests = st.multiselect(
        "What do you enjoy?",
        [
            "Nature",
            "Walking",
            "Gardening",
            "Birdwatching",
            "Photography",
        ],
    )

    location = st.selectbox(
        "Where can you go?",
        [
            "Garden or park",
            "Neighbourhood",
            "Outdoor trail",
            "At home",
        ],
    )

    submitted = st.form_submit_button(
        "🌿 Plan My Outdoor Activity"
    )


# ---------------- GENERATE ACTIVITY ----------------
if submitted:
    # Remove the previous suggestion while generating a new one.
    st.session_state.current_activity = None
    st.session_state.current_details = None

    if not interests:
        st.warning("Please select at least one interest.")

    else:
        recent_names = get_recent_activity_names(
            st.session_state.history,
            limit=10,
        )

        history_context = (
            "\n".join(f"- {name}" for name in recent_names)
            if recent_names
            else "No activities completed yet."
        )

        rejected_suggestions = []

        base_prompt = f"""
You are GreenBuddy, an AI assistant that helps people
spend less time on screens and enjoy safe outdoor activities.

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
- Avoid activities that are substantially similar to the recent activities.
- Choose a different activity type where practical.
- Do not simply rename a previously completed activity.

PERSONALISATION
- Match the selected interests and location.
- If the location is At home, suggest an activity suitable for home.
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

Keep the response friendly, practical, and concise.
Return only the activity plan.
"""

        accepted_activity = None
        last_error = None

        with st.spinner("GreenBuddy is planning your activity..."):
            for attempt in range(MAX_ATTEMPTS):
                retry_context = ""

                if rejected_suggestions:
                    retry_context = f"""

IMPORTANT: Your previous suggestion was rejected.
Do not suggest any of these rejected activities:
{chr(10).join("- " + name for name in rejected_suggestions)}

Generate a different activity that follows every rule.
"""

                prompt = base_prompt + retry_context

                try:
                    response = requests.post(
                        OLLAMA_URL,
                        json={
                            "model": MODEL_NAME,
                            "prompt": prompt,
                            "stream": False,
                        },
                        timeout=180,
                    )

                    response.raise_for_status()
                    response_data = response.json()

                    activity = str(
                        response_data.get("response", "")
                    ).strip()

                    if not activity:
                        last_error = "The AI returned an empty response."
                        continue

                    activity_name = extract_activity_name(activity)

                    if not activity_name:
                        last_error = "Could not identify the activity name."
                        continue

                    previous_names = {
                        name.casefold()
                        for name in recent_names
                    }

                    # Reject an exact repeat of a recent activity name.
                    if activity_name.casefold() in previous_names:
                        rejected_suggestions.append(activity_name)
                        last_error = "The AI repeated a recent activity."
                        continue

                    # Check the duration reported by the AI.
                    if not duration_fits(activity, available_time):
                        rejected_suggestions.append(activity_name)
                        last_error = (
                            "The activity duration was missing "
                            "or did not match the selected time."
                        )
                        continue

                    accepted_activity = activity
                    break

                except requests.exceptions.ConnectionError:
                    last_error = (
                        "Cannot connect to Ollama. "
                        "Make sure Ollama is running."
                    )
                    break

                except requests.exceptions.Timeout:
                    last_error = (
                        "The AI took too long to respond. Please try again."
                    )
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
            st.warning(
                "GreenBuddy could not create a suitable new activity "
                "after a few attempts. Please try again."
            )

            if last_error:
                st.caption(f"Reason: {last_error}")


# ---------------- DISPLAY ACTIVITY ----------------
if st.session_state.current_activity:
    st.divider()
    st.subheader("🌿 Your Personalised Activity Plan")
    st.markdown(st.session_state.current_activity)

    if st.button("✅ Mark Activity as Completed"):
        details = st.session_state.current_details

        if not details:
            st.error("Activity details are missing. Generate a new plan.")
        else:
            entry = {
                **details,
                "activity": st.session_state.current_activity,
            }

            updated_history = [
                *st.session_state.history,
                entry,
            ]

            try:
                save_history(updated_history)

                st.session_state.history = updated_history
                st.session_state.current_activity = None
                st.session_state.current_details = None

                st.success("Activity saved to your local history!")
                st.rerun()

            except OSError:
                st.error(
                    "Could not save history. Check folder permissions."
                )



# ---------------- ACTIVITY HISTORY ----------------
st.divider()
st.subheader("📚 Your Activity Memory")
st.caption("Your completed activities, saved locally on this device.")

history = st.session_state.history

valid_history = [
    item for item in history
    if isinstance(item, dict)
    and str(item.get("activity", "")).strip()
]

# Summary metrics
total_completed = len(valid_history)

st.metric("🌿 Activities completed", total_completed)

if valid_history:
    # Newest activity first
    latest_history = list(reversed(valid_history))

    # Highlight the most recently completed activity
    latest = latest_history[0]
    latest_name = extract_activity_name(
        str(latest.get("activity", ""))
    )

    st.markdown("### 🌱 Latest completed activity")

    with st.container(border=True):
        st.markdown(f"**{latest_name or 'Completed activity'}**")
        st.caption(
            f"Time: {latest.get('time', 'N/A')} · "
            f"Location: {latest.get('location', 'N/A')}"
        )

        latest_interests = latest.get("interests", [])
        if isinstance(latest_interests, list):
            latest_interests = ", ".join(latest_interests)

        st.write("**Interests:**", latest_interests or "N/A")

        with st.expander("View activity details"):
            st.markdown(str(latest.get("activity", "")).strip())

    # Full activity history
    st.markdown("### 📖 Previous activities")

    for number, item in enumerate(latest_history, start=1):
        activity_text = str(item.get("activity", "")).strip()
        activity_name = extract_activity_name(activity_text)

        # Avoid showing the latest activity twice
        if number == 1:
            continue

        with st.expander(
            f"{number - 1}. {activity_name or 'Completed activity'}"
        ):
            st.write("**Available time:**", item.get("time", "N/A"))

            interests_value = item.get("interests", [])
            if isinstance(interests_value, list):
                interests_value = ", ".join(interests_value)

            st.write("**Interests:**", interests_value or "N/A")
            st.write("**Location:**", item.get("location", "N/A"))
            st.markdown(activity_text)

else:
    st.info(
        "No completed activities yet. Generate an activity "
        "and mark it as completed to start building your history."
    )
