import streamlit as st
import pandas as pd
import random
import os

st.set_page_config(
    page_title="감정 기반 음악 추천",
    page_icon="🎧",
    layout="centered"
)

st.title("🎧 오늘의 음악 한 곡")
st.caption("지금의 감정에 맞는 클래식 음악을 추천해드려요")
st.divider()

@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "music.xlsx")

    df = pd.read_excel(file_path, engine="openpyxl")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

st.subheader("💭 지금의 상태를 골라주세요")

q1 = st.radio(
    "지금 내 마음과 더 가까운 문장은?",
    [
        "조용히 가라앉고 싶고, 깊이 몰입하고 싶다",
        "기분을 전환하고 에너지를 얻고 싶다",
        "마음이 불안하거나 예민해서 위로가 필요하다"
    ]
)

if q1 == "조용히 가라앉고 싶고, 깊이 몰입하고 싶다":
    big_emotion = "숭고함"
elif q1 == "기분을 전환하고 에너지를 얻고 싶다":
    big_emotion = "활력"
else:
    big_emotion = "불안"

st.divider()

st.subheader("🎼 지금 더 가까운 분위기는?")

if big_emotion == "숭고함":
    q2 = st.radio(
        "아래 중에서 가장 끌리는 느낌을 골라주세요",
        [
            "따뜻하고 부드러운 느낌",
            "조용하고 안정적인 분위기",
            "현실을 벗어난 깊은 몰입",
            "감탄이 나오는 크고 인상적인 느낌",
            "추억을 떠올리며 차분해지는 느낌"
        ]
    )

    small_map = {
        "따뜻하고 부드러운 느낌": "다정함",
        "조용하고 안정적인 분위기": "평화로움",
        "현실을 벗어난 깊은 몰입": "초월",
        "감탄이 나오는 크고 인상적인 느낌": "경이",
        "추억을 떠올리며 차분해지는 느낌": "향수"
    }

elif big_emotion == "활력":
    q2 = st.radio(
        "지금 필요한 에너지는 어떤 느낌인가요?",
        [
            "밝고 가벼운 기분 전환",
            "단단하고 자신감 있는 에너지"
        ]
    )

    small_map = {
        "밝고 가벼운 기분 전환": "기쁨",
        "단단하고 자신감 있는 에너지": "힘"
    }

else:
    q2 = st.radio(
        "지금 상태에 더 가까운 것은?",
        [
            "감정을 천천히 내려놓고 싶다",
            "긴장을 풀고 마음을 가라앉히고 싶다"
        ]
    )

    small_map = {
        "감정을 천천히 내려놓고 싶다": "슬픔",
        "긴장을 풀고 마음을 가라앉히고 싶다": "긴장"
    }

small_emotion = small_map[q2]

st.divider()

if st.button("🎵 오늘의 음악 추천"):
    filtered = df[
        (df["대분류"] == big_emotion) &
        (df["소분류"] == small_emotion)
    ]

    if filtered.empty:
        st.warning("해당 분위기에 맞는 곡이 아직 없어요 😢")
    else:
        song = filtered.sample(1).iloc[0]

        st.subheader("🎶 오늘의 추천 곡")
        st.markdown(f"### 🎵 {song['곡']}\n**작곡가** · {song['작곡가']}")

        with st.expander("📝 곡 설명 자세히 보기"):
            st.write(song["곡 설명"])

        st.caption("🎧 조용한 공간에서 이어폰으로 감상해보세요")
