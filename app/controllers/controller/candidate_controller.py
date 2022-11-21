import csv
import uuid
from typing import List

from fastapi import (APIRouter, Body, Depends, HTTPException, Request,
                     Response, status)
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, StreamingResponse

from app.controllers.controller.deps import get_current_user
from app.controllers.controller.schemas import Candidate, CandidateUpdate, User

candidate_router = APIRouter()


@candidate_router.get("/candidate", response_description="List all candidates", response_model=List[Candidate], tags=["Candidate Controller"])
async def list_candidates(request: Request, user: User = Depends(get_current_user)):
    candidates = list(request.app.database["candidates"].find())
    return candidates


@candidate_router.get("/candidate/{id}", response_description="Get a single candidate by id", response_model=Candidate, tags=["Candidate Controller"])
async def find_candidate(id: str, request: Request, user: User = Depends(get_current_user)):
    if (candidate := request.app.database["candidates"].find_one({"uuid": id})) is not None:
        return candidate

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Candidate with ID {id} not found")


@candidate_router.post(
    "/candidate",
    response_description="Create a new candidate",
    status_code=status.HTTP_201_CREATED, response_model=Candidate, tags=["Candidate Controller"])
async def create_candidate(
        request: Request, candidate: Candidate = Body(...), user: User = Depends(get_current_user)) -> JSONResponse:
    candidate.uuid = str(uuid.uuid4())
    candidate = jsonable_encoder(candidate)
    request.app.database["candidates"].insert_one(candidate)
    return candidate


@candidate_router.put("/candidate/{id}", response_description="Update a candidate", response_model=Candidate, tags=["Candidate Controller"])
async def update_candidate(id: str, request: Request, candidate: CandidateUpdate = Body(...), user: User = Depends(get_current_user)):
    candidate = {k: v for k, v in candidate.dict().items() if v is not None}

    if len(candidate) >= 1:
        request.app.database["candidates"].update_one(
            {"uuid": id}, {"$set": candidate}
        )

    if (
        existing_candidate := request.app.database["candidates"].find_one({"uuid": id})
    ) is not None:
        return existing_candidate

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Candidate with ID {id} not found")


@candidate_router.delete("/candidate/{id}", response_description="Delete a candidate", tags=["Candidate Controller"])
async def delete_candidate(id: str, request: Request, response: Response, user: User = Depends(get_current_user)):
    delete_result = request.app.database["candidates"].delete_one(
        {"uuid": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Candidate with ID {id} not found")


@candidate_router.post("/all-candidates", response_description="List all candidates", response_model=List[Candidate], tags=["Candidate Controller"])
async def list_all_candidates(request: Request, candidate: CandidateUpdate = Body(...), user: User = Depends(get_current_user)):
    candidate = {k: v for k, v in candidate.dict().items() if v is not None}
    candidates = list(request.app.database["candidates"].find(candidate))

    return candidates


@candidate_router.get("/generate-reports", response_description="List all candidates", tags=["Candidate Controller"])
async def generate_reports(request: Request, user: User = Depends(get_current_user)):
    file_name = "candidate_reports.csv"
    data = await list_candidates(request)

    await genereate_file(file_name=file_name, data=data)

    def iterfile():
        with open(file_name, mode='rb') as myFile:
            yield from myFile

    return StreamingResponse(content=iterfile(), media_type="text/csv")


async def genereate_file(file_name: str, data: list):
    with open(file_name, 'w') as myFile:
        writer = csv.writer(myFile)
        writer.writerow(Candidate.__fields__.keys())
        for dictionary in data:
            del [dictionary['_id']]
            writer.writerow(dictionary.values())
