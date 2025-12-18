# app.py - Version optimisée pour déploiement

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from pathlib import Path

# =====================================================
# CONFIGURATION
# =====================================================
st.set_page_config(
    page_title="Martin Alquier – Business Analyst",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# FONCTIONS UTILITAIRES POUR LES IMAGES
# =====================================================
def load_image(image_path, default_placeholder=True, alt_text="Image"):
    """
    Charge une image avec gestion d'erreur. Retourne un placeholder si l'image n'est pas trouvée.
    """
    try:
        # Vérifier si c'est une URL
        if image_path.startswith('http'):
            return image_path
        
        # Vérifier les chemins locaux
        possible_paths = [
            image_path,
            f"assets/{image_path}",
            f"images/{image_path}",
            f"data/{image_path}"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        # Si aucune image trouvée et placeholder activé
        if default_placeholder:
            if "logo" in image_path.lower() or "inetum" in image_path.lower():
                return "https://images.unsplash.com/photo-1552664730-d307ca884978?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80"
            elif "efrei" in image_path.lower():
                return "https://upload.wikimedia.org/wikipedia/fr/thumb/6/6b/Logo_Efrei_Paris.svg/1200px-Logo_Efrei_Paris.svg.png"
            elif "dauphine" in image_path.lower():
                return "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Logo_Universit%C3%A9_Paris-Dauphine.svg/1200px-Logo_Universit%C3%A9_Paris-Dauphine.svg.png"
            else:
                return f"https://via.placeholder.com/400x200/667eea/ffffff?text={alt_text.replace(' ', '+')}"
        
        return None
    except Exception as e:
        if default_placeholder:
            return f"https://via.placeholder.com/400x200/667eea/ffffff?text={alt_text.replace(' ', '+')}"
        return None

# =====================================================
# CSS PERSONNALISÉ
# =====================================================
def load_custom_css():
    st.markdown("""
    <style>
    /* Styles précédents restent les mêmes... */
    .main {
        padding: 2rem;
    }
    
    .card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
    }
    
    .skill-tag {
        display: inline-block;
        background: #eef2ff;
        color: #4f46e5;
        padding: 0.4rem 0.8rem;
        margin: 0.2rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    .section-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 2rem 0 1rem 0;
    }
    
    .profile-circle {
        border-radius: 50%;
        overflow: hidden;
        width: 150px;
        height: 150px;
        margin: 0 auto 20px auto;
        border: 4px solid #667eea;
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
    }
    
    .profile-circle img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    
    .experience-image-frame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        border: 3px solid #667eea;
        transition: transform 0.3s ease;
        height: 200px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    .experience-image-frame:hover {
        transform: scale(1.02);
    }
    
    .experience-image-frame img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    
    .education-image-frame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        border: 3px solid #42be65;
        transition: transform 0.3s ease;
        height: 180px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #f0fff4 0%, #e6ffed 100%);
    }
    
    .education-image-frame:hover {
        transform: scale(1.02);
    }
    
    .education-image-frame img {
        width: 100%;
        height: 100%;
        object-fit: contain;
        padding: 10px;
        background: white;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main {
            padding: 1rem;
        }
        
        .profile-circle {
            width: 120px;
            height: 120px;
        }
        
        .experience-image-frame,
        .education-image-frame {
            height: 150px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

load_custom_css()

# =====================================================
# COMPOSANTS RÉUTILISABLES
# =====================================================
def kpi_card(title, value, subtitle="", color="#0f62fe", icon="📊", trend=None):
    trend_html = ""
    if trend:
        trend_color = "#42be65" if trend > 0 else "#da1e28"
        trend_icon = "📈" if trend > 0 else "📉"
        trend_html = f'<span style="color:{trend_color};font-weight:600;"> {trend_icon} {abs(trend)}%</span>'
    
    return f"""
    <div style="
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.08);
        border-left: 5px solid {color};
        transition: transform 0.3s ease;
        margin-bottom: 1rem;
    ">
        <div style="display: flex; align-items: center; margin-bottom: 10px;">
            <span style="font-size: 1.5rem; margin-right: 10px;">{icon}</span>
            <h4 style="margin:0;color:#333;font-weight:600;">{title}</h4>
        </div>
        <div style="display: flex; align-items: baseline;">
            <h2 style="margin:0;color:#111;">{value}</h2>
            {trend_html}
        </div>
        <p style="margin:10px 0 0 0;color:#666;font-size:0.9rem;">{subtitle}</p>
    </div>
    """

def experience_card_with_image(company, role, duration, description, image_path, location="Paris, France", 
                               tags=None, achievements=None, company_color="#667eea"):
    
    safe_image_path = load_image(image_path, alt_text=company)
    
    with st.container():
        col1, col2 = st.columns([4, 1])
        
        with col1:
            st.markdown(f"""
            <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                <div style="
                    width: 50px;
                    height: 50px;
                    border-radius: 10px;
                    background: {company_color};
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin-right: 15px;
                    color: white;
                    font-weight: bold;
                    font-size: 1.2rem;
                ">
                    {company[0]}
                </div>
                <div>
                    <h3 style="color:#333;margin-bottom:0.2rem;">{company}</h3>
                    <p style="color:#666;margin:0;font-size:0.9rem;">
                    📍 {location} | ⏱️ {duration}
                    </p>
                </div>
            </div>
            <h4 style="color:#667eea;margin-top:0;margin-bottom:1rem;">{role}</h4>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="experience-image-frame">', unsafe_allow_html=True)
            if safe_image_path:
                st.image(safe_image_path, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Description
        st.markdown(f"""
        <div style="
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
        ">
            {description}
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()

def education_card_with_image(diploma, school, duration, description, image_path, 
                             location="Paris, France", specialities=None):
    
    safe_image_path = load_image(image_path, alt_text=school)
    
    with st.container():
        col1, col2 = st.columns([4, 1])
        
        with col1:
            st.markdown(f"""
            <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                <div style="
                    width: 50px;
                    height: 50px;
                    border-radius: 50%;
                    background: linear-gradient(135deg, #42be65 0%, #00a854 100%);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin-right: 15px;
                    color: white;
                    font-weight: bold;
                    font-size: 1.2rem;
                ">
                    🎓
                </div>
                <div>
                    <h3 style="color:#333;margin-bottom:0.2rem;">{diploma}</h3>
                    <p style="color:#666;margin:0;font-size:0.9rem;">
                    🏫 {school} | 📍 {location}
                    </p>
                </div>
            </div>
            <h4 style="color:#42be65;margin-top:0;margin-bottom:1rem;">
            📅 {duration}
            </h4>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="education-image-frame">', unsafe_allow_html=True)
            if safe_image_path:
                st.image(safe_image_path, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Description
        st.markdown(f"""
        <div style="
            background: #f0fff4;
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
        ">
            {description}
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()

# =====================================================
# DONNÉES (Personnalisez ces données avec vos informations)
# =====================================================
EXPERIENCES = [
    {
        "company": "INETUM",
        "role": "Consultant Data Analyst",
        "duration": "Sept 2022 - Présent",
        "location": "Paris La Défense, France",
        "description": "Consultant en data analytics pour la Direction Générale et l'Audit Interne. Missions de dashboarding KPI, automatisation des rapports et support décisionnel pour le CODIR.",
        "image_path": "inetum_logo.jpg",  # Placez votre image dans assets/inetum_logo.jpg
        "company_color": "#0056b3",
    },
    {
        "company": "Zigourrat",
        "role": "Consultant Digital Innovation",
        "duration": "Mars 2021 - Août 2022",
        "location": "Paris, France",
        "description": "Consultant en innovation digitale et Web3.0. Analyse marketing data et recommandations stratégiques pour clients du secteur tech.",
        "image_path": "zigourrat_logo.jpg",  # Placez votre image dans assets/zigourrat_logo.jpg
        "company_color": "#FF6B6B",
    }
]

EDUCATIONS = [
    {
        "diploma": "Master en Data Science & Business Analytics",
        "school": "EFREI Paris - Grande École du Numérique",
        "duration": "2020 - 2022",
        "location": "Paris, France",
        "description": "Formation d'excellence en Data Science avec double compétence business et technique. Spécialisation en Machine Learning, Big Data et Intelligence Artificielle.",
        "image_path": "efrei_logo.png",  # Placez votre image dans assets/efrei_logo.png
    },
    {
        "diploma": "Bachelor Business & Management",
        "school": "Université Paris-Dauphine | PSL",
        "duration": "2017 - 2020",
        "location": "Paris, France",
        "description": "Formation en gestion d'entreprise avec spécialisation en finance et stratégie. Double compétence quantitative et managériale.",
        "image_path": "dauphine_logo.jpg",  # Placez votre image dans assets/dauphine_logo.jpg
    }
]

# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:
    # Photo de profil
    st.markdown('<div class="profile-circle">', unsafe_allow_html=True)
    try:
        profile_pic = load_image("photo.jpeg", alt_text="Martin Alquier")
        st.image(profile_pic, use_container_width=True)
    except:
        st.image("https://via.placeholder.com/150/667eea/ffffff?text=MA", 
                use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
        <h3 style='text-align:center;margin-bottom:0;color:#333;'>Martin Alquier</h3>
        <p style='text-align:center;color:#667eea;margin-top:4px;font-weight:600;'>
        🎯 Business Analyst • Data & IA
        </p>
        <p style='text-align:center;color:#666;font-size:0.9rem;'>
        Transforme la donnée en décisions mesurables
        </p>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Navigation
    st.markdown("### 🔍 Navigation")
    page = st.radio(
        "",
        [
            "🏠 Accueil",
            "🏢 Expériences",
            "📂 Projets",
            "📈 Dashboard",
            "🛠️ Compétences",
            "🎓 Formation",
            "📄 Contact"
        ],
        label_visibility="collapsed"
    )
    
    st.divider()
    
    # Contact
    st.markdown("### 📱 Contact")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/martinalquier)")
    with col2:
        st.markdown("[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/martinalquier)")
    with col3:
        st.markdown("[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:martin.alquier@business.com)")

# =====================================================
# PAGES
# =====================================================
if page == "🏠 Accueil":
    st.title("👋 Bienvenue sur mon Portfolio Data")
    
    st.markdown("""
    <div class="card">
        <h3 style="color:white;margin:0;">🎯 Mission</h3>
        <p style="color:white;opacity:0.9;">
        Business Analyst spécialisé en Data & IA, je combine expertise métier et technique pour transformer 
        la donnée en décisions stratégiques et en valeur business mesurable.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        ### 📖 À propos
        
        Avec un double parcours **Business / Data Engineering**, j'accompagne les entreprises dans leur 
        transformation digitale par la data. Mon approche allie rigueur analytique, vision stratégique 
        et innovation technologique.
        
        **Valeur ajoutée :**
        - 🎯 Alignement data-stratégie business
        - 📊 Création de dashboards actionnables
        - 🤖 Intégration solutions IA/ML
        - 🔄 Automatisation des processus
        - 📈 Mesure d'impact ROI
        """)
    
    with col2:
        st.markdown('<div class="section-header">🚀 Highlights</div>', unsafe_allow_html=True)
        st.markdown(kpi_card("Années d'expérience", "4+", "Data & Consulting", "#667eea", "💼"), 
                   unsafe_allow_html=True)
        st.markdown(kpi_card("Projets Data", "15+", "Dashboards & Automations", "#42be65", "📈"), 
                   unsafe_allow_html=True)
        st.markdown(kpi_card("Start-ups accompagnées", "12", "Accélérateur Kryptosphere", "#f1c21b", "🚀"), 
                   unsafe_allow_html=True)

elif page == "🏢 Expériences":
    st.title("🏢 Parcours Professionnel")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(kpi_card("Entreprises", "3", "Consulting & Startup", "#667eea", "🏢"), 
                   unsafe_allow_html=True)
    with col2:
        st.markdown(kpi_card("Années exp.", "4+", "Data & Digital", "#42be65", "📅"), 
                   unsafe_allow_html=True)
    with col3:
        st.markdown(kpi_card("Projets majeurs", "20+", "Data & Innovation", "#f1c21b", "🚀"), 
                   unsafe_allow_html=True)
    
    st.markdown("### 📍 Mes expériences en détail")
    
    for exp in EXPERIENCES:
        experience_card_with_image(
            company=exp["company"],
            role=exp["role"],
            duration=exp["duration"],
            location=exp["location"],
            description=exp["description"],
            image_path=exp["image_path"],
            company_color=exp["company_color"]
        )

elif page == "🎓 Formation":
    st.title("🎓 Formation & Éducation")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(kpi_card("Diplômes", "2", "Master & Bachelor", "#42be65", "🎓"), 
                   unsafe_allow_html=True)
    with col2:
        st.markdown(kpi_card("Certifications", "5+", "Techniques & Métier", "#667eea", "📜"), 
                   unsafe_allow_html=True)
    with col3:
        st.markdown(kpi_card("Années d'études", "5", "Business & Data", "#f1c21b", "📚"), 
                   unsafe_allow_html=True)
    
    st.markdown("### 🏫 Mon parcours académique")
    
    for edu in EDUCATIONS:
        education_card_with_image(
            diploma=edu["diploma"],
            school=edu["school"],
            duration=edu["duration"],
            location=edu["location"],
            description=edu["description"],
            image_path=edu["image_path"]
        )

# ... (les autres pages restent similaires)

# =====================================================
# FOOTER
# =====================================================
st.divider()
col1, col2, col3 = st.columns(3)
with col2:
    st.markdown(
        """
        <div style="text-align:center;color:#666;font-size:0.9rem;padding:2rem 0;">
            <p>© 2024 Martin Alquier – Business Analyst Data & IA</p>
            <p>Dernière mise à jour : Novembre 2024</p>
        </div>
        """,
        unsafe_allow_html=True
    )
