import flet


def menu_component(
        page: flet.Page,
        route: str,
        name: str,
        icon: flet.icons,
        description: str
) -> flet.Container:
    component = flet.Container(
        bgcolor=flet.colors.BLACK38,
        border_radius=10,
        width=250,
        height=120,
        margin=flet.margin.all(10),
        padding=flet.padding.all(25),
        on_click=lambda _: page.go(route),
        content=flet.Column(
            controls=[
                flet.Row(
                    controls=[
                        flet.Icon(name=icon),
                        flet.Text(name, size=16, weight=flet.FontWeight.W_700),
                    ]
                ),
                flet.Text(description),
            ]
        ),
    )
    return component
