from http import HTTPStatus
from typing import Annotated, Union
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, TypeAdapter


router = APIRouter()
