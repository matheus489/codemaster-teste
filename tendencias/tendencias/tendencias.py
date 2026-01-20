import reflex as rx
from bs4 import BeautifulSoup
import requests 
import os
from openai import OpenAI
from dotenv import load_dotenv
import re

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class TagCloud(rx.Component):
    # Definimos a biblioteca npm que o Reflex deve instalar
    library = "react-tagcloud"
    # O nome do componente dentro da biblioteca
    tag = "TagCloud"
    
    # As propriedades (props) que o componente aceita
    min_size: rx.Var[int]
    max_size: rx.Var[int]
    tags: rx.Var[list[dict]]
    color_options: rx.Var[dict]
    
    # Evento opcional para quando se clica numa palavra
    def on_click(self, tag):
        return rx.console_log(f"Clicou em: {tag['value']}")

# Criamos um atalho fácil para usar o componente
tag_cloud = TagCloud.create

class TrendState(rx.State):
    urls: list[str] = ["", "", ""]
    cloud_data: list[dict[str, int]] = []
    is_analyzing: bool = False
    keywords: list[dict[str, str]] = []

    def set_url(self, index: int, value: str):
        self.urls[index] = value

    async def analisar_tendencias(self):
        # Validação: Pelo menos um link preenchido
        if not any(url.strip() for url in self.urls):
            yield rx.window_alert("Por favor, insira pelo menos um link válido.")
            return

        self.is_analyzing = True
        self.keywords = []
        yield

        texto_geral = ""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        try:
            # 1. Raspagem dos Links
            for url in self.urls:
                if url.strip():
                    try:
                        response = requests.get(url, headers=headers, timeout=10)
                        response.raise_for_status()
                        soup = BeautifulSoup(response.text, "html.parser")
                        
                        # Pegamos o texto de parágrafos e títulos para evitar menus/rodapés
                        paragraphs = soup.find_all(['p', 'h1', 'h2', 'h3'])
                        texto_geral += " ".join([p.get_text() for p in paragraphs])
                    except Exception as e:
                        print(f"Erro ao ler {url}: {e}")

            if len(texto_geral) < 100:
                yield rx.window_alert("Não foi possível extrair conteúdo suficiente dos links.")
                return

            # 2. Chamada à OpenAI para extrair termos quentes
            # Limitamos o texto para não estourar os tokens (ex: 12.000 caracteres)
            prompt_contexto = texto_geral[:12000]
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Age como um analista de tendências de mercado. Analisa o texto e identifica as 30 palavras-chave ou conceitos mais relevantes. Retorna EXATAMENTE no formato: palavra:peso, palavra:peso. O peso deve ser de 1 a 10 (importância). Exemplo: IA:10, Apple:8, Design:5..."},
                    {"role": "user", "content": f"Analisa estas tendências: {prompt_contexto}"}
                ]
            )

            raw_output = response.choices[0].message.content
            processed_data = []

            for item in raw_output.split(","):
                if ":" in item:
                    partes = item.split(":")
                    if len(partes) >= 2:
                        word = partes[0].strip()
                        peso_bruto = partes[1].strip()
                        
                        # --- LIMPEZA COM REGEX ---
                        # \D remove tudo o que NÃO for um dígito (0-9)
                        peso_limpo = re.sub(r'\D', '', peso_bruto)
                        
                        # Converte apenas se sobrou algum número, senão usa 1
                        val_count = int(peso_limpo) if peso_limpo else 1
                        
                        # Formata para o react-tagcloud (value e count)
                        processed_data.append({
                            "value": word,
                            "count": val_count * 5 # Multiplicamos para o tamanho ser visível
                        })
                
            self.cloud_data = processed_data
            self.is_analyzing = False

        except Exception as e:
            yield rx.window_alert(f"Erro na análise: {str(e)}")
        
        finally:
            self.is_analyzing = False
            yield

# def classic_word_tag(tag: rx.Var) -> rx.Component:
#     # Lógica de peso (mesma de antes)
#     is_hot = tag["size"].contains("10") | tag["size"].contains("9") | tag["size"].contains("8")
    
#     return rx.text(
#         tag["text"],
#         style={
#             "font_size": tag["size"],
#             "font_weight": rx.cond(is_hot, "800", "400"),
#             # Cores variadas para um look de "nuvem"
#             "color": rx.cond(
#                 is_hot, 
#                 "#0066CC", # Destaque azul
#                 "#86868B"  # Cinza secundário
#             ),
#             # "transition": "all 0.2s ease",
#             # "_hover": {
#             #     "color": "#00B2FF",
#             #     "transform": "scale(1.2)",
#             #     "cursor": "pointer"
#             # },
#             # Opcional: Algumas palavras rotacionadas para efeito visual
#         }
#     )

def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            # Título Estilo Apple
            rx.vstack(
                rx.heading(
                    "Monitor de ", 
                    rx.text.span("Tendências", color="#0066CC"), 
                    size="9", weight="bold", letter_spacing="-0.04em"
                ),
                rx.text("Rastreie o mercado através de links estratégicos.", color="#86868B", size="4"),
                align="center",
                spacing="2",
                color="#1C1C1E",
            ),

            # Inputs
            rx.vstack(
                rx.input(placeholder="URL 01", on_change=lambda v: TrendState.set_url(0, v), **input_style),
                rx.input(placeholder="URL 02", on_change=lambda v: TrendState.set_url(1, v), **input_style),
                rx.input(placeholder="URL 03", on_change=lambda v: TrendState.set_url(2, v), **input_style),
                width="100%",
                max_width="500px",
                spacing="3",
            ),

            rx.button(
                "Analisar Agora",
                on_click=TrendState.analisar_tendencias,
                is_loading=TrendState.is_analyzing,
                width="100%", max_width="500px",
                bg="#0066CC", color="white", border_radius="12px",
                height="3em", font_weight="500",
                _hover={"bg": "#0071e3", "transform": "scale(1.01)"},
            ),

            # Nuvem de Palavras (Cards de Badges)
            rx.cond(
                TrendState.cloud_data,
                rx.box(
                    tag_cloud(
                        tags=TrendState.cloud_data,
                        min_size=12,
                        max_size=45,
                        # Opções de cores no estilo Apple (Tons de azul e cinza)
                        color_options={
                            "luminosity": "dark",
                            "hue": "blue",
                        },
                    ),
                    width="100%",
                )
            ),
            
            align="center",
            width="100%",
            max_width="1000px",
        ),
        width="100%",
        min_height="100vh",
        bg="#F5F5F7",
    )

# Estilo reutilizável para os inputs
input_style = dict(
    color="#1C1C1E",
    height="3.5em",
    border_radius="12px",
    width="100%",
    bg="white",
    border="1px solid #d2d2d7",
    padding_left="1em",
    _focus={"border": "1px solid #0066cc", "box_shadow": "0 0 0 4px rgba(0,102,204,0.1)"},
)


app = rx.App(
    theme=rx.theme(
        appearance="light",
    ),
    stylesheets=[
        "styles.css",
    ],
)
app.add_page(index, title="Monitor de Tendências") 
