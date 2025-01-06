import asyncio


async def wait_and_run_callback(duration: float, callback):
    """
    Wait for the audio duration (non-blocking) and run a callback.

    :param duration: Duration in seconds.
    :param callback: Callback function to run after the wait.
    """
    await asyncio.sleep(duration)
    await callback()
