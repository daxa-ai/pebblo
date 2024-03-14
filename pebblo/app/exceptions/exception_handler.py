from fastapi import Request
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse


async def not_found_error(request: Request, exc: HTTPException):
    """Redirects to not-found route when 404 exception occurs"""
    return RedirectResponse("/pebblo/not-found")


exception_handlers = {404: not_found_error, 500: not_found_error}
