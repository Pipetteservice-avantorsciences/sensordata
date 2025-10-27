from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, RootModel


class ItemWithSerialNumber(BaseModel):
    serial_number: str = Field(..., alias='SerialNumber')


class From(BaseModel):
    asset: ItemWithSerialNumber = Field(..., alias='Asset')
    base_device: Any = Field(..., alias='BaseDevice')
    device: ItemWithSerialNumber = Field(..., alias='Device')
    access_point: ItemWithSerialNumber = Field(..., alias='AccessPoint')


class To(BaseModel):
    recipient_id: str = Field(..., alias='RecipientId')
    name: str = Field(..., alias='Name')


class Headers(BaseModel):
    from_: From = Field(..., alias='From')
    message_id: str = Field(..., alias='MessageId')
    to: To = Field(..., alias='To')
    timestamp: datetime = Field(..., alias='TimeStamp')


class Measurement(BaseModel):
    type: str = Field(..., alias='Type')
    units: str = Field(..., alias='Units')
    value: float = Field(..., alias='Value')


class SensorState(BaseModel):
    motion: str = Field(..., alias='Motion')
    reed: str = Field(..., alias='Reed')


class PayloadItem(BaseModel):
    event_id: str = Field(..., alias='EventId')
    event_date: datetime = Field(..., alias='EventDate')
    measurement: Measurement = Field(..., alias='Measurement')
    previous_field_strength: Measurement = Field(
        ..., alias='PreviousFieldStrength'
    )
    process_date: str = Field(..., alias='ProcessDate')
    sensor_state: SensorState = Field(..., alias='SensorState')
    type: str = Field(..., alias='Type')


class WebhookRequestBodyItem(BaseModel):
    headers: Headers = Field(..., alias='Headers')
    payload: list[PayloadItem] = Field(..., alias='Payload')


class WebhookRequestBody(RootModel):
    root: list[WebhookRequestBodyItem]
