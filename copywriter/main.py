import streamlit as st
from openai import OpenAI
import time

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');

    /* Fonte e fundo geral */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #1D1D1F;
    }
            
    /* 4. Bloquear a borda padrão que o Streamlit coloca ao redor dos inputs */
    div[data-baseweb="input"] {
        border: none !important;
        background-color: transparent !important;
    }

    /* Estilizar o Container Principal */
    .stApp {
        background-color: #F5F5F7;
    }

    /* Estilizar Botões */
    .stButton>button {
        
        border-radius: 12px;
        padding: 10px 24px;
        font-weight: 500;
        border: none;
        background-color: #0066CC;
        color: white;
        transition: all 0.2s ease;
    }
    
    .stButton>button:hover {
        background-color: #0071E3;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3);
    }
            
    /* Estilização Principal do Campo de Entrada */
    .stTextInput input {
        border-radius: 12px !important;
        border: 1px solid #D1D1D6 !important;
        background-color: #FFFFFF !important;
        padding: 12px 16px !important; /* Respiro interno */
        font-size: 1rem !important;
        color: #1D1D1F !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: inset 0 1px 4px rgba(0,0,0,0.02) !important; /* Profundidade subtil */
    }

    /* Efeito ao passar o rato (Hover) */
    .stTextInput input:hover {
        border-color: #A1A1A6 !important;
    }

    /* Efeito ao clicar (Focus) */
    .stTextInput input:focus {
        border-color: #0066CC !important;
        box-shadow: 0 0 0 4px rgba(0, 102, 204, 0.15) !important;
        outline: none !important;
        background-color: #FFFFFF !important;
    }

    /* Estilização do Label (Título) */
    .stTextInput label p {
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        color: #86868B !important;
        letter-spacing: -0.01em !important;
    }

    /* Estilo do Placeholder */
    .stTextInput input::placeholder {
        color: #A1A1A6 !important;
        font-weight: 400;
    }      

    /* Títulos e Subtítulos */
    h1 {
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
        color: #1D1D1F !important;
    }
    
    h3 {
        color: #1D1D1F !important;
        font-weight: 600 !important;
        font-size: 1.2rem !important;
    }   

    /* Feedback de sucesso */
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
    }
    
    /* Centralizar o botão primário */
    div.stButton {
        text-align: center;
        margin-top: 20px;
    }

    /* Ajuste nos títulos dentro dos cards */
    .stMarkdown h3 {
        font-size: 1.1rem !important;
        letter-spacing: -0.01em !important;
        margin-bottom: 15px !important;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    /* Força o container do spinner a ser invisível e centralizado */
    .stSpinner {
        text-align: center !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        padding: 20px !important;
        background: transparent !important;
    }
    
    .stSpinner > div {
        border-top-color: #0066CC !important; /* Azul Apple */
    }
    </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="Codemasters | AI Copywriter", layout="wide", page_icon="✍️")

try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception as e:
    st.error(f"Erro ao ler a Chave API: {e}")
    st.stop()

# --- HEADER ESTILO APPLE ---
st.markdown("""
    <div style="text-align: center; padding: 40px 0px 20px 0px;">
        <h1 style="font-size: 3.5rem; font-weight: 700; letter-spacing: -0.05em; margin-bottom: 10px;">
            Gerador de Conteúdo <span style="color: #0066CC;">AI</span>
        </h1>
        <p style="font-size: 1.5rem; color: #86868B; font-weight: 400; max-width: 600px; margin: 0 auto 40px auto; line-height: 1.4;">
            Transforme ideias em estratégias multicanal com a precisão de um clique.
        </p>
    </div>
    """, unsafe_allow_html=True)

# --- INPUT AREA EM CARD ---
col_space1, col_input, col_space2 = st.columns([1, 2, 1])

with col_input:
    tema = st.text_input(
        "O que vamos criar hoje?", 
        placeholder="Ex: Curso de IA em Lisboa para empreendedores...",
        help="Insira o tema principal ou o link do seu produto."
    )

col_btn_1, col_btn_2, col_btn_3 = st.columns([1, 0.6, 1])

with col_btn_2:
    gerar = st.button("Gerar Estratégia Completa", type="primary", use_container_width=True)

if gerar:
    if not tema:
        st.warning("Por favor, insira um tema para gerar o conteúdo.")
    else:

        status_zone = st.container().empty()
        
        try:
            with status_zone:
                with st.spinner("A criar a sua estratégia...", ):
                    canais = {
                        "Instagram": "Cria uma legenda criativa com emojis para um Post de Instagram. Até 500 caracteres.",
                        "LinkedIn": "Escreve um post profissional e focado em autoridade para LikedIn. Até 700 caracteres",
                        "E-mail": "Escreve um e-mail de vendas curto e direto. Até 400 caracteres."
                    }
                    
                    resultados = {}

                    for i, (canal, instrucao) in enumerate(canais.items()):
                        # Chamada da API
                        response = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[
                                {"role": "system", "content": f"Tu és um expert em marketing digital em Portugal. {instrucao}"},
                                {"role": "user", "content": f"O tema é: {tema}"}
                            ]
                        )
                        
                        resultados[canal] = response.choices[0].message.content

            status_zone.container().empty()  # Limpa o spinner
            # Criamos as 3 colunas visualmente
            col1, col2, col3 = st.columns(3, gap="medium",)
            
            # Apple Style: Usamos containers que o CSS acima vai estilizar
            with col1:
                box1 = st.container(border=True)
                box1.subheader("📱 Instagram")
                ph1 = box1.empty()

            with col2:
                box2 = st.container(border=True)
                box2.subheader("💼 LinkedIn")
                ph2 = box2.empty()

            with col3:
                box3 = st.container(border=True)
                box3.subheader("📧 E-mail")
                ph3 = box3.empty()

            texto_insta = resultados["Instagram"]
            texto_linkedin = resultados["LinkedIn"]
            texto_email = resultados["E-mail"]

            max_len = max(len(texto_insta), len(texto_linkedin), len(texto_email))

            for i in range(max_len + 1):
                # Atualiza Instagram se ainda houver letras
                if i <= len(texto_insta):
                        # Mostra o texto até ao índice atual + o cursor visual
                    ph1.markdown(texto_insta[:i] + "▌")
                
                # Atualiza LinkedIn se ainda houver letras
                if i <= len(texto_linkedin):
                    ph2.markdown(texto_linkedin[:i] + "▌")
                    
                # Atualiza E-mail se ainda houver letras
                if i <= len(texto_email):
                    ph3.markdown(texto_email[:i] + "▌")
                
                # A pausa acontece UMA vez por ciclo de atualização das 3 caixas
                time.sleep(0.01) # Ajuste a velocidade aqui
            
            ph1.markdown(texto_insta)
            ph2.markdown(texto_linkedin)
            ph3.markdown(texto_email)

            st.success("Estratégia gerada com sucesso!")

        except Exception as e:
            st.error(f"Ocorreu um erro na API: {e}")
            st.info("Verifica se a tua chave OpenAI tem saldo ou se o limite de tokens foi atingido.")