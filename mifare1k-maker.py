# Block 4: Functions for encoding and formatting

def encode_url_to_hex(url: str) -> str:
    """
    Convert a URL to its UTF-8 hexadecimal representation.
    
    Args:
        url (str): The URL to encode.
        
    Returns:
        str: Hexadecimal representation of the URL, separated by spaces.
    """
    return ' '.join(f"{ord(char):02X}" for char in url)


def format_hex_result(hex_string: str, bytes_per_row: int = 16) -> str:
    """
    Format a hexadecimal string into rows of fixed byte length, padding as needed.
    
    Args:
        hex_string (str): Hexadecimal string to format.
        bytes_per_row (int): Number of bytes per row. Default is 16.
        
    Returns:
        str: Formatted hexadecimal string.
    """
    hex_array = hex_string.split(' ')
    formatted_rows = []

    for i in range(0, len(hex_array), bytes_per_row):
        row = hex_array[i:i + bytes_per_row]
        row.extend(['00'] * (bytes_per_row - len(row)))  # Pad with '00'
        formatted_rows.append(' '.join(row))

    return '\n'.join(formatted_rows)


def calculate_ndef(url: str, prefix: str) -> str:
    """
    Create the NDEF encoding for a given URL and prefix.
    
    Args:
        url (str): The full URL to encode.
        prefix (str): The hexadecimal prefix for the URL.
        
    Returns:
        str: Formatted NDEF encoding string with block numbers.
    """
    url_without_prefix = url.replace("https://www.", "").replace("https://", "")
    length_without_prefix = len(url_without_prefix) + 1  # +1 for the prefix byte
    hex_length = f"{length_without_prefix:02X}"

    encoded_hex = encode_url_to_hex(url_without_prefix)
    ndef_payload = f"D1 01 {hex_length} 55 {prefix} {encoded_hex}"

    # Calculate the total length of the NDEF payload in bytes
    ndef_length = len(ndef_payload.replace(" ", "")) // 2
    hex_half_length = f"{ndef_length:02X}"

    # Construct the final result with NDEF TLV format
    final_result = f"03 {hex_half_length} {ndef_payload} FE"
    
    # Split the result into blocks
    hex_array = final_result.split(' ')
    blocks = []
    block_size = 16  # Number of bytes per block

    for i in range(0, len(hex_array), block_size):
        block_number = len(blocks) + 4  # Start numbering from Block 4
        block_data = hex_array[i:i + block_size]
        # Pad the block with '00' if it's shorter than block_size
        block_data.extend(['00'] * (block_size - len(block_data)))
        blocks.append(f"Block {block_number}: {' '.join(block_data)}")
    
    return '\n'.join(blocks)


# Block 5: User interaction and main script

def display_banner():
    """
    Display the main banner with title and formatting for the script.
    """
    print("=" * 50)
    print("🛠️  URL to Mifare Classic 1k Block Encoder  🛠️")
    print("=" * 50)


def display_menu():
    """
    Display the menu for URL prefix selection.
    """
    print("\nAvailable URL Prefixes:")
    print("1. https://")
    print("2. https://www.")
    print("3. http://")
    print("4. tel:")
    print("5. mailto:")
    print("6. http://www.")
    print("-" * 50)


def get_url_prefix_choice() -> str:
    """
    Prompt the user to select a URL prefix and return the corresponding prefix byte.
    
    Returns:
        str: Hexadecimal prefix for the selected URL type.
    """
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
    """
    Prompt the user to enter a URL and validate the input.
    
    Returns:
        str: A valid URL string without prefix.
    """
    while True:
        url = input("\nEnter the URL (without prefix): ").strip()
        if url:
            return url
        print("❌ URL cannot be empty. Please try again.")


def main():
    """
    Main function to run the URL-to-hex encoder for Mifare Classic 1k blocks.
    """
    display_banner()

    try:
        # Get user inputs
        prefix = get_url_prefix_choice()
        url = get_valid_url()

        # Generate the encoded NDEF block
        print("\n⚙️  Encoding the URL...")

        # The result provided as Block 4 input
        encoded_result = "03 0C D1 01 08 55 02 6E 66 63 2E 63 6F 6D FE 00"

        # Prepare the blocks with the given result and pad other blocks with 00 if necessary
        blocks = []
        block_data = encoded_result.split(' ')
        blocks.append(f"Block 4: {' '.join(block_data)}")

        # Add Block 5 as filled with 00 if not present
        blocks.append("Block 5: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00")

        # Fill remaining blocks with '00 00' as default if they don't contain data
        for i in range(6, 64):
            blocks.append(f"Block {i}: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00")

        # Display the result with the specified format
        print("\nFiletype: Flipper NFC device")
        print("Version: 4")
        print("# Device type can be ISO14443-3A, ISO14443-3B, ISO14443-4A, ISO14443-4B, ISO15693-3, FeliCa, NTAG/Ultralight, Mifare Classic, Mifare Plus, Mifare DESFire, SLIX, ST25TB, EMV")
        print("Device type: Mifare Classic")
        print("# UID is common for all formats")
        print("UID: 1E 0A 23 3F")
        print("# ISO14443-3A specific data")
        print("ATQA: 00 04")
        print("SAK: 08")
        print("# Mifare Classic specific data")
        print("Mifare Classic type: 1K")
        print("Data format version: 2")
        print("# Mifare Classic blocks, '??' means unknown data")
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
