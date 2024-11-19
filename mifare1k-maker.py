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
        str: Formatted NDEF encoding string.
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
    return format_hex_result(final_result)


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
    print("-" * 50)


def get_url_prefix_choice() -> str:
    """
    Prompt the user to select a URL prefix and return the corresponding prefix byte.
    
    Returns:
        str: Hexadecimal prefix for the selected URL type.
    """
    display_menu()
    while True:
        choice = input("Select URL prefix (1 or 2): ").strip()
        if choice == "1":
            return "01"
        elif choice == "2":
            return "04"
        else:
            print("❌ Invalid choice. Please enter 1 or 2.")


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
        encoded_result = calculate_ndef(url, prefix)

        # Display the result
        print("\n🎉 NDEF Block for Mifare Classic 1k:")
        print("=" * 50)
        print(encoded_result)
        print("=" * 50)
        print("\n✅ Encoding complete!")
    except Exception as error:
        print(f"❌ An error occurred: {error}")


if __name__ == "__main__":
    main()
