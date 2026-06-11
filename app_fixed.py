import streamlit as st
from google import genai
import json
import requests
from bs4 import BeautifulSoup
import re
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", None)

if not API_KEY:
    st.error("Missing GEMINI_API_KEY. Add it in .env locally or Streamlit Secrets online.")
    st.stop()

client = genai.Client(api_key=API_KEY)

st.set_page_config(page_title="Cosmos Lens", page_icon="🔭", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 20% 20%, rgba(59,130,246,0.22), transparent 30%),
        radial-gradient(circle at 80% 10%, rgba(168,85,247,0.18), transparent 30%),
        radial-gradient(circle at 50% 90%, rgba(14,165,233,0.16), transparent 35%),
        #020617;
    color: white;
}

/* FORCE READABILITY */
label, p, span, div, h1, h2, h3, h4, h5, h6 {
    color: #ffffff !important;
}

.stCheckbox label,
.stRadio label,
.stMultiSelect label,
.stTextInput label,
.stTextArea label,
.stSelectSlider label {
    color: #ffffff !important;
    opacity: 1 !important;
}

[data-testid="stMarkdownContainer"] {
    color: #ffffff !important;
}

.hero {
    min-height: 72vh;
    padding: 4rem;
    border-radius: 36px;
    background:
        linear-gradient(135deg, rgba(15,23,42,0.65), rgba(30,64,175,0.35)),
        url("https://images-assets.nasa.gov/image/PIA22313/PIA22313~large.jpg");
    background-size: cover;
    background-position: center;
    border: 1px solid rgba(255,255,255,0.22);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    box-shadow: 0 20px 80px rgba(0,0,0,0.45);
}

.hero h1 {
    font-size: clamp(2.4rem, 8vw, 5rem);
    font-weight: 800;
    margin-bottom: 0.5rem;
}

.hero h2 {
    font-size: clamp(1.3rem, 4vw, 2.1rem);
    margin-bottom: 1.5rem;
}

.hero p {
    font-size: 1.2rem;
    max-width: 850px;
    line-height: 1.7;
}

.mission-hero {
    padding: 2.5rem;
    border-radius: 30px;
    background: linear-gradient(135deg, rgba(99,102,241,0.45), rgba(14,165,233,0.25));
    border: 1px solid rgba(255,255,255,0.18);
    margin-bottom: 2rem;
}

.card {
    padding: 1.5rem;
    border-radius: 22px;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
    margin-bottom: 1.2rem;
    font-size: 1.05rem;
}

