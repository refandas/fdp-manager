import flet
import pypdf
import components.controls.navigation
from components.pages.constants import DEFAULT_MERGED_FILE_NAME
from utils.pdf import PDFFile

# Type control reference
files = flet.Ref[flet.Column]()
select_files_button = flet.Ref[flet.ElevatedButton]()
merge_button = flet.Ref[flet.ElevatedButton]()

pdf = PDFFile()
pdf.files = dict()


def _file_picker_result(event: flet.FilePickerResultEvent) -> None:
    merge_button.current.disabled = True if event.files is None else False
    pdf.files.clear()
    files.current.controls.clear()

    if event.files is not None:
        for file in event.files:
            files.current.controls.append(
                flet.Row([
                    flet.Icon(name=flet.icons.PICTURE_AS_PDF),
                    flet.Text(file.name),
                ])
            )
            pdf.files[file.name] = file.path
    event.page.update()


def _merge_file(event: flet.FilePickerResultEvent, save_dialog: flet.FilePicker) -> None:
    merger = pypdf.PdfWriter()
    for file in pdf.files:
        merger.append(pdf.files[file])

    merger.write(save_dialog.result.path)
    merger.close()

    files.current.controls.clear()
    merge_button.current.disabled = True if event.files is None else False
    event.page.update()


def _merge_components(file_picker: flet.FilePicker, save_dialog: flet.FilePicker) -> flet.Container:
    feature_components = flet.Container(
        margin=flet.margin.all(20),
        content=flet.Column(
            expand=True,
            alignment=flet.MainAxisAlignment.START,
            controls=[
                flet.ElevatedButton(
                    text="Select files",
                    ref=select_files_button,
                    icon=flet.icons.FOLDER_OPEN,
                    on_click=lambda _: file_picker.pick_files(allow_multiple=True),
                ),
                flet.Column(ref=files),
                flet.ElevatedButton(
                    text="Merge PDF",
                    ref=merge_button,
                    icon=flet.icons.FILE_DOWNLOAD_OUTLINED,
                    on_click=lambda _: save_dialog.save_file(
                        file_name=DEFAULT_MERGED_FILE_NAME
                    ),
                    disabled=True,
                ),
            ],
        ),
    )
    return feature_components


def render(page: flet.Page) -> flet.Container:
    file_picker = flet.FilePicker(on_result=_file_picker_result)
    save_dialog = flet.FilePicker(on_result=lambda event: _merge_file(event, save_dialog))

    # hide dialog in a overlay
    page.overlay.append(file_picker)
    page.overlay.append(save_dialog)

    merge_view = flet.Container(
        height=page.height,
        content=flet.Row(
            expand=True,
            controls=[
                components.controls.navigation.Menu(),
                _merge_components(file_picker, save_dialog),
            ],
        ),
    )
    return merge_view
