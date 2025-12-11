import re

class DataLeakDetector:
      def __init__(self):
            # ===========================
            # 1. Danh sách từ khóa cơ bản
            # ===========================
            self.keywords = [
            "bán data", "leak data", "lộ data", "dữ liệu khách hàng", "data khách hàng",
            "dump", "combo data", "full info", "cccd", "scan cccd", "scan cmnd",
            "email list", "phone list", "data viet nam", "data vn", "database vn",
            "data người dùng", "data user", "data cá nhân"
            ]

            # ===========================
            # 2. Regex phát hiện thông tin cá nhân
            # ===========================
            self.regex_patterns = {
            "cccd": r"\b\d{12}\b",
            "cmnd": r"\b\d{9}\b",
            "vn_phone": r"\b(03|05|07|08|09)\d{8}\b",
            "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
            }
            # ===========================
            # 3. Các từ khóa ngữ cảnh rao bán
            # ===========================
            self.selling_indicators = [
            "bán", "giá", "contact", "telegram", "zalo", "dm", "inbox",
            "có sample", "dùng thử", "uy tín", "chất lượng cao"
            ]
      # ------------------------------------------------------------------
      # Check 1: Dựa trên từ khóa
      # ------------------------------------------------------------------
      def check_keywords(self, text):
            text_lower = text.lower()
            hits = []

            for kw in self.keywords:
                  if kw in text_lower:
                        hits.append(kw)

            return hits
      # ------------------------------------------------------------------
      # Check 2: Dựa trên regex (định danh cá nhân)
      # ------------------------------------------------------------------
      def check_regex(self, text):
            matches = {}

            for name, pattern in self.regex_patterns.items():
                  found = re.findall(pattern, text)
                  if found:
                        matches[name] = len(found)

            return matches
      # ------------------------------------------------------------------
      # Check 3: Dựa trên ngữ cảnh rao bán
      # ------------------------------------------------------------------
      def check_selling_context(self, text):
            text_lower = text.lower()
            hits = []

            for word in self.selling_indicators:
                  if word in text_lower:
                        hits.append(word)

            return hits

      # ------------------------------------------------------------------
      # Tạo điểm rủi ro cuối cùng
      # ------------------------------------------------------------------
      def score(self, text):
            score = 0

            # Keyword score
            kw_hits = self.check_keywords(text)
            score += len(kw_hits) * 20

            # Regex score
            regex_hits = self.check_regex(text)
            for category, count in regex_hits.items():
                  if category in ["cccd", "cmnd"]:
                        score += count * 10
                  elif category == "vn_phone":
                        score += count * 3
                  elif category == "email":
                        score += count * 2

            # Selling context
            sell_hits = self.check_selling_context(text)
            score += len(sell_hits) * 10

            return {
                  "score": score,
                  "keyword_hits": kw_hits,
                  "regex_hits": regex_hits,
                  "selling_context_hits": sell_hits
            }

      # ------------------------------------------------------------------
      # Phát hiện cuối cùng (LEAK / SAFE)
      # ------------------------------------------------------------------
      def detect(self, text, threshold=40):
            result = self.score(text)
            if result["score"] >= threshold:
                  result["label"] = "LEAK"
            else:
                  result["label"] = "SAFE"
            return result