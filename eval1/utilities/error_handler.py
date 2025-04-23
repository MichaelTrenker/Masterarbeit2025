import logging
import sys
import os


class ErrorHandler:
    """
    Manages error logging and application exit strategies.

    This class provides a centralized mechanism to handle errors, allowing for logging with additional
    contextual information and managing whether the application should exit following an error.
    """

    def __init__(self):
        """
        Initializes the ErrorHandler with a logger configured to the current module name.
        """
        self.logger = logging.getLogger(__name__)

    def handle_error(self, error, context: str = None, exit_on_failure=True):
        """
        Logs errors with an optional context and determines whether to exit the application.

        Args:
            error: The error message or exception object to log.
            context (str, optional): A description of the error context to provide additional information.
            exit_on_failure (bool): If True, the application will exit after logging the error.
        """
        if context is None:
            self.logger.error(f"Error in unknown context: {error}", exc_info=True)
        else:
            self.logger.error(f"Error in context {context}: {error}", exc_info=True)
        if exit_on_failure:
            self.logger.critical(f"[-] Critical failure! Application will be stopped!")
            #sys.exit(1)
            os._exit(1)
        else:
            # ToDo create specific routines for certain error types
            pass
