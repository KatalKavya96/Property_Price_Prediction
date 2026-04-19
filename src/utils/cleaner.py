import re


def clean_text(text: str) -> str:
    if not text:
        return text

    cleaned = text

    cleaned = cleaned.replace(")issignificantly", ") is significantly")
    cleaned = cleaned.replace(")is", ") is")

    cleaned = re.sub(r"\r\n", "\n", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)

    # Keep headings on clean lines
    cleaned = re.sub(r"\s*(###\s)", r"\n\n\1", cleaned)

    # Keep bullets on new lines
    cleaned = re.sub(r"\s*-\s", r"\n- ", cleaned)

    # Collapse excessive spaces, but preserve new lines
    cleaned = re.sub(r"[ \t]{2,}", " ", cleaned)

    return cleaned.strip()