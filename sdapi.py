# path/filename: sdapi_async.py
from typing import Optional, Dict
import httpx


class SDAPIAsync:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=None)

    async def generate_image(self, model: Optional[str] = "dreamlike", prompt: str = "string",
                             negative_prompt: str = "", add_trigger: bool = True,
                             guidance_scale: float = 7.5, height: int = 512,
                             num_inference_steps: int = 50, width: int = 512) -> Dict:
        params = {
            "model": model,
            "response_format": 'b64_json'
        }
        data = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "add_trigger": add_trigger,
            "opts": {
                "guidance_scale": guidance_scale,
                "height": height,
                "num_inference_steps": num_inference_steps,
                "width": width
            }
        }
        response = await self.client.post(f"{self.base_url}/generate_image/", json=data, params=params)
        response.raise_for_status()
        return response.json()

    async def upscale_image(self, image: str, upscale_factor: int = 2) -> Dict:
        data = {
            "image": image,
            "upscale_factor": upscale_factor
        }
        response = await self.client.post(f"{self.base_url}/upscale_image/", json=data)
        response.raise_for_status()
        return response.json()

    async def get_model_list(self) -> Dict:
        response = await self.client.get(f"{self.base_url}/model_list")
        response.raise_for_status()
        return response.json()

    async def close(self):
        await self.client.aclose()

    async def __aenter__(self) -> 'SDAPIAsync':
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()
