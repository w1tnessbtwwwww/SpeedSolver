import datetime

from sqlalchemy import Date, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base
from sqlalchemy.dialects.postgresql import UUID

import uuid

from typing import List, Optional

from app.utils.verify_codes_generator.code_generator import generate_confirmation_code

Base = declarative_base()

class Objective(Base):
    __tablename__ = "objectives"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column(nullable=True)
    parent_objectiveId: Mapped[UUID] = mapped_column(ForeignKey("objectives.id", ondelete='CASCADE'), nullable=True)
    projectId: Mapped[UUID] = mapped_column(UUID, ForeignKey("projects.id", ondelete='CASCADE'), nullable=False)
    
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now())
    deadline_date: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=7),
    )

    responsible_person_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=True)

    author_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    author: Mapped["User"] = relationship("User", back_populates="authored_objectives", foreign_keys=[author_id])
    responsible_person: Mapped["User"] = relationship("User", back_populates="responsible_tasks", foreign_keys=[responsible_person_id])

    project: Mapped["Project"] = relationship("Project", back_populates="objectives")
    parent_objective: Mapped["Objective"] = relationship("Objective", back_populates="child_objectives", remote_side=[id])
    child_objectives: Mapped[list["Objective"]] = relationship("Objective", back_populates="parent_objective")
    


class Organization(Base):
    __tablename__ = "organizations"
    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column(nullable=True)
    leaderId: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    leader: Mapped["User"] = relationship("User", back_populates="organizations")
    teams: Mapped[List["Team"]] = relationship("Team", back_populates="organization") # type: ignore
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())

class Project(Base):
    __tablename__ = "projects"
    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column(nullable=True)
    creator_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now())


    creator: Mapped["User"] = relationship("User", back_populates="created_projects")
    objectives: Mapped[List["Objective"]] = relationship("Objective", back_populates="project")
    moderators: Mapped["ProjectModerator"] = relationship("ProjectModerator", back_populates="project")
    members: Mapped[List["ProjectMember"]] = relationship("ProjectMember", back_populates="project")

class TeamModerator(Base):
    __tablename__ = "team_moderators"
    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    userId: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    teamId: Mapped[UUID] = mapped_column(ForeignKey("teams.id"))
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())


    team: Mapped["Team"] = relationship("Team", back_populates="moderators") # type: ignore
    user: Mapped["User"] = relationship("User", back_populates="teams_moderation") # type: ignore

class TeamMember(Base):
    __tablename__ = "team_members"
    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    userId: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    teamId: Mapped[UUID] = mapped_column(ForeignKey("teams.id"))
    
    invited_by_request_id: Mapped[UUID] = mapped_column(ForeignKey("team_invitations.id", ondelete="CASCADE"), nullable=True)

    invited_by_request: Mapped["TeamInvitation"] = relationship("TeamInvitation", back_populates="team_member")

    team: Mapped["Team"] = relationship("Team", back_populates="members") # type: ignore
    user: Mapped["User"] = relationship("User", back_populates="teams") # type: ignore

class TeamInvitation(Base):
    __tablename__ = "team_invitations"
    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    invited_user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    invited_by_leader_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    teamId: Mapped[UUID] = mapped_column(ForeignKey("teams.id"))
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())

    team_member: Mapped["TeamMember"] = relationship("TeamMember", back_populates="invited_by_request")
    invited_user: Mapped["User"] = relationship("User", back_populates="team_invitations", foreign_keys="[TeamInvitation.invited_user_id]")
    invited_by_leader: Mapped["User"] = relationship("User", foreign_keys="[TeamInvitation.invited_by_leader_id]")
    team: Mapped["Team"] = relationship("Team")

class TeamProject(Base):
    __tablename__ = "team_projects"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    teamId: Mapped[UUID] = mapped_column(ForeignKey("teams.id", ondelete="CASCADE"))
    projectId: Mapped[UUID] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    team: Mapped["Team"] = relationship("Team", back_populates="projects") # type: ignore
    project: Mapped["Project"] = relationship("Project") # type: ignore

class ProjectModerator(Base):
    __tablename__ = "project_moderators"
    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    userId: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    projectId: Mapped[UUID] = mapped_column(ForeignKey("projects.id"))

    project: Mapped["Project"] = relationship("Project", back_populates="moderators") # type: ignore
    user: Mapped["User"] = relationship("User", back_populates="projects_moderation") # type: ignore

class Team(Base):
    __tablename__ = "teams"
    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column(nullable=True)
    leaderId: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=True)
    organizationId: Mapped[UUID] = mapped_column(ForeignKey("organizations.id", ondelete="SET NULL"), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now(), nullable=True)


    organization: Mapped["Organization"] = relationship("Organization", back_populates="teams") # type: ignore
    leader: Mapped["User"] = relationship("User", back_populates="teams_lead")
    members: Mapped[list["TeamMember"]] = relationship("TeamMember", back_populates="team") # type: ignore
    projects: Mapped[list["TeamProject"]] = relationship("TeamProject", back_populates="team") # type: ignore
    moderators: Mapped[list["TeamModerator"]] = relationship("TeamModerator", back_populates="team") # type: ignore
    team_roles: Mapped[list["CustomTeamRole"]] = relationship("CustomTeamRole", back_populates="team")
    all_team_role_links: Mapped[list["LinkTeamRole"]] = relationship("LinkTeamRole", back_populates="team")

