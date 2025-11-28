import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    uid: Mapped[str] = mapped_column(String, unique=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String)
    username: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)

    address = relationship("Address", back_populates="user", uselist=False)
    credit_card = relationship("CreditCard", back_populates="user", uselist=False)


class Address(Base):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    city: Mapped[str] = mapped_column(String)
    street_name: Mapped[str] = mapped_column(String)
    country: Mapped[str] = mapped_column(String)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user = relationship("User", back_populates="address")


class CreditCard(Base):
    __tablename__ = "credit_cards"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    cc_number: Mapped[str] = mapped_column(String)
    cc_type: Mapped[str] = mapped_column(String)
    cc_expiry: Mapped[str] = mapped_column(String)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user = relationship("User", back_populates="credit_card")
