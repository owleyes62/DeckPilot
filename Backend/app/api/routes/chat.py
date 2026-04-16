from app.core.database import get_db
from app.schemas.chat import (ChatMessageCreate, ChatMessageExchangeResponse,
                              ChatMessageResponse, ChatSessionCreate,
                              ChatSessionResponse)
from app.services.chat_orchestrator_service import ChatOrchestratorService
from app.services.chat_service import ChatService
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/sessions", response_model=ChatSessionResponse, status_code=201)
async def create_session(
    payload: ChatSessionCreate | None = None,
    db: AsyncSession = Depends(get_db),
):
    service = ChatService(db)
    return await service.create_session(title=payload.title if payload else None)


@router.get("/sessions", response_model=list[ChatSessionResponse])
async def list_sessions(
    db: AsyncSession = Depends(get_db),
):
    service = ChatService(db)
    return await service.list_sessions()


@router.get("/sessions/{session_id}", response_model=ChatSessionResponse)
async def get_session(
    session_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = ChatService(db)
    return await service.get_session_by_id(session_id)


@router.get("/sessions/{session_id}/messages", response_model=list[ChatMessageResponse])
async def list_messages(
    session_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = ChatService(db)
    return await service.list_visible_messages_by_session(session_id=session_id)


@router.post(
    "/sessions/{session_id}/messages",
    response_model=ChatMessageExchangeResponse,
    status_code=201,
)
async def send_message(
    session_id: int,
    payload: ChatMessageCreate,
    db: AsyncSession = Depends(get_db),
):
    service = ChatOrchestratorService(db)
    return await service.send_user_message(
        session_id=session_id,
        content=payload.content,
    )
