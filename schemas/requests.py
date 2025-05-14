from pydantic import BaseModel, Field
from typing import Optional

class ChatlogIndexRequest(BaseModel):
    minimum_revenue:Optional[float] = Field(None, example = None)
    maximum_revenue:Optional[float] = Field(None, example = None)
    chatter_message:Optional[str] = Field(None, example = "Nice cock")
    chatter_name:Optional[str] = Field(None, example = "")
    fan_message:Optional[str] = Field(None, example = "Im horny")
    fan_name:Optional[str] = Field(None, example = "")
    model_name:Optional[str] = Field(None, example = "")

class ConversationIndexRequest(BaseModel):
    minimum_revenue:Optional[float] = Field(None, example = None)
    maximum_revenue:Optional[float] = Field(None, example = None)
    conversation_message:Optional[str] = Field(None, example = "Nice cock")
    chatter_name:Optional[str] = Field(None, example = "")
    fan_name:Optional[str] = Field(None, example = "")
    model_name:Optional[str] = Field(None, example = "")
    