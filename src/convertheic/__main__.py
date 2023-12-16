from PIL import Image
import pillow_heif

heif_file = pillow_heif.read_heif("photos/2023-11-08_19-40-04_295.heic")

image = Image.frombytes(
    heif_file.mode,
    heif_file.size,
    heif_file.data,
    "raw",
)

image.save("photos/richard.png", format("png"))
