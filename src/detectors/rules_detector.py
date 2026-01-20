import re
import unicodedata


class DataLeakDetector:
    """
    Vietnam leak detector (dirty text safe)
    """

    def __init__(self):
        self.pattern = re.compile(
            r"""
            (
                vi.{0,3}t.{0,3}na[mn]e? |
                vietnam[a-z0-9_]* |
                viet[\s\-_]*nam[a-z0-9_]* |
                vi[eê]̣?t[\s\-_]*nam[a-z0-9_]* |
                [a-z0-9_]*vn[a-z0-9_]* |
                \.vn
            )
            """,
            re.IGNORECASE | re.UNICODE | re.VERBOSE
        )

    def normalize(self, text: str) -> str:
        if not text:
            return ""
        return unicodedata.normalize("NFC", text.lower())

    def detect(self, post: dict) -> dict:
        text = self.normalize(
            f"{post.get('title','')} {post.get('content','')}"
        )

        is_vn = bool(self.pattern.search(text))

        post["detect_result"] = {
            "label": "LEAK" if is_vn else "SAFE",
            "country": "VN" if is_vn else None,
        }

        return post
