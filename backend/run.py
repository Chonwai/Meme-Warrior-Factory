import os
import sys
import uvicorn
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import time
import random
import string
from typing import List, Optional
from dotenv import load_dotenv

# 加載環境變量
load_dotenv()

# 創建FastAPI應用
app = FastAPI(
    title="MemeWarriors API",
    description="API for MemeWarriors - Generate meme images with OpenAI",
    version="1.0.0"
)

# 設置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://meme-warrior-factory-next-js.vercel.app",  # 前端應用URL
        "http://localhost:3000",  # 本地開發前端
        "http://127.0.0.1:3000"   # 本地開發前端替代
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 定義請求模型
class MemeGenerationRequest(BaseModel):
    prompt: str

# 定義回應模型
class MemeGenerationResponse(BaseModel):
    success: bool
    items: Optional[List[dict]] = None
    error: Optional[str] = None

# 檢查OpenAI API密鑰
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("警告: 未設置OPENAI_API_KEY環境變量!")

# 圖像生成功能
async def generate_image(prompt: str):
    """使用OpenAI API生成圖像"""
    try:
        if not OPENAI_API_KEY:
            return {"success": False, "error": "未設置OpenAI API密鑰"}
        
        # 準備API請求
        url = "https://api.openai.com/v1/images/generations"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }
        data = {
            "model": "dall-e-2",
            "prompt": f"Create a simple, clean, pixel art icon of {prompt}. The image should be a single object with a simple background, suitable for a game icon.",
            "n": 1,
            "size": "1024x1024"
        }
        
        # 發送請求
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        # 解析回應
        result = response.json()
        image_url = result["data"][0]["url"]
        
        return {
            "success": True,
            "image_url": image_url,
            "prompt": prompt
        }
    except Exception as e:
        print(f"生成圖像時出錯: {str(e)}")
        return {"success": False, "error": str(e)}

# 生成名稱
def generate_name(prompt: str):
    """根據提示詞生成一個名稱"""
    # 簡單的名稱生成邏輯
    words = prompt.split()
    name_base = words[0] if words else "Meme"
    random_suffix = ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
    return f"{name_base.capitalize()}Warrior_{random_suffix}"

# API端點 - 根
@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "歡迎使用MemeWarriors API",
        "version": "1.0.0",
        "docs": "/docs"
    }

# API端點 - 測試
@app.get("/minimal-test")
async def minimal_test():
    return {
        "success": True,
        "message": "API正常運行",
        "timestamp": time.time()
    }

# API端點 - 生成Meme（無需認證）
@app.post("/meme/generate_test", response_model=MemeGenerationResponse)
async def generate_meme_test(request: MemeGenerationRequest):
    """生成Meme圖像的測試端點，無需認證"""
    try:
        print(f"正在處理提示詞: {request.prompt}")
        
        # 解析提示詞，生成兩個不同主題（簡化版）
        themes = []
        if "," in request.prompt:
            themes = [t.strip() for t in request.prompt.split(",")][:2]
        else:
            themes = [request.prompt, f"Variant of {request.prompt}"]
        
        # 為每個主題生成圖像和名稱
        result_items = []
        for i, theme in enumerate(themes):
            # 生成圖像
            image_result = await generate_image(theme)
            if not image_result["success"]:
                return {
                    "success": False,
                    "error": image_result.get("error", "生成圖像失敗")
                }
            
            # 生成名稱
            name = generate_name(theme)
            
            # 添加到結果
            result_items.append({
                "id": i + 1,
                "name": name,
                "prompt": theme,
                "image_url": image_result["image_url"],
                "coin_icon_url": image_result["image_url"]  # 使用同一圖像作為硬幣圖標
            })
        
        return {
            "success": True,
            "items": result_items
        }
    except Exception as e:
        print(f"處理請求時出錯: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

# API端點 - 生成Meme（帶test_mode參數）
@app.post("/meme/generate", response_model=MemeGenerationResponse)
async def generate_meme(
    request: MemeGenerationRequest,
    test_mode: bool = Query(False, description="設為true跳過認證（用於前端測試）")
):
    """生成Meme圖像的正式端點，支持test_mode參數跳過認證"""
    # 由於簡化實現，此端點與測試端點功能相同
    return await generate_meme_test(request)

# Vercel需要的handler
if "VERCEL" in os.environ:
    print("運行在Vercel環境中")
    # 如果運行在Vercel中，可能需要使用Mangum適配器
    try:
        from mangum import Mangum
        handler = Mangum(app)
        print("已創建Mangum handler")
    except ImportError:
        print("無法導入Mangum，可能會影響Vercel部署")

# 本地運行入口點
if __name__ == "__main__":
    # 創建輸出目錄（如果有需要）
    meme_storage_path = os.getenv("MEME_STORAGE_PATH", "./meme_images")
    os.makedirs(meme_storage_path, exist_ok=True)
    
    # 啟動服務器
    print(f"啟動FastAPI服務器，OpenAI API密鑰: {'已設置' if OPENAI_API_KEY else '未設置'}")
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000, 
        log_level="info"
    )
