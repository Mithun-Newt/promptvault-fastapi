from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from schemas import UserLogin
from fastapi.security import OAuth2PasswordRequestForm
from security import verify_password
from security import create_access_token
from sqlalchemy.orm import Session

from database import get_db

from models import User

from schemas import UserCreate
from schemas import UserResponse

from security import hash_password


router = APIRouter()


@router.post(
    "/api/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.username == user.username
    ).first()


    if existing_user:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )


    new_user = User(

        username=user.username,

        password_hash=hash_password(
            user.password
        )
    )


    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return new_user

@router.post("/api/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.username == form_data.username
    ).first()


    if not existing_user:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )


    valid_password = verify_password(

        form_data.password,

        existing_user.password_hash
    )


    if not valid_password:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )


    access_token = create_access_token({
        "sub": existing_user.username
    })


    return {
        "access_token": access_token,
        "token_type": "bearer"
    }