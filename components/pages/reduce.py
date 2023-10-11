import flet
import components.controls.navigation
import pypdf
import time
from utils.pdf import PDFFile
from components.pages.constants import DEFAULT_REDUCE_FILE_NAME

# Type control reference
select_file_button = flet.Ref[flet.ElevatedButton]()
display_pdf_name = flet.Ref[flet.Row]()
reduce_button = flet.Ref[flet.ElevatedButton]()
image_quality = flet.Ref[flet.Dropdown]()

pdf_file = PDFFile()


def _file_picker_result(event: flet.FilePickerResultEvent) -> None:
    reduce_button.current.disabled = True if event.files is None else False
    image_quality.current.disabled = True if event.files is None else False
    display_pdf_name.current.clean()

    if event.files is not None:
        # since the return value of the `event.files` is a `list` and reduce feature only
        # supports single pdf file, so only the first index is used
        pdf_file.name = event.files[0].name
        pdf_file.path = event.files[0].path

        display_pdf_name.current.controls.append(
            flet.Icon(name=flet.icons.PICTURE_AS_PDF)
        )
        display_pdf_name.current.controls.append(flet.Text(pdf_file.name))
    event.page.update()


def _reduce_file(event: flet.FilePickerResultEvent, save_dialog: flet.FilePicker) -> None:
    if save_dialog.result.path is not None:
        pdf_file.reader = pypdf.PdfReader(pdf_file.path)
        pdf_file.writer = pypdf.PdfWriter()

        progress_modal = flet.AlertDialog(
            modal=True,
            title=flet.Text("Reducing file size"),
            content=flet.Row(
                spacing=20,
                controls=[
                    flet.ProgressRing(),
                    flet.Text("Reducing file size is in progress")
                ]
            )
        )

        event.page.dialog = progress_modal
        progress_modal.open = True
        event.page.update()

        for page in pdf_file.reader.pages:
            pdf_file.writer.add_page(page)

        for page in pdf_file.writer.pages:
            for img in page.images:
                img.replace(img.image, quality=int(image_quality.current.value))

        with open(save_dialog.result.path, "wb") as file:
            pdf_file.writer.write(file)

        progress_modal.content = flet.Row(
            spacing=10,
            controls=[
                flet.Icon(flet.icons.DONE_OUTLINE_ROUNDED),
                flet.Text("Finished")
            ]
        )
        event.page.update()

        time.sleep(2)
        progress_modal.open = False

        # reset the view
        display_pdf_name.current.clean()
        image_quality.current.disabled = True if event.files is None else False
        reduce_button.current.disabled = True if event.files is None else False
        event.page.update()


def _reduce_components(file_picker: flet.FilePicker, save_dialog: flet.FilePicker) -> flet.Container:
    feature_components = flet.Container(
        margin=flet.margin.all(20),
        content=flet.Column(
            expand=True,
            alignment=flet.MainAxisAlignment.START,
            spacing=20,
            controls=[
                flet.ElevatedButton(
                    text="Select file",
                    ref=select_file_button,
                    icon=flet.icons.FOLDER_OPEN,
                    on_click=lambda _: file_picker.pick_files(),
                ),
                flet.Row(ref=display_pdf_name),
                flet.Text(
                    value="The PDF file size reduction feature works by reducing the image size in the PDF. Adjust "
                    "the image quality below according to your desired preference. The lower the image quality, the "
                    "smaller PDF file size.",
                    width=750,
                ),
                flet.Dropdown(
                    label="Image Quality",
                    ref=image_quality,
                    disabled=True,
                    options=[
                        flet.dropdown.Option(quality) for quality in range(10, 100, 20)
                    ],
                ),
                flet.ElevatedButton(
                    text="Reduce PDF",
                    ref=reduce_button,
                    icon=flet.icons.FILE_DOWNLOAD_OUTLINED,
                    on_click=lambda _: save_dialog.save_file(
                        file_name=DEFAULT_REDUCE_FILE_NAME
                    ),
                    disabled=True,
                ),
            ],
        ),
    )
    return feature_components


def render(page: flet.Page) -> flet.Container:
    file_picker = flet.FilePicker(on_result=_file_picker_result)
    save_dialog = flet.FilePicker(
        on_result=lambda event: _reduce_file(event, save_dialog)
    )

    # hide dialog in a overlay
    page.overlay.append(file_picker)
    page.overlay.append(save_dialog)

    reduce_view = flet.Container(
        height=page.height,
        content=flet.Row(
            expand=True,
            controls=[
                components.controls.navigation.Menu(),
                _reduce_components(file_picker, save_dialog),
            ],
        ),
    )
    return reduce_view