.child { border-left: 8px solid #22c55e; }
.student { border-left: 8px solid #3b82f6; }
.academic { border-left: 8px solid #a855f7; }
.visual { border-left: 8px solid #ec4899; }
.why { border-left: 8px solid #facc15; }
.teacher { border-left: 8px solid #f97316; }
.vocab { border-left: 8px solid #14b8a6; }
.timeline { border-left: 8px solid #38bdf8; }
.whatif { border-left: 8px solid #fb7185; }
.path { border-left: 8px solid #84cc16; }
.diagram { border-left: 8px solid #c084fc; }
.debate { border-left: 8px solid #f59e0b; }
.news { border-left: 8px solid #06b6d4; }
.career { border-left: 8px solid #10b981; }
.related { border-left: 8px solid #818cf8; }
.score { border-left: 8px solid #eab308; }

.badge {
    padding: 1.2rem;
    border-radius: 18px;
    background: linear-gradient(135deg, rgba(34,197,94,0.25), rgba(59,130,246,0.25));
    border: 1px solid rgba(255,255,255,0.2);
    font-size: 1.3rem;
    font-weight: bold;
}


/* BUTTON + WIDGET FIXES */
.stButton > button {
    background: linear-gradient(135deg, #2563eb, #7c3aed) !important;
    color: #ffffff !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    padding: 0.6rem 1rem !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
    color: #ffffff !important;
    border-color: rgba(255,255,255,0.45) !important;
}

.stButton > button:focus {
    color: #ffffff !important;
    border-color: #93c5fd !important;
    box-shadow: 0 0 0 0.2rem rgba(59,130,246,0.35) !important;
}

/* Text inside normal Streamlit buttons */
.stButton > button p {
    color: #ffffff !important;
}

/* Checkboxes */
[data-testid="stCheckbox"] label,
[data-testid="stCheckbox"] span,
[data-testid="stCheckbox"] p {
    color: #ffffff !important;
}

/* Radio buttons */
[data-testid="stRadio"] label,
[data-testid="stRadio"] span,
[data-testid="stRadio"] p {
    color: #ffffff !important;
}

/* Multiselect */
[data-baseweb="select"] {
    color: #ffffff !important;
}

[data-baseweb="tag"] {
    background-color: #2563eb !important;
    color: #ffffff !important;
}

[data-baseweb="tag"] span {
    color: #ffffff !important;
}

/* Input fields */
.stTextInput input,
.stTextArea textarea {
    color: #ffffff !important;
    background-color: rgba(15,23,42,0.85) !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #cbd5e1 !important;
}

/* Slider labels/ticks */
[data-testid="stSlider"] label,
[data-testid="stSlider"] span,
[data-testid="stSlider"] p {
    color: #ffffff !important;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 16px;
    padding: 1rem;
}

/* MOBILE FIXES */
@media (max-width: 768px) {
    .hero {
        min-height: auto !important;
        padding: 2rem 1rem !important;
        border-radius: 24px !important;
    }

    .hero h1 {
        font-size: 2.4rem !important;
    }

    .hero h2 {
        font-size: 1.25rem !important;
    }

    .hero p {
        font-size: 0.95rem !important;
    }

    .mission-hero {
        padding: 1.4rem !important;
        border-radius: 22px !important;
    }

    .card {
        padding: 1rem !important;
        font-size: 0.95rem !important;
    }

    img {
        width: 100% !important;
        height: auto !important;
    }
}
</style>
""", unsafe_allow_html=True)

defaults = {
    "entered": False,
    "article": "",
    "result": None,
    "follow_answer": "",
    "fetched_text": ""
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def strip_markdown(text):
    if not isinstance(text, str):
        return ""
    return text.replace("**", "").replace("__", "").replace("*", "")


def html_text(text):
    return strip_markdown(text).replace("\n", "<br>")


def clean_json(text):
    text = text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "").replace("```", "").strip()
    elif text.startswith("```"):
        text = text.replace("```", "").strip()

    first = text.find("{")
    last = text.rfind("}")

    if first != -1 and last != -1:
        text = text[first:last + 1]

    return text


def fetch_url_text(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        paragraphs = soup.find_all(["p", "h1", "h2", "h3"])
        text = " ".join([p.get_text(" ", strip=True) for p in paragraphs])
        text = re.sub(r"\s+", " ", text)

        return text[:3500]

    except Exception:
        return ""


def render_card(title, content, style):
    st.markdown(
        f"""
<div class="card {style}">
<h3>{title}</h3>
<p>{html_text(content)}</p>
</div>
""",
        unsafe_allow_html=True
    )


if not st.session_state.entered:
    st.markdown("""
    <div class="hero">
        <h1>🔭 Cosmos Lens</h1>
        <h2>One Discovery. Infinite Perspectives.</h2>
        <p>
        Turn NASA and JWST discoveries into adaptive explanations,
        vocabulary cards, timelines, diagrams, debates, quizzes,
        career pathways, and guided learning journeys.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🔭 Explore the Universe Through JWST")

    g1, g2, g3 = st.columns(3)

    with g1:
        st.image(
            "https://images-assets.nasa.gov/image/PIA25681/PIA25681~medium.jpg",
            caption="Carina Nebula | NASA",
            use_container_width=True
        )

    with g2:
        st.image(
            "https://images-assets.nasa.gov/image/PIA25696/PIA25696~medium.jpg",
            caption="Stephan's Quintet | NASA",
            use_container_width=True
        )

    with g3:
        st.image(
            "https://images-assets.nasa.gov/image/PIA25697/PIA25697~medium.jpg",
            caption="SMACS 0723 Deep Field | NASA",
            use_container_width=True
        )

    st.markdown("### 🎥 Watch: James Webb Space Telescope")
    st.video("https://www.youtube.com/watch?v=7nT7JGZMbtM")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Learning Modes", "6+")
    c2.metric("Mission Quiz", "Interactive")
    c3.metric("NASA Links", "Supported")
    c4.metric("AI Tutor", "Built-in")

    if st.button("🚀 Launch Mission Control"):
        st.session_state.entered = True
        st.rerun()

    st.stop()


examples = {
    "🪐 WASP-39 b": "The James Webb Space Telescope detected carbon dioxide in the atmosphere of WASP-39 b, a giant exoplanet about 700 light-years from Earth. Scientists studied starlight passing through the planet's atmosphere and found chemical fingerprints of carbon dioxide.",
    "🌌 Early Galaxies": "The James Webb Space Telescope observed some of the earliest galaxies ever seen, allowing scientists to study light that traveled for more than 13 billion years. These observations help researchers understand how galaxies formed soon after the Big Bang.",
    "⭐ TRAPPIST-1": "The James Webb Space Telescope is studying planets in the TRAPPIST-1 system to understand their atmospheres and whether rocky planets around small stars could have conditions suitable for life."
}

st.markdown("""
<div class="mission-hero">
<h1>🚀 Mission Control</h1>
<h3>Decode NASA discoveries for every learner.</h3>
</div>
""", unsafe_allow_html=True)

st.markdown("### Quick Start Examples")
cols = st.columns(3)

for i, (name, text) in enumerate(examples.items()):
    if cols[i].button(name):
        st.session_state.article = text
        st.session_state.result = None
        st.session_state.fetched_text = ""
        st.rerun()

left, right = st.columns([1.2, 1])

with left:
    link = st.text_input(
        "Paste a NASA/JWST article link:",
        placeholder="https://www.nasa.gov/..."
    )

    fetch_link = st.button("🔗 Fetch Link Text")

    if fetch_link:
        if not link.strip():
            st.warning("Paste a link first.")
        else:
            with st.spinner("Fetching article text..."):
                fetched = fetch_url_text(link.strip())

            if fetched:
                st.session_state.fetched_text = fetched
                st.session_state.article = fetched[:2500]
                st.success("Article text fetched successfully.")
                st.rerun()
            else:
                st.error("Could not fetch readable text from this link. Paste the article manually.")

    article = st.text_area(
        "Or paste the discovery text here:",
        height=230,
        value=st.session_state.article
    )

    reading_level = st.select_slider(
        "Choose reading level:",
        options=["Age 8", "Age 12", "High School", "College", "Expert"],
        value="High School"
    )

    selected_modes = st.multiselect(
        "Choose up to 3 explanation modes:",
        [
            "Child Explorer",
            "Student Explanation",
            "Academic Mode",
            "Visual Analogy",
            "Why It Matters",
            "Teacher Mode"
        ],
        default=["Student Explanation", "Visual Analogy", "Why It Matters"],
        max_selections=3
    )

    st.markdown("### Mission Add-ons")
    generate_quiz = st.checkbox("Interactive MCQ quiz", value=True)
    generate_vocab = st.checkbox("Vocabulary constellation", value=True)
    generate_timeline = st.checkbox("Discovery timeline", value=True)
    generate_whatif = st.checkbox("What If? scenario", value=False)
    generate_diagram = st.checkbox("Visual diagram", value=True)
    generate_path = st.checkbox("Learning path", value=False)
    generate_debate = st.checkbox("Scientist debate", value=False)
    generate_newsroom = st.checkbox("Newsroom mode", value=False)
    generate_difficulty = st.checkbox("Difficulty meter", value=False)
    generate_related = st.checkbox("Related discoveries", value=False)
    generate_career = st.checkbox("Career explorer", value=False)

    translate = st.button("✨ Launch Translation Mission")

with right:
    st.image(
        "https://images-assets.nasa.gov/image/GSFC_20171208_Archive_e001518/GSFC_20171208_Archive_e001518~medium.jpg",
        caption="James Webb Space Telescope | NASA",
        use_container_width=True
    )

mode_styles = {
    "Child Explorer": ("👦 Child Explorer", "child"),
    "Student Explanation": ("🎓 Student Explanation", "student"),
    "Academic Mode": ("📚 Academic Mode", "academic"),
    "Visual Analogy": ("🎨 Visual Analogy", "visual"),
    "Why It Matters": ("🌍 Why It Matters", "why"),
    "Teacher Mode": ("🧑‍🏫 Teacher Mode", "teacher"),
}

if translate:
    content = article.strip()

    if link.strip():
        content += f"\n\nReference link: {link.strip()}"

    advanced_features = [
        generate_quiz,
        generate_vocab,
        generate_timeline,
        generate_whatif,
        generate_diagram,
        generate_path,
        generate_debate,
        generate_newsroom,
        generate_difficulty,
        generate_related,
        generate_career
    ]

    if sum(advanced_features) > 5:
        st.warning("Choose up to 5 mission add-ons at once to avoid overloading Gemini.")
        st.stop()

    if not content:
        st.error("Paste a discovery, fetch a link, or choose an example first.")
        st.stop()

    if not selected_modes:
        st.error("Choose at least one explanation mode.")
        st.stop()

    prompt = f"""
You are Cosmos Lens, an award-level NASA/JWST educational AI platform.

Reading level: {reading_level}

Discovery:
{content[:2500]}

Selected explanation modes:
{selected_modes}

Return ONLY valid JSON. No markdown. No extra text.

Use this exact structure:

{{
  "modes": {{
    "Student Explanation": "text"
  }},
  "vocabulary": [
    {{"term": "term", "definition": "definition"}}
  ],
  "quiz": [
    {{
      "question": "question",
      "options": {{"A": "option A", "B": "option B", "C": "option C", "D": "option D"}},
      "answer": "A",
      "explanation": "why answer is correct"
    }}
  ],
  "timeline": [
    {{"event": "short event", "description": "short description"}}
  ],
  "what_if": "scientifically grounded scenario",
  "diagram_steps": ["step 1", "step 2", "step 3"],
  "learning_path": ["topic 1", "topic 2", "topic 3"],
  "debate": {{
    "optimist_view": "text",
    "skeptical_view": "text"
  }},
  "newsroom": {{
    "headline": "text",
    "press_release": "text",
    "social_post": "text"
  }},
  "difficulty": {{
    "score": "number from 1 to 10",
    "reason": "why",
    "required_knowledge": ["concept 1", "concept 2"]
  }},
  "related_discoveries": ["related discovery 1", "related discovery 2", "related discovery 3"],
  "careers": [
    {{"career": "career name", "why_it_connects": "short explanation"}}
  ]
}}

Rules:
- Only include selected modes inside modes.
- Match quiz difficulty to reading level.
- If vocabulary requested = {generate_vocab}, create 5 useful terms, otherwise [].
- If quiz requested = {generate_quiz}, create 5 MCQs, otherwise [].
- If timeline requested = {generate_timeline}, create 4 items, otherwise [].
- If what-if requested = {generate_whatif}, create one, otherwise "".
- If diagram requested = {generate_diagram}, create 4 short diagram steps, otherwise [].
- If learning path requested = {generate_path}, create 4 next topics, otherwise [].
- If debate requested = {generate_debate}, create balanced optimist and skeptical views, otherwise empty strings.
- If newsroom requested = {generate_newsroom}, create headline, press release, social post, otherwise empty strings.
- If difficulty requested = {generate_difficulty}, create score/reason/required knowledge, otherwise empty fields.
- If related requested = {generate_related}, create related discovery names, otherwise [].
- If career requested = {generate_career}, create 3 careers, otherwise [].
- Do not use markdown bold symbols like **.
- Keep output concise.
"""

    try:
        with st.spinner("Mission Control is processing..."):
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

        raw_output = clean_json(response.text)
        st.session_state.result = json.loads(raw_output)

    except Exception as e:
        st.warning("🚀 Gemini is busy or quota-limited. Try fewer add-ons or try again shortly.")
        st.stop()

result = st.session_state.result

if result:
    st.markdown("## 🌌 Your Translated Discovery")

    for mode, content in result.get("modes", {}).items():
        title, style = mode_styles.get(mode, (mode, "student"))
        render_card(title, content, style)

    difficulty = result.get("difficulty", {})
    if difficulty and difficulty.get("score"):
        knowledge = ", ".join(difficulty.get("required_knowledge", []))
        render_card(
            "📊 Discovery Difficulty Meter",
            f"Complexity Score: {difficulty.get('score')}/10\n\nReason: {difficulty.get('reason', '')}\n\nRequired Knowledge: {knowledge}",
            "score"
        )

    vocab = result.get("vocabulary", [])
    if vocab:
        st.markdown("## 🧠 Vocabulary Constellation")
        vocab_cols = st.columns(2)
        for i, item in enumerate(vocab):
            with vocab_cols[i % 2]:
                render_card(item.get("term", "Term"), item.get("definition", ""), "vocab")

    debate = result.get("debate", {})
    if debate and (debate.get("optimist_view") or debate.get("skeptical_view")):
        st.markdown("## ⚖️ Scientist Debate")
        d1, d2 = st.columns(2)
        with d1:
            render_card("Optimist View", debate.get("optimist_view", ""), "debate")
        with d2:
            render_card("Skeptical View", debate.get("skeptical_view", ""), "debate")

    newsroom = result.get("newsroom", {})
    if newsroom and any(newsroom.values()):
        st.markdown("## 📰 Discovery Newsroom")
        render_card("Headline", newsroom.get("headline", ""), "news")
        render_card("Press Release", newsroom.get("press_release", ""), "news")
        render_card("Social Post", newsroom.get("social_post", ""), "news")

    timeline = result.get("timeline", [])
    if timeline:
        st.markdown("## 🕰️ Discovery Timeline")
        for item in timeline:
            render_card(item.get("event", "Event"), item.get("description", ""), "timeline")

    diagram = result.get("diagram_steps", [])
    if diagram:
        st.markdown("## 🧩 Visual Diagram")
        render_card("Discovery Flow", " ➜ ".join(diagram), "diagram")

    what_if = result.get("what_if", "")
    if what_if:
        st.markdown("## 🤔 What If?")
        render_card("Scenario", what_if, "whatif")

    path = result.get("learning_path", [])
    if path:
        st.markdown("## 🧭 Suggested Learning Path")
        for topic in path:
            render_card("Next Step", f"➡️ {topic}", "path")

    related = result.get("related_discoveries", [])
    if related:
        st.markdown("## 🔗 Related Discoveries")
        for item in related:
            render_card("Explore Next", item, "related")

    careers = result.get("careers", [])
    if careers:
        st.markdown("## 🧑‍🚀 Career Explorer")
        for c in careers:
            render_card(c.get("career", "Career"), c.get("why_it_connects", ""), "career")

    quiz = result.get("quiz", [])
    if quiz:
        st.markdown("## 📝 Mission Quiz")

        user_answers = {}

        for i, q in enumerate(quiz):
            st.markdown(f"### Question {i + 1}")
            st.write(strip_markdown(q.get("question", "")))

            options = q.get("options", {})
            formatted_options = [
                f"A) {strip_markdown(options.get('A', ''))}",
                f"B) {strip_markdown(options.get('B', ''))}",
                f"C) {strip_markdown(options.get('C', ''))}",
                f"D) {strip_markdown(options.get('D', ''))}"
            ]

            user_answers[i] = st.radio(
                "Choose your answer:",
                formatted_options,
                index=None,
                key=f"quiz_{i}"
            )

        if st.button("✅ Check Answers"):
            score = 0

            for i, q in enumerate(quiz):
                correct = q.get("answer", "").strip().upper()

                if user_answers[i] is None:
                    st.warning(f"Question {i + 1}: Not answered.")
                    continue

                chosen = user_answers[i][0]

                if chosen == correct:
                    score += 1
                    st.success(f"Question {i + 1}: Correct ✅")
                else:
                    st.error(f"Question {i + 1}: Incorrect ❌ Correct answer: {correct}")

                st.info(strip_markdown(q.get("explanation", "")))

            st.markdown(f"## Final Score: {score}/{len(quiz)}")

            if score == len(quiz):
                st.balloons()
                st.markdown('<div class="badge">🌟 JWST Scientist Level!</div>', unsafe_allow_html=True)
            elif score >= len(quiz) * 0.7:
                st.markdown('<div class="badge">🚀 Mission Specialist Level!</div>', unsafe_allow_html=True)
            elif score >= len(quiz) * 0.4:
                st.markdown('<div class="badge">🛰 NASA Cadet Level!</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="badge">🔭 Keep Exploring Level!</div>', unsafe_allow_html=True)

    st.markdown("## 💬 Ask a Follow-Up Question")

    follow_question = st.text_input(
        "Ask something about this discovery:",
        placeholder="Example: How does JWST detect gases?"
    )

    if st.button("Ask Cosmos Tutor") and follow_question.strip():
        follow_prompt = f"""
You are Cosmos Tutor.

Original discovery:
{article[:1200]}

Student question:
{follow_question}

Answer clearly at this reading level: High School.
Do not use markdown bold symbols.
Keep it focused on this discovery.
"""

        try:
            with st.spinner("Cosmos Tutor is thinking..."):
                follow_response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=follow_prompt
                )

            st.session_state.follow_answer = strip_markdown(follow_response.text)

        except Exception:
            st.error("Cosmos Tutor is busy. Try again in a moment.")

    if st.session_state.follow_answer:
        render_card("🔭 Cosmos Tutor", st.session_state.follow_answer, "student")