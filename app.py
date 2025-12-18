# app.py - Version finale pour déploiement GitHub/Streamlit
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

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
# FONCTIONS POUR CHARGER LES IMAGES
# =====================================================
def load_image(image_name, alt_text="Image"):
    """
    Charge une image depuis le dossier assets/ avec fallback
    """
    image_paths = [
        f"assets/{image_name}",           # Chemin principal
        image_name,                        # Chemin direct
        f"images/{image_name}",            # Alternative
    ]
    
    for path in image_paths:
        if os.path.exists(path):
            return path
    
    # Fallback pour développement local si l'image n'existe pas
    placeholders = {
        "photo.jpeg": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80",
        "inetum_logo.jpg": "https://images.unsplash.com/photo-1552664730-d307ca884978?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80",
        "zigourrat_logo.jpg": "https://images.unsplash.com/photo-1551434678-e076c223a692?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80",
        "efrei_logo.png": "https://upload.wikimedia.org/wikipedia/fr/thumb/6/6b/Logo_Efrei_Paris.svg/400px-Logo_Efrei_Paris.svg.png",
        "dauphine_logo.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Logo_Universit%C3%A9_Paris-Dauphine.svg/400px-Logo_Universit%C3%A9_Paris-Dauphine.svg.png",
        "certifications.jpg": "https://images.unsplash.com/photo-1532619187608-e5375cab36aa?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80"
    }
    
    return placeholders.get(image_name, f"https://via.placeholder.com/400x200/667eea/ffffff?text={alt_text.replace(' ', '+')}")

# =====================================================
# CSS PERSONNALISÉ
# =====================================================
st.markdown("""
<style>
/* Styles généraux */
.main {
    padding: 1rem;
}

/* Cartes */
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

/* Tags */
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

/* Cadres images */
.profile-circle {
    border-radius: 50%;
    overflow: hidden;
    width: 150px;
    height: 150px;
    margin: 0 auto 20px auto;
    border: 4px solid #667eea;
    box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
}

.experience-image-frame {
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 6px 20px rgba(0,0,0,0.1);
    border: 3px solid #667eea;
    height: 180px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
}

.education-image-frame {
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 6px 20px rgba(0,0,0,0.1);
    border: 3px solid #42be65;
    height: 160px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #f0fff4 0%, #e6ffed 100%);
}

/* Responsive */
@media (max-width: 768px) {
    .main { padding: 0.5rem; }
    .profile-circle { width: 120px; height: 120px; }
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# COMPOSANTS RÉUTILISABLES
# =====================================================
def kpi_card(title, value, subtitle="", color="#667eea", icon="📊", trend=None):
    trend_html = ""
    if trend:
        trend_color = "#42be65" if trend > 0 else "#da1e28"
        trend_icon = "📈" if trend > 0 else "📉"
        trend_html = f'<span style="color:{trend_color};font-weight:600;"> {trend_icon} {abs(trend)}%</span>'
    
    return f"""
    <div style="
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.08);
        border-left: 5px solid {color};
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

