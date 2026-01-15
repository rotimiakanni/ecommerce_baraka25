from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.api.deps import get_db, get_current_active_user
from app.models.product import Product


router = APIRouter()


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(
    product_in: ProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    product = Product(**product_in.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.get("/", response_model=list[ProductRead])
def list_products(
    limit: int = 10,
    skip: int = 0,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    products = (
        db.query(Product)
        .filter(Product.is_active == True)  # noqa: E712
        .offset(skip)
        .limit(limit)
        .all()
    )
    return products


@router.get("/{product_id}", response_model=ProductRead)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
