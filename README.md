# URL to Mifare Classic 1k Block Encoder

This script encodes a given URL into a hexadecimal representation suitable for use with Mifare Classic 1k blocks, using NDEF (NFC Data Exchange Format) standards. It allows customization of URL prefixes and formats the result into a well-organized block structure.

---

## Features

- **Encode URLs to Hexadecimal**: Convert URLs into their UTF-8 hexadecimal representation.
- **Format Hexadecimal Output**: Arrange the encoded hexadecimal values into rows for easier readability.
- **NDEF Encoding**: Generate a complete NDEF payload for the given URL.
- **User-Friendly Interface**: Includes a banner and menu for selecting URL prefixes and input validation.
- **Flipper Zero**: Display all the code to the Flipper Zero format.
---

## Usage

### Prerequisites

- Python 3.x installed on your system.

### How to Run

1. Clone or download the script.
2. Open a terminal and navigate to the script's directory.
3. Run the script:

   ```bash
   python mifare1k-flipmaker.py
   ```
4. Follow the prompts:
- Select a URL prefix.
- Enter the URL (excluding the prefix).
5. The script will generate and display the NDEF block.

### Example
```plaintext
=========================================================
🛠️  URL to Mifare Classic 1k Block Encoder  🛠️
=========================================================

Available URL Prefixes:
1. https://
2. https://www.
3. http://
4. tel:
5. mailto:
6. http://www.
---------------------------------------------------------
Select URL prefix (from 1 to 6): 2

Enter the URL (without prefix): example.com

⚙️  Encoding the URL...

🎉 NDEF Block for Mifare Classic 1k:
=========================================================
Block 4: 03 10 D1 01 0C 55 02 65 78 61 6D 70 6C 65 2E 63
Block 5: 6F 6D FE 00 00 00 00 00 00 00 00 00 00 00 00 00
=========================================================

✅ Encoding complete!

```
### Customization
- Modify bytes_per_row in format_hex_result for different row lengths.
- Add more prefix options by extending the get_url_prefix_choice function.
