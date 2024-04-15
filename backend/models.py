from fastapi import HTTPException
from sqlalchemy import ForeignKey, String, Integer,TIMESTAMP, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, validates


class Base(DeclarativeBase):
    pass


class Executor(Base):
    __tablename__ = 'executor'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)

    orders: Mapped[list['Order']] = relationship(
        back_populates='executor', uselist=True,
        lazy="selectin"
    )


class Order(Base):
    __tablename__ = 'walk_order'

    id: Mapped[int] = mapped_column(primary_key=True)
    flat: Mapped[int] = mapped_column(Integer)
    breed: Mapped[str] = mapped_column(String)
    dog_name: Mapped[str] = mapped_column(String)
    start_datetime: Mapped[DateTime] = mapped_column(
        TIMESTAMP(timezone=False),
    )
    executor_id: Mapped[int] = mapped_column(ForeignKey('executor.id'))

    executor: Mapped['Executor'] = relationship(
        back_populates='orders', uselist=False,
        lazy="selectin"
    )

    @validates("start_datetime")
    def validate_start_datetime(self, key, start_datetime):
        if (
            start_datetime.minute not in (0, 30) or
            start_datetime.second != 0 or
            start_datetime.microsecond != 0
        ):
            raise HTTPException(
                status_code=400,
                detail="Дата начала прогулки должна быть кратна 30 минутам.",
            )
        elif (
            start_datetime.hour < 7 or
            (start_datetime.hour == 23 and start_datetime.minute == 30)
        ):
            raise HTTPException(
                status_code=400,
                detail="Дата начала прогулки должна быть с 7:00 до 23:00.",
            )
        return start_datetime
