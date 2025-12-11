class MonitoringError(Exception):
    """Base exception for data monitoring tool."""
    pass

class ScraperError(MonitoringError):
    """Raised when scraping fails."""
    pass

class ParserError(MonitoringError):
    """Raised when parsing fails."""
    pass

class DetectionError(MonitoringError):
    """Raised when detection logic fails."""
    pass

class AlertError(MonitoringError):
    """Raised when alert sending fails."""
    pass
