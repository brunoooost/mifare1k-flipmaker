# url2nfc-fliper

This Python project generates NFC-compatible data for URLs, formatted in a way that can be written to NFC tags using devices like **Flipper Zero**. The application processes URLs, converts them into a specific hexadecimal format, and prepares them for encoding on NFC tags.

## Features ⭐

- **URL Processing:** The script processes a URL, identifies its protocol, and extracts relevant details.
- **Hexadecimal Conversion:** The URL is converted into a hexadecimal string, compatible with NFC data encoding.
- **Flipper Zero Compatibility:** The output is formatted for use with the Flipper Zero device, including padding, block numbering, and specific headers.
- **Customizable Blocks:** The NFC data is formatted into adjusted blocks, with padding if necessary.


## Example Output 📑

After entering a URL like `https://example.com`, the output might look like this:

```
=== Generated NFC File ===
Filetype: Flipper NFC device
Version: 4
# Device type: Mifare Classic
Device type: Mifare Classic
UID: 1E 0A 23 3F
# ISO14443-3A specific data
ATQA: 00 04
SAK: 08
Mifare Classic type: 1K
Data format version: 2
# Mifare Classic blocks
Block 0: 1E 0A 23 3F 08 08 04 00 62 63 64 65 66 67 68 69
Block 1: 14 01 03 E1 03 E1 03 E1 03 E1 03 E1 03 E1 03 E1
...
Block 63: D3 F7 D3 F7 D3 F7 7F 07 88 40 FF FF FF FF FF FF
```

### **Generated Blocks**:

Each data block will consist of 32 hexadecimal characters, and will be numbered to make it easier to write to the NFC tag. The output also includes additional padding where necessary to complete the blocks.

