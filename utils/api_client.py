import requests
from typing import Optional, Dict, Any, Union


class ApiClient:
    def __init__(self, base_url: str, default_headers: Optional[Dict[str, str]] = None, timeout: int = 10):
        self.base_url = base_url.rstrip('/')
        self.default_headers = default_headers or {}
        self.timeout = timeout

    async def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Union[Dict, str]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> requests.Response:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        all_headers = {**self.default_headers, **(headers or {})}

        response = requests.request(
            method=method.upper(),
            url=url,
            params=params,
            data=data,
            json=json,
            headers=all_headers,
            timeout=self.timeout,
            **kwargs
        )
        return response

    async def get(self, endpoint: str, **kwargs) -> requests.Response:
        return await self.request("GET", endpoint, **kwargs)

    async def post(self, endpoint: str, **kwargs) -> requests.Response:
        return await self.request("POST", endpoint, **kwargs)

    async def put(self, endpoint: str, **kwargs) -> requests.Response:
        return await self.request("PUT", endpoint, **kwargs)

    async def patch(self, endpoint: str, **kwargs) -> requests.Response:
        return await self.request("PATCH", endpoint, **kwargs)

    async def delete(self, endpoint: str, **kwargs) -> requests.Response:
        return await self.request("DELETE", endpoint, **kwargs)

