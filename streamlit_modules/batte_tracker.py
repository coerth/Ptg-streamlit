import streamlit as st

def run_tracker():
    # Initialize battle log in session state
    if "battle_log" not in st.session_state:
        st.session_state.battle_log = []

    st.title("⚔️ Warhammer Battle Tracker")
    st.header("➕ Add a New Round")

    # Input fields
    round_number = len(st.session_state.battle_log) + 1
    player_1_points = st.number_input("Player 1 Points", min_value=0, step=1)
    player_2_points = st.number_input("Player 2 Points", min_value=0, step=1)
    image_url = st.text_input("Image URL (optional)", placeholder="https://...")

    # Add round button
    if st.button("Add Round"):
        st.session_state.battle_log.append({
            "round": round_number,
            "player_1": player_1_points,
            "player_2": player_2_points,
            "image": image_url
        })
        st.success(f"Round {round_number} added!")

    # Show battle log
    if st.session_state.battle_log:
        st.header("📜 Battle Log")
        for entry in st.session_state.battle_log:
            st.subheader(f"Round {entry['round']}")
            st.markdown(f"- Player 1: **{entry['player_1']}** points")
            st.markdown(f"- Player 2: **{entry['player_2']}** points")
            if entry['image']:
                st.image(entry['image'], caption=f"Round {entry['round']}")
