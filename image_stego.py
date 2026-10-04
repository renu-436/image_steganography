from PIL import Image

from encryption import encrypt_message, decrypt_message


# ==================================================
# DATA FORMAT
# ==================================================

MAGIC = b"STEG"

VERSION = 1

# Header:
# MAGIC        = 4 bytes
# VERSION     = 1 byte
# SALT        = 16 bytes
# DATA LENGTH = 4 bytes
#
# Total = 25 bytes

HEADER_SIZE = 4 + 1 + 16 + 4


# ==================================================
# CONVERT BYTES TO BITS
# ==================================================

def bytes_to_bits(data):

    bits = []

    for byte in data:

        for i in range(7, -1, -1):

            bits.append((byte >> i) & 1)

    return bits


# ==================================================
# CONVERT BITS TO BYTES
# ==================================================

def bits_to_bytes(bits):

    result = bytearray()

    for i in range(0, len(bits), 8):

        byte_bits = bits[i:i + 8]

        if len(byte_bits) < 8:
            break

        value = 0

        for bit in byte_bits:

            value = (value << 1) | bit

        result.append(value)

    return bytes(result)


# ==================================================
# CREATE HEADER
# ==================================================

def create_header(salt, encrypted_length):

    header = (
        MAGIC +
        bytes([VERSION]) +
        salt +
        encrypted_length.to_bytes(4, "big")
    )

    return header


# ==================================================
# HIDE MESSAGE
# ==================================================

def hide_message(image_path, output_path, message, password):

    try:

        image = Image.open(image_path).convert("RGB")

    except Exception:

        print("\nERROR: Could not open cover image.")

        return False

    width, height = image.size

    # --------------------------------------------------
    # IMAGE CAPACITY
    # --------------------------------------------------

    total_bits = width * height * 3

    total_bytes = total_bits // 8

    # --------------------------------------------------
    # ENCRYPT MESSAGE
    # --------------------------------------------------

    salt, encrypted_data = encrypt_message(
        message,
        password
    )

    # --------------------------------------------------
    # CREATE HEADER
    # --------------------------------------------------

    header = create_header(
        salt,
        len(encrypted_data)
    )

    # Complete data
    data = header + encrypted_data

    required_bytes = len(data)

    required_bits = required_bytes * 8

    # --------------------------------------------------
    # DISPLAY STORAGE INFORMATION
    # --------------------------------------------------

    print("\n+----------------------+----------------+")
    print("| Storage Information  | Value          |")
    print("+----------------------+----------------+")

    print(
        f"| Image capacity      | "
        f"{str(total_bytes) + ' bytes':<14}|"
    )

    print(
        f"| Required space      | "
        f"{str(required_bytes) + ' bytes':<14}|"
    )

    available_bytes = total_bytes - required_bytes

    if available_bytes < 0:
        available_bytes = 0

    print(
        f"| Available space     | "
        f"{str(available_bytes) + ' bytes':<14}|"
    )

    print("+----------------------+----------------+")

    # --------------------------------------------------
    # CHECK CAPACITY
    # --------------------------------------------------

    if required_bits > total_bits:

        print("\nERROR: Message is too large for this image.")

        print(
            "Please use a larger image or a shorter message."
        )

        return False

    # --------------------------------------------------
    # CONVERT DATA TO BITS
    # --------------------------------------------------

    bits = bytes_to_bits(data)

    pixels = image.load()

    bit_index = 0

    # --------------------------------------------------
    # HIDE BITS INSIDE RGB VALUES
    # --------------------------------------------------

    for y in range(height):

        for x in range(width):

            r, g, b = pixels[x, y]

            channels = [r, g, b]

            for channel in range(3):

                if bit_index < len(bits):

                    # Clear the LSB
                    channels[channel] = (
                        channels[channel] & 254
                    )

                    # Store secret bit
                    channels[channel] = (
                        channels[channel] | bits[bit_index]
                    )

                    bit_index += 1

            pixels[x, y] = tuple(channels)

            # --------------------------------------------------
            # FINISHED HIDING
            # --------------------------------------------------

            if bit_index >= len(bits):

                # Make sure output is PNG
                if not output_path.lower().endswith(".png"):
                    output_path += ".png"

                try:

                    image.save(
                        output_path,
                        format="PNG"
                    )

                except Exception:

                    print(
                        "\nERROR: Could not save output image."
                    )

                    return False

                print("\n================================")
                print("       MESSAGE HIDDEN")
                print("================================")

                print("Output image:", output_path)
                print("Data stored:", required_bytes, "bytes")

                return True

    return False


# ==================================================
# EXTRACT MESSAGE
# ==================================================

