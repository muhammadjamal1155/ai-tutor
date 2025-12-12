"""Unit tests for main module."""

import pytest
from src.main import main


def test_main_runs():
    """Test that main function runs without error."""
    # Should not raise any exception
    main()
