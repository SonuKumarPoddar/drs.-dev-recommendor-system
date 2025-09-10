import streamlit as st
import pickle
import pandas as pd
import gdown

# -------------------------------
# Download similarity.pkl from Google Drive using gdown
# -------------------------------

similarity_file_id = "1oiUnots4Ytd6igNrH2X6Cd4i6MhcgB7F"  # your Google Drive file ID
gdown.download(f"https://drive.google.com/uc?id={similarity_file_id}", "similarity.pkl", quiet=False)

# Load similarity.pkl
with open("similarity.pkl", "rb") as f:
    similarity = pickle.load(f)

# Load movie_dict.pkl from GitHub (already uploaded)
with open("movie_dict.pkl", "rb") as f:
    movies_dict = pickle.load(f)
movies = pd.DataFrame(movies_dict)

# -------------------------------
# Recommend Function
# -------------------------------
def recommend_basic(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]
    return [movies.iloc[i[0]].title for i in movies_list]

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="AI Movie Recommender", page_icon="🍿", layout="wide")

# -------------------------------
# Global styling (floating text, hover, slide-in)
# -------------------------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(to right, #141e30, #243b55);
    color: white;
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}
@keyframes float {
  0%   { transform: translateY(0px); opacity: 1; }
  50%  { transform: translateY(-20px); opacity: 0.7; }
  100% { transform: translateY(0px); opacity: 1; }
}
.movie-text {
  display: inline-block;
  margin: 10px;
  font-size: 22px;
  font-weight: bold;
  color: #FFD700;
  animation: float 3s ease-in-out infinite;
}
div.stButton > button {
    background-color: #1e1e2f;
    color: white;
    border: none;
    padding: 12px 20px;
    margin: 6px 0;
    border-radius: 12px;
    font-size: 16px;
    transition: all 0.28s ease-in-out;
    box-shadow: 0 2px 6px rgba(0,0,0,0.3);
    width: 100%;
    text-align: left;
}
div.stButton > button:hover {
    transform: translateY(-4px) scale(1.03) !important;
    background: linear-gradient(90deg, #ffd54f 0%, #ff9800 100%) !important;
    color: black !important;
    box-shadow: 0 10px 30px rgba(255,152,0,0.45) !important;
    cursor: pointer;
}
@keyframes slideIn {
  from {opacity: 0; transform: translateY(12px);}
  to {opacity: 1; transform: translateY(0);}
}
.description-box {
    animation: slideIn 0.45s ease-out;
    margin:10px 0; 
    padding:15px; 
    background:#2c2c3c; 
    border-radius:12px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.45);
}
.small-note { color: #ddd; font-size:13px; }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Floating Movie Names Animation (top)
# -------------------------------
st.markdown("""
<div style="text-align:center; margin-bottom:18px;">
<span class="movie-text">🎬 Inception</span>
<span class="movie-text" style="animation-delay:0.3s;">🍿 Titanic</span>
<span class="movie-text" style="animation-delay:0.6s;">🎥 Avatar</span>
<span class="movie-text" style="animation-delay:0.9s;">🌌 Interstellar</span>
<span class="movie-text" style="animation-delay:1.2s;">🦇 The Dark Knight</span>
<span class="movie-text" style="animation-delay:1.5s;">💡 The Matrix</span>
<span class="movie-text" style="animation-delay:1.8s;">⚡ Avengers</span>
<span class="movie-text" style="animation-delay:2.1s;">🧙‍♂ Harry Potter</span>
</div>
""", unsafe_allow_html=True)

# -------------------------------
# UI - header & selected movie info
# -------------------------------
st.title("🍿 Dev Recommender 🎬")
st.markdown("<div style='font-size:20px; color:yellow; margin-bottom:6px;'>✨ Find your next favorite movie instantly! ✨</div>", unsafe_allow_html=True)

selected_movie_name = st.selectbox("🎥 Select a movie you like:", movies['title'].values)
selected_movie = movies[movies['title'] == selected_movie_name].iloc[0]

st.markdown(f"""
<div class="description-box">
  <h3>🎬 {selected_movie['title']}</h3>
  <p class="small-note"><b>🆔 Movie ID:</b> {selected_movie.get('movie_id', '')}</p>
  <p>{selected_movie.get('tags','')}</p>
</div>
""", unsafe_allow_html=True)

# -------------------------------
# Recommend button (compute once, save in session)
# -------------------------------
if st.button("Recommend 🚀"):
    recs = recommend_basic(selected_movie_name)
    st.session_state["recommendations"] = recs
    st.session_state.pop("selected_top", None)
    st.session_state.pop("selected_bottom", None)

# -------------------------------
# Show recommendations split into top 5 / bottom 5
# -------------------------------
if "recommendations" in st.session_state:
    recs = st.session_state["recommendations"]
    if not recs:
        st.info("No recommendations found.")
    else:
        top_recs = recs[:5]
        bottom_recs = recs[5:]

        st.subheader("🔝 Top Recommendations")
        col_left_top, col_right_top = st.columns([2,3])

        with col_left_top:
            st.markdown("<div class='small-note'>Click any movie to view its full description on the right.</div>", unsafe_allow_html=True)
            for idx, title in enumerate(top_recs):
                key = f"top_{idx}"
                if st.button(f"🎬 {title}", key=key):
                    st.session_state["selected_top"] = title

        with col_right_top:
            if "selected_top" in st.session_state:
                clicked = st.session_state["selected_top"]
                info = movies[movies['title'] == clicked].iloc[0]
                st.markdown(f"""
                <div class="description-box">
                    <h3>🎬 {info['title']}</h3>
                    <p class="small-note"><b>🆔 Movie ID:</b> {info.get('movie_id','')}</p>
                    <p>{info.get('tags','')}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("👈 Click a top recommendation to see its description here.")

        st.markdown("---")

        st.subheader("⬇ More Like This")
        col_left_bot, col_right_bot = st.columns([2,3])

        with col_left_bot:
            st.markdown("<div class='small-note'>Click any movie to view its full description on the right.</div>", unsafe_allow_html=True)
            for idx, title in enumerate(bottom_recs):
                key = f"bottom_{idx}"
                if st.button(f"🎬 {title}", key=key):
                    st.session_state["selected_bottom"] = title

        with col_right_bot:
            if "selected_bottom" in st.session_state:
                clicked = st.session_state["selected_bottom"]
                info = movies[movies['title'] == clicked].iloc[0]
                st.markdown(f"""
                <div class="description-box">
                    <h3>🎬 {info['title']}</h3>
                    <p class="small-note"><b>🆔 Movie ID:</b> {info.get('movie_id','')}</p>
                    <p>{info.get('tags','')}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("👈 Click a bottom recommendation to see its description here.")