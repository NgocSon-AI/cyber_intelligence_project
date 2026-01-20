# src/utils/exception.py
"""
Custom exception classes for the Cyber Intelligence Project.

This module defines a hierarchy of custom exceptions that provide
specific error handling for different components of the application.
All exceptions inherit from MonitoringError for consistent error handling.
"""

from typing import Optional, Any


class MonitoringError(Exception):
    """
    Base exception for all cyber intelligence monitoring operations.

    This is the root exception class that all other custom exceptions
    inherit from, allowing for consistent error handling across the application.

    Attributes:
        message: Error message
        details: Additional error details/context
    """

    def __init__(self, message: str, details: Optional[Any] = None):
        """
        Initialize the monitoring error.

        Args:
            message: Human-readable error message
            details: Additional context or data about the error
        """
        super().__init__(message)
        self.message = message
        self.details = details

    def __str__(self) -> str:
        """Return string representation of the error."""
        if self.details:
            return f"{self.message} (Details: {self.details})"
        return self.message


class ScraperError(MonitoringError):
    """
    Exception raised when web scraping operations fail.

    This includes failures in browser automation, network requests,
    or page loading issues.
    """
    pass


class ParserError(MonitoringError):
    """
    Exception raised when data parsing operations fail.

    This includes failures in HTML parsing, data extraction,
    or content processing.
    """
    pass


class DetectionError(MonitoringError):
    """
    Exception raised when data leak detection operations fail.

    This includes failures in AI model inference, rule evaluation,
    or detection logic processing.
    """
    pass


class AlertError(MonitoringError):
    """
    Exception raised when alert/notification operations fail.

    This includes failures in Telegram bot messaging, email sending,
    or other notification mechanisms.
    """
    pass


class DatabaseError(MonitoringError):
    """
    Exception raised when database operations fail.

    This includes failures in data persistence, queries, or
    database connection issues.
    """
    pass


class ConfigurationError(MonitoringError):
    """
    Exception raised when configuration-related operations fail.

    This includes missing environment variables, invalid config values,
    or configuration file parsing errors.
    """
    pass
