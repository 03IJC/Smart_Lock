from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..core.dependencies import get_current_user
from ..database.session import get_db
from ..models.user import User
from ..schemas.log import *
from ..services.log_service import LogService

router = APIRouter(prefix = "/logs", tags = ["Logs"])

@router.get("", response_model = PaginatedLogs)
def get_logs(
    event_type: Optional[EventType] = None,
    lock_id: Optional[int] = None,
    user_id: Optional[int] = None,
    success: Optional[bool] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,

    limit: int = 50,
    offset: int = 0,


    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    filters = LogFilter(
        event_type = event_type,
        lock_id = lock_id,
        user_id = user_id,
        success = success,
        start_time = start_time,
        end_time = end_time,
    )

    items, total = LogService(db).query_logs(filters, limit, offset)

    return PaginatedLogs(
        items = [LogResponse.model_validate(item) for item in items],
        total = total,
        limit = limit,
        offset = offset,
    )