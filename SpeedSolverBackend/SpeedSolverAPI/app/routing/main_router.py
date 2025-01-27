from fastapi import APIRouter
from app.routing.access_router import auth_router
from app.routing.team_router import team_router
from app.routing.account_router import account_router
from app.routing.organization_router import organization_router
from app.routing.email_router import email_router
from app.routing.verification_router import verification_router
from app.routing.project_router import project_router
from app.routing.cicd_router import cicd_router
from app.routing.objective_router import objective_router
from app.routing.inviting_router import inviting_router

main_router = APIRouter (
   prefix = "/v1"
)

# cycling
project_router.include_router(objective_router)

team_router.include_router(inviting_router)

# main
main_router.include_router(cicd_router)
main_router.include_router(auth_router)
main_router.include_router(verification_router)
main_router.include_router(email_router)
main_router.include_router(account_router)
main_router.include_router(organization_router)
main_router.include_router(team_router)
main_router.include_router(project_router)