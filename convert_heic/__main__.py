import logging
from pathlib import Path
from typing import Annotated, List
from PIL import Image
import pillow_heif
import typer


app = typer.Typer()


def _convert(file_path: Path, output_file_type: str, output_path: Path) -> None:
    output_file_path = output_path / f"{file_path.stem}.{output_file_type}"
    if file_path.suffix == ".heic":
        logging.info(f"Converting file={file_path}")
        heif_file = pillow_heif.read_heif(str(file_path))
        image: Image = Image.frombytes(
            heif_file.mode,
            heif_file.size,
            heif_file.data,
            "raw",
        )
        image.save(fp=str(output_file_path), format=output_file_type)
    else:
        logging.debug(f"file={file_path} is not .heic, skipping.")


def _convert_directory(directory_path: Path, output_file_type: str, output_path: Path) -> None:
    for sub_directory_path in directory_path.iterdir():
        _path_triage(input_path=sub_directory_path, output_file_type=output_file_type, output_path=output_path)


def _path_triage(input_path: Path, output_file_type: str, output_path: Path) -> None:
    if input_path.is_file():
        _convert(file_path=input_path, output_file_type=output_file_type, output_path=output_path)
    elif input_path.is_dir():
        _convert_directory(directory_path=input_path, output_file_type=output_file_type, output_path=output_path)
    else:
        logging.warning(f"path_file={input_path} does not exist.")


@app.command()
def convert(
        file_or_directory: Annotated[
            List[Path], typer.Argument(help="Provide file or directory, only heic files will be processed")
        ],
        output_path: Annotated[Path, typer.Option(help="Output directory")] = "outputs",
        output_file_type: Annotated[
            str,
            typer.Option(help="See https://pillow-wiredfool.readthedocs.io/en/latest/handbook/image-file-formats.html")
        ] = "png",
        verbose_mode: Annotated[bool, typer.Option(help="Use DEBUG level instead of INFO in logger")] = False,
):
    logging.basicConfig(
        level=logging.DEBUG if verbose_mode else logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%SZ",
    )
    if not output_path.exists():
        logging.warning(f"output_path={output_path} does not exist, creating it.")
        output_path.mkdir(parents=True, exist_ok=True)
    for path_file in file_or_directory:
        _path_triage(input_path=path_file, output_file_type=output_file_type, output_path=output_path)


if __name__ == "__main__":
    app()
