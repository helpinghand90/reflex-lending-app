import reflex as rx

from .navbar import base_navbar
from .footer import base_footer

def base_layout(*args, **kwargs) -> rx.Component:
    return rx.box(
        base_navbar(),
        rx.vstack(
            rx.fragment(
                *args,
                **kwargs,
            ),
            width='100%',
            max_width='100%',
            padding='0',
        ),
        base_footer(),
        id='my-base-container',
        width='100%',
        max_width='100%',
        padding='0',
    )