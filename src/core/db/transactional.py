from functools import wraps

from core.db.session import Session


class Transactional:
    def __call__(self, func):
        @wraps(func)
        async def _transactional(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)
                await Session.commit()
                return result
            except Exception as e:
                await Session.rollback()
                raise e

        return _transactional
