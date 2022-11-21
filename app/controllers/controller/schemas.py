from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from app.controllers.controller.enums import (CareerLevel, Degree, Gender,
                                              JobMajor)


class User(BaseModel):
    uuid: str = Field(None)
    first_name: str = Field(...)
    last_name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "uuid": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "first_name": "Real",
                "last_name": "Huseyn",
                "email": "realhuseynli@gmail.com",
                "password": "12345678"
            }
        }


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "uuid": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "first_name": "Real",
                "last_name": "Huseyn",
                "email": "realhuseynli@gmail.com",
                "password": "12345678"
            }
        }


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


class UserUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]

    class Config:
        schema_extra = {
            "example": {
                "first_name": "Real",
                "last_name": "Huseyn",
                "email": "realhuseynli@gmail.com"
            }
        }


class Candidate(BaseModel):
    uuid: str = Field(None)
    first_name: str = Field(...)
    last_name: str = Field(...)
    email: EmailStr = Field(...)
    career_level: CareerLevel = Field(...)
    job_major: JobMajor = Field(...)
    years_of_experience: int = Field(...)
    degree_type: Degree = Field(...)
    skills: List[str] = Field(...)
    nationality: str = Field(...)
    city: str = Field(...)
    salary: str = Field(...)
    gender: Gender = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "uuid": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "first_name": "Real",
                "last_name": "Huseyn",
                "email": "realhuseynli@gmail.com",
                "career_level": "Middle",
                "job_major": "Computer Science",
                "years_of_experience": "4",
                "degree_type": "Master",
                "skills": ["Kubernetes", "Docker", "Python", "Terraform"],
                "nationality": "Azerbaijanian",
                "city": "Baku",
                "salary": "4000",
                "gender": "Male"
            }
        }


class CandidateUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    career_level: Optional[CareerLevel]
    job_major: Optional[JobMajor]
    years_of_experience: Optional[int]
    degree_type: Optional[Degree]
    skills: Optional[List[str]]
    nationality: Optional[str]
    city: Optional[str]
    salary: Optional[float]
    gender: Optional[Gender]

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "uuid": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "first_name": "Real",
                "last_name": "Huseyn",
                "email": "realhuseynli@gmail.com",
                "career_level": "Middle",
                "job_major": "Computer Science",
                "years_of_experience": "2",
                "degree_type": "Master",
                "skills": ["Kubernetes", "Docker", "Python", "Terraform"],
                "nationality": "Azerbaijanian",
                "city": "Baku",
                "salary": "4000",
                "gender": "Male"
            }
        }
