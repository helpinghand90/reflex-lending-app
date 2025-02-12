"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config

from lending_app import ui


def home_page() -> rx.Component:
    # Welcome Page (Index)
    return ui.base_layout(
        rx.vstack(
            rx.hstack(
                rx.box(width="10%"),
                rx.box(
                    rx.heading("Welcome to Reflex GPT!", size="9"),
                    rx.text(
                        "Get started by editing something like ",
                        rx.code(f"{config.app_name}/{config.app_name}.py"),
                        size="5",
                    ),
                    rx.link(
                        rx.button("Check out our docs!"),
                        href="https://reflex.dev/docs/getting-started/introduction/",
                        is_external=True,
                    ),
                    width="80%",
                ),
                rx.box(width="10%"),
                width="100%",
            ),
            rx.box(height="5vh"),
            rx.divider(),
            rx.box(height="5vh"),
            rx.hstack(
                rx.box(
                    rx.heading("Welcome to Part 2!", size="9", text_align="center"),
                    rx.text(
                        "lets keep going",
                        size="5",
                        text_align="center",
                    ),
                    width="100%",
                    text_align="center",
                ),
                width="100%",
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
            id="home-vstack",
            width="100%",  # Ensure full width
        ),
    )
