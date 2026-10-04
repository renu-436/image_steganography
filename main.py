from getpass import getpass

from image_stego import (
    hide_message,
    extract_message,
    show_capacity,
    check_image
)


# ==================================================
# IMAGE - HIDE DATA
# ==================================================

def image_hide_menu():

    while True:

        print("\n================================")
        print("        IMAGE - HIDE DATA")
        print("================================")

        print("1. Hide Text")
        print("2. Back")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":

            image_path = input(
                "\nEnter cover image path: "
            ).strip()

            if not check_image(image_path):
                continue

            show_capacity(image_path)

            message = input(
                "\nEnter secret message: "
            )

            if not message:

                print("ERROR: Message cannot be empty.")
                continue

            password = getpass(
                "Create password: "
            )

            confirm_password = getpass(
                "Confirm password: "
            )

            if not password:

                print("ERROR: Password cannot be empty.")
                continue

            if password != confirm_password:

                print("ERROR: Passwords do not match.")
                continue

            output_path = input(
                "Enter output image path "
                "(example: images/stego.png): "
            ).strip()

            hide_message(
                image_path,
                output_path,
                message,
                password
            )

        elif choice == "2":

            break

        else:

            print("\nInvalid choice.")


# ==================================================
# IMAGE - EXTRACT DATA
# ==================================================

def image_extract_menu():

    while True:

        print("\n================================")
        print("       IMAGE - EXTRACT DATA")
        print("================================")

        print("1. Extract Text")
        print("2. Back")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":

            image_path = input(
                "\nEnter stego image path: "
            ).strip()

            if not check_image(image_path):
                continue

            password = getpass(
                "Enter password: "
            )

            if not password:

                print("ERROR: Password cannot be empty.")
                continue

            message = extract_message(
                image_path,
                password
            )

            if message is not None:

                print("\n================================")
                print("       MESSAGE EXTRACTED")
                print("================================")

                print(message)

        elif choice == "2":

            break

        else:

            print("\nInvalid choice.")


# ==================================================
# IMAGE STEGANOGRAPHY MENU
# ==================================================

def image_steganography_menu():

    while True:

        print("\n================================")
        print("       IMAGE STEGANOGRAPHY")
        print("================================")

        print("1. Hide Data")
        print("2. Extract Data")
        print("3. Check Image")
        print("4. Back")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":

            image_hide_menu()

        elif choice == "2":

            image_extract_menu()

        elif choice == "3":

            image_path = input(
                "\nEnter image path: "
            ).strip()

            if check_image(image_path):

                show_capacity(image_path)

        elif choice == "4":

            break

        else:

            print("\nInvalid choice.")


# ==================================================
# MAIN MENU
# ==================================================

def main():

    while True:

        print("\n")
        print("==========================================")
        print("       STEGANOGRAPHY MULTI-TOOL")
        print("==========================================")

        print("1. Image Steganography")
        print("2. Audio Steganography")
        print("3. Text Steganography")
        print("4. Settings")
        print("5. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":

            image_steganography_menu()

        elif choice == "2":

            print("\nAudio Steganography is coming later.")

        elif choice == "3":

            print("\nText Steganography is coming later.")

        elif choice == "4":

            print("\nSettings will be added later.")

        elif choice == "5":

            print("\nExiting Steganography Multi-Tool...")
            break

        else:

            print("\nInvalid choice. Please select 1-5.")


# ==================================================
# PROGRAM START
# ==================================================

if __name__ == "__main__":
    main()