from typing import Optional

from pydantic import BaseModel


class CreatePlan(BaseModel):
    start_date: str
    end_date: str
    title: str
    notes: Optional[str] = None


class ReadPlan(BaseModel):
    id: int


class UpdatePlan(BaseModel):
    id: int
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    title: Optional[str] = None
    notes: Optional[str] = None


class DeletePlan(BaseModel):
    id: int
