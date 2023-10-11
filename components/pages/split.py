import datetime
import flet
import pypdf
import components.controls.navigation
from utils.pdf import PDFFile

# Type control reference
start_page_input = flet.Ref[flet.Dropdown]()
end_page_input = flet.Ref[flet.Dropdown]()
select_file_button = flet.Ref[flet.ElevatedButton]()
split_button = flet.Ref[flet.ElevatedButton]()
display_pdf_name = flet.Ref[flet.Row]()
field_input = flet.Ref[flet.Column]()

pdf_file = PDFFile()
pdf_file.reader = pdf_file.writer = None


def _file_picker_result(event: flet.FilePickerResultEvent) -> None:
    split_button.current.disabled = True if event.files is None else False
    field_input.current.disabled = True if event.files is None else False
    display_pdf_name.current.clean()

    if event.files is not None:
        # since the return value of the `event.files` is a `list` and split feature only
        # supports single pdf file, so only the first index is used
        pdf_file.name = event.files[0].name
        pdf_file.path = event.files[0].path

        display_pdf_name.current.controls.append(flet.Icon(name=flet.icons.PICTURE_AS_PDF))
        display_pdf_name.current.controls.append(flet.Text(pdf_file.name))

        # set up the page number input
        pdf_file.reader = pypdf.PdfReader(pdf_file.path)
        for page_number in range(1, len(pdf_file.reader.pages) + 1):
            start_page_input.current.options.append(flet.dropdown.Option(page_number))
            end_page_input.current.options.append(flet.dropdown.Option(page_number))

    event.page.update()


def _split_file(event: flet.FilePickerResultEvent, save_dialog: flet.FilePicker) -> None:
    if save_dialog.result.path is not None:
        pdf_file.writer = pypdf.PdfWriter()

        start_page = int(start_page_input.current.value) - 1
        end_page = int(end_page_input.current.value)

        for page in range(start_page, end_page):
            pdf_file.writer.add_page(pdf_file.reader.pages[page])

        with open(save_dialog.result.path, "wb") as file:
            pdf_file.writer.write(file)

        # reset the view
        display_pdf_name.current.clean()
        start_page_input.current.options.clear()
        end_page_input.current.options.clear()
        start_page_input.current.value = ""
        end_page_input.current.value = ""
        field_input.current.disabled = True if event.files is None else False
        split_button.current.disabled = True if event.files is None else False

        event.page.update()


def _split_components(file_picker: flet.FilePicker, save_dialog: flet.FilePicker) -> flet.Container:
    feature_components = flet.Container(
        margin=flet.margin.all(20),
        content=flet.Column(
            expand=True,
            alignment=flet.MainAxisAlignment.START,
            controls=[
                flet.ElevatedButton(
                    text="Select file",
                    ref=select_file_button,
                    icon=flet.icons.FOLDER_OPEN,
                    on_click=lambda _: file_picker.pick_files(),
                ),
                flet.Row(ref=display_pdf_name),
                flet.Column(
                    ref=field_input,
                    controls=[
                        flet.Row(
                            [
                                flet.Text("Start page", width=150),
                                flet.Dropdown(ref=start_page_input, width=100),
                            ]
                        ),
                        flet.Row(
                            [
                                flet.Text("End page", width=150),
                                flet.Dropdown(ref=end_page_input, width=100),
                            ]
                        ),
                    ],
                ),
                flet.ElevatedButton(
                    text="Split PDF",
                    ref=split_button,
                    icon=flet.icons.FILE_DOWNLOAD_OUTLINED,
                    on_click=lambda _: save_dialog.save_file(
                        file_name=f"Split-{datetime.datetime.today().strftime('%d-%b-%Y-%H-%M-%S')}.pdf"
                    ),
                    disabled=True,
                ),
            ],
        ),
    )
    return feature_components


def render(page: flet.Page) -> flet.Container:
    file_picker = flet.FilePicker(on_result=_file_picker_result)
    save_dialog = flet.FilePicker(on_result=lambda event: _split_file(event, save_dialog))

    # hide dialog in a overlay
    page.overlay.append(file_picker)
    page.overlay.append(save_dialog)

    split_view = flet.Container(
        height=page.height,
        content=flet.Row(
            expand=True,
            controls=[
                components.controls.navigation.Menu(),
                _split_components(file_picker, save_dialog),
            ],
        ),
    )
    return split_view
