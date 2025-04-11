from pydantic import BaseModel, Field
from typing import List


class TextModel(BaseModel):
    body: str


class MessageModel(BaseModel):
    sender: str = Field(alias='from')
    id: str
    timestamp: str
    text: TextModel
    type: str


class ProfileModel(BaseModel):
    name: str


class ContactModel(BaseModel):
    profile: ProfileModel
    wa_id: str


class MetadataModel(BaseModel):
    display_phone_number: str
    phone_number_id: str


class ValueModel(BaseModel):
    messaging_product: str
    metadata: MetadataModel
    contacts: List[ContactModel] | None = None
    messages: List[MessageModel] | None = None


class ChangeModel(BaseModel):
    value: ValueModel
    field: str


class EntryModel(BaseModel):
    id: str
    changes: List[ChangeModel]


class WebhookBody(BaseModel):
    object: str
    entry: List[EntryModel]

    def is_message(self):
        return self.entry[0].changes[0].value.messages is not None

    def message(self):
        return self.entry[0].changes[0].value.messages[0]

    def sender(self):
        return self.message().sender

    def text(self):
        return self.message().text.body

    def message_id(self):
        return self.message().id
