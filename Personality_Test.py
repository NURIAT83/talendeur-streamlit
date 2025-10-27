#Personality Test

#Library Imports
import streamlit as st
import json
import sqlite3
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from io import BytesIO
import base64
from pathlib import Path
#Dashboard Title

st.set_page_config(page_title="Candidate's Profile", layout="wide")


#Questions 
BIG_FIVE_120_QUESTIONS = [
    # EXTRAVERSION - Friendliness/Warmth (4 questions)
    {"text": "I make friends easily", "trait": "extraversion", "facet": "friendliness", "reverse": False},
    {"text": "I warm up quickly to others", "trait": "extraversion", "facet": "friendliness", "reverse": False},
    {"text": "I keep others at a distance", "trait": "extraversion", "facet": "friendliness", "reverse": True},
    {"text": "I avoid contacts with others", "trait": "extraversion", "facet": "friendliness", "reverse": True},
    
    # EXTRAVERSION - Gregariousness (4 questions)
    {"text": "I love large parties", "trait": "extraversion", "facet": "gregariousness", "reverse": False},
    {"text": "I talk to a lot of different people at parties", "trait": "extraversion", "facet": "gregariousness", "reverse": False},
    {"text": "I prefer to be alone", "trait": "extraversion", "facet": "gregariousness", "reverse": True},
    {"text": "I avoid crowds", "trait": "extraversion", "facet": "gregariousness", "reverse": True},
    
    # EXTRAVERSION - Assertiveness (4 questions)
    {"text": "I take charge", "trait": "extraversion", "facet": "assertiveness", "reverse": False},
    {"text": "I am the first to act", "trait": "extraversion", "facet": "assertiveness", "reverse": False},
    {"text": "I wait for others to lead the way", "trait": "extraversion", "facet": "assertiveness", "reverse": True},
    {"text": "I hold back my opinions", "trait": "extraversion", "facet": "assertiveness", "reverse": True},
    
    # EXTRAVERSION - Activity Level (4 questions)
    {"text": "I am always busy", "trait": "extraversion", "facet": "activity_level", "reverse": False},
    {"text": "I am always on the go", "trait": "extraversion", "facet": "activity_level", "reverse": False},
    {"text": "I like to take it easy", "trait": "extraversion", "facet": "activity_level", "reverse": True},
    {"text": "I do a lot in my spare time", "trait": "extraversion", "facet": "activity_level", "reverse": False},
    
    # EXTRAVERSION - Excitement-Seeking (4 questions)
    {"text": "I love excitement", "trait": "extraversion", "facet": "excitement_seeking", "reverse": False},
    {"text": "I seek adventure", "trait": "extraversion", "facet": "excitement_seeking", "reverse": False},
    {"text": "I dislike loud music", "trait": "extraversion", "facet": "excitement_seeking", "reverse": True},
    {"text": "I prefer quiet to loud", "trait": "extraversion", "facet": "excitement_seeking", "reverse": True},
    
    # EXTRAVERSION - Cheerfulness (4 questions)
    {"text": "I radiate joy", "trait": "extraversion", "facet": "cheerfulness", "reverse": False},
    {"text": "I have a lot of fun", "trait": "extraversion", "facet": "cheerfulness", "reverse": False},
    {"text": "I seldom joke around", "trait": "extraversion", "facet": "cheerfulness", "reverse": True},
    {"text": "I laugh a lot", "trait": "extraversion", "facet": "cheerfulness", "reverse": False},
    
    # AGREEABLENESS - Trust (4 questions)
    {"text": "I trust others", "trait": "agreeableness", "facet": "trust", "reverse": False},
    {"text": "I believe that others have good intentions", "trait": "agreeableness", "facet": "trust", "reverse": False},
    {"text": "I distrust people", "trait": "agreeableness", "facet": "trust", "reverse": True},
    {"text": "I suspect hidden motives in others", "trait": "agreeableness", "facet": "trust", "reverse": True},
    
    # AGREEABLENESS - Morality (4 questions)
    {"text": "I use others for my own ends", "trait": "agreeableness", "facet": "morality", "reverse": True},
    {"text": "I cheat to get ahead", "trait": "agreeableness", "facet": "morality", "reverse": True},
    {"text": "I take advantage of others", "trait": "agreeableness", "facet": "morality", "reverse": True},
    {"text": "I stick to the rules", "trait": "agreeableness", "facet": "morality", "reverse": False},
    
    # AGREEABLENESS - Altruism (4 questions)
    {"text": "I love to help others", "trait": "agreeableness", "facet": "altruism", "reverse": False},
    {"text": "I am concerned about others", "trait": "agreeableness", "facet": "altruism", "reverse": False},
    {"text": "I am indifferent to the feelings of others", "trait": "agreeableness", "facet": "altruism", "reverse": True},
    {"text": "I value cooperation over competition", "trait": "agreeableness", "facet": "altruism", "reverse": False},
    
    # AGREEABLENESS - Cooperation (4 questions)
    {"text": "I love a good fight", "trait": "agreeableness", "facet": "cooperation", "reverse": True},
    {"text": "I yell at people", "trait": "agreeableness", "facet": "cooperation", "reverse": True},
    {"text": "I get angry easily", "trait": "agreeableness", "facet": "cooperation", "reverse": True},
    {"text": "I rarely lose my composure", "trait": "agreeableness", "facet": "cooperation", "reverse": False},
    
    # AGREEABLENESS - Modesty (4 questions)
    {"text": "I believe I am better than others", "trait": "agreeableness", "facet": "modesty", "reverse": True},
    {"text": "I think highly of myself", "trait": "agreeableness", "facet": "modesty", "reverse": True},
    {"text": "I boast about my virtues", "trait": "agreeableness", "facet": "modesty", "reverse": True},
    {"text": "I dislike talking about myself", "trait": "agreeableness", "facet": "modesty", "reverse": False},
    
    # AGREEABLENESS - Sympathy (4 questions)
    {"text": "I feel others' emotions", "trait": "agreeableness", "facet": "sympathy", "reverse": False},
    {"text": "I sympathize with the homeless", "trait": "agreeableness", "facet": "sympathy", "reverse": False},
    {"text": "I am not interested in other people's problems", "trait": "agreeableness", "facet": "sympathy", "reverse": True},
    {"text": "I try to understand others", "trait": "agreeableness", "facet": "sympathy", "reverse": False},
    
    # CONSCIENTIOUSNESS - Self-Efficacy (4 questions)
    {"text": "I complete tasks successfully", "trait": "conscientiousness", "facet": "self_efficacy", "reverse": False},
    {"text": "I am sure of my abilities", "trait": "conscientiousness", "facet": "self_efficacy", "reverse": False},
    {"text": "I have difficulty starting tasks", "trait": "conscientiousness", "facet": "self_efficacy", "reverse": True},
    {"text": "I misjudge situations", "trait": "conscientiousness", "facet": "self_efficacy", "reverse": True},
    
    # CONSCIENTIOUSNESS - Orderliness (4 questions)
    {"text": "I like order", "trait": "conscientiousness", "facet": "orderliness", "reverse": False},
    {"text": "I keep things tidy", "trait": "conscientiousness", "facet": "orderliness", "reverse": False},
    {"text": "I leave my belongings around", "trait": "conscientiousness", "facet": "orderliness", "reverse": True},
    {"text": "I make a mess of things", "trait": "conscientiousness", "facet": "orderliness", "reverse": True},
    
    # CONSCIENTIOUSNESS - Dutifulness (4 questions)
    {"text": "I keep my promises", "trait": "conscientiousness", "facet": "dutifulness", "reverse": False},
    {"text": "I tell the truth", "trait": "conscientiousness", "facet": "dutifulness", "reverse": False},
    {"text": "I break my promises", "trait": "conscientiousness", "facet": "dutifulness", "reverse": True},
    {"text": "I stick to my chosen path", "trait": "conscientiousness", "facet": "dutifulness", "reverse": False},
    
    # CONSCIENTIOUSNESS - Achievement-Striving (4 questions)
    {"text": "I work hard", "trait": "conscientiousness", "facet": "achievement_striving", "reverse": False},
    {"text": "I do more than what's expected of me", "trait": "conscientiousness", "facet": "achievement_striving", "reverse": False},
    {"text": "I do just enough work to get by", "trait": "conscientiousness", "facet": "achievement_striving", "reverse": True},
    {"text": "I set high standards for myself", "trait": "conscientiousness", "facet": "achievement_striving", "reverse": False},
    
    # CONSCIENTIOUSNESS - Self-Discipline (4 questions)
    {"text": "I get things done quickly", "trait": "conscientiousness", "facet": "self_discipline", "reverse": False},
    {"text": "I finish what I start", "trait": "conscientiousness", "facet": "self_discipline", "reverse": False},
    {"text": "I waste my time", "trait": "conscientiousness", "facet": "self_discipline", "reverse": True},
    {"text": "I find it difficult to get down to work", "trait": "conscientiousness", "facet": "self_discipline", "reverse": True},
    
    # CONSCIENTIOUSNESS - Cautiousness (4 questions)
    {"text": "I think before I act", "trait": "conscientiousness", "facet": "cautiousness", "reverse": False},
    {"text": "I consider the consequences", "trait": "conscientiousness", "facet": "cautiousness", "reverse": False},
    {"text": "I jump into things without thinking", "trait": "conscientiousness", "facet": "cautiousness", "reverse": True},
    {"text": "I act without thinking", "trait": "conscientiousness", "facet": "cautiousness", "reverse": True},
    
    # NEUROTICISM - Anxiety (4 questions)
    {"text": "I worry about things", "trait": "neuroticism", "facet": "anxiety", "reverse": False},
    {"text": "I fear for the worst", "trait": "neuroticism", "facet": "anxiety", "reverse": False},
    {"text": "I am relaxed most of the time", "trait": "neuroticism", "facet": "anxiety", "reverse": True},
    {"text": "I am afraid of many things", "trait": "neuroticism", "facet": "anxiety", "reverse": False},
    
    # NEUROTICISM - Anger (4 questions)
    {"text": "I get irritated easily", "trait": "neuroticism", "facet": "anger", "reverse": False},
    {"text": "I get angry easily", "trait": "neuroticism", "facet": "anger", "reverse": False},
    {"text": "I lose my temper", "trait": "neuroticism", "facet": "anger", "reverse": False},
    {"text": "I remain calm under pressure", "trait": "neuroticism", "facet": "anger", "reverse": True},
    
    # NEUROTICISM - Depression (4 questions)
    {"text": "I often feel blue", "trait": "neuroticism", "facet": "depression", "reverse": False},
    {"text": "I dislike myself", "trait": "neuroticism", "facet": "depression", "reverse": False},
    {"text": "I am usually happy", "trait": "neuroticism", "facet": "depression", "reverse": True},
    {"text": "I feel desperate", "trait": "neuroticism", "facet": "depression", "reverse": False},
    
    # NEUROTICISM - Self-Consciousness (4 questions)
    {"text": "I am afraid to draw attention to myself", "trait": "neuroticism", "facet": "self_consciousness", "reverse": False},
    {"text": "I am easily embarrassed", "trait": "neuroticism", "facet": "self_consciousness", "reverse": False},
    {"text": "I am not bothered by difficult social situations", "trait": "neuroticism", "facet": "self_consciousness", "reverse": True},
    {"text": "I feel comfortable with myself", "trait": "neuroticism", "facet": "self_consciousness", "reverse": True},
    
    # NEUROTICISM - Immoderation (4 questions)
    {"text": "I go on binges", "trait": "neuroticism", "facet": "immoderation", "reverse": False},
    {"text": "I do things I later regret", "trait": "neuroticism", "facet": "immoderation", "reverse": False},
    {"text": "I resist my impulses", "trait": "neuroticism", "facet": "immoderation", "reverse": True},
    {"text": "I never spend more than I can afford", "trait": "neuroticism", "facet": "immoderation", "reverse": True},
    
    # NEUROTICISM - Vulnerability (4 questions)
    {"text": "I panic easily", "trait": "neuroticism", "facet": "vulnerability", "reverse": False},
    {"text": "I feel that I am unable to deal with things", "trait": "neuroticism", "facet": "vulnerability", "reverse": False},
    {"text": "I can handle complex problems", "trait": "neuroticism", "facet": "vulnerability", "reverse": True},
    {"text": "I know how to cope", "trait": "neuroticism", "facet": "vulnerability", "reverse": True},
    
    # OPENNESS - Imagination (4 questions)
    {"text": "I have a vivid imagination", "trait": "openness", "facet": "imagination", "reverse": False},
    {"text": "I like to get lost in thought", "trait": "openness", "facet": "imagination", "reverse": False},
    {"text": "I have difficulty imagining things", "trait": "openness", "facet": "imagination", "reverse": True},
    {"text": "I seldom daydream", "trait": "openness", "facet": "imagination", "reverse": True},
    
    # OPENNESS - Artistic Interests (4 questions)
    {"text": "I see beauty in things that others might not notice", "trait": "openness", "facet": "artistic_interests", "reverse": False},
    {"text": "I believe in the importance of art", "trait": "openness", "facet": "artistic_interests", "reverse": False},
    {"text": "I do not like art", "trait": "openness", "facet": "artistic_interests", "reverse": True},
    {"text": "I love music", "trait": "openness", "facet": "artistic_interests", "reverse": False},
    
    # OPENNESS - Emotionality (4 questions)
    {"text": "I experience my emotions intensely", "trait": "openness", "facet": "emotionality", "reverse": False},
    {"text": "I feel others' emotions", "trait": "openness", "facet": "emotionality", "reverse": False},
    {"text": "I seldom get emotional", "trait": "openness", "facet": "emotionality", "reverse": True},
    {"text": "I am not easily affected by my emotions", "trait": "openness", "facet": "emotionality", "reverse": True},
    
    # OPENNESS - Adventurousness (4 questions)
    {"text": "I prefer variety to routine", "trait": "openness", "facet": "adventurousness", "reverse": False},
    {"text": "I love to try new things", "trait": "openness", "facet": "adventurousness", "reverse": False},
    {"text": "I dislike changes", "trait": "openness", "facet": "adventurousness", "reverse": True},
    {"text": "I prefer to stick with things that I know", "trait": "openness", "facet": "adventurousness", "reverse": True},
    
    # OPENNESS - Intellect (4 questions)
    {"text": "I love to read challenging material", "trait": "openness", "facet": "intellect", "reverse": False},
    {"text": "I am quick to understand things", "trait": "openness", "facet": "intellect", "reverse": False},
    {"text": "I have difficulty understanding abstract ideas", "trait": "openness", "facet": "intellect", "reverse": True},
    {"text": "I avoid philosophical discussions", "trait": "openness", "facet": "intellect", "reverse": True},
    
    # OPENNESS - Liberalism (4 questions)
    {"text": "I tend to vote for liberal political candidates", "trait": "openness", "facet": "liberalism", "reverse": False},
    {"text": "I believe that there is no absolute right or wrong", "trait": "openness", "facet": "liberalism", "reverse": False},
    {"text": "I believe in one true religion", "trait": "openness", "facet": "liberalism", "reverse": True},
    {"text": "I believe laws should be strictly enforced", "trait": "openness", "facet": "liberalism", "reverse": True},
]

