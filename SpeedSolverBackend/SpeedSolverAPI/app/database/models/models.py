import datetime
from sqlalchemy import Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from typing import List

Base = declarative_base()

class Objective(Base):
    __tablename__ = "objectives"

    objectiveId: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column(nullable=True)
    parent_objectiveId: Mapped[UUID] = mapped_column(ForeignKey("objectives.objectiveId"), nullable=True)

    parent_objective: Mapped["Objective"] = relationship("Objective", back_populates="child_objectives", remote_side=[objectiveId])
    child_objectives: Mapped[list["Objective"]] = relationship("Objective", back_populates="parent_objective")


class Organization(Base):
    __tablename__ = "organizations"
    organizationId: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column(nullable=True)
    leaderId: Mapped[UUID] = mapped_column(ForeignKey("users.userId", ondelete="CASCADE"), nullable=False)
    leader: Mapped["User"] = relationship("User", back_populates="organizations")
    teams: Mapped[List["Team"]] = relationship("Team", back_populates="organization") # type: ignore

class Project(Base):
    __tablename__ = "projects"
    projectId: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column(nullable=True)


class TeamMember(Base):
    __tablename__ = "team_members"
    teamMemberId: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    userId: Mapped[UUID] = mapped_column(ForeignKey("users.userId"))
    teamId: Mapped[UUID] = mapped_column(ForeignKey("teams.teamId"))

    team: Mapped["Team"] = relationship("Team", back_populates="members") # type: ignore
    user: Mapped["User"] = relationship("User", back_populates="teams") # type: ignore


class TeamProject(Base):
    __tablename__ = "team_projects"

    teamProjectId: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    teamId: Mapped[UUID] = mapped_column(ForeignKey("teams.teamId"))
    projectId: Mapped[UUID] = mapped_column(ForeignKey("projects.projectId"))
    team: Mapped["Team"] = relationship("Team", back_populates="projects") # type: ignore
    project: Mapped["Project"] = relationship("Project") # type: ignore



class Team(Base):
    __tablename__ = "teams"
    teamId: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column(nullable=True)
    leaderId: Mapped[UUID] = mapped_column(ForeignKey("users.userId"), nullable=True)
    organizationId: Mapped[UUID] = mapped_column(ForeignKey("organizations.organizationId", ondelete="SET NULL"), nullable=True)

    organization: Mapped["Organization"] = relationship("Organization", back_populates="teams") # type: ignore
    leader: Mapped["User"] = relationship("User", back_populates="teams_lead")
    members: Mapped[list["TeamMember"]] = relationship("TeamMember", back_populates="team") # type: ignore
    projects: Mapped[list["TeamProject"]] = relationship("TeamProject", back_populates="team") # type: ignore

class UserProfile(Base):
    __tablename__ = "user_profiles"
    userProfileId: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    surname: Mapped[str] = mapped_column(nullable=True)
    name: Mapped[str] = mapped_column(nullable=True)
    patronymic: Mapped[str] = mapped_column(nullable=True)
    birthdate: Mapped[Date] = mapped_column(Date, nullable=True, default=datetime.date.today())
    userId: Mapped[UUID] = mapped_column(ForeignKey("users.userId"))

    user: Mapped["User"] = relationship("User", back_populates="profile") # type: ignore

class EmailVerification(Base):
    __tablename__ = "email_verifications"

    verification_id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    userId: Mapped[UUID] = mapped_column(ForeignKey("users.userId"), unique=True)

    verification_code: Mapped[str] = mapped_column()

    user: Mapped["User"] = relationship("User", back_populates="verification")
    

class User(Base):
    __tablename__ = "users"
    userId: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(nullable=True, unique=True)
    password: Mapped[str] = mapped_column()
    registered: Mapped[Date] = mapped_column(Date, default=datetime.date.today(), nullable=True) 
    is_mail_verified: Mapped[bool] = mapped_column(default=False, nullable=False)


    profile: Mapped["UserProfile"] = relationship("UserProfile", back_populates="user", cascade="all, delete-orphan") # type: ignore

    teams: Mapped[List["TeamMember"]] = relationship("TeamMember", back_populates="user", cascade="all, delete-orphan") # type: ignore
    teams_lead: Mapped[List["Team"]] = relationship("Team", back_populates="leader")

    team_invitations: Mapped[List["TeamInvitation"]] = relationship("TeamInvitation", back_populates="invited_user", foreign_keys="[TeamInvitation.invited_user_id]", cascade="all, delete-orphan")
    organizations: Mapped[List["Organization"]] = relationship("Organization", back_populates="leader")
    
    verification: Mapped["EmailVerification"] = relationship("Verification", back_populates="user")

class TeamInvitation(Base):
    __tablename__ = "team_invitations"
    teamInvitationId: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    invited_user_id: Mapped[UUID] = mapped_column(ForeignKey("users.userId"))
    invited_by_leader_id: Mapped[UUID] = mapped_column(ForeignKey("users.userId"))
    teamId: Mapped[UUID] = mapped_column(ForeignKey("teams.teamId"))

    invited_user: Mapped["User"] = relationship("User", back_populates="team_invitations", foreign_keys="[TeamInvitation.invited_user_id]")
    invited_by_leader: Mapped["User"] = relationship("User", foreign_keys="[TeamInvitation.invited_by_leader_id]")
    team: Mapped["Team"] = relationship("Team")