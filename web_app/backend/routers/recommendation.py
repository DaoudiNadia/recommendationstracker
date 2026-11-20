import logging
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy import inspect as sa_inspect
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from pydantic_classes import *
from sql_alchemy import *
from database import get_db, integrity_error_detail
from bal_stdlib import *

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/recommendation/", response_model=None, tags=["Recommendation"])
def get_all_recommendation(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    return database.query(Recommendation).all()


@router.get("/recommendation/count/", response_model=None, tags=["Recommendation"])
def get_count_recommendation(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Recommendation entities"""
    count = database.query(Recommendation).count()
    return {"count": count}


@router.get("/recommendation/paginated/", response_model=None, tags=["Recommendation"])
def get_paginated_recommendation(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Recommendation entities"""
    total = database.query(Recommendation).count()
    recommendation_list = database.query(Recommendation).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": recommendation_list
    }
@router.get("/recommendation/search/", response_model=None, tags=["Recommendation"])
def search_recommendation(
    note: str = None,
    title: str = None,
    database: Session = Depends(get_db)
) -> list:
    """Search Recommendation entities by attributes"""
    query = database.query(Recommendation)

    if note is not None:
        query = query.filter(Recommendation.note.ilike(f"%{note}%"))
    if title is not None:
        query = query.filter(Recommendation.title.ilike(f"%{title}%"))

    results = query.all()
    return results


@router.get("/recommendation/{recommendation_id}/", response_model=None, tags=["Recommendation"])
@router.get("/recommendation/{recommendation_id}", response_model=None, tags=["Recommendation"], include_in_schema=False)
async def get_recommendation(recommendation_id: int, database: Session = Depends(get_db)) -> Recommendation:
    db_recommendation = database.query(Recommendation).filter(Recommendation.id == recommendation_id).first()
    if db_recommendation is None:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    return db_recommendation



@router.post("/recommendation/", response_model=None, tags=["Recommendation"])
async def create_recommendation(recommendation_data: RecommendationCreate, database: Session = Depends(get_db)) -> Recommendation:


    db_recommendation = Recommendation(
        added_on=recommendation_data.added_on,        category=recommendation_data.category.name,        note=recommendation_data.note,        status=recommendation_data.status.name,        title=recommendation_data.title        )

    database.add(db_recommendation)
    database.flush()
    database.refresh(db_recommendation)





    database.commit()
    database.refresh(db_recommendation)
    return db_recommendation


@router.post("/recommendation/bulk/", response_model=None, tags=["Recommendation"])
async def bulk_create_recommendation(items: list[RecommendationCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Recommendation entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_recommendation = Recommendation(
                added_on=item_data.added_on,                category=item_data.category.name,                note=item_data.note,                status=item_data.status.name,                title=item_data.title            )
            database.add(db_recommendation)
            database.flush()  # Get ID without committing
            created_items.append(db_recommendation.id)
        except ValueError as e:
            errors.append({"index": idx, "error": str(e)})
        except IntegrityError as e:
            # The driver's text goes to the log; a failed flush ends the session's work.
            logger.error("Bulk creation of Recommendation failed at item %s: %s", idx, e)
            errors.append({"index": idx, "error": integrity_error_detail(e)})
            break

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Recommendation entities"
    }


@router.delete("/recommendation/bulk/", response_model=None, tags=["Recommendation"])
async def bulk_delete_recommendation(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Recommendation entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_recommendation = database.query(Recommendation).filter(Recommendation.id == item_id).first()
        if db_recommendation:
            conflict = recommendation_delete_conflict(db_recommendation)
            if conflict:
                raise HTTPException(status_code=409, detail="Cannot delete Recommendation " + str(item_id) + ": " + conflict)
            database.delete(db_recommendation)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Recommendation entities"
    }

@router.put("/recommendation/{recommendation_id}/", response_model=None, tags=["Recommendation"])
async def update_recommendation(recommendation_id: int, recommendation_data: RecommendationCreate, database: Session = Depends(get_db)) -> Recommendation:
    db_recommendation = database.query(Recommendation).filter(Recommendation.id == recommendation_id).first()
    if db_recommendation is None:
        raise HTTPException(status_code=404, detail="Recommendation not found")

    setattr(db_recommendation, 'added_on', recommendation_data.added_on)
    setattr(db_recommendation, 'category', recommendation_data.category.name)
    setattr(db_recommendation, 'note', recommendation_data.note)
    setattr(db_recommendation, 'status', recommendation_data.status.name)
    setattr(db_recommendation, 'title', recommendation_data.title)
    database.commit()
    database.refresh(db_recommendation)

    return db_recommendation


def recommendation_delete_conflict(db_recommendation, deleting=None, wholes=()):
    """Why this Recommendation cannot be deleted (None when it can): a related record
    would be left without a link it requires. Covers the parts deleted with it;
    ``deleting`` holds every record of the delete, since none of them can block it,
    and ``wholes`` the records on the way down to this part."""
    if deleting is None:
        state = sa_inspect(db_recommendation)
        deleting = [db_recommendation] + [item[0] for item in state.mapper.cascade_iterator("delete", state)]
    return None


@router.delete("/recommendation/{recommendation_id}/", response_model=None, tags=["Recommendation"])
async def delete_recommendation(recommendation_id: int, database: Session = Depends(get_db)):
    db_recommendation = database.query(Recommendation).filter(Recommendation.id == recommendation_id).first()
    if db_recommendation is None:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    conflict = recommendation_delete_conflict(db_recommendation)
    if conflict:
        raise HTTPException(status_code=409, detail="Cannot delete Recommendation " + str(recommendation_id) + ": " + conflict)
    # Snapshot the columns before deleting: cascading the association-class
    # links loads relationship collections whose back-references would make
    # the JSON encoder recurse endlessly on the live object.
    deleted_recommendation = {
        attr.key: getattr(db_recommendation, attr.key)
        for attr in db_recommendation.__mapper__.column_attrs
    }
    database.delete(db_recommendation)
    database.commit()
    return deleted_recommendation



