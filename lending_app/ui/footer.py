import reflex as rx


def footer_item(text: str, href: str) -> rx.Component:
    return rx.link(
        rx.text(text, size="3"),
        href=href,
    )


def footer_items_customer_service() -> rx.Component:
    return rx.flex(
        rx.heading("Customer Service", size="4", weight="bold", as_="h3"),
        footer_item("How It Works", "/how_it_works"),
        footer_item("Frequently Asked Questions", "/faqs"),
        footer_item("Contact", "/contact"),
        footer_item("About Us", "/about"),
        spacing="4",
        text_align=["center", "center", "start"],
        flex_direction="column",
    )


def footer_items_legal() -> rx.Component:
    return rx.flex(
        rx.heading("Legal", size="4", weight="bold", as_="h3"),
        footer_item("Credit Guide", "/credit_guide"),
        footer_item("Target Market Determination", "/target_market"),
        footer_item("Warning About Borrowing", "/warning_borrowing"),
        footer_item("Electronic Authorisation", "/electronic_authorisation"),
        footer_item("Privacy Policy & Credit Check Consent", "/privacy_policy"),
        footer_item("Website Ts & Cs", "/website_tandc"),
        footer_item("Complaints", "/complaints"),
        spacing="4",
        text_align=["center", "center", "start"],
        flex_direction="column",
    )


# def social_link(icon: str, href: str) -> rx.Component:
#     return rx.link(rx.icon(icon), href=href)


# def socials() -> rx.Component:
#     return rx.flex(
#         social_link("instagram", "/#"),
#         social_link("twitter", "/#"),
#         social_link("facebook", "/#"),
#         social_link("linkedin", "/#"),
#         spacing="3",
#         justify="end",
#         width="100%",
#     )


def base_footer() -> rx.Component:
    return rx.flex(
        rx.container(
            rx.vstack(
                rx.flex(
                    rx.vstack(
                        rx.hstack(
                            rx.image(
                                src="/logo.jpg",
                                width="2.25em",
                                height="auto",
                                border_radius="25%",
                            ),
                            rx.heading(
                                "WLL",
                                size="7",
                                weight="bold",
                            ),
                            align_items="center",
                        ),
                        rx.text(
                            "White Label Lending, Inc",
                            size="3",
                            white_space="nowrap",
                            weight="medium",
                        ),
                        spacing="4",
                        align_items=[
                            "center",
                            "center",
                            "start",
                        ],
                    ),
                    footer_items_customer_service(),
                    footer_items_legal(),
                    justify="between",
                    spacing="6",
                    flex_direction=["column", "column", "row"],
                    width="100%",
                ),
                rx.divider(),
                rx.hstack(
                    rx.hstack(
                        footer_item("Warning About Borrowing", "/#"),
                        # footer_item("Terms of Service", "/#"),
                        spacing="4",
                        align="center",
                        width="100%",
                    ),
                    # socials(),
                    justify="between",
                    width="100%",
                ),
                spacing="5",
                width="100%",
            ),
        ),
        width="100%",
        bg=rx.color("accent", 3),
        padding="1em",
    )
