from pydantic import BaseModel


class AddressBase(BaseModel):
    city: str
    street_name: str
    country: str

    class Config:
        from_attributes = True


class CreditCardBase(BaseModel):
    cc_number: str
    cc_type: str
    cc_expiry: str

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: int
    uid: str
    name: str
    username: str
    email: str
    address: AddressBase | None = None
    credit_card: CreditCardBase | None = None

    class Config:
        from_attributes = True
