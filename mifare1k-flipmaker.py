# Constants
BLOCK_SIZE = 16
PREFIX_OPTIONS = {
    "1": ("https://", "04"),
    "2": ("https://www.", "02"),
    "3": ("http://", "03"),
    "4": ("tel:", "05"),
    "5": ("mailto:", "06"),
    "6": ("http://www.", "01"),
}


def encode_url_to_hex(url: str) -> str:
    """Encodes a URL to a space-separated hexadecimal string."""
    return ' '.join(f"{ord(char):02X}" for char in url)


def format_hex_result(hex_string: str, bytes_per_row: int = BLOCK_SIZE) -> str:
    """Formats a hex string into rows of a specified byte width."""
    hex_array = hex_string.split(' ')
    formatted_rows = []

    for i in range(0, len(hex_array), bytes_per_row):
        row = hex_array[i:i + bytes_per_row]
        # Pad with '00' if the row is shorter than required bytes_per_row
        row.extend(['00'] * (bytes_per_row - len(row)))
        formatted_rows.append(' '.join(row))

    return '\n'.join(formatted_rows)


def calculate_ndef(url: str, prefix_hex: str) -> str:
    """
    Encodes a URL into the NDEF format for Mifare Classic 1k.

    Args:
        url: The URL without its prefix.
        prefix_hex: Hexadecimal representation of the URL prefix.

    Returns:
        A formatted string containing the NDEF TLV blocks.
    """
    url_without_prefix = url.replace("https://www.", "").replace("https://", "")
    length_without_prefix = len(url_without_prefix) + 1  # +1 for the prefix byte
    hex_length = f"{length_without_prefix:02X}"

    encoded_hex = encode_url_to_hex(url_without_prefix)
    ndef_payload = f"D1 01 {hex_length} 55 {prefix_hex} {encoded_hex}"

    # Calculate total payload length in bytes
    ndef_length = len(ndef_payload.replace(" ", "")) // 2
    hex_half_length = f"{ndef_length:02X}"

    # Construct the NDEF TLV format
    final_result = f"03 {hex_half_length} {ndef_payload} FE"

    # Split the result into blocks for Mifare Classic
    hex_array = final_result.split(' ')
    blocks = []
    block_number = 4  # Blocks start from Block 4

    for i in range(0, len(hex_array), BLOCK_SIZE):
        if block_number % 4 == 3:  # Skip blocks like 7, 11, 15, etc.
            block_number += 1
            continue

        block_data = hex_array[i:i + BLOCK_SIZE]
        block_data.extend(['00'] * (BLOCK_SIZE - len(block_data)))  # Pad if necessary
        blocks.append(f"Block {block_number}: {' '.join(block_data)}")
        block_number += 1

    return '\n'.join(blocks)


def display_banner():
    """Displays the application banner."""
    print("=" * 57)
    print("🛠️  URL to Mifare Classic 1k Block Encoder  🛠️")
    print("=" * 57)


def display_menu():
    """Displays the menu for URL prefix selection."""
    print("\nAvailable URL Prefixes:")
    for key, (prefix, _) in PREFIX_OPTIONS.items():
        print(f"{key}. {prefix}")
    print("-" * 57)


def get_url_prefix_choice() -> str:
    """Prompts the user to select a URL prefix."""
    display_menu()
    while True:
        choice = input("Select URL prefix (from 1 to 6): ").strip()
        if choice in PREFIX_OPTIONS:
            return PREFIX_OPTIONS[choice][1]  # Return the corresponding hex code
        print("❌ Invalid choice. Please enter a number from 1 to 6.")


def get_valid_url() -> str:
    """Prompts the user for a valid URL."""
    while True:
        url = input("\nEnter the URL (without prefix): ").strip()
        if url:
            return url
        print("❌ URL cannot be empty. Please try again.")


def main():
    """Main function to drive the program."""
    display_banner()

    try:
        # Get user inputs
        prefix_hex = get_url_prefix_choice()
        url = get_valid_url()

        # Generate the encoded NDEF blocks
        print("\n⚙️  Encoding the URL...")
        encoded_result = calculate_ndef(url, prefix_hex)

        # Display the result
        print("\n🎉 NDEF Block for Mifare Classic 1k:")
        print("=" * 57)
        print(encoded_result)
        print("=" * 57)
        print("\n✅ Encoding complete!\n")
    except Exception as error:
        print(f"❌ An error occurred: {error}")


if __name__ == "__main__":
    main()
