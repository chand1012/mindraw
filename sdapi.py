# path/filename: sdapi_async.py
from typing import Optional, Dict
import httpx


class SDAPIAsync:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=None)

    async def generate_image(self, prompt: str = "string",
                             negative_prompt: str = "",
                             guidance_scale: float = 7.5, height: int = 512,
                             num_inference_steps: int = 50, width: int = 512) -> Dict:

        data = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "n_steps": num_inference_steps,
            "guidance_scale": guidance_scale,
            "width": width,
            "height": height
        }
        response = await self.client.post(f"{self.base_url}/generate_image/", json=data)
        response.raise_for_status()
        return response.json()

    async def close(self):
        await self.client.aclose()

    async def __aenter__(self) -> 'SDAPIAsync':
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()
