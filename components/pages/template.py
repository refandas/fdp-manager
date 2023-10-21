import time
from typing import Union
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


def modal_load_file() -> flet.AlertDialog:
    modal = flet.AlertDialog(
        modal=True,
        content=flet.Row(
            spacing=20,
            controls=[
                flet.ProgressRing(),
                flet.Text("Loading file")
            ]
        )
    )
    return modal


def _modal_process_file(title: str, description: str) -> flet.AlertDialog:
    modal = flet.AlertDialog(
        modal=True,
        title=flet.Text(title),
        content=flet.Row(
            spacing=20,
            controls=[
                flet.ProgressRing(),
                flet.Text(description)
            ]
        )
    )
    return modal


def _modal_process_file_finished(message: Union[str, None] = None) -> flet.Row:
    modal = flet.Row(
        spacing=10,
        controls=[
            flet.Icon(flet.icons.DONE_OUTLINE_ROUNDED),
            flet.Text(message)
        ]
    )
    return modal


def setup_modal(title: str, description: str, page: flet.Page) -> flet.AlertDialog:
    modal = _modal_process_file(title, description)
    page.dialog = modal
    modal.open = True
    page.update()

    return modal


def close_modal(
        modal: flet.AlertDialog,
        page: flet.Page,
        message: Union[str, None] = None,
        sleep: bool = True
) -> None:
    modal.content = _modal_process_file_finished(message)
    page.update()

    if sleep:
        time.sleep(2)
    modal.open = False
