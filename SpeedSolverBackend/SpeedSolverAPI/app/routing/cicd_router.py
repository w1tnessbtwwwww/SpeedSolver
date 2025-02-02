from fastapi import APIRouter


cicd_router = APIRouter(
    prefix="/cicd",
    tags=["CICD"]
)

@cicd_router.put("/update")
async def update_cicd():
    ...

@cicd_router.get("/get")
async def get_cicd():
    ...

@cicd_router.delete("/delete")
async def delete_cicd():
    ...

@cicd_router.patch("/patch")
async def patch_cicd():
    ...