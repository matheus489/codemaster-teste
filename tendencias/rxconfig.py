import reflex as rx

config = rx.Config(
    app_name="tendencias",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)