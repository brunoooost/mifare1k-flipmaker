
def encode_url_to_hex(url: str) -> str:
    return ' '.join(f"{ord(char):02X}" for char in url)


def format_hex_result(hex_string: str, bytes_per_row: int = 16) -> str:
    hex_array = hex_string.split(' ')
    formatted_rows = []

    for i in range(0, len(hex_array), bytes_per_row):
        row = hex_array[i:i + bytes_per_row]
        row.extend(['00'] * (bytes_per_row - len(row)))  # Pad with '00'
        formatted_rows.append(' '.join(row))

    return '\n'.join(formatted_rows)


def calculate_ndef(url: str, prefix: str) -> str:
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

        # Skip blocks like 7, 11, 15, etc. (block_number % 4 == 3)
        if (block_number % 4) == 3:
            continue

        block_data = hex_array[i:i + block_size]
        # Pad the block with '00' if it's shorter than block_size
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
        print("\n✅ Encoding complete!\n")
    except Exception as error:
        print(f"❌ An error occurred: {error}")


if __name__ == "__main__":
    main()
