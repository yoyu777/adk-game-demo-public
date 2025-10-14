"""
20 Questions Game - Main Entry Point

- ui_components.py: UI elements and layout
- game_controller.py: Game logic and interactions
"""

import logging
from game_controller import GameController

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    # Main entry point for the 20 Questions Game
    try:
        app = GameController()
        app.run()
    except Exception as e:
        logger.error(f"Error starting application: {e}")
        raise


if __name__ == '__main__':
    main()