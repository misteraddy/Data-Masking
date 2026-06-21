import os

from datafog.services import TextService


INPUT_DIR = "input"
PROCESSED_DIR = "processed"

os.makedirs(PROCESSED_DIR, exist_ok=True)

service = TextService(engine="smart")


def mask_pii(text):
    result = service.annotate_text_sync(text)

    entities = result.get("entities", []) if isinstance(result, dict) else []

    masked_text = text
    replacements = []

    for entity in entities:
        start = entity.get("start")
        end = entity.get("end")

        if start is None or end is None:
            continue

        label = (
            entity.get("label")
            or entity.get("type")
            or entity.get("entity_type")
            or "PII"
        )

        replacements.append(
            (start, end, f"[{label}]")
        )

    for start, end, replacement in sorted(
        replacements,
        key=lambda x: x[0],
        reverse=True
    ):
        masked_text = (
            masked_text[:start]
            + replacement
            + masked_text[end:]
        )

    return masked_text


def process_file(file_name):
    input_path = os.path.join(INPUT_DIR, file_name)

    with open(input_path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    masked_text = mask_pii(text)

    output_path = os.path.join(PROCESSED_DIR, file_name)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(masked_text)

    print(f"Processed: {file_name}")


def main():
    files = [
        file_name
        for file_name in os.listdir(INPUT_DIR)
        if file_name.endswith(".txt")
    ]

    if not files:
        print("No txt files found.")
        return

    for file_name in files:
        process_file(file_name)

    print("All files processed successfully.")


if __name__ == "__main__":
    main()