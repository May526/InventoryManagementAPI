from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import api.schemas.item as item_schema
import api.cruds.item as item_crud
# import api.models.item as item_model
from api.db import get_db
from typing import List,Optional

router = APIRouter()


@router.post('/v1/stocks', response_model=item_schema.item)
async def create_item(item_body: item_schema.item,
                      db: AsyncSession = Depends(get_db)):

    return await item_crud.create_item(db, item_body)


@router.get('/v1/stocks/{name}', response_model=item_schema.item)
async def get_item(name: str, db: AsyncSession = Depends(get_db)):
    item = await item_crud.get_item(db, name)
    return {item.name: item.amount}

# @router.get('/v1/stocks/{name}', response_model=item_schema.item)
# async def get_item(name: str, db: AsyncSession = Depends(get_db)):
#     return await item_crud.get_item(db, name)


@router.get('/v1/stocks/')
async def get_items(db: AsyncSession = Depends(get_db)):
    items = await item_crud.get_items(db)
    result = {item.name: item.amount for item in items}
    return result

# @router.get('/v1/stocks', response_model=List[item_schema.item])
# async def get_items(db: AsyncSession = Depends(get_db)):
#     return await item_crud.get_items(db)

@router.delete('/v1/stocks')
async def delete_item(db: AsyncSession = Depends(get_db)):
    return await item_crud.delete_item(db)