def experience_card(company, role, duration, description, image_name, tags=None):
    image_path = load_image(image_name, alt_text=company)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"### {company}")
        st.markdown(f"**{role}**")
        st.markdown(f"*{duration}*")
        st.markdown(description)
        
        if tags:
            st.markdown("**Compétences :**")
            for tag in tags:
                st.markdown(f'<span class="skill-tag">{tag}</span>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="experience-image-frame">', unsafe_allow_html=True)
        st.image(image_path, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()

def education_card(diploma, school, duration, description, image_name, specialities=None):
    image_path = load_image(image_name, alt_text=school)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"### {diploma}")
        st.markdown(f"**{school}**")
        st.markdown(f"*{duration}*")
        st.markdown(description)
        
        if specialities:
            st.markdown("**Spécialités :**")
            cols = st.columns(2)
            for idx, spec in enumerate(specialities):
                with cols[idx % 2]:
                    st.markdown(f'<span class="skill-tag">{spec}</span>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="education-image-frame">', unsafe_allow_html=True)
        st.image(image_path, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()

# =====================================================
# DONNÉES (À PERSONNALISER)
# =====================================================
EXPERIENCES = [
    {
        "company": "INETUM",
        "role": "Consultant Data Analyst",
        "duration": "Sept 2022 - Présent",
        "description": "Consultant en data analytics pour la Direction Générale et l'Audit Interne. Dashboarding KPI, automatisation des rapports et support décisionnel CODIR.",
        "image": "inetum_logo.jpg",
        "tags": ["Power BI", "SQL", "Python", "DataViz", "Azure"]
    },
    {
        "company": "Zigourrat",
        "role": "Consultant Digital Innovation",
        "duration": "Mars 2021 - Août 2022",
        "description": "Consultant en innovation digitale et Web3.0. Analyse marketing data et recommandations stratégiques.",
        "image": "zigourrat_logo.jpg",
        "tags": ["Web3", "Marketing", "Growth", "Blockchain", "SEO"]
    }
]

EDUCATIONS = [
    {
        "diploma": "Master en Data Science & Business Analytics",
        "school": "EFREI Paris",
        "duration": "2020 - 2022",
        "description": "Formation d'excellence en Data Science avec double compétence business et technique.",
        "image": "efrei_logo.png",
        "specialities": ["Machine Learning", "Big Data", "Data Visualization", "Business Intelligence"]
    },
    {
        "diploma": "Bachelor Business & Management",
        "school": "Université Paris-Dauphine",
        "duration": "2017 - 2020",
        "description": "Formation en gestion d'entreprise avec spécialisation finance et stratégie.",
        "image": "dauphine_logo.jpg",
        "specialities": ["Corporate Finance", "Business Strategy", "Marketing Analytics"]
    }
]

# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:
    # Photo de profil
    profile_pic = load_image("photo.jpeg", alt_text="Martin Alquier")
    st.markdown('<div class="profile-circle">', unsafe_allow_html=True)
    st.image(profile_pic, use_container_width=True)
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
        ["🏠 Accueil", "🏢 Expériences", "🎓 Formation", "📈 Dashboard", "📄 Contact"],
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
        st.markdown("[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:contact@example.com)")

# =====================================================
# PAGES
# =====================================================
if page == "🏠 Accueil":
    st.title("👋 Bienvenue sur mon Portfolio Data")
    
    st.markdown("""
    <div class="card">
        <h3 style="color:white;margin:0;">🎯 Mission</h3>
        <p style="color:white;opacity:0.9;">
        Business Analyst spécialisé en Data & IA, je transforme la donnée en décisions stratégiques et en valeur business mesurable.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        ### 📖 À propos
        
        Avec un double parcours **Business / Data Engineering**, j'accompagne les entreprises dans leur 
        transformation digitale par la data.
        
        **Valeur ajoutée :**
        - 🎯 Alignement data-stratégie business
        - 📊 Création de dashboards actionnables
        - 🤖 Intégration solutions IA/ML
        - 🔄 Automatisation des processus
        - 📈 Mesure d'impact ROI
        """)
    
    with col2:
        st.markdown("### 🚀 Highlights")
        st.markdown(kpi_card("Expérience", "4+ ans", "Data & Consulting", "#667eea", "💼"), unsafe_allow_html=True)
        st.markdown(kpi_card("Projets", "15+", "Dashboards & IA", "#42be65", "📈"), unsafe_allow_html=True)
        st.markdown(kpi_card("Startups", "12", "Accompagnées", "#f1c21b", "🚀"), unsafe_allow_html=True)

elif page == "🏢 Expériences":
    st.title("🏢 Parcours Professionnel")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(kpi_card("Entreprises", "3", "Consulting & Startup", "#667eea", "🏢"), unsafe_allow_html=True)
    with col2:
        st.markdown(kpi_card("Années", "4+", "Expérience", "#42be65", "📅"), unsafe_allow_html=True)
    with col3:
        st.markdown(kpi_card("Projets", "20+", "Réalisés", "#f1c21b", "🚀"), unsafe_allow_html=True)
    
    st.markdown("### 📍 Expériences détaillées")
    
    for exp in EXPERIENCES:
        experience_card(
            company=exp["company"],
            role=exp["role"],
            duration=exp["duration"],
            description=exp["description"],
            image_name=exp["image"],
            tags=exp["tags"]
        )

elif page == "🎓 Formation":
    st.title("🎓 Formation & Éducation")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(kpi_card("Diplômes", "2", "Master & Bachelor", "#42be65", "🎓"), unsafe_allow_html=True)
    with col2:
        st.markdown(kpi_card("Certifications", "5+", "Techniques", "#667eea", "📜"), unsafe_allow_html=True)
    with col3:
        st.markdown(kpi_card("Années", "5", "Études", "#f1c21b", "📚"), unsafe_allow_html=True)
    
    st.markdown("### 🏫 Parcours académique")
    
    for edu in EDUCATIONS:
        education_card(
            diploma=edu["diploma"],
            school=edu["school"],
            duration=edu["duration"],
            description=edu["description"],
            image_name=edu["image"],
            specialities=edu["specialities"]
        )

elif page == "📈 Dashboard":
    st.title("📈 Dashboard Business")
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(kpi_card("Revenu", "210 K€", "+12% vs M-1", "#667eea", "💰", 12), unsafe_allow_html=True)
    with col2:
        st.markdown(kpi_card("Marge", "32%", "+4 pts", "#42be65", "📈", 4), unsafe_allow_html=True)
    with col3:
        st.markdown(kpi_card("NPS", "85", "+5 pts", "#f1c21b", "😊", 5), unsafe_allow_html=True)
    with col4:
        st.markdown(kpi_card("Coûts", "110 K€", "-8%", "#da1e28", "📉", -8), unsafe_allow_html=True)
    
    # Graphique
    df = pd.DataFrame({
        "Mois": ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin"],
        "Revenu": [180, 195, 210, 220, 240, 250],
        "Coûts": [120, 115, 110, 115, 120, 125]
    })
    
    fig = px.line(df, x="Mois", y=["Revenu", "Coûts"], title="Évolution des revenus et coûts")
    st.plotly_chart(fig, use_container_width=True)

elif page == "📄 Contact":
    st.title("📄 Contactez-moi")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 💬 Discutons de votre projet")
        
        with st.form("contact_form"):
            name = st.text_input("Nom complet")
            email = st.text_input("Email")
            company = st.text_input("Entreprise")
            message = st.text_area("Message", height=150)
            
            if st.form_submit_button("📤 Envoyer"):
                st.success("✅ Message envoyé ! Je vous répondrai dans les 24h.")
    
    with col2:
        st.markdown("""
        ### 📍 Informations
        
        **Email**  
        martin.alquier@business.com
        
        **Téléphone**  
        +33 6 XX XX XX XX
        
        **Localisation**  
        📍 Paris, France
        
        **Disponibilité**  
        🟢 Pour nouvelles opportunités
        """)

# =====================================================
# FOOTER
# =====================================================
st.divider()
st.markdown(
    """
    <div style="text-align:center;color:#666;font-size:0.9rem;padding:1rem 0;">
        <p>© 2024 Martin Alquier – Portfolio Data & IA | 
        <a href="https://github.com/martmartin1103-cyber/martin-portfolio-data" style="color:#667eea;">GitHub</a> | 
        <a href="https://martin-portfolio-data.streamlit.app" style="color:#667eea;">Live Demo</a></p>
    </div>
    """,
    unsafe_allow_html=True
)
