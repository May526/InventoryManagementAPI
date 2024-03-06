from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
import re

import api.cruds.item as item_crud
import api.models.item as item_model
import api.models.sales as sales_model
import api.schemas.sales as sales_schema
from api.middlewares.http_request_middleware import InvalidParamException


async def create_sales(
    db: AsyncSession, request: sales_schema.sales
) -> sales_schema.sales:
    item = item_model.item(**request.dict())
    db_item = await item_crud.get_item_by_name(db, name=item.name)

    if not db_item:
        raise InvalidParamException()

    # # 名前の検証
    # if not re.match(r'^[A-Za-z]{1,8}$', item.name):
    #     raise InvalidParamException()

    # # amountの検証 (正の整数であること)
    # if not isinstance(item.amount, int) or item.amount <= 0:
    #     raise  InvalidParamException()

    if db_item.amount < item.amount:
        raise InvalidParamException()

    db_item.amount -= item.amount
    await db.commit()

    if item.price:
        # priceの検証 (0より大きい小数であること)
        if not isinstance(item.price, float) or item.price <= 0:
            raise  InvalidParamException()
        sales = item.amount * item.price
            # if item.amount else item.price
        sales_record = sales_model.sales(sales=sales)
        db.add(sales_record)
        # db_sales = await check_sales(db)
        # db_sales.sales += sales
        # await db.flush()
        await db.commit()

    return request


async def check_sales(db: AsyncSession) -> sales_schema.sales_sum:
    query = select(func.sum(sales_model.sales.sales))
    result = await db.scalar(query)
    if result:
        return sales_schema.sales_sum(sales=round(result,2))
    else:
        return sales_schema.sales_sum(sales=0.0)