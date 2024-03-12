
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse
from fastapi import Request


async def not_found_error(request: Request, exc: HTTPException):
    return RedirectResponse('/pebblo/not-found')


async def internal_error(request: Request, exc: HTTPException):
    return RedirectResponse('/not-found')


exception_handlers = {404: not_found_error, 500: internal_error}