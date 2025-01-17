from fastapi.requests import Request


def extract_ip_address(request: Request) -> str:
    user_ip = (
            request.headers.get("X-Forwarded-For") or
            request.headers.get("X-Real-Ip") or
            request.headers.get("REMOTE_ADDR") or
            request.client.host
    )
    return user_ip
