from .ping import router as ping_router
from .tasks import router as task_router
from .users import router as user_router
from .auth import router as auth_router

routers = [ping_router, task_router, user_router, auth_router]
