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
pdf.ordered_files = list()


def _file_picker_result(event: flet.FilePickerResultEvent) -> None:
    merge_button.current.disabled = True if event.files is None else False
    pdf.files.clear()
    files.current.controls.clear()

    if event.files is not None:
        for index, file in enumerate(event.files):
            file_component = flet.DragTarget(
                group="files",
                on_accept=_shift_pdf_order,
                content=flet.Draggable(
                    group="files",
                    content=flet.Container(
                        bgcolor=flet.colors.BLACK26,
                        padding=flet.padding.all(5),
                        border=flet.border.all(1, flet.colors.GREY),
                        border_radius=flet.border_radius.all(5),
                        height=40,
                        width=500,
                        alignment=flet.alignment.center_left,
                        content=flet.Row(
                            data=index,
                            controls=[
                                flet.Icon(name=flet.icons.MENU_ROUNDED),
                                flet.Text(file.name),
                            ],
                        ),
                    ),
                ),
            )
            files.current.controls.append(file_component)
            pdf.files[file.name] = file.path
    event.page.update()


def _shift_pdf_order(event: flet.DragTargetAcceptEvent) -> None:
    src = event.page.get_control(event.src_id)

    # get index of the data
    src_index = src.content.content.data
    dest_index = event.control.content.content.content.data

    # get all the data from the Text
    # the sequence of element access is as follows:
    # flet.Column(flet.DragTarget(flet.Draggable(flet.Container(flet.Row(flet.Text)))))
    pdf.ordered_files = [content.content.content.content.controls[1].value
                         for content
                         in files.current.controls]

    # shift the pdf data
    pdf.ordered_files.insert(dest_index, pdf.ordered_files.pop(src_index))

    # render the data
    if src_index > dest_index:
        for i in range(dest_index, len(pdf.ordered_files)):
            files.current.controls[i].content.content.content.controls[1].value = pdf.ordered_files[i]
    elif src_index < dest_index:
        for i in range(src_index, dest_index + 1):
            files.current.controls[i].content.content.content.controls[1].value = pdf.ordered_files[i]

    event.page.update()


def _merge_file(event: flet.FilePickerResultEvent, save_dialog: flet.FilePicker) -> None:
    merger = pypdf.PdfWriter()
    for file in pdf.ordered_files:
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
