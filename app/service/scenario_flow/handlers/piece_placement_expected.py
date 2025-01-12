import chess

from app.backend.chess_engine.user_commands import recognise_raw_move_from_text
from app.levels.types import UserInputHandler, UserInputHandlerResult, ScenarioStepCallback, LevelState
from app.service.scenario_flow.callbacks.assistant_text import build_assistant_text_callback


def build_user_piece_placement_expected_handler(
        expected_piece: chess.PieceType,
        expected_square: chess.Square,
        unexpected_move_text: str,
        callbacks: list[ScenarioStepCallback]
) -> UserInputHandler:
    def user_piece_placement_expected_handler(text: str, _: 'LevelState') -> 'UserInputHandlerResult':
        raw_move = recognise_raw_move_from_text(text)
        print("Expected: ", expected_piece, expected_square)
        print("RAW MOVE: ", raw_move)
        if raw_move.piece is None or raw_move.fieldTo is None:
            return UserInputHandlerResult(
                accepted=False,
                callbacks=[]
            )


        if raw_move.piece != expected_piece or raw_move.fieldTo != expected_square:
            return UserInputHandlerResult(
                accepted=True,
                callbacks=[build_assistant_text_callback(unexpected_move_text)]
            )

        return UserInputHandlerResult(
            accepted=True,
            callbacks=callbacks
        )

    return user_piece_placement_expected_handler