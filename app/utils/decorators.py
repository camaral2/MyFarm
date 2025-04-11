from functools import wraps
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from psycopg2.errors import UniqueViolation
from fastapi import HTTPException, status

def db_safe(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        db = kwargs.get("db")
        if not db:
            raise ValueError("Missing 'db' in kwargs")

        try:
            result = func(*args, **kwargs)
            db.commit()
            return result

        except IntegrityError as e:
            db.rollback()
            if isinstance(e.orig, UniqueViolation):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail={"error": "Duplicate entry", "message": "This record already exists"}
                )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": "Database integrity error", "message": str(e.orig) if e.orig else str(e)}
            )

        except SQLAlchemyError as e:
            db.rollback()
            print('Error_1:' + str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"error": "Database operation failed", "message": str(e)}
            )

        except Exception as e:
            db.rollback()
            print('Error_2:' + str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"error": "Internal server error", "message": str(e)}
            )

    return wrapper
