# app.py - Version finale pour GitHub et Streamlit Cloud
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# =====================================================
# CONFIG
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
def load_image(image_filename, alt_text="Image"):
    """
    Charge une image depuis le dossier assets/ avec fallback pour GitHub
    """
    # Chemins à essayer (priorité aux chemins locaux)
    possible_paths = [
        f"assets/{image_filename}",  # Chemin principal sur GitHub
        f"images/{image_filename}",  # Alternative
        image_filename,              # Chemin direct
    ]
    
    for path in possible_paths:
        try:
            if os.path.exists(path):
                return path
        except:
            continue
    
    # Fallback avec URLs Unsplash pour le développement
    placeholders = {
        "photo.jpeg": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80",
        "inetum_logo.jpg": "https://images.unsplash.com/photo-1552664730-d307ca884978?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80",
        "zigourrat_logo.jpg": "https://images.unsplash.com/photo-1551434678-e076c223a692?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80",
        "efrei_logo.png": "https://upload.wikimedia.org/wikipedia/fr/thumb/6/6b/Logo_Efrei_Paris.svg/400px-Logo_Efrei_Paris.svg.png",
        "dauphine_logo.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Logo_Universit%C3%A9_Paris-Dauphine.svg/400px-Logo_Universit%C3%A9_Paris-Dauphine.svg.png",
        "metaland_logo.jpg": "https://images.unsplash.com/photo-1553877522-43269d4ea984?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80",
        "certifications.jpg": "https://images.unsplash.com/photo-1532619187608-e5375cab36aa?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80"
    }
    
    return placeholders.get(image_filename, f"https://via.placeholder.com/400x200/667eea/ffffff?text={alt_text.replace(' ', '+')}")