def extract_message(image_path, password):

    try:

        image = Image.open(image_path).convert("RGB")

    except Exception:

        print("\nERROR: Could not open stego image.")

        return None

    width, height = image.size

    pixels = image.load()

    # --------------------------------------------------
    # EXTRACT HEADER
    # --------------------------------------------------

    header_bits = []

    required_header_bits = HEADER_SIZE * 8

    for y in range(height):

        for x in range(width):

            r, g, b = pixels[x, y]

            for value in (r, g, b):

                header_bits.append(value & 1)

                if len(header_bits) >= required_header_bits:
                    break

            if len(header_bits) >= required_header_bits:
                break

        if len(header_bits) >= required_header_bits:
            break

    # --------------------------------------------------
    # CHECK HEADER SIZE
    # --------------------------------------------------

    if len(header_bits) < required_header_bits:

        print(
            "\nERROR: Image is too small or "
            "does not contain valid data."
        )

        return None

    header = bits_to_bytes(header_bits)

    # --------------------------------------------------
    # CHECK MAGIC VALUE
    # --------------------------------------------------

    if header[:4] != MAGIC:

        print(
            "\nERROR: This image does not contain "
            "valid steganography data."
        )

        return None

    # --------------------------------------------------
    # CHECK VERSION
    # --------------------------------------------------

    version = header[4]

    if version != VERSION:

        print(
            "\nERROR: Unsupported steganography version."
        )

        return None

    # --------------------------------------------------
    # EXTRACT SALT
    # --------------------------------------------------

    salt = header[5:21]

    # --------------------------------------------------
    # EXTRACT ENCRYPTED DATA LENGTH
    # --------------------------------------------------

    encrypted_length = int.from_bytes(
        header[21:25],
        "big"
    )

    # --------------------------------------------------
    # CHECK DATA SIZE
    # --------------------------------------------------

    total_data_size = HEADER_SIZE + encrypted_length

    total_bits = total_data_size * 8

    image_capacity_bits = width * height * 3

    if total_bits > image_capacity_bits:

        print(
            "\nERROR: Invalid or corrupted "
            "steganography data."
        )

        return None

    # --------------------------------------------------
    # EXTRACT REQUIRED BITS
    # --------------------------------------------------

    data_bits = []

    for y in range(height):

        for x in range(width):

            r, g, b = pixels[x, y]

            for value in (r, g, b):

                if len(data_bits) < total_bits:

                    data_bits.append(value & 1)

                else:

                    break

            if len(data_bits) >= total_bits:
                break

        if len(data_bits) >= total_bits:
            break

    # --------------------------------------------------
    # CHECK EXTRACTED DATA
    # --------------------------------------------------

    if len(data_bits) < total_bits:

        print(
            "\nERROR: Image does not contain enough data."
        )

        return None

    # Convert bits to bytes

    data = bits_to_bytes(data_bits)

    # --------------------------------------------------
    # GET ENCRYPTED MESSAGE
    # --------------------------------------------------

    encrypted_data = data[
        HEADER_SIZE:
        HEADER_SIZE + encrypted_length
    ]

    # --------------------------------------------------
    # DECRYPT MESSAGE
    # --------------------------------------------------

    message = decrypt_message(
        encrypted_data,
        password,
        salt
    )

    if message is None:

        print(
            "\nERROR: Incorrect password "
            "or corrupted data."
        )

        return None

    return message


# ==================================================
# IMAGE CAPACITY
# ==================================================

def show_capacity(image_path):

    try:

        image = Image.open(image_path)

    except Exception:

        print("\nERROR: Could not open image.")

        return

    width, height = image.size

    # Raw LSB capacity

    total_bits = width * height * 3

    total_bytes = total_bits // 8

    # Header uses 25 bytes

    header_bytes = HEADER_SIZE

    usable_bytes = total_bytes - header_bytes

    if usable_bytes < 0:

        usable_bytes = 0

    print(
        "\n+----------+-------------+--------+----------------+----------------+"
    )

    print(
        "| Format   | Dimensions  | Mode   | Raw Capacity   | Usable Space   |"
    )

    print(
        "+----------+-------------+--------+----------------+----------------+"
    )

    print(
        f"| {image.format:<8} | "
        f"{str(width) + ' x ' + str(height):<11} | "
        f"{image.mode:<6} | "
        f"{str(total_bytes) + ' bytes':<14} | "
        f"{str(usable_bytes) + ' bytes':<14} |"
    )

    print(
        "+----------+-------------+--------+----------------+----------------+"
    )


# ==================================================
# CHECK IMAGE
# ==================================================

def check_image(image_path):

    try:

        image = Image.open(image_path)

        print("\nImage information")
        print("------------------")

        print("Format:", image.format)
        print("Size:", image.size)
        print("Mode:", image.mode)

        return True

    except Exception:

        print("\nERROR: Could not open image.")

        return False