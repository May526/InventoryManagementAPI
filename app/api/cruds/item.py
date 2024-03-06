from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

import api.models.item as item_model
import api.models.sales as sales_model
import api.schemas.item as item_schema
from api.middlewares.http_request_middleware import InvalidParamException

async def get_item_by_name(db: AsyncSession, name: str):
    query = select(item_model.item).where(item_model.item.name == name)
    result = await db.scalar(query)
    return result

async def get_item_all(db: AsyncSession):
    query = select(item_model.item).where(item_model.item.amount > 0).order_by(item_model.item.name)
    result = await db.scalars(query)
    return result.all()

async def create_item(
    db: AsyncSession, item_create: item_schema.item
) -> item_model.item:
    item = item_model.item(**item_create.dict())
    db_item = await get_item_by_name(db, name=item.name)

    # # 名前の検証
    # if not re.match(r'^[A-Za-z]{1,8}$', item.name):
    #     raise InvalidParamException()

    # # amountの検証 (正の整数であること)
    # if not isinstance(item.amount, int) or item.amount <= 0:
    #     raise  InvalidParamException()

    if db_item:
        db_item.amount += item.amount
        await db.flush()
        await db.commit()
        await db.refresh(db_item)
        return item
    else:
        db.add(item)
        await db.flush()
        await db.commit()
        await db.refresh(item)
        return item

async def get_item(db: AsyncSession, name: str) -> item_schema.item:
    item = await get_item_by_name(db, name=name)
    if item:
        return item
    else:
        return item_schema.item(name=name, amount=0)

async def get_items(db: AsyncSession) -> List[item_schema.item]:
    return await get_item_all(db)
    # items = await get_item_all(db)
    # return item_schema.item.model_validate(items)
    # print(f"\nitems: {items}\n")
    # print(f"\ntype(items): {type(items)}\n")
    # result = []
    # for item in items:
    #     _item = item.scalar()
    #     print(f"\ntype(item): {type(_item)}\n")
    #     print(f"\nitem.name: {_item['name']}\n")
    #     result.append(item_schema.item(name=_item.name, amount=_item.amount))
    # return result
    # return [item_schema.item(name=item.name, amount=item.amount) for item in items]
    # return items
    # filtered_items = [{item.name: item.amount} for item in items if item.amount > 0]
    # print("filtered items: ", filtered_items)
    # sorted_items = sorted(filtered_items, key=lambda x: next(iter(x)))
    # print("sorted items: ", sorted_items)
    # # for item in items:
    # #     print("Item Name:", item.name, "Amount:", item.amount)
    # # return sorted(({item.name: item.amount} for item in items if item.amount > 0), key=lambda x: next(iter(x)))
    # return sorted_items

# async def delete_item(db: AsyncSession, original: List[item_schema.item]) -> None:
#     item = item_model.item(original)
#     await db.delete(item)
#     await db.commit()

async def delete_item(db: AsyncSession) -> None:
    query = delete(item_model.item)
    await db.execute(query)
    query = delete(sales_model.sales)
    await db.execute(query)
    await db.commit()