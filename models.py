from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer




class User(Base):
    """
    SQLAlchemy model representing a user in the system.

    Attributes:
        id (int): Primary key, auto-incremented.
        name (str): User's full name. Max length 50, cannot be null.
        age (int): User's age. cannot be null.
        email (str): User's email address. Must be unique, indexed for fast lookup, cannot be null. 
    """
    __tablename__ = "users"

    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name:Mapped[str]= mapped_column(String(50), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    email:Mapped[str] = mapped_column(String(100),unique= True, index=True, nullable=False)

    def __repr__(self) -> str:
        """
        Return a string representation of the User instance.
        Useful for debugging and logging.
         """
        return f"User(id={self.id!r}, name='{self.name!r}', age={self.age!r}, email='{self.email!r}')"
    