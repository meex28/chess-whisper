import chess

from app.backend.chess_engine.user_commands import recognise_move_command
from app.levels.types import UserInputHandlerResult, ScenarioStepCallback, UserInputHandler
from app.service.scenario_flow.callbacks import assistant_unrecognized_input_callback, build_assistant_text_callback
from app.service.session_state import LevelState


def build_user_confirmation_handler(callbacks: list[ScenarioStepCallback]) -> UserInputHandler:
    def run(user_input: str, _: LevelState) -> UserInputHandlerResult:
        confirmation_words = ["tak", "pewnie", "oczywiście", "jazda", "dawaj"]
        accepted = False
        for word in confirmation_words:
            if word in user_input:
                accepted = True
                break

        return UserInputHandlerResult(
            accepted=accepted,
            callbacks=callbacks if accepted else []
        )
    return run

def build_user_move_expected_handler(expected_move: chess.Move, unexpected_move_response: str, callbacks: list[ScenarioStepCallback]) -> UserInputHandler:
    def run(user_input: str, level_state: LevelState) -> UserInputHandlerResult:
        recognised_move = recognise_move_command(
            player_color=level_state.user_color,
            board=level_state.board,
            raw_text=user_input
        )

        if recognised_move is None:
            # TODO: if we have more handlers we shouldn't accept allways this handler but do better validation in recognise_move_command
            return UserInputHandlerResult(
                accepted=True,
                callbacks=[assistant_unrecognized_input_callback]
            )

        print("recognised_move:", recognised_move)
        print("expected_move:", expected_move)

        is_expected = recognised_move.from_square == expected_move.from_square and recognised_move.to_square == expected_move.to_square

        if not is_expected:
            return UserInputHandlerResult(
                accepted=True,
                callbacks=[build_assistant_text_callback(unexpected_move_response)]
            )

        return UserInputHandlerResult(
            accepted=True,
            callbacks=callbacks
        )
    return run