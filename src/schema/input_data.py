from datetime import date
from typing import Annotated, Literal
from pydantic import BaseModel, Field, computed_field

class InputFeatures(BaseModel):
    Store: Annotated[int, Field(gt=0, lt=1116, description="Store ID")]

    Is_Promo_Active: Annotated[
        Literal[0, 1], Field(description="Is there an ongoing promotion")
    ]
    School_holiday: Annotated[
        Literal[0, 1], Field(description="School holiday status")
    ]
    Storetype: Annotated[
        Literal["a", "b", "c", "d"], Field(description="Type of Store")
    ]
    Assortment: Annotated[
        Literal["Basic", "Extended", "Extra"],
        Field(description="Assortment of Store"),
    ]
    Competition_Distance: Annotated[
        int,
        Field(
            gt=0, lt=111000, description="Distance to competition in meters"
        ),
    ]
    Is_Promo2_Active: Annotated[
        Literal[0, 1], Field(description="Is Promo2 active")
    ]
    Date: date = Field(description="Date for prediction (YYYY-MM-DD)")

    Next_holiday: date = Field(description="Date of next holiday (YYYY-MM-DD)")

    # --- Computed Fields ---

    @computed_field
    @property
    def DayOfWeek(self) -> str:
        day=self.Date.weekday() + 1  # Convert to 1-7 range
        return str(day)
    
    @computed_field
    @property
    def days_till_next_holiday(self) -> int:
        return (self.Next_holiday - self.Date).days
    
    @computed_field
    @property
    def month(self) -> int:
        return self.Date.month

    @computed_field
    @property
    def day(self) -> int:
        return self.Date.day

    @computed_field
    @property
    def promo_x_storetype(self) -> str:
        return f"{self.Is_Promo_Active}-{self.Storetype}"

    @computed_field
    @property
    def promo2_x_storetype(self) -> str:
        return f"{self.Is_Promo2_Active}-{self.Storetype}"

    @computed_field
    @property
    def promo_x_dayofweek(self) -> str:
        return f"{self.Is_Promo_Active}-{self.DayOfWeek}"

    @computed_field
    @property
    def promo2_x_dayofweek(self) -> str:
        return f"{self.Is_Promo2_Active}-{self.DayOfWeek}"


class InsertData(BaseModel):
    Store: Annotated[int, Field(gt=0, lt=1116, description="Store ID")]
    Date: date = Field(description="Date of actual data (YYYY-MM-DD)")
    Sales: Annotated[int, Field(ge=0, description="Actual Sales")]
    Customers: Annotated[int, Field(ge=0, description="Actual Customers")]
