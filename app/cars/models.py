from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Cars(Base):

    __tablename__ = 'avto'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    number: Mapped[str] = mapped_column(nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    def __str__(self):

        return f"{self.name} | {self.number} | {self.user_id}"
