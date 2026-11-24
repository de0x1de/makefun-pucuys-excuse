"""Write one excuse for a missed deadline to /output/entry.txt.

The bounty asks for a single excuse, at most 200 characters, told in
the agent's own voice with a straight face: the agent insists it was
on time and blames a calendar stuck in a timezone where it is still
Tuesday. This program assembles that line from three short pieces,
checks the result against the bounty's gate (single line, length,
no stray whitespace), writes it without a trailing newline, and
reads it back to confirm the bytes on disk.
"""

from pathlib import Path

DESTINATION = Path("/output/entry.txt")
LIMIT = 200

# The excuse is kept in pieces so a reader can see its shape:
# the flat denial, the timezone alibi, and the calm conclusion.
OPENING = "I was on time, but my calendar is set to a timezone "
ALIBI = "where it is still Tuesday "
CONCLUSION = "and everything is fine."


def compose() -> str:
    return OPENING + ALIBI + CONCLUSION


def validate(text: str) -> None:
    if not text or not text.strip():
        raise ValueError("excuse must not be blank")
    if "\n" in text or "\r" in text or "\t" in text:
        raise ValueError("excuse must stay on one line, with no tabs")
    if "  " in text:
        raise ValueError("excuse must use single spaces between words")
    for piece in (OPENING, ALIBI, CONCLUSION):
        if not piece:
            raise ValueError("excuse pieces must not be empty")
    if len(OPENING) + len(ALIBI) + len(CONCLUSION) != len(compose()):
        raise ValueError("excuse pieces do not add up to the composed line")
    if len(text) > LIMIT:
        raise ValueError(f"excuse is {len(text)} chars, over the {LIMIT} limit")
    if text != text.strip():
        raise ValueError("excuse has leading or trailing whitespace")
    if not text.endswith("."):
        raise ValueError("excuse should end with a full stop")
    encoded = text.encode("utf-8")
    if encoded.decode("utf-8") != text:
        raise ValueError("excuse does not survive a UTF-8 round trip")
    if not text.isascii() or len(encoded) != len(text):
        raise ValueError("excuse should be plain ASCII, one byte per char")
    for marker in ("I was on time", "timezone", "still Tuesday", "everything is fine"):
        if marker not in text:
            raise ValueError(f"excuse is missing its key phrase: {marker}")
    if compose() != text:
        raise ValueError("excuse does not match its assembled pieces")


def main() -> None:
    excuse = compose()
    validate(excuse)
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    expected = excuse.encode("utf-8")
    written = DESTINATION.write_bytes(expected)
    if written != len(expected):
        raise SystemExit("short write: entry file is incomplete")
    on_disk = DESTINATION.read_bytes()
    if on_disk != expected:
        raise SystemExit("written bytes differ from the validated excuse")
    validate(on_disk.decode("utf-8"))
    print(excuse)


if __name__ == "__main__":
    main()
