# ConvertHeic

Convert heic photos to png/jpg

## RTFM

| Required argument  | Description                                                  | Type       |
|--------------------|--------------------------------------------------------------|------------|
| file_or_directory  | Provide file or directory, only heic files will be processed | List[Path] |

| Option name         | Description                                                                            | Type                | Default value     |
|---------------------|----------------------------------------------------------------------------------------|---------------------|-------------------|
| --output-path       | Output directory                                                                       | Path                | outputs           |
| --output-file-type  | See https://pillow-wiredfool.readthedocs.io/en/latest/handbook/image-file-formats.html | str                 | png               |
| --resize-with-ratio | Try to resize the image to fit the new size, respecting ratio                          | Tuple[float, float] | None              |
| --verbose-mode      | Use DEBUG level instead of INFO in logger                                              | bool                | --no-verbose-mode |

## Examples

Converting `heic` photos to `png`
````commandline
python -m convert-heic C:\Users\rdall\Downloads\Perpignan
````

Converting `heic` photos to `JPEG` and a new size
````commandline
python -m convert-heic C:\Users\rdall\Downloads\Perpignan --output-file-type JPEG --resize-with-ratio 1920 1080 --output-path C:\Users\rdall\Downloads\Perpignan\Outputs
````
