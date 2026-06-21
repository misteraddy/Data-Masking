import os
import datafog

# Define directories
INTERMEDIATE_DIR = "intermediate_folder"
OUTPUT_DIR = "output"

# Create directories if they do not exist
os.makedirs(INTERMEDIATE_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


def mask_pii(text: str) -> str:
    """Uses DataFog's built-in sanitizer to mask PII items

    using the 'smart' pipeline engine.
    """
    if not text.strip():
        return text

    # DataFog's sanitize function handles the string replacement internally
    return datafog.sanitize(text, engine="smart")


# -----------------------------
# Example OCR Text for Testing
# -----------------------------
ocr_text = """
John Smith
SSN: 123-45-6789

Address:
123 Main Street
New York, NY 10001

Phone: (212) 555-1234
Email: john.smith@example.com

Driver License: D1234567
Policy Number: POL-987654321

Credit Card: 4111 1111 1111 1111
"""

# Save original OCR text to intermediate directory
intermediate_file = os.path.join(INTERMEDIATE_DIR, "ocr_text.txt")
with open(intermediate_file, "w", encoding="utf-8") as f:
    f.write(ocr_text)

# Mask the PII in the text
masked_text = mask_pii(ocr_text)

# Save the masked output to output directory
output_file = os.path.join(OUTPUT_DIR, "masked_ocr_text.txt")
with open(output_file, "w", encoding="utf-8") as f:
    f.write(masked_text)

# Print status and results
print("Original OCR text saved to:", intermediate_file)
print("Masked output saved to:", output_file)
print("\n--- Masked Text Output ---\n")
print(masked_text)