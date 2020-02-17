"""Decorator for retrying a coroutine."""
import asyncio
from functools import wraps
from typing import Any, Callable, Coroutine, Optional


def async_retry(retries: int = 3, sleep: int = 1) -> Callable:
    """Decorate coroutine to retry if an exception is raised.

    Args:
        retries (int): Number of times to retry. Default is 3.
        sleep (int): Seconds to sleep between each retry. Default to 1.

    Raises last exception when number of retries is reached.
    """
    def wrapper(coro: Callable[..., Coroutine]) -> Callable[..., Coroutine]:
        @wraps(coro)
        async def retry(*args: Any, **kwargs: Any) -> Optional[Any]:
            for retry in range(1, retries+1):
                try:
                    return await coro(*args, **kwargs)
                except Exception:
                    if retry == retries:
                        raise
                await asyncio.sleep(sleep)
        return retry
    return wrapper