class CustomTeamRole(Base):
    __tablename__ = "custom_team_roles"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    name: Mapped[String] = mapped_column(String(50))
    team_id: Mapped[UUID] = mapped_column(ForeignKey("teams.id", ondelete="CASCADE"), nullable=True)
    color: Mapped[str] = mapped_column(default=str("#ffffff"), nullable=True)

    team: Mapped["Team"] = relationship("Team", back_populates="team_roles")


class LinkTeamRole(Base):
    __tablename__ = "links_team_roles"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    team_id: Mapped[UUID] = mapped_column(ForeignKey("teams.id", ondelete="CASCADE"))

    user: Mapped["User"] = relationship("User", back_populates="all_roles")
    team: Mapped["Team"] = relationship("Team", back_populates="all_team_role_links")

class UserProfile(Base):
    __tablename__ = "user_profiles"
    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    surname: Mapped[str] = mapped_column(nullable=True)
    name: Mapped[str] = mapped_column(nullable=True)
    patronymic: Mapped[str] = mapped_column(nullable=True)
    birthdate: Mapped[Date] = mapped_column(Date, nullable=True, default=datetime.date.today())
    about: Mapped[str] = mapped_column(nullable=True)
    userId: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete='CASCADE'))
    avatar_path: Mapped[Optional[str]] = mapped_column()

    user: Mapped["User"] = relationship("User", back_populates="profile") # type: ignore

class EmailVerification(Base):
    __tablename__ = "email_verifications"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    userId: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    verification_code: Mapped[str] = mapped_column(default=str(generate_confirmation_code()))
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())

    user: Mapped["User"] = relationship("User", back_populates="verification")

    

class User(Base):
    __tablename__ = "users"
    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(nullable=True, unique=True)
    password: Mapped[str] = mapped_column()
    registered: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), nullable=True) 
    is_mail_verified: Mapped[bool] = mapped_column(default=False, nullable=False)


    team_invitations: Mapped[List["TeamInvitation"]] = relationship("TeamInvitation", back_populates="invited_user", foreign_keys="[TeamInvitation.invited_user_id]", cascade="all, delete-orphan")
    project_invitations: Mapped[List["ProjectInvitation"]] = relationship("ProjectInvitation", back_populates="invited_user", foreign_keys="[ProjectInvitation.invited_user_id]", cascade="all, delete-orphan")
    profile: Mapped["UserProfile"] = relationship("UserProfile", back_populates="user") # type: ignore
    teams: Mapped[List["TeamMember"]] = relationship("TeamMember", back_populates="user", cascade="all, delete-orphan") # type: ignore
    projects: Mapped[List["ProjectMember"]] = relationship("ProjectMember", back_populates="user", cascade="all, delete-orphan")
    teams_lead: Mapped[List["Team"]] = relationship("Team", back_populates="leader")
    organizations: Mapped[List["Organization"]] = relationship("Organization", back_populates="leader", cascade="all, delete-orphan")
    verification: Mapped["EmailVerification"] = relationship("EmailVerification", back_populates="user")
    teams_moderation: Mapped[List["TeamModerator"]] = relationship("TeamModerator", back_populates="user")
    projects_moderation: Mapped[List["ProjectModerator"]] = relationship("ProjectModerator", back_populates="user")
    created_projects: Mapped[List["Project"]] = relationship("Project", back_populates="creator")
    authored_objectives: Mapped[List["Objective"]] = relationship("Objective", back_populates="author", foreign_keys="Objective.author_id")
    all_roles: Mapped[List["LinkTeamRole"]] = relationship("LinkTeamRole", back_populates="user")
    responsible_tasks: Mapped[List["Objective"]] = relationship("Objective", back_populates="responsible_person", foreign_keys="Objective.responsible_person_id")


class ProjectMember(Base):
    __tablename__ = "project_members"
    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    userId: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete='CASCADE'))
    projectId: Mapped[UUID] = mapped_column(ForeignKey("projects.id", ondelete='CASCADE'))

    user: Mapped["User"] = relationship("User", back_populates="projects")
    project: Mapped["Project"] = relationship("Project", back_populates="members")

class ProjectInvitation(Base):
    __tablename__ = "project_invitations"
    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    invited_user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete='CASCADE'))
    invited_by_leader_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete='CASCADE'))
    projectId: Mapped[UUID] = mapped_column(ForeignKey("projects.id", ondelete='CASCADE'))

    invited_user: Mapped["User"] = relationship("User", back_populates="project_invitations", foreign_keys="[ProjectInvitation.invited_user_id]")
    invited_by_leader: Mapped["User"] = relationship("User", foreign_keys="[ProjectInvitation.invited_by_leader_id]")
    project: Mapped["Project"] = relationship("Project")