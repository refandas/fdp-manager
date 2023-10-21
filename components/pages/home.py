import flet
from components.pages.template import menu_component


def merge(page: flet.Page) -> flet.Container:
    merge_component = menu_component(
        page=page,
        route="/merge",
        name="Merge PDF",
        icon=flet.icons.CALL_MERGE_ROUNDED,
        description="Combine multiple PDF files into a single PDF file"
    )
    return merge_component


def split(page: flet.Page) -> flet.Container:
    split_component = menu_component(
        page=page,
        route="/split",
        name="Split a PDF",
        icon=flet.icons.CALL_SPLIT_ROUNDED,
        description="Separate a single PDF file"
    )
    return split_component


def reduce(page: flet.Page) -> flet.Container:
    reduce_component = menu_component(
        page=page,
        route="/reduce",
        name="Reduce a PDF",
        icon=flet.icons.PHOTO_SIZE_SELECT_SMALL_ROUNDED,
        description="Reduce the size of PDF"
    )
    return reduce_component


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
                reduce(page),
            ],
        ),
    )
    return all_menu
