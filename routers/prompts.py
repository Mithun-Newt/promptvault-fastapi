from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi import status
from security import get_current_user

from models import User

from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session
from sqlalchemy import or_

from database import get_db

from models import Prompt

from schemas import PromptCreate
from schemas import PromptPatch
from schemas import PromptResponse


router = APIRouter()

templates = Jinja2Templates(directory="templates")


# ---------------- HOME PAGE ----------------

@router.get("/", include_in_schema=False)
def home(request: Request):

    return templates.TemplateResponse(
        request,
        "home.html",
        {}
    )


# ---------------- GET ALL PROMPTS ----------------

@router.get(
    "/api/prompts",
    response_model=list[PromptResponse]
)
def get_prompts(
    search: str = "",
    favorites: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    query = db.query(Prompt).filter(Prompt.user_id == current_user.id)


    if search:

        query = query.filter(

            or_(

                Prompt.title.ilike(f"%{search}%"),

                Prompt.content.ilike(f"%{search}%"),

                Prompt.category.ilike(f"%{search}%")
            )
        )


    if favorites:

        query = query.filter(
            Prompt.favorite == True
        )


    prompts = query.all()

    return prompts


# ---------------- GET SINGLE PROMPT ----------------

@router.get(
    "/api/prompts/{prompt_id}",
    response_model=PromptResponse
)
def get_prompt(
    prompt_id: int,
    db: Session = Depends(get_db)
):

    prompt = db.query(Prompt).filter(
        Prompt.id == prompt_id
    ).first()


    if not prompt:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prompt not found"
        )


    return prompt


# ---------------- CREATE PROMPT ----------------

@router.post(
    "/api/prompts",
    response_model=PromptResponse,
    status_code=status.HTTP_201_CREATED
)
def create_prompt(
    prompt: PromptCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    
):

    new_prompt = Prompt(

    title=prompt.title,

    content=prompt.content,

    category=prompt.category,

    user_id=current_user.id
)

    db.add(new_prompt)

    db.commit()

    db.refresh(new_prompt)

    return new_prompt


# ---------------- UPDATE PROMPT ----------------

@router.patch(
    "/api/prompts/{prompt_id}",
    response_model=PromptResponse
)
def update_prompt(
    prompt_id: int,
    updated_data: PromptPatch,
    db: Session = Depends(get_db)
):

    prompt = db.query(Prompt).filter(
        Prompt.id == prompt_id
    ).first()


    if not prompt:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prompt not found"
        )


    if updated_data.title is not None:

        prompt.title = updated_data.title


    if updated_data.content is not None:

        prompt.content = updated_data.content


    if updated_data.category is not None:

        prompt.category = updated_data.category


    if updated_data.favorite is not None:

        prompt.favorite = updated_data.favorite


    db.commit()

    db.refresh(prompt)

    return prompt


# ---------------- DELETE PROMPT ----------------

@router.delete("/api/prompts/{prompt_id}")
def delete_prompt(
    prompt_id: int,
    db: Session = Depends(get_db)
):

    prompt = db.query(Prompt).filter(
        Prompt.id == prompt_id
    ).first()


    if not prompt:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prompt not found"
        )


    db.delete(prompt)

    db.commit()

    return {
        "message": "Prompt deleted successfully"
    }