"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import asyncio
import reflex as rx
from openai import OpenAI
import os
from dotenv import load_dotenv

from rxconfig import config

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class State(rx.State):
    tema: str = ""
    texto_insta: str = ""
    texto_linkedin: str = ""
    texto_email: str = ""
    resultado: str = ""
    is_loading: bool = False

    def set_tema(self, valor: str):
        self.tema = valor

    async def gerar_estrategia(self):

        if not self.tema:
            yield rx.window_alert("Por favor, insira um tema.")
            return 
        
        # 2. Ativar o estado de carregamento e limpar resultados anteriores
        self.is_loading = True
        self.texto_insta = ""
        self.texto_linkedin = ""
        self.texto_email = ""
        yield

        try:
            res_insta = ""
            res_linkedin = ""
            res_email = ""

            canais = {
                "Instagram": "Cria uma legenda criativa com emojis para um Post de Instagram. Até 500 caracteres.",
                "LinkedIn": "Escreve um post profissional e focado em autoridade para LinkedIn. Até 700 caracteres",
                "E-mail": "Escreve um e-mail de vendas curto e direto. Até 400 caracteres."
            }

            for canal, instrucao in canais.items():
                # Chamada da API
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": f"Tu és um expert em marketing digital em Portugal. {instrucao}"},
                        {"role": "user", "content": f"O tema é: {self.tema}"}
                    ]
                )
                
                conteudo = response.choices[0].message.content

                if canal == "Instagram":
                    res_insta = conteudo
                elif canal == "LinkedIn":
                    res_linkedin = conteudo
                elif canal == "E-mail":
                    res_email = conteudo
            
            self.is_loading = False

            max_len = max(len(res_insta), len(res_linkedin), len(res_email))

            for i in range(1, max_len + 1):
                # Instagram
                if i < len(res_insta):
                    self.texto_insta = res_insta[:i] + "▌"
                else:
                    self.texto_insta = res_insta # Remove o cursor ao terminar

                # LinkedIn
                if i < len(res_linkedin):
                    self.texto_linkedin = res_linkedin[:i] + "▌"
                else:
                    self.texto_linkedin = res_linkedin

                # E-mail
                if i < len(res_email):
                    self.texto_email = res_email[:i] + "▌"
                else:
                    self.texto_email = res_email
                
                # O yield faz o Reflex atualizar a tela a cada caractere
                yield 
                await asyncio.sleep(0.02) # Velocidade da digitação

        except Exception as e:
            yield rx.window_alert(f"Erro na API: {str(e)}")
            return 
        
        finally:
            self.is_loading = False
            yield

# --- COMPONENTES UI (Estilo Apple) ---

def apple_card(titulo: str, conteudo: str) -> rx.Component:
    return rx.vstack(
        rx.heading(
            titulo, 
            size="3", 
            color="#86868B", # Cinza Apple secundário
            font_weight="600",
            letter_spacing="-0.01em",
            margin_bottom="0.5em"
        ),
        rx.cond(
            State.is_loading & (conteudo == ""),
            skeleton_loader(),
            rx.markdown(
                conteudo, 
                color="#1D1D1F", 
                font_size="0.95em",
                line_height="1.5"
            ),
        ),
        padding="24px",
        bg="white",
        height="100%",
        border_radius="24px", # Cantos mais suaves
        box_shadow="0 4px 20px rgba(0, 0, 0, 0.04)",
        width="360px",
        align_items="start",
        # Pequena animação de entrada para o card em si
        transition="transform 0.2s ease",
        _hover={"transform": "translateY(-2px)"},
    )

def skeleton_loader() -> rx.Component:
    return rx.vstack(
        rx.box(class_name="skeleton-pulse", width="100%", height="12px"),
        rx.box(class_name="skeleton-pulse", width="90%", height="12px"),
        rx.box(class_name="skeleton-pulse", width="95%", height="12px"),
        rx.box(class_name="skeleton-pulse", width="60%", height="12px"),
        spacing="3",
        width="100%",
        margin_top="1em",
    )


def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            # Título principal
            rx.heading("Gerador de Conteúdo ",
                rx.text.span("IA", color="#0066CC"),
                size="9", 
                weight="bold", 
                letter_spacing="-0.02em", 
                color="#1D1D1F",
                text_align="center"),

            rx.text("Transforme ideias em estratégias multicanal com a precisão de um clique.", 
                color="#86868B", 
                size="5",
                text_align="center",
                max_width="600px",
                margin_bottom="1.5em",
            ),
            
            # Input estilizado
            rx.input(
                on_change=State.set_tema,
                placeholder="Ex: Curso de IA para iniciantes em Lisboa",
                color="#1D1D1F",
                width="100%",
                max_width="500px",
                height="3.5em",
                border_radius="14px",
                bg="white",
                border="1px solid #d2d2d7",
                padding_left="1.5em",

                _focus={
                    "border": "1px solid #0066cc", 
                    "box_shadow": "0 0 0 4px rgba(0,102,204,0.1)"
                },

                _hover={"border": "1px solid #A1A1A6"},
            ),
            
            # Botão Azul Apple
            rx.button("Gerar Estratégia Completa",
                on_click=State.gerar_estrategia,
                is_loading=State.is_loading,
                bg="#0066cc",
                color="white",
                size="4",
                _hover={
                    "bg": "#0071e3",
                    "transform": "scale(1.02)",
                },
                _active={"transform": "scale(0.98)"},
                border_radius="14px",
                padding="1.5em 2.5em",
                font_weight="500",
                transition="all 0.2s ease-in-out",
            ),

            # Grid de resultados
            rx.grid(
                apple_card("Instagram", State.texto_insta),
                apple_card("LinkedIn", State.texto_linkedin),
                apple_card("E-mail", State.texto_email),
                columns="3",
                spacing="9",
                width="100%",
                margin_top="2em",
            ),
            align="center",
            spacing="6",
            padding_y="5em",
            width="100%",
            max_width="1100px",
        ),
        bg="#f5f5f7",  # Fundo cinza claro oficial
        width="100%",
        spacing="4",          # Espaço entre os elementos
        padding_y="4em",      # Respiro no topo e fundo
    )

app = rx.App(
    stylesheets=["styles.css"],
)
app.add_page(index)
