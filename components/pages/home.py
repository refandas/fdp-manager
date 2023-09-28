import flet


def merge(page: flet.Page) -> flet.Container:
    merge_component_menu = flet.Container(
        bgcolor=flet.colors.BLACK38,
        border_radius=10,
        width=250,
        height=120,
        margin=flet.margin.all(10),
        padding=flet.padding.all(25),
        on_click=lambda _: page.go("/merge"),
        content=flet.Column(
            controls=[
                flet.Row(
                    controls=[
                        flet.Icon(name=flet.icons.CALL_MERGE_ROUNDED),
                        flet.Text("Merge PDF", size=16, weight=flet.FontWeight.W_700),
                    ]
                ),
                flet.Text("Combine multiple PDF files into a single PDF file"),
            ]
        ),
    )
    return merge_component_menu


def split(page: flet.Page) -> flet.Container:
    split_component_menu = flet.Container(
        bgcolor=flet.colors.BLACK38,
        border_radius=10,
        width=250,
        height=120,
        margin=flet.margin.all(10),
        padding=flet.padding.all(25),
        on_click=lambda _: page.go("/split"),
        content=flet.Column(
            controls=[
                flet.Row(
                    controls=[
                        flet.Icon(name=flet.icons.CALL_SPLIT_ROUNDED),
                        flet.Text("Split a PDF", size=16, weight=flet.FontWeight.W_700),
                    ]
                ),
                flet.Text("Separate a single PDF file"),
            ],
        ),
    )
    return split_component_menu


def render(page: flet.Page):
    all_menu = flet.Container(
        padding=20,
        content=flet.Row(
            spacing=20,
            height=150,
            wrap=True,
            vertical_alignment=flet.CrossAxisAlignment.CENTER,
            controls=[
                merge(page),
                split(page),
            ],
        ),
    )
    return all_menu
