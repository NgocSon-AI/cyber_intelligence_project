import re
import unicodedata
from typing import Dict, List


class VietnamRelevanceDetector:
    """
    Comprehensive Vietnam-related content detector
    Designed for leak forums / dark web / dirty text
    """

    def __init__(self):
        # ===== STRONG INDICATORS =====
        self.strong_patterns = [
            r"\bvietnam\b",
            r"\bviet[\s\-_]*nam\b",
            r"\bvi[eê]̣?t[\s\-_]*nam\b",
            r"\.vn\b",
        ]

        # ===== WEAK / DIRTY TEXT INDICATORS =====
        self.weak_patterns = [
            r"\bvn\b",
            r"vi.{0,2}t.{0,2}na[mn]",
            r"viet[a-z0-9_]{0,10}",
        ]

        # ===== ORGANIZATIONS / TELCO / COMMON ENTITIES =====
        self.entity_keywords = [
            "viettel",
            "vinaphone",
            "mobifone",
            "vnpt",
            "vng",
            "fpt",
            "vietnamairlines",
            "vietcombank",
            "bidv",
            "agribank",
        ]

        self.compiled_strong = [
            re.compile(p, re.IGNORECASE | re.UNICODE) for p in self.strong_patterns
        ]
        self.compiled_weak = [
            re.compile(p, re.IGNORECASE | re.UNICODE) for p in self.weak_patterns
        ]

    # ---------- TEXT NORMALIZATION ----------

    def normalize(self, text: str) -> str:
        if not text:
            return ""

        text = text.lower()
        text = unicodedata.normalize("NFD", text)
        text = "".join(
            c for c in text if unicodedata.category(c) != "Mn"
        )
        return text

    # ---------- DETECTION CORE ----------

    def detect(self, post: Dict) -> Dict:
        """
        Input:
            post = {
                "title": "...",
                "content": "..."
            }

        Output:
            post["detect_result"] = {
                label,
                score,
                confidence,
                reasons
            }
        """

        text = self.normalize(
            f"{post.get('title', '')} {post.get('content', '')}"
        )

        score = 0
        reasons: List[str] = []

        # --- Strong patterns ---
        for patt in self.compiled_strong:
            if patt.search(text):
                score += 3
                reasons.append(f"strong_match:{patt.pattern}")

        # --- Weak patterns ---
        for patt in self.compiled_weak:
            if patt.search(text):
                score += 1
                reasons.append(f"weak_match:{patt.pattern}")

        # --- Entity keywords ---
        for kw in self.entity_keywords:
            if kw in text:
                score += 2
                reasons.append(f"entity:{kw}")

        # --- Classification ---
        if score >= 6:
            label = "HIGH_CONFIDENCE_VN"
            confidence = "HIGH"
        elif score >= 3:
            label = "MEDIUM_CONFIDENCE_VN"
            confidence = "MEDIUM"
        elif score >= 1:
            label = "LOW_CONFIDENCE_VN"
            confidence = "LOW"
        else:
            label = "NOT_VN"
            confidence = "NONE"

        post["detect_result"] = {
            "label": label,
            "country": "VN" if score > 0 else None,
            "score": score,
            "confidence": confidence,
            "reasons": reasons,
        }

        return post
