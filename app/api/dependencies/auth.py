"""Auth dependencies."""
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_401_UNAUTHORIZED

from app.api.dependencies.db_session import get_session
from app.db.admin.repo import AdminRepo
from app.schemas.admin import AdminSchema
from app.services.auth import Auth, CustomHTTPBearer

bearer = CustomHTTPBearer()


async def authenticate_user_by_token(
    credentials: HTTPAuthorizationCredentials = Security(bearer),
    auth: Auth = Depends(Auth),
    db_session: AsyncSession = Depends(get_session),
) -> AdminSchema:
    token_data = auth.decode_access_token(credentials.credentials)

    admin_repo = AdminRepo(db_session)
    admin = await admin_repo.get_or_none(username=token_data.sub)
    if admin is None:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="User not found.")

    return admin
