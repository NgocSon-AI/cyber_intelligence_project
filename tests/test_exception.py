"""
Test module for custom exceptions in data-monitoring project.
Run with: python -m tests.test_exception
"""

from src.utils.exception import (
    MonitoringError,
    ScraperError,
    ParserError,
    DetectionError,
    AlertError
)

def test_exceptions():
    # Test MonitoringError
    try:
        raise MonitoringError("Base monitoring error")
    except MonitoringError as e:
        print(f"Caught MonitoringError: {e}")

    # Test ScraperError
    try:
        raise ScraperError("Cannot fetch web page")
    except ScraperError as e:
        print(f"Caught ScraperError: {e}")

    # Test ParserError
    try:
        raise ParserError("Parsing failed")
    except ParserError as e:
        print(f"Caught ParserError: {e}")

    # Test DetectionError
    try:
        raise DetectionError("Detection failed")
    except DetectionError as e:
        print(f"Caught DetectionError: {e}")

    # Test AlertError
    try:
        raise AlertError("Failed to send alert")
    except AlertError as e:
        print(f"Caught AlertError: {e}")

if __name__ == "__main__":
    test_exceptions()
