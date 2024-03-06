from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import api.schemas.sales as sales_schema

import api.cruds.sales as sales_crud
from api.db import get_db

router = APIRouter()


@router.post('/v1/sales', response_model=sales_schema.sales)
async def create_sales(request: sales_schema.sales, db: AsyncSession = Depends(get_db)):
    updated_sales = sales_crud.create_sales(db, request)
    # response.headers["Location"] = f"http://xx.xx.xx.xx:80/v1/sales/{updated_sales.name}"
    return await updated_sales


@router.get('/v1/sales', response_model=sales_schema.sales_sum)
async def check_sales(db: AsyncSession = Depends(get_db)):

    return await sales_crud.check_sales(db)
