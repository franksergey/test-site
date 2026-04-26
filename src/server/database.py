from typing import ClassVar

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Базовый класс для всех ORM-моделей в проекте.

    Он не является таблицей сам по себе, но предоставляет общую
    конфигурацию для всех своих дочерних классов (моделей).

    Attributes:
        metadata: Экземпляр `MetaData` с настроенной конвенцией именования.
            Это гарантирует, что все ключи, индексы и ограничения в базе
            данных будут иметь предсказуемые и единообразные имена.
    """

    metadata: ClassVar[MetaData] = MetaData(
        naming_convention={
            "ix": "ix_%(table_name)s_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": (
                "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s"
            ),
            "pk": "pk_%(table_name)s",
        }
    )


class EmailEntry(Base):
    __tablename__ = "emails"

    id: Mapped[int] = mapped_column(primary_key=True)

    email: Mapped[str]
