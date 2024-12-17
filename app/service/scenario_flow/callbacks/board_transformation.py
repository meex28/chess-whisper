from app.backend.chess_engine.board_transformations import BoardTransformation
from app.backend.chess_engine.engine import save_svg
from app.levels.types import ScenarioStepCallback
from app.service.session_state import get_level_state, save_level_state


def build_board_transformation_callback(transformations: list[BoardTransformation]) -> ScenarioStepCallback:
    def run():
        level_state = get_level_state()

        for transformation in transformations:
            result = transformation(level_state.board)
            level_state.board = result.board
            board_svg_path = 'assets/current_board.svg'
            save_svg(result.board_svg, board_svg_path)
            level_state.board_svg_path = board_svg_path

        save_level_state(level_state)
    return run