# =====================================================
# CSS PERSONNALISÉ
# =====================================================
def load_custom_css():
    st.markdown("""
    <style>
    /* Style général */
    .main {
        padding: 2rem;
    }
    
    /* Cartes améliorées */
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
    
    .card-secondary {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    
    .card-success {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    
    /* Timeline */
    .timeline {
        position: relative;
        padding-left: 2rem;
    }
    
    .timeline-item {
        position: relative;
        margin-bottom: 2rem;
        padding-left: 1.5rem;
    }
    
    .timeline-item:before {
        content: '';
        position: absolute;
        left: -8px;
        top: 0;
        width: 16px;
        height: 16px;
        border-radius: 50%;
        background: #667eea;
    }
    
    /* Tags compétences */
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
    
    /* Boutons */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
    }
    
    /* Section header */
    .section-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 2rem 0 1rem 0;
    }
    
    /* Cercle pour photo de profil */
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
    
    /* Cadre pour photos d'expérience */
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
    
    /* Cadre pour photos de formation */
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
    
    /* Badges */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 8px;
        margin-bottom: 8px;
    }
    
    .badge-primary {
        background: #eef2ff;
        color: #4f46e5;
    }
    
    .badge-success {
        background: #dcfce7;
        color: #166534;
    }
    
    .badge-warning {
        background: #fef3c7;
        color: #92400e;
    }
    
    /* Card expérience améliorée */
    .experience-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        border-left: 5px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .experience-card:hover {
        box-shadow: 0 12px 30px rgba(0,0,0,0.12);
        transform: translateY(-3px);
    }
    
    /* Card formation améliorée */
    .education-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        border-left: 5px solid #42be65;
        transition: all 0.3s ease;
    }
    
    .education-card:hover {
        box-shadow: 0 12px 30px rgba(0,0,0,0.12);
        transform: translateY(-3px);
    }
    
    /* Responsive */
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
    """

def experience_card_with_image(company, role, duration, description, image_filename, location="Paris, France", 
                               tags=None, achievements=None, company_color="#667eea"):
    
    image_path = load_image(image_filename, alt_text=company)
    
    with st.container():
        # En-tête avec logo/photo
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
            # Cadre pour l'image
            st.markdown('<div class="experience-image-frame">', unsafe_allow_html=True)
            try:
                st.image(image_path, use_container_width=True)
            except:
                # Placeholder avec initiales de l'entreprise
                st.markdown(f"""
                <div style="
                    width: 100%;
                    height: 100%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    background: linear-gradient(135deg, {company_color} 0%, #764ba2 100%);
                    color: white;
                    font-size: 2rem;
                    font-weight: bold;
                ">
                    {company[0:2]}
                </div>
                """, unsafe_allow_html=True)
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
        
        # Tags
        if tags:
            st.markdown("**🔧 Technologies & Compétences :**")
            cols = st.columns(6)
            for i, tag in enumerate(tags):
                with cols[i % 6]:
                    st.markdown(f'<span class="badge badge-primary">{tag}</span>', unsafe_allow_html=True)
        
        # Réalisations avec indicateurs
        if achievements:
            with st.expander(f"🏆 Réalisations chez {company}", expanded=False):
                for idx, achievement in enumerate(achievements):
                    col_a, col_b = st.columns([4, 1])
                    with col_a:
                        st.markdown(f"**{achievement['title']}**")
                        st.markdown(f"{achievement['description']}")
                        if 'metrics' in achievement:
                            for metric in achievement['metrics']:
                                st.markdown(f'<span class="badge badge-success">{metric}</span>', 
                                          unsafe_allow_html=True)
                    with col_b:
                        if 'impact' in achievement:
                            impact_value = achievement['impact']
                            impact_color = "#42be65" if impact_value > 0 else "#da1e28"
                            st.markdown(f"""
                            <div style="
                                background: {impact_color};
                                color: white;
                                padding: 0.5rem;
                                border-radius: 8px;
                                text-align: center;
                                font-weight: bold;
                            ">
                                {f"+{impact_value}%" if impact_value > 0 else f"{impact_value}%"}
                            </div>
                            """, unsafe_allow_html=True)
        
        st.divider()

def education_card_with_image(diploma, school, duration, description, image_filename, 
                             location="Paris, France", specialities=None, honors=None):
    
    image_path = load_image(image_filename, alt_text=school)
    
    with st.container():
        # En-tête avec logo école
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
            # Cadre pour le logo de l'école
            st.markdown('<div class="education-image-frame">', unsafe_allow_html=True)
            try:
                st.image(image_path, use_container_width=True)
            except:
                # Placeholder avec initiales de l'école
                st.markdown(f"""
                <div style="
                    width: 100%;
                    height: 100%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    background: linear-gradient(135deg, #42be65 0%, #00a854 100%);
                    color: white;
                    font-size: 1.5rem;
                    font-weight: bold;
                    padding: 10px;
                ">
                    {school.split()[0][0:2] if len(school.split()) > 0 else "🎓"}
                </div>
                """, unsafe_allow_html=True)
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
        
        # Spécialités
        if specialities:
            st.markdown("**📚 Spécialités & Modules :**")
            cols = st.columns(4)
            for i, speciality in enumerate(specialities):
                with cols[i % 4]:
                    st.markdown(f'''
                    <div style="
                        background: #dcfce7;
                        padding: 0.5rem;
                        border-radius: 8px;
                        text-align: center;
                        margin: 0.2rem;
                        border-left: 3px solid #42be65;
                    ">
                        {speciality}
                    </div>
                    ''', unsafe_allow_html=True)
        
        # Distinctions
        if honors:
            with st.expander("🏅 Distinctions & Projets académiques", expanded=False):
                for honor in honors:
                    col_a, col_b = st.columns([4, 1])
                    with col_a:
                        st.markdown(f"**{honor['title']}**")
                        st.markdown(f"{honor['description']}")
                    with col_b:
                        st.markdown(f'''
                        <div style="
                            background: #fef3c7;
                            padding: 0.5rem;
                            border-radius: 8px;
                            text-align: center;
                            font-weight: bold;
                            color: #92400e;
                        ">
                            {honor.get('year', duration.split('-')[0])}
                        </div>
                        ''', unsafe_allow_html=True)
        
        st.divider()

# =====================================================
# DONNÉES MISES À JOUR POUR LES IMAGES LOCALES
# =====================================================
EXPERIENCES = [
    {
        "company": "INETUM",
        "role": "Consultant Data Analyst",
        "duration": "Sept 2022 - Présent",
        "location": "Paris La Défense, France",
        "description": "Consultant en data analytics pour la Direction Générale et l'Audit Interne. Missions de dashboarding KPI, automatisation des rapports et support décisionnel pour le CODIR.",
        "image_filename": "inetum_logo.png",  # Image dans assets/inetum_logo.png
        "company_color": "#0056b3",
        "tags": ["Power BI", "SQL", "Python", "DataViz", "Process Mining", "Azure", "Tableau", "DAX"],
        "achievements": [
            {
                "title": "Dashboarding Direction Générale",
                "description": "Création de 6 dashboards KPI pour le CODIR couvrant Sales, RH et Coûts",
                "metrics": ["6 Dashboards", "30+ KPI", "12 Datasources"],
                "impact": 30
            },
            {
                "title": "Automatisation des rapports",
                "description": "Automatisation complète du reporting mensuel avec Python et Power BI",
                "metrics": ["Python Scripts", "Power Automate", "SQL Jobs"],
                "impact": 40
            },
            {
                "title": "Formation équipes métier",
                "description": "Formation de 50+ collaborateurs à l'utilisation des outils data",
                "metrics": ["50+ Personnes", "10 Sessions", "95% Satisfaction"],
                "impact": 95
            }
        ]
    },
    {
        "company": "Zigourrat",
        "role": "Consultant Digital Innovation",
        "duration": "Mars 2021 - Août 2022",
        "location": "Paris, France",
        "description": "Consultant en innovation digitale et Web3.0. Analyse marketing data et recommandations stratégiques pour clients du secteur tech.",
        "image_filename": "zigourrat_logo.jpg",  # Image dans assets/zigourrat_logo.jpg
        "company_color": "#FF6B6B",
        "tags": ["Web3", "Marketing Analytics", "Growth", "Blockchain", "SEO/SEA", "CRM"],
        "achievements": [
            {
                "title": "Stratégie Web3",
                "description": "Mise en place de stratégies Web3 pour 3 clients avec suivi KPI",
                "metrics": ["3 Clients", "Web3 Strategy", "NFT Projects"],
                "impact": 50
            },
            {
                "title": "Optimisation acquisition",
                "description": "Optimisation des campagnes marketing digital avec analyse ROI",
                "metrics": ["ROI +45%", "CAC -30%", "LTV +25%"],
                "impact": 45
            }
        ]
    },
    {
        "company": "MetaLand",
        "role": "Founder & CEO",
        "duration": "Jan 2020 - Fév 2021",
        "location": "Remote & Paris",
        "description": "Fondation et direction d'une startup dans le domaine du métaverse. Gestion produit, stratégie growth et analyse data.",
        "image_filename": "metaland_logo.jpg",  # Image dans assets/metaland_logo.jpg
        "company_color": "#9D4EDD",
        "tags": ["Product Management", "Startup", "Growth Hacking", "KPI", "CRM", "SEO/SEA"],
        "achievements": [
            {
                "title": "Lancement produit MVP",
                "description": "Lancement du MVP avec 1000 utilisateurs actifs en 3 mois",
                "metrics": ["1000 Users", "MVP Launch", "Product-Market Fit"],
                "impact": 120
            },
            {
                "title": "Levée de fonds",
                "description": "Levée de 150K€ auprès de business angels",
                "metrics": ["150K€ Raised", "3 Angels", "6 Months Runway"],
                "impact": 150
            }
        ]
    }
]

EDUCATIONS = [
    {
        "diploma": "Master en Data Science & Business Analytics",
        "school": "EFREI Paris - Grande École du Numérique",
        "duration": "2020 - 2022",
        "location": "Paris, France",
        "description": "Formation d'excellence en Data Science avec double compétence business et technique. Spécialisation en Machine Learning, Big Data et Intelligence Artificielle.",
        "image_filename": "efrei_logo.png",  # Image dans assets/efrei_logo.png
        "specialities": [
            "Machine Learning", 
            "Big Data & Hadoop", 
            "Deep Learning", 
            "Data Visualization",
            "Business Intelligence",
            "Cloud Computing",
            "Data Engineering",
            "Statistical Analysis"
        ],
        "honors": [
            {
                "title": "Prix du meilleur projet Data",
                "description": "Projet de prédiction de fraude avec 95% de précision",
                "year": "2022"
            },
            {
                "title": "Hackathon Data for Good",
                "description": "1ère place au hackathon sur l'optimisation des dons alimentaires",
                "year": "2021"
            }
        ]
    },
    {
        "diploma": "Bachelor Business & Management",
        "school": "Université Paris-Dauphine | PSL",
        "duration": "2017 - 2020",
        "location": "Paris, France",
        "description": "Formation en gestion d'entreprise avec spécialisation en finance et stratégie. Double compétence quantitative et managériale.",
        "image_filename": "dauphine_logo.jpg",  # Image dans assets/dauphine_logo.jpg
        "specialities": [
            "Corporate Finance", 
            "Business Strategy", 
            "Marketing Analytics", 
            "Entrepreneurship",
            "Project Management",
            "Econometrics",
            "Digital Transformation"
        ],
        "honors": [
            {
                "title": "Mention Très Bien",
                "description": "Diplôme obtenu avec mention Très Bien (16,5/20)",
                "year": "2020"
            },
            {
                "title": "Projet entrepreneurial",
                "description": "Création d'une marketplace étudiante avec 500 utilisateurs",
                "year": "2019"
            }
        ]
    },
    {
        "diploma": "Certifications Professionnelles",
        "school": "Microsoft, Google, Scrum.org",
        "duration": "2021 - 2023",
        "location": "En ligne & Paris",
        "description": "Certifications techniques et métier complémentaires pour renforcer l'expertise data et management.",
        "image_filename": "certifications.jpg",  # Image dans assets/certifications.jpg
        "specialities": [
            "Microsoft Certified: Data Analyst Associate", 
            "Google Analytics Individual Qualification", 
            "Certified ScrumMaster®", 
            "Azure Fundamentals",
            "Power BI Data Analyst",
            "Tableau Desktop Specialist"
        ],
        "honors": [
            {
                "title": "Top 10% Microsoft Exam",
                "description": "Score de 925/1000 à l'examen PL-300",
                "year": "2023"
            }
        ]
    }
]

PROJECTS = [
    {
        "title": "Système de prédiction des coûts logistiques",
        "client": "Dassault Systèmes x Mistral AI",
        "description": "IA prédictive pour l'optimisation de la supply chain",
        "technologies": ["Python", "Scikit-learn", "Mistral AI", "Streamlit"],
        "link": "#"
    },
    {
        "title": "Plateforme de mentoring start-up",
        "client": "Kryptosphere Accelerator",
        "description": "Accompagnement de 12 start-up en stratégie data",
        "technologies": ["Business Strategy", "Data Architecture", "KPI Design"],
        "link": "#"
    }
]

SKILLS_DATA = {
    "Techniques": ["Python", "SQL", "Power BI", "Tableau", "Excel", "Git"],
    "Business": ["Analyse KPI", "Product Management", "Stratégie", "Reporting", "Agile"],
    "Soft Skills": ["Communication", "Leadership", "Problem Solving", "Teamwork"]
}

# =====================================================
# GRAPHIQUES AMÉLIORÉS
# =====================================================
def radar_competences():
    skills = {
        "Analyse Business": 90,
        "Data Analysis": 85,
        "KPI & Reporting": 90,
        "Product / Agile": 80,
        "IA & Innovation": 75,
        "Stratégie": 85,
        "Visualisation": 88
    }

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=list(skills.values()),
        theta=list(skills.keys()),
        fill="toself",
        fillcolor="rgba(102, 126, 234, 0.6)",
        line=dict(color="rgb(102, 126, 234)", width=2),
        name="Compétences"
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=10)
            ),
            bgcolor="rgba(245, 247, 255, 0.5)"
        ),
        showlegend=False,
        margin=dict(l=40, r=40, t=40, b=40),
        height=300,
        paper_bgcolor="rgba(0,0,0,0)"
    )

    return fig

