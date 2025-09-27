"""
Test Suite for Press A Button Now Game
=======================================

This package contains comprehensive tests for all game components,
ensuring reliability, data integrity, and proper functionality across
different usage scenarios and edge cases.

Test Coverage:
    - Data loading and validation (Google Sheets integration)
    - Game logic and state transitions
    - Node execution and edge selector behavior
    - Visualization and graph construction
    - Error handling and recovery scenarios

Test Categories:
    Unit Tests: Individual class and method functionality
    Integration Tests: Cross-component interaction verification
    Data Tests: Google Sheets connectivity and validation
    Game Flow Tests: Complete gameplay scenario verification

Running Tests:
    pytest button_1/tests/                    # All tests
    pytest button_1/tests/test_button_df.py   # Data connector tests
    pytest button_1/tests/test_button_dat.py  # Data aggregator tests
    pytest button_1/tests/test_node_engine.py # Game logic tests
    pytest button_1/tests/test_story_graph.py # Visualization tests

Test Files:
    test_button_df.py: Google Sheets connector reliability
    test_button_dat.py: Data validation and query methods
    test_node_engine.py: Node execution and edge selection
    test_story_graph.py: Graph construction and visualization

Dependencies:
    - pytest: Test framework and assertion library
    - pytest-mock: Mocking capabilities for external dependencies
    - All production dependencies for integration testing
"""