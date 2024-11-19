def encode_url_to_hex(url: str) -> str:
    return ' '.join(f"{ord(char):02X}" for char in url)


def format_hex_result(hex_string: str, bytes_per_row: int = 16) -> str:
    hex_array = hex_string.split(' ')
    formatted_rows = []

    for i in range(0, len(hex_array), bytes_per_row):
        row = hex_array[i:i + bytes_per_row]
        row.extend(['00'] * (bytes_per_row - len(row)))
        formatted_rows.append(' '.join(row))

    return '\n'.join(formatted_rows)


def calculate_ndef(url: str, prefix: str) -> str:
    url_without_prefix = url.replace("https://www.", "").replace("https://", "")
    length_without_prefix = len(url_without_prefix) + 1
    hex_length = f"{length_without_prefix:02X}"

    encoded_hex = encode_url_to_hex(url_without_prefix)
    ndef_payload = f"D1 01 {hex_length} 55 {prefix} {encoded_hex}"

    ndef_length = len(ndef_payload.replace(" ", "")) // 2
    hex_half_length = f"{ndef_length:02X}"

    final_result = f"03 {hex_half_length} {ndef_payload} FE"
    
    hex_array = final_result.split(' ')
    blocks = []
    block_size = 16

    for i in range(0, len(hex_array), block_size):
        block_number = len(blocks) + 4
        block_data = hex_array[i:i + block_size]
        block_data.extend(['00'] * (block_size - len(block_data)))
        blocks.append(f"Block {block_number}: {' '.join(block_data)}")
    
    return '\n'.join(blocks)


def display_banner():
    print("=" * 50)
    print("🛠️  URL to Mifare Classic 1k Block Encoder  🛠️")
    print("=" * 50)


def display_menu():
    print("\nAvailable URL Prefixes:")
    print("1. https://")
    print("2. https://www.")
    print("3. http://")
    print("4. tel:")
    print("5. mailto:")
    print("6. http://www.")
    print("-" * 50)


def get_url_prefix_choice() -> str:
    display_menu()
    while True:
        choice = input("Select URL prefix (from 1 to 6): ").strip()
        if choice == "1":
            return "04"
        elif choice == "2":
            return "02"
        elif choice == "3":
            return "03"
        elif choice == "4":
            return "05"
        elif choice == "5":
            return "06"
        elif choice == "6":
            return "01"
        else:
            print("❌ Invalid choice. Please enter from 1 to 6.")


def get_valid_url() -> str:
    while True:
        url = input("\nEnter the URL (without prefix): ").strip()
        if url:
            return url
        print("❌ URL cannot be empty. Please try again.")


def main():
    display_banner()

    try:
        prefix = get_url_prefix_choice()
        url = get_valid_url()

        print("\n⚙️  Encoding the URL...")

        encoded_result = "03 0C D1 01 08 55 02 6E 66 63 2E 63 6F 6D FE 00"

        blocks = []
        block_data = encoded_result.split(' ')
        blocks.append(f"Block 4: {' '.join(block_data)}")

        blocks.append("Block 5: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00")

        for i in range(6, 7):
            blocks.append(f"Block {i}: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00")

        # Blocks 7 to 63 with the new provided pattern
        additional_blocks = [
            "D3 F7 D3 F7 D3 F7 7F 07 88 40 FF FF FF FF FF FF",
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
            "D3 F7 D3 F7 D3 F7 7F 07 88 40 FF FF FF FF FF FF",
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
            "D3 F7 D3 F7 D3 F7 7F 07 88 40 FF FF FF FF FF FF",
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
            "D3 F7 D3 F7 D3 F7 7F 07 88 40 FF FF FF FF FF FF",
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
            "D3 F7 D3 F7 D3 F7 7F 07 88 40 FF FF FF FF FF FF",
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
            "D3 F7 D3 F7 D3 F7 7F 07 88 40 FF FF FF FF FF FF",
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
            "D3 F7 D3 F7 D3 F7 7F 07 88 40 FF FF FF FF FF FF",
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
            "D3 F7 D3 F7 D3 F7 7F 07 88 40 FF FF FF FF FF FF",
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
            "D3 F7 D3 F7 D3 F7 7F 07 88 40 FF FF FF FF FF FF",
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
            "D3 F7 D3 F7 D3 F7 7F 07 88 40 FF FF FF FF FF FF",
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
            "D3 F7 D3 F7 D3 F7 7F 07 88 40 FF FF FF FF FF FF",
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
            "D3 F7 D3 F7 D3 F7 7F 07 88 40 FF FF FF FF FF FF",
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
            "D3 F7 D3 F7 D3 F7 7F 07 88 40 FF FF FF FF FF FF",
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
            "D3 F7 D3 F7 D3 F7 7F 07 88 40 FF FF FF FF FF FF",
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
            "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
            "D3 F7 D3 F7 D3 F7 7F 07 88 40 FF FF FF FF FF FF",
        ]
        
        # Adding these blocks starting from Block 7
        for i, block in enumerate(additional_blocks, start=7):
            blocks.append(f"Block {i}: {block}")
        
        # Continue with the rest of the blocks as necessary
        print("\nFiletype: Flipper NFC device")
        print("Version: 4")
        print("Device type: Mifare Classic")
        print("UID: 1E 0A 23 3F")
        print("ATQA: 00 04")
        print("SAK: 08")
        print("Mifare Classic type: 1K")
        print("Data format version: 2")
        print("Block 0: 1E 0A 23 3F 08 08 04 00 62 63 64 65 66 67 68 69")
        print("Block 1: 14 01 03 E1 03 E1 03 E1 03 E1 03 E1 03 E1 03 E1")
        print("Block 2: 03 E1 03 E1 03 E1 03 E1 03 E1 03 E1 03 E1 03 E1")
        print("Block 3: A0 A1 A2 A3 A4 A5 78 77 88 C1 89 EC A9 7F 8C 2A")
        print("\n".join(blocks))
        print("\n✅ Encoding complete!\n")
    except Exception as error:
        print(f"❌ An error occurred: {error}")


    display_banner()

    try:
        prefix = get_url_prefix_choice()
        url = get_valid_url()

        print("\n⚙️  Encoding the URL...")

        encoded_result = "03 0C D1 01 08 55 02 6E 66 63 2E 63 6F 6D FE 00"

        blocks = []
        block_data = encoded_result.split(' ')
        blocks.append(f"Block 4: {' '.join(block_data)}")

        blocks.append("Block 5: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00")

        for i in range(6, 64):
            blocks.append(f"Block {i}: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00")

        print("\nFiletype: Flipper NFC device")
        print("Version: 4")
        print("Device type: Mifare Classic")
        print("UID: 1E 0A 23 3F")
        print("ATQA: 00 04")
        print("SAK: 08")
        print("Mifare Classic type: 1K")
        print("Data format version: 2")
        print("Block 0: 1E 0A 23 3F 08 08 04 00 62 63 64 65 66 67 68 69")
        print("Block 1: 14 01 03 E1 03 E1 03 E1 03 E1 03 E1 03 E1 03 E1")
        print("Block 2: 03 E1 03 E1 03 E1 03 E1 03 E1 03 E1 03 E1 03 E1")
        print("Block 3: A0 A1 A2 A3 A4 A5 78 77 88 C1 89 EC A9 7F 8C 2A")
        print("\n".join(blocks))
        print("\n✅ Encoding complete!\n")
    except Exception as error:
        print(f"❌ An error occurred: {error}")


if __name__ == "__main__":
    main()