def create_revenue_chart():
    df = pd.DataFrame({
        "Mois": ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin", "Juil", "Août", "Sep", "Oct", "Nov", "Déc"],
        "Revenu": [180, 195, 210, 220, 240, 250, 260, 270, 280, 290, 300, 310],
        "Coûts": [120, 115, 110, 115, 120, 125, 130, 135, 140, 145, 150, 155],
        "Marge": [60, 80, 100, 105, 120, 125, 130, 135, 140, 145, 150, 155]
    })
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df["Mois"],
        y=df["Revenu"],
        name="Revenu",
        marker_color="#667eea"
    ))
    fig.add_trace(go.Scatter(
        x=df["Mois"],
        y=df["Marge"],
        name="Marge",
        line=dict(color="#42be65", width=3),
        yaxis="y2"
    ))
    
    fig.update_layout(
        title="Évolution des revenus et marges",
        xaxis_title="Mois",
        yaxis_title="Revenu (K€)",
        yaxis2=dict(
            title="Marge (K€)",
            overlaying="y",
            side="right"
        ),
        height=400,
        plot_bgcolor="rgba(245, 247, 255, 0.5)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    
    return fig

# =====================================================
# SIDEBAR – PROFIL
# =====================================================
with st.sidebar:
    # Photo de profil avec effet
    profile_image = load_image("photo.jpeg", alt_text="Martin Alquier")
    st.markdown('<div class="profile-circle">', unsafe_allow_html=True)
    st.image(profile_image, use_container_width=True)
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
    
    # Compétences radar
    st.markdown("### 📊 Compétences")
    st.plotly_chart(radar_competences(), use_container_width=True, config={'displayModeBar': False})
    
    # Tags compétences
    st.markdown("#### 🔧 Technologies")
    cols = st.columns(3)
    tech_skills = ["Python", "SQL", "Power BI", "Tableau", "Excel", "Git"]
    for i, skill in enumerate(tech_skills):
        with cols[i % 3]:
            st.markdown(f'<span class="skill-tag">{skill}</span>', unsafe_allow_html=True)
    
    st.divider()
    
    # Contact sidebar
    st.markdown("### 📱 Contact")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/martinalquier)")
    with col2:
        st.markdown("[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/martinalquier)")
    with col3:
        st.markdown("[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:martin.alquier@business.com)")
    
    st.divider()
    
    # Logo école
    try:
        efrei_logo = load_image("efrei_logo.png", alt_text="EFREI Paris")
        st.image(efrei_logo, use_container_width=True)
    except:
        pass

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
    
    st.divider()
    
    # Dernières réalisations
    st.markdown("### 🌟 Dernières réalisations")
    cols = st.columns(3)
    with cols[0]:
        st.markdown(kpi_card("Gain d'efficacité", "+30%", "Automatisation reporting", "#667eea", "⚡", 12), 
                   unsafe_allow_html=True)
    with cols[1]:
        st.markdown(kpi_card("Satisfaction client", "95%", "NPS augmenté", "#42be65", "😊", 15), 
                   unsafe_allow_html=True)
    with cols[2]:
        st.markdown(kpi_card("Réduction coûts", "-18%", "Optimisation supply chain", "#f1c21b", "💰", -8), 
                   unsafe_allow_html=True)

# -----------------------------------------------------
elif page == "🏢 Expériences":
    st.title("🏢 Parcours Professionnel")
    
    # Introduction avec statistiques
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
    
    # Timeline des expériences avec images
    for exp in EXPERIENCES:
        experience_card_with_image(
            company=exp["company"],
            role=exp["role"],
            duration=exp["duration"],
            location=exp["location"],
            description=exp["description"],
            image_filename=exp["image_filename"],
            company_color=exp["company_color"],
            tags=exp["tags"],
            achievements=exp["achievements"]
        )
    
    # Section témoignages ou références
    st.markdown("### 💬 Témoignages")
    with st.expander("Voir les recommandations", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div style="
                background: #f8f9fa;
                padding: 1.5rem;
                border-radius: 10px;
                margin: 1rem 0;
                border-left: 4px solid #667eea;
            ">
                <p style="font-style: italic; color: #555;">
                "Martin a transformé notre approche data avec des dashboards qui sont devenus indispensables à notre prise de décision quotidienne."
                </p>
                <p style="text-align: right; font-weight: bold; color: #333;">
                — Directeur Général, INETUM
                </p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div style="
                background: #f8f9fa;
                padding: 1.5rem;
                border-radius: 10px;
                margin: 1rem 0;
                border-left: 4px solid #42be65;
            ">
                <p style="font-style: italic; color: #555;">
                "Une vision stratégique exceptionnelle couplée à une expertise technique solide. Un partenaire idéal pour nos projets d'innovation."
                </p>
                <p style="text-align: right; font-weight: bold; color: #333;">
                — CEO, Zigourrat
                </p>
            </div>
            """, unsafe_allow_html=True)

# -----------------------------------------------------
elif page == "📂 Projets":
    st.title("📂 Portfolio de Projets")
    
    # Filtres
    col1, col2, col3 = st.columns(3)
    with col1:
        category = st.selectbox("Filtrer par catégorie", ["Tous", "Data Science", "Business Intelligence", "IA/ML", "Stratégie"])
    with col2:
        year = st.selectbox("Année", ["Toutes", "2024", "2023", "2022"])
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        show_details = st.checkbox("Afficher détails", value=True)
    
    # Grille de projets
    st.markdown("### 🚀 Projets récents")
    for project in PROJECTS:
        with st.container():
            st.markdown(f"#### {project['title']}")
            st.markdown(f"**Client :** {project['client']}")
            st.markdown(project['description'])
            
            st.markdown("**Technologies :**")
            for tech in project['technologies']:
                st.markdown(f'<span class="skill-tag">{tech}</span>', unsafe_allow_html=True)
            
            if project['link'] != "#":
                st.markdown(f"[🔗 Voir le projet]({project['link']})")
            
            st.divider()

# -----------------------------------------------------
elif page == "📈 Dashboard":
    st.title("📈 Tableau de Bord Business")
    
    # Filtres période
    col1, col2, col3 = st.columns(3)
    with col1:
        period = st.selectbox("Période", ["Année 2024", "Trimestre en cours", "Mois en cours"])
    with col2:
        metric = st.selectbox("Métrique principale", ["Revenu", "Marge", "NPS", "Coûts"])
    with col3:
        comparison = st.selectbox("Comparaison", ["vs année précédente", "vs cible", "vs benchmark"])
    
    # KPI Principaux
    st.markdown("### 🎯 Indicateurs Clés")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(kpi_card("Revenu Mensuel", "210 K€", "+12% vs M-1", "#667eea", "💰", 12), 
                   unsafe_allow_html=True)
    with col2:
        st.markdown(kpi_card("Marge Brute", "32%", "+4 pts", "#42be65", "📈", 4), 
                   unsafe_allow_html=True)
    with col3:
        st.markdown(kpi_card("NPS Client", "85", "+5 pts", "#f1c21b", "😊", 5), 
                   unsafe_allow_html=True)
    with col4:
        st.markdown(kpi_card("Coûts Opérationnels", "110 K€", "-8%", "#da1e28", "📉", -8), 
                   unsafe_allow_html=True)
    
    # Graphiques
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(create_revenue_chart(), use_container_width=True)
    
    with col2:
        # Données sectorielles
        sector_data = pd.DataFrame({
            "Secteur": ["Tech", "Finance", "Retail", "Health", "Manufacturing"],
            "CA": [45, 30, 15, 25, 20],
            "Croissance": [12, 8, 5, 15, 7]
        })
        
        fig = px.bar(sector_data, x="Secteur", y="CA", 
                    title="Chiffre d'affaires par secteur",
                    color="Croissance",
                    color_continuous_scale="Viridis")
        fig.update_layout(height=400, plot_bgcolor="rgba(245, 247, 255, 0.5)")
        st.plotly_chart(fig, use_container_width=True)
    
    # Tableau détaillé
    st.markdown("### 📊 Données détaillées")
    df = pd.DataFrame({
        "Mois": ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin"],
        "Revenu": [180, 195, 210, 220, 240, 250],
        "Coûts": [120, 115, 110, 115, 120, 125],
        "Marge %": [33, 41, 48, 48, 50, 50],
        "NPS": [75, 78, 82, 83, 85, 85],
        "Clients": [45, 48, 52, 55, 58, 60]
    })
    
    st.dataframe(df.style.background_gradient(subset=["Marge %"], cmap="YlGn"), 
                use_container_width=True)

# -----------------------------------------------------
elif page == "🛠️ Compétences":
    st.title("🛠️ Compétences & Expertise")
    
    # Radar des compétences
    col1, col2 = st.columns([2, 1])
    with col1:
        st.plotly_chart(radar_competences(), use_container_width=True)
    with col2:
        st.markdown("### 📊 Niveau d'expertise")
        st.metric("Data Analysis", "Expert", "+2%")
        st.metric("Business Strategy", "Avancé", "+5%")
        st.metric("Data Visualization", "Expert", "+3%")
        st.metric("Machine Learning", "Intermédiaire", "+8%")
    
    # Grille des compétences
    for category, skills in SKILLS_DATA.items():
        st.markdown(f'<div class="section-header">{category}</div>', unsafe_allow_html=True)
        cols = st.columns(6)
        for i, skill in enumerate(skills):
            with cols[i % 6]:
                st.markdown(f'<div style="text-align:center;padding:0.5rem;background:#f8f9fa;border-radius:8px;margin:0.2rem;">{skill}</div>', unsafe_allow_html=True)
    
    # Certifications
    st.markdown("### 🏆 Certifications")
    certs = st.columns(3)
    with certs[0]:
        st.markdown("""
        <div style="background:white;padding:1rem;border-radius:10px;box-shadow:0 4px 12px rgba(0,0,0,0.08);">
            <h4 style="color:#333;">Microsoft Certified</h4>
            <p style="color:#666;font-size:0.9rem;">Data Analyst Associate</p>
            <p style="color:#667eea;font-size:0.8rem;">Obtenu : 2023</p>
        </div>
        """, unsafe_allow_html=True)
    with certs[1]:
        st.markdown("""
        <div style="background:white;padding:1rem;border-radius:10px;box-shadow:0 4px 12px rgba(0,0,0,0.08);">
            <h4 style="color:#333;">Google Analytics</h4>
            <p style="color:#666;font-size:0.9rem;">Individual Qualification</p>
            <p style="color:#667eea;font-size:0.8rem;">Obtenu : 2022</p>
        </div>
        """, unsafe_allow_html=True)
    with certs[2]:
        st.markdown("""
        <div style="background:white;padding:1rem;border-radius:10px;box-shadow:0 4px 12px rgba(0,0,0,0.08);">
            <h4 style="color:#333;">Scrum Master</h4>
            <p style="color:#666;font-size:0.9rem;">Certified ScrumMaster®</p>
            <p style="color:#667eea;font-size:0.8rem;">Obtenu : 2021</p>
        </div>
        """, unsafe_allow_html=True)

# -----------------------------------------------------
elif page == "🎓 Formation":
    st.title("🎓 Formation & Éducation")
    
    # Introduction avec statistiques
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
    
    # Timeline des formations avec images
    for edu in EDUCATIONS:
        education_card_with_image(
            diploma=edu["diploma"],
            school=edu["school"],
            duration=edu["duration"],
            location=edu["location"],
            description=edu["description"],
            image_filename=edu["image_filename"],
            specialities=edu["specialities"],
            honors=edu["honors"]
        )

# -----------------------------------------------------
elif page == "📄 Contact":
    st.title("📄 Contactez-moi")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 💬 Discutons de votre projet
        
        Vous avez un projet data, besoin d'un dashboard, ou souhaitez optimiser vos processus ?
        Prenons le temps d'échanger sur vos besoins.
        """)
        
        with st.form("contact_form"):
            name = st.text_input("Nom complet")
            email = st.text_input("Email")
            company = st.text_input("Entreprise")
            subject = st.selectbox("Sujet", [
                "Demande de conseil",
                "Projet Data/BI",
                "Opportunité professionnelle",
                "Autre"
            ])
            message = st.text_area("Message", height=150)
            
            submitted = st.form_submit_button("📤 Envoyer le message")
            if submitted:
                st.success("✅ Message envoyé ! Je vous répondrai dans les 24h.")
    
    with col2:
        st.markdown("""
        ### 📍 Informations de contact
        
        **Email professionnel**  
        martin.alquier@business.com
        
        **Téléphone**  
        +33 6 XX XX XX XX
        
        **Localisation**  
        📍 Paris, France
        
        **Disponibilité**  
        🟢 Disponible pour de nouvelles opportunités
        """)
        
        st.divider()
        
        st.markdown("### 🔗 Liens")
        st.markdown("""
        [![LinkedIn](https://img.shields.io/badge/-LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/martinalquier)
        [![GitHub](https://img.shields.io/badge/-GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/martinalquier)
        [![Tableau Public](https://img.shields.io/badge/-Tableau-E97627?style=for-the-badge&logo=tableau&logoColor=white)](https://public.tableau.com/)
        """)

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
            <p style="font-size:0.8rem;">
            <a href="https://github.com/martmartin1103-cyber/martin-portfolio-data" style="color:#667eea;text-decoration:none;">
                📂 GitHub Repository
            </a> | 
            <a href="https://martin-portfolio-data.streamlit.app" style="color:#667eea;text-decoration:none;">
                🌐 Live Demo
            </a>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
