import flet
import components.pages.home
import components.pages.merge
import components.pages.split


def home_view(page: flet.Page) -> flet.View:
    view = flet.View(
        route="/",
        controls=[
            components.pages.home.render(page),
        ],
    )
    return view


def merge_view(page: flet.Page) -> flet.View:
    view = flet.View(
        route="/merge",
        controls=[
            components.pages.merge.render(page),
        ],
    )
    return view


def split_view(page: flet.Page) -> flet.View:
    view = flet.View(
        route="/split",
        controls=[
            components.pages.split.render(page),
        ],
    )
    return view


def change(route: flet.RouteChangeEvent, page: flet.Page) -> None:
    # set the home view
    page.views.clear()
    page.views.append(home_view(page))

    # change the view if the route has changed
    if page.route == "/merge":
        page.views.append(merge_view(page))
    elif page.route == "/split":
        page.views.append(split_view(page))


def view_pop(view: flet.ViewPopEvent, page: flet.Page) -> None:
    page.views.pop()
    top_view = page.views[-1]
    page.go(top_view.route)
