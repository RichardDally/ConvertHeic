import logging
import sys
from pathlib import Path
from typing import Annotated, List, Tuple, Optional
from PIL import Image
import pillow_heif
import typer


app = typer.Typer()


def _convert(file_path: Path, output_file_type: str, output_path: Path, new_size: Optional[Tuple[float, float]]) -> None:
    output_file_path = output_path / f"{file_path.stem}.{output_file_type}"
    if file_path.suffix == ".heic":
        logging.info(f"Converting file={file_path}")
        heif_file = pillow_heif.read_heif(str(file_path))
        image: Image = Image.frombytes(
            mode=heif_file.mode,
            size=heif_file.size,
            data=heif_file.data,
            decoder_name="raw",
        )
        if new_size:
            image.thumbnail(size=new_size)
        image.save(fp=str(output_file_path), format=output_file_type)
    else:
        logging.debug(f"file={file_path} is not .heic, skipping.")


def _convert_directory(directory_path: Path, output_file_type: str, output_path: Path, new_size: Optional[Tuple[float, float]]) -> None:
    for sub_directory_path in directory_path.iterdir():
        _path_triage(input_path=sub_directory_path, output_file_type=output_file_type, output_path=output_path, new_size=new_size)


def _path_triage(input_path: Path, output_file_type: str, output_path: Path, new_size: Optional[Tuple[float, float]]) -> None:
    if input_path.is_file():
        _convert(file_path=input_path, output_file_type=output_file_type, output_path=output_path, new_size=new_size)
    elif input_path.is_dir():
        _convert_directory(directory_path=input_path, output_file_type=output_file_type, output_path=output_path, new_size=new_size)
    else:
        logging.error(f"path_file={input_path} does not exist.")


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
        resize_with_ratio: Annotated[
            Tuple[float, float],
            typer.Option(help="Try to resize the image to fit the new size, respecting ratio"),
        ] = None,
        verbose_mode: Annotated[bool, typer.Option(help="Use DEBUG level instead of INFO in logger")] = False,
):
    verbosity_level = logging.DEBUG if verbose_mode else logging.INFO
    logging.basicConfig(
        level=verbosity_level,
        format="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%SZ",
        stream=sys.stdout,
    )
    logging.info(f"verbosity_level={verbosity_level}")
    if not output_path.exists():
        logging.info(f"output_path={output_path} does not exist, creating it.")
        output_path.mkdir(parents=True, exist_ok=True)
    for path_file in file_or_directory:
        _path_triage(input_path=path_file, output_file_type=output_file_type, output_path=output_path, new_size=resize_with_ratio)


if __name__ == "__main__":
    app()
