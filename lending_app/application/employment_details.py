import reflex as rx
import logging

from lending_app import ui

from .app_state import AppState


def not_loggedin_app_placeholder() -> rx.Component:
    return rx.hstack(
        rx.box(
            rx.box(height="20vh"),
            rx.heading(
                "Please log in to start your application", size="9", text_align="center"
            ),
            rx.box(height="10vh"),
            rx.button(
                "Login/Register",
                on_click=AppState.initiate_login,
                style={"font-size": "1.5em", "padding": "1em 2em"},
            ),
            width="100%",
            text_align="center",
            minimum_height="85vh",
        ),
        width="100%",
    )


# employment details

# contact details


def form_tooltip(contents: str) -> rx.Component:
    return rx.tooltip(
        rx.icon(tag="info"),  # Icon that triggers the tooltip
        content=contents,  # Tooltip content
        position="top",  # Position of the tooltip relative to the icon
    )


def form_text_input(
    title, name, placeholder: str = "", tooltip_contents: str = ""
) -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.text(title, size="2"),
            rx.cond(len(tooltip_contents) > 0, form_tooltip(tooltip_contents), None),
        ),
        rx.input(
            name=name,
            placeholder=placeholder,
            type="text",
            required=True,
        ),
        rx.box(height="1px"),
        width="100%",
    )


def form_date_input(
    title, name, placeholder: str = "", tooltip_contents: str = ""
) -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.text(title, size="2"),
            rx.cond(len(tooltip_contents) > 0, form_tooltip(tooltip_contents), None),
        ),
        rx.input(
            name=name,
            placeholder=placeholder,
            type="date",
            required=True,
        ),
        rx.box(height="1px"),
        width="100%",
    )


def form_dollar_input(
    title, name, placeholder: str = "", tooltip_contents: str = ""
) -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.text(title, size="2"),
            rx.cond(len(tooltip_contents) > 0, form_tooltip(tooltip_contents), None),
        ),
        rx.hstack(
            rx.text(
                "$",
                size="2",
                background_color="lightgrey",
                line_height="2.5em",
                min_width="2em",
                text_align="center",
                border_radius="5px",
            ),
            rx.input(
                name=name,
                placeholder=placeholder,
                type="int",
                required=True,
                style={"border-radius": "5px"},
            ),
            rx.text(
                ".00",
                size="2",
                background_color="lightgrey",
                line_height="2.5em",
                min_width="2em",
                text_align="center",
                border_radius="5px",
            ),
            width="100%",
            align_items="center",
        ),
        rx.box(height="1px"),
        width="100%",
    )


def form_dropdown_input(
    title, name, placeholder, options: list, tooltip_contents: str = ""
) -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.text(title, size="2"),
            rx.cond(len(tooltip_contents) > 0, form_tooltip(tooltip_contents), None),
        ),
        rx.select(
            name=name,
            items=options,
            placeholder=placeholder,
            required=True,
            width="100%",
        ),
        rx.box(height="1px"),
        width="100%",
    )


def employment_and_financials_details_form():
    return rx.vstack(
        rx.heading("Employment Details", size="6"),
        rx.divider(),
        rx.form(
            rx.vstack(
                form_dropdown_input(
                    title="Employment Status",
                    name="employment_status",
                    placeholder="Employment Status",
                    options=[
                        "Full Time",
                        "Part Time",
                        "Casual",
                        "Self-Employed",
                        "Contract",
                        "Retired",
                        "Student",
                        "Unemployed",
                        "Centrelink Benefit",
                        "Home Duties",
                    ],
                ),
                rx.box(height="1em"),
                rx.heading("Financial Details", size="6"),
                rx.divider(),
                form_dropdown_input(
                    title="Pay Cycle",
                    name="pay_cycle",
                    placeholder="How often you are paid?",
                    options=[
                        "Weekly",
                        "Fortnightly",
                        "Monthly",
                    ],
                ),
                form_date_input(
                    title="Next Pay Date",
                    name="next_pay_date",
                    tooltip_contents="What is the date you next receive your pay into your bank account?",
                ),
                form_dollar_input(
                    title="Pay After Tax",
                    name="pay_after_tax",
                    tooltip_contents="What is the amount paid into your account each pay?",
                ),
                form_dollar_input(
                    title="Monthly Rent/Mortgage Repayments",
                    name="monthly_rent_or_mortgage_payments",
                ),
                form_dropdown_input(
                    title="Monthly Living Expenses",
                    name="monthly_living_expenses",
                    placeholder="$0",
                    options=[
                        "$0",
                        "Less than $400",
                        "$400 to $599",
                        "$600 to $899",
                        "$900 to $1499",
                        "More the $1500",
                    ],
                ),
                form_dropdown_input(
                    title="Monthly Debt Repayments",
                    name="monthly_debt_repayments",
                    placeholder="$0",
                    options=[
                        "$0",
                        "Less than $400",
                        "$400 to $599",
                        "$600 to $999",
                        "$1000 to $1499",
                        "More the $1500",
                    ],
                ),
                rx.hstack(
                    rx.button("Save & Next", type="submit", width="40%", height="auto"),
                    justify="end",
                    width="100%",
                ),
            ),
            reset_on_submit=False,
            on_submit=AppState.handle_submit,
            min_width="20em",
        ),
    )


def employment_details_page() -> rx.Component:
    return ui.base_layout(
        rx.cond(
            AppState.is_authenticated,
            rx.hstack(
                rx.box(width="10%"),
                rx.vstack(
                    employment_and_financials_details_form(),
                    width="100%",
                    height="100%",
                    align_items="center",
                    justify_content="center",
                ),
                rx.box(width="10%"),
                width="100%",
                min_height="85vh",
                align_items="center",
                justify_content="center",
            ),
            not_loggedin_app_placeholder(),
        ),
        align_items="center",
        justify_content="center",
    )