# Facet names for reference
FACET_NAMES = {
    "extraversion": {
        "friendliness": "Friendliness",
        "gregariousness": "Gregariousness",
        "assertiveness": "Assertiveness",
        "activity_level": "Activity Level",
        "excitement_seeking": "Excitement-Seeking",
        "cheerfulness": "Cheerfulness"
    },
    "agreeableness": {
        "trust": "Trust",
        "morality": "Morality",
        "altruism": "Altruism",
        "cooperation": "Cooperation",
        "modesty": "Modesty",
        "sympathy": "Sympathy"
    },
    "conscientiousness": {
        "self_efficacy": "Self-Efficacy",
        "orderliness": "Orderliness",
        "dutifulness": "Dutifulness",
        "achievement_striving": "Achievement-Striving",
        "self_discipline": "Self-Discipline",
        "cautiousness": "Cautiousness"
    },
    "neuroticism": {
        "anxiety": "Anxiety",
        "anger": "Anger",
        "depression": "Depression",
        "self_consciousness": "Self-Consciousness",
        "immoderation": "Immoderation",
        "vulnerability": "Vulnerability"
    },
    "openness": {
        "imagination": "Imagination",
        "artistic_interests": "Artistic Interests",
        "emotionality": "Emotionality",
        "adventurousness": "Adventurousness",
        "intellect": "Intellect",
        "liberalism": "Liberalism"
    }
}

TRAIT_NAMES = {
    "extraversion": "Extraversion",
    "agreeableness": "Agreeableness", 
    "conscientiousness": "Conscientiousness",
    "neuroticism": "Neuroticism",
    "openness": "Openness"
}

# Assign a color to each trait for visualization
# Using colors with good contrast (high saturation and brightness)
TRAIT_COLORS = {
    "extraversion": "#0066CC",      # Strong blue
    "agreeableness": "#00B894",     # Mint green
    "conscientiousness": "#B8860B", # Dark goldenrod/deep mustard
    "neuroticism": "#D63031",       # Bright red
    "openness": "#6C5CE7"           # Lavender purple
}

#Convert hex to rgb
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return ','.join(str(int(hex_color[i:i+2], 16)) for i in (0, 2, 4))

###Create structure to save results of the session  on sqlite database

def initiate_db(db_path="test_results.db"):
    conn=sqlite3.connect(db_path)
    cursor=conn.cursor()

    #creates also an users table
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        registration_date TEXT,
        last_access TEXT
    )""")
    #save changes
    conn.commit()
    #closes connection
    conn.close()

# Create a function to check the user exists
def register_user(user_id, db_path="test_results.db"):
    #Connect to the database
    conn=sqlite3.connect(db_path)
    cursor=conn.cursor()
    #Get current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #Insert new user if not exists ( in users table)
    cursor.execute("""
        INSERT INTO users (user_id, registration_date, last_access)
        VALUES (?, ?, ?)
    """, (user_id, timestamp, timestamp))

    #save changes
    conn.commit()
    #closes connection
    conn.close()

#Function for returning users

def update_last_access(user_id, db_path="test_results.db"):
    conn=sqlite3.connect(db_path)
    cursor=conn.cursor()
    #Get current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #Update last access time
    cursor.execute("""
        UPDATE users
        SET last_access = ?
        WHERE user_id = ?
    """, (timestamp, user_id))

    #save changes
    conn.commit()
    #closes connection
    conn.close()



### Get user history
def get_user_history(user_id, db_path="test_results.db"):
    #check if path exists
    if not Path(db_path).exists():
        return None,None
    
    conn = sqlite3.connect(db_path)

    try:
        df_summary=pd.read_sql_query(
            "SELECT * FROM results_summary WHERE user_id = ? ORDER BY timestamp DESC",
            conn, params=(user_id,)
        )
        df_detailed = pd.read_sql_query(
            "SELECT * FROM results_detailed WHERE user_id = ? ORDER BY timestamp DESC",
            conn, params=(user_id,)
        )
    except:
        df_summary, df_detailed = None, None
    conn.close()
    return df_summary, df_detailed

#Function to check if user exists

def check_user_exists(user_id, db_path="test_results.db"):
    conn=sqlite3.connect(db_path)
    cursor=conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] > 0

def manage_user_session():
    # Initialize database
    initiate_db()
    
    # Check if there is a user in session
    if 'user_id' in st.session_state and st.session_state.user_id:
        # Update last access time for existing session
        update_last_access(st.session_state.user_id)
        return st.session_state.user_id
    
    st.title("Personality Test Access")
    tab1, tab2 = st.tabs(["Returning User", "New User"])

    with tab1:
        st.subheader("Welcome back!")
        login_id = st.text_input("Enter your user ID:", key="login_id")
        if st.button("Login", key="btn_login"):
            if login_id.strip():
                if check_user_exists(login_id.strip()):
                    st.session_state.user_id = login_id.strip()
                    update_last_access(login_id.strip())
                    st.success(f"Welcome back, {login_id}!")
                    st.rerun()
                else:
                    st.error("❌ This ID doesn't exist. Register in the 'New User' tab.")
            else:
                st.warning("⚠️ Please enter an ID")
    
    with tab2:
        st.subheader("Create your User ID")
        st.info("Please save your User ID for future access to your test results. You can use letters, numbers, hyphens and underscores.")
        new_id = st.text_input("Choose a User ID:", key="new_id")
        if st.button("Register", key="btn_register"):
            if new_id.strip():
                # Validate that it has only letters, numbers, hyphens and underscores
                if new_id.replace("_", "").replace("-", "").isalnum():
                    if not check_user_exists(new_id.strip()):
                        register_user(new_id.strip())
                        st.session_state.user_id = new_id.strip()
                        update_last_access(new_id.strip())
                        st.success(f"✅ Registration successful! Welcome, {new_id}!")
                        st.info(f"Remember your ID: **{new_id}** to access your results later")
                        st.rerun()
                    else:
                        st.error("❌ This ID already exists. Please choose a different one.")
                else:
                    st.error("❌ ID can only contain letters, numbers, hyphens and underscores")
            else:
                st.warning("⚠️ Please choose an ID")
    
    return None
    


#Configuration
questions_per_page = 12
total_questions = len(BIG_FIVE_120_QUESTIONS)
total_pages = total_questions // questions_per_page

#function to initiate session state
def init_session_state():
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 0
    if 'answers' not in st.session_state:
        st.session_state.answers = [None] * total_questions
    if 'test_completed' not in st.session_state:
        st.session_state.test_completed = False
    if 'big_five_scores' not in st.session_state:
        st.session_state.big_five_scores = None
    if 'facet_scores' not in st.session_state:
        st.session_state.facet_scores = None

def calculate_scores(answers):
    """Calculate trait and facet scores"""
    # Initialize scores
    trait_scores = {trait: 0 for trait in TRAIT_NAMES.keys()}
    trait_counts = {trait: 0 for trait in TRAIT_NAMES.keys()}
    
    facet_scores = {
        trait: {facet: 0 for facet in FACET_NAMES[trait].keys()}
        for trait in TRAIT_NAMES.keys()
    }
    facet_counts = {
        trait: {facet: 0 for facet in FACET_NAMES[trait].keys()}
        for trait in TRAIT_NAMES.keys()
    }
    
    # Calculate scores
    for i, question in enumerate(BIG_FIVE_120_QUESTIONS):
        if answers[i] is not None:
            score = answers[i]
            if question["reverse"]:
                score = 6 - score
            
            trait = question["trait"]
            facet = question["facet"]
            
            trait_scores[trait] += score
            trait_counts[trait] += 1
            
            facet_scores[trait][facet] += score
            facet_counts[trait][facet] += 1
    
    # Normalize to percentage (0-100)
    for trait in trait_scores:
        if trait_counts[trait] > 0:
            max_score = trait_counts[trait] * 5
            trait_scores[trait] = round((trait_scores[trait] / max_score) * 100)
    
    for trait in facet_scores:
        for facet in facet_scores[trait]:
            if facet_counts[trait][facet] > 0:
                max_score = facet_counts[trait][facet] * 5
                facet_scores[trait][facet] = round((facet_scores[trait][facet] / max_score) * 100)
    
    return trait_scores, facet_scores

def display_paginated_test():
    """Display the paginated personality test"""
   
    
    if not st.session_state.test_completed:
        st.header("Big Five Personality Assessment")
        st.title("Let's get to know you better!")
        st.info("this test takes approximately 10-15 minutes to complete.")
        # Calculate progress percentage
        answered = sum(1 for ans in st.session_state.answers if ans is not None)
        progress_pct = (answered / total_questions) * 100
        
        # Progress bar with percentage only
        st.progress(answered / total_questions)
        st.markdown(f"<h3 style='text-align: center;'>{int(progress_pct)}% Complete</h3>", unsafe_allow_html=True)
        st.markdown("---")
        
        # Get questions for current page
        start_idx = st.session_state.current_page * questions_per_page
        end_idx = min(start_idx + questions_per_page, total_questions)
        page_questions = BIG_FIVE_120_QUESTIONS[start_idx:end_idx]
        
        # Display questions
        for i, question in enumerate(page_questions):
            question_idx = start_idx + i
            
            st.markdown(f"**{question['text']}**")
            
            # Answer options
            options = ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]
            
            current_answer = st.session_state.answers[question_idx]
            default_index = current_answer - 1 if current_answer is not None else 2
            
            answer = st.radio(
                "Select your answer:",
                options=options,
                index=default_index,
                key=f"q_{question_idx}",
                horizontal=True,
                label_visibility="collapsed"
            )
            
            st.session_state.answers[question_idx] = options.index(answer) + 1
            st.markdown("---")
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if st.session_state.current_page > 0:
                if st.button("⬅️ Previous", use_container_width=True):
                    st.session_state.current_page -= 1
                    st.rerun()
        
        with col3:
            if st.session_state.current_page < total_pages - 1:
                if st.button("Next ➡️", use_container_width=True):
                    st.session_state.current_page += 1
                    st.rerun()
            else:
                if st.button("Complete", use_container_width=True):
                    # Check all answered
                    if all(ans is not None for ans in st.session_state.answers):
                        st.session_state.test_completed = True
                        trait_scores, facet_scores = calculate_scores(st.session_state.answers)
                        st.session_state.big_five_scores = trait_scores
                        st.session_state.facet_scores = facet_scores
                        st.rerun()
                    else:
                        st.warning("Please answer all questions before completing the test.")
    
    else:
        display_results()

def display_results():
    st.header("Your Personality Test Results")
    st.success("Assessment Complete!, great job!")

    trait_scores = st.session_state.big_five_scores
    facet_scores = st.session_state.facet_scores
    user_id = st.session_state.user_id 


    #Sunburst chart for hierarchy exploration
    st.subheader("Hierarchy Explorer")
    sunburst_fig = create_facet_sunburst(trait_scores, facet_scores)
    st.plotly_chart(sunburst_fig, use_container_width=True)

    #Main traits results
    #The five traits are 
    st.subheader("Personality Traits")

    results_df=pd.DataFrame([{"Trait": TRAIT_NAMES[trait], "Score": f"{score}%"}
        for trait, score in trait_scores.items()
    ])

    st.dataframe(results_df, use_container_width=True, hide_index=True)

    #Create main chart
    create_radar_chart(trait_scores, facet_scores)

    # Facet results - show detailed facet tables and individual facet radar charts
    if facet_scores:
        st.subheader("Personality Facets")
        facet_scores_local = facet_scores

        for trait, facets in facet_scores_local.items():
            with st.expander(f"{TRAIT_NAMES[trait]} - Facets"):
                facet_df = pd.DataFrame([
                    {"Facet": FACET_NAMES[trait][facet], "Score": f"{score}%"}
                    for facet, score in facets.items()
                ])
                st.dataframe(facet_df, use_container_width=True, hide_index=True)

                # Individual facet radar chart
                create_facet_radar_chart(trait, facets)

    # After displaying results, show post-test options (call here where variables are defined)
    options_after_test(user_id, trait_scores, facet_scores)


def create_facet_sunburst(trait_scores, facet_scores):
    """Create sunburst chart showing traits and facets hierarchy"""
    labels = ["You"]
    parents = [""]
    values = [0]
    colors_list = ["#f0f0f0"]
    text_list = [""]  # Custom text for display
    
    for trait, score in trait_scores.items():
        labels.append(TRAIT_NAMES[trait])
        parents.append("You")
        values.append(score)
        colors_list.append(TRAIT_COLORS[trait])
        text_list.append(f"{score}%")  # Show percentage
        
        for facet, facet_score in facet_scores[trait].items():
            labels.append(FACET_NAMES[trait][facet])
            parents.append(TRAIT_NAMES[trait])
            values.append(facet_score)
            colors_list.append(TRAIT_COLORS[trait])
            text_list.append(f"{facet_score}%")  # Show percentage
    
    fig = go.Figure(go.Sunburst(
        labels=labels,
        parents=parents,
        values=values,
        text=text_list,
        textinfo="label+text",  # Show label and percentage
        marker=dict(
            colors=colors_list,
            line=dict(color='white', width=3)  # Thicker white lines
        ),
        branchvalues="remainder",
        hovertemplate='<b>%{label}</b><br>Score: %{value}%<br><extra></extra>',
        insidetextorientation='auto'  # Let Plotly choose best orientation
    ))
    
    fig.update_layout(
        title={
            'text': "Your Personality Profile - Interactive Exploration<br><sub>Size represents your score in each dimension (0-100%)</sub>",
            'x': 0.5,
            'xanchor': 'center'
        },
        height=750,
        margin=dict(t=100, l=0, r=0, b=80),
        annotations=[
            dict(
                text="💡 Tip: Click on the 5 main personality traits (inner ring) to zoom in and explore their facets<br>Click the center 'You' to return to the full view",
                x=0.5,
                y=-0.08,
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(size=12, color="#555555"),
                align="center"
            )
        ],
        uniformtext=dict(minsize=10, mode='hide')  # Hide text that doesn't fit (smaller threshold)
    )
    
    # Configure text styling - white text for dark backgrounds
    fig.update_traces(
        textfont=dict(
            size=11,  # Slightly smaller for better fit
            family="Arial, sans-serif",
            color="white"  # White text for better contrast on all colors
        ),
        # Make center "You" larger
        root=dict(color="#f0f0f0")
    )
    
    return fig
def create_radar_chart(trait_scores, facet_scores):
    traits = list(trait_scores.keys())
    labels = [TRAIT_NAMES[t] for t in traits]
    scores = list(trait_scores.values())

    # Close the loop for radar chart plotting
    labels_plot = labels + [labels[0]]
    scores_plot = scores + [scores[0]]

    # Build a single radar trace for the five main traits
    fig = go.Figure(
        data=[
            go.Scatterpolar(
                r=scores_plot,
                theta=labels_plot,
                fill='toself',
                line=dict(color='rgba(50,50,50,0.9)', width=2),
                fillcolor='rgba(100,100,100,0.2)',
                marker=dict(size=6)
            )
        ]
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100])
        ),
        showlegend=False,
        title="Big Five Personality Traits",
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

  
        


def reset_test():
    """Reset the test session state."""
    st.session_state.current_page = 0
    st.session_state.answers = [None] * total_questions
    st.session_state.test_completed = False
    st.session_state.big_five_scores = None
    st.session_state.facet_scores = None
    st.rerun()

def create_facet_radar_chart(trait, facets):
    """Create a radar chart for the facets of a given trait."""
    facet_names = [FACET_NAMES[trait][facet] for facet in facets.keys()]
    facet_scores = list(facets.values())

    # Close the loop for radar chart
    facet_names += [facet_names[0]]
    facet_scores += [facet_scores[0]]

    # Get color for the trait
    color = TRAIT_COLORS[trait]

    fig = go.Figure(
        data=[
            go.Scatterpolar(
                r=facet_scores,
                theta=facet_names,
                fill='toself',
                line=dict(color=color),
                fillcolor=f'rgba({hex_to_rgb(color)}, 0.3)',
                name=f"{TRAIT_NAMES[trait]} Facets"
            )
        ]
    )
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
        title=f"{TRAIT_NAMES[trait]} Facet Radar Chart"
    )
    st.plotly_chart(fig, use_container_width=True)



   

  


#Create results structure for extraction

def create_results_structure(user_id, trait_scores, facet_scores):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return {
        "user_id": user_id,
        "timestamp": timestamp,
        "trait_scores": trait_scores,
        "facet_scores": facet_scores
    }

#Results to dataframes

def results_to_dataframes(results_list):

    #two main dataframes
    summary_data = []
    detailed_data = []

    for result in results_list:
        user_id = result["user_id"]
        timestamp = result["timestamp"]
        trait_scores = result["trait_scores"]
        facet_scores = result["facet_scores"]

        # Rows for summary dataframe
        summary_row = {"user_id": user_id, 
                       "timestamp": timestamp,
                       "Extraversion":trait_scores.get("extraversion", 0),
                       "Agreeableness":trait_scores.get("agreeableness", 0),
                       "Conscientiousness":trait_scores.get("conscientiousness", 0),
                       "Neuroticism":trait_scores.get("neuroticism", 0),
                       "Openness":trait_scores.get("openness", 0)
                      }
        summary_data.append(summary_row)

    #Rows for detailed dataframe
    detailed_row={"user_id": user_id, 
                       "timestamp": timestamp,
                       "Extraversion":trait_scores.get("extraversion", 0),
                       "Agreeableness":trait_scores.get("agreeableness", 0),
                       "Conscientiousness":trait_scores.get("conscientiousness", 0),
                       "Neuroticism":trait_scores.get("neuroticism", 0),
                       "Openness":trait_scores.get("openness", 0)
                      }
    #Add facets
    for trait, facets in facet_scores.items():
            for facet_name, value in facets.items(): 
                col_name = f"{TRAIT_NAMES[trait]}_{FACET_NAMES[trait][facet_name]}"
                detailed_row[col_name] = value
        
    detailed_data.append(detailed_row)  

    df_summary=pd.DataFrame(summary_data)
    df_detailed=pd.DataFrame(detailed_data)

    return df_summary, df_detailed

#Save to csv

def save_results_to_csv(df_summary, df_detailed,summary_path="results_summary.csv", detailed_path="results_detailed.csv"):

    df_summary.to_csv(summary_path, index=False, encoding='utf-8-sig')
    df_detailed.to_csv(detailed_path, index=False, encoding='utf-8-sig')

    return summary_path, detailed_path

#Save to sqlite database

def save_to_sqlite(df_summary, df_detailed, db_path="test_results.db"):
    conn=sqlite3.connect(db_path)
    #Save summary
    df_summary.to_sql("results_summary", conn, if_exists="append", index=False)
    #Save detailed
    df_detailed.to_sql("results_detailed", conn, if_exists="append", index=False)
    conn.close()
    return db_path

#Function to load sqlite database results

def load_from_sqlite(db_path="test_results.db"):
    conn=sqlite3.connect(db_path)
    df_summary=pd.read_sql_query("SELECT * FROM results_summary WHERE user_id = ?", conn)
    df_detailed=pd.read_sql_query("SELECT * FROM results_detailed WHERE user_id = ?", conn)
    conn.close()
    return df_summary, df_detailed

def delete_results(user_id, db_path="test_results.db"):
    try:
        conn=sqlite3.connect(db_path)
        cursor=conn.cursor()
        cursor.execute("DELETE FROM results_summary WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM results_detailed WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Error deleting results: {e}")
        return False
    
#Options after taking the test
def options_after_test(user_id, trait_scores, facet_scores):
    st.header("What would you like to do next?")
  
    col1, col2, col3 = st.columns(3)

    #option 1:save results (both csv and sqlite)
    with col1:
        if st.button("💾 Save Results", use_container_width=True, help="Save these results to your history"):
            results_structure = create_results_structure(user_id, trait_scores, facet_scores)
            df_summary, df_detailed = results_to_dataframes([results_structure])
            
            save_results_to_csv(df_summary, df_detailed)
            save_to_sqlite(df_summary, df_detailed)
            
            st.success("✅ Results saved to your history!")
            st.balloons()
    
    #Option to retake the test without saving the results
    with col2:

      if st.button("🔄 Retake Test", use_container_width=True, help="Start over without saving these results"): 
          reset_test()

    # Retake the test and save the results
    with col3:

        if st.button("💾🔄 Save & Retake", use_container_width=True, help="Save these results and take the test again"):
            results_structure = create_results_structure(user_id, trait_scores, facet_scores)
            df_summary, df_detailed = results_to_dataframes([results_structure])
            
            save_results_to_csv(df_summary, df_detailed)
            save_to_sqlite(df_summary, df_detailed)
            
            st.success("✅ Results saved!")
            reset_test()

    # Separte an option to delete all user results with a warning and a confirmation

    st.markdown("---")
    with st.expander("❌ Delete All Your Test Results", expanded=False):
        st.error("⚠️ Warning: This action is irreversible! All your saved test results will be permanently deleted from our database.")
        confirm_delete = st.checkbox("I understand the consequences and want to delete all my test results.")
        if st.button("Delete My Results", use_container_width=True, disabled=not confirm_delete):
            if delete_results(user_id):
                st.success("✅ All your test results have been deleted.")
            else:
                st.error("❌ There was an error deleting your results. Please try again later.")
       
    
   
    

       



## Login System

user_id=manage_user_session()

#If the user is not logged in, stop execution
if not user_id:
    st.stop()

#LOG IN USER
st.title("About You")
st.success(f"Active user: **{user_id}**")

#Logout bottom
if st.button("Logout"):
    if "user_id" in st.session_state:
        del st.session_state.user_id
    st.rerun()

st.divider()

#Main Page after login

def main():

   
    init_session_state()
    display_paginated_test()

if __name__ == "__main__":
    main()

