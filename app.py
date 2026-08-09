import streamlit as st
import random
import json
import time

# ==========================================
# 1. CONFIGURATION DE LA PAGE
# ==========================================
st.set_page_config(
    page_title="Examen Civique France",
    page_icon="🇫🇷",
    layout="centered"
)

# Cacher le menu Streamlit et le footer pour un look "Application native"
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


# ==========================================
# 2. CONSTANTES
# ==========================================
TEMPS_MAX_SECONDES = 45 * 60  # 45 minutes
SCORE_REQUIS = 32


# ==========================================
# 3. CHARGEMENT DES DONNÉES
# ==========================================
@st.cache_data 
def load_questions(file):
    """Charge les questions depuis un fichier JSON."""
    try:
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Attention : Le fichier {file} est introuvable.")
        return []

questions_connaissance = load_questions("questions_connaissance.json")
questions_situation = load_questions("questions_situation.json")


# ==========================================
# 4. INITIALISATION DE LA SESSION
# ==========================================
# st.session_state permet de garder en mémoire l'état de l'application entre chaque clic
if "started" not in st.session_state:
    st.session_state.started = False       # L'examen a-t-il commencé ?
    st.session_state.questions = []        # Liste finale des questions sélectionnées
    st.session_state.index = 0             # Numéro de la question actuelle
    st.session_state.score = 0             # Score du joueur
    st.session_state.errors = []           # Historique des erreurs
    st.session_state.start_time = 0        # Heure de début pour le chrono


# ==========================================
# 5. INTERFACE PRINCIPALE
# ==========================================
st.title("Simulateur Examen Civique (CR)")

# ---------------------------------------------------------
# ÉCRAN 1 : SÉLECTION DU MODE (Si l'examen n'a pas commencé)
# ---------------------------------------------------------
if not st.session_state.started:
    st.write("Bienvenue dans le simulateur officiel. Veuillez choisir le mode d'entraînement :")
    
    # Ajout d'une bannière visuelle ou d'un séparateur propre pour moderniser la forme
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Mode 1 : Entraînement")
        st.write("40 questions de connaissances pures.")
        if st.button("Lancer l'entraînement"):
            q_choisies = random.sample(questions_connaissance, min(40, len(questions_connaissance)))
            st.session_state.questions = q_choisies
            st.session_state.start_time = time.time()
            st.session_state.started = True
            st.rerun()

    with col2:
        st.subheader("Mode 2 : Examen Réel")
        st.write("28 connaissances + 12 mises en situation.")
        if st.button("Lancer l'examen réel"):
            # Tirage au sort respectant les quotas de l'examen officiel
            q_con = random.sample(questions_connaissance, min(28, len(questions_connaissance)))
            q_sit = random.sample(questions_situation, min(12, len(questions_situation)))
            
            q_choisies = q_con + q_sit
            random.shuffle(q_choisies) # Mélange pour ne pas avoir toutes les situations à la fin
            
            st.session_state.questions = q_choisies
            st.session_state.start_time = time.time()
            st.session_state.started = True
            st.rerun()


# ---------------------------------------------------------
# ÉCRAN 2 : L'EXAMEN EN COURS (Si l'examen a commencé)
# ---------------------------------------------------------
else:
    # --- GESTION DU CHRONOMÈTRE ---
    temps_ecoule = time.time() - st.session_state.start_time
    temps_restant = TEMPS_MAX_SECONDES - temps_ecoule
    
    minutes = int(temps_restant // 60)
    secondes = int(temps_restant % 60)
    
    # --- AFFICHAGE DE LA PROGRESSION ---
    col_prog, col_timer = st.columns(2)
    col_prog.write(f"**Question {st.session_state.index + 1} / {len(st.session_state.questions)}**")
    
    if temps_restant > 0:
        col_timer.write(f"⏱️ **Temps restant : {minutes:02d}:{secondes:02d}**")
    else:
        col_timer.error("⏱️ Temps écoulé !")

    # Barre de progression visuelle
    progression = st.session_state.index / len(st.session_state.questions)
    st.progress(progression)


    # --- CONDITIONS DE FIN D'EXAMEN ---
    if st.session_state.index >= len(st.session_state.questions) or temps_restant <= 0:
        
        st.markdown("---")
        st.header("🏁 Résultat de l'examen")
        
        nb_questions_posees = st.session_state.index
        if nb_questions_posees == 0:
            score40 = 0
        else:
            score40 = int((st.session_state.score / len(st.session_state.questions)) * 40)

        if score40 >= SCORE_REQUIS:
            st.success(f"Félicitations ! Vous auriez validé l'examen. 🎉\n\n**Score final : {score40} / 40**")
        else:
            st.error(f"Dommage, c'est insuffisant pour cette fois (Minimum requis : {SCORE_REQUIS}/40). ❌\n\n**Score final : {score40} / 40**")

        st.subheader("📋 Vos erreurs et corrections :")
        if not st.session_state.errors:
            st.info("Un sans-faute ! Excellente maîtrise de la civique française.")
        else:
            for i, err in enumerate(st.session_state.errors):
                with st.expander(f"Erreur {i+1} : {err['question'][:50]}..."):
                    st.write("**Question :**", err["question"])
                    st.write("❌ **Vous avez répondu :**", err["choisie"])
                    st.write("✅ **La bonne réponse était :**", err["correcte"])

        if st.button("🔄 Recommencer un examen"):
            st.session_state.clear()
            st.rerun()

        st.stop()


    # --- AFFICHAGE DE LA QUESTION ACTUELLE ---
    q = st.session_state.questions[st.session_state.index]

    # Mélange des options pour ne pas s'habituer à leur position
    if "shuffled_options" not in st.session_state:
        st.session_state.shuffled_options = q["options"].copy()
        random.shuffle(st.session_state.shuffled_options)

    with st.form(key=f"form_question_{st.session_state.index}"):
        st.subheader(q["question"])
        
        choice = st.radio("Sélectionnez votre réponse :", st.session_state.shuffled_options, index=None)

        submit_button = st.form_submit_button(label="Valider la réponse")

        if submit_button:
            if choice is None:
                st.warning("⚠️ Veuillez sélectionner une réponse avant de valider.")
            else:
                if choice == q["reponse"]:
                    st.session_state.score += 1
                else:
                    st.session_state.errors.append({
                        "question": q["question"],
                        "choisie": choice,
                        "correcte": q["reponse"]
                    })
                
                # Passage à la question suivante
                st.session_state.index += 1
                # Suppression des options mélangées pour la prochaine question
                del st.session_state.shuffled_options 
                st.rerun()