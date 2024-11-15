﻿// <auto-generated />
using System;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Infrastructure;
using Microsoft.EntityFrameworkCore.Migrations;
using Microsoft.EntityFrameworkCore.Storage.ValueConversion;
using Npgsql.EntityFrameworkCore.PostgreSQL.Metadata;
using SpeedSolverDatabase;

#nullable disable

namespace SpeedSolverDatabase.Migrations
{
    [DbContext(typeof(SpeedContext))]
    [Migration("20241018122458_added datetime to messages")]
    partial class addeddatetimetomessages
    {
        /// <inheritdoc />
        protected override void BuildTargetModel(ModelBuilder modelBuilder)
        {
#pragma warning disable 612, 618
            modelBuilder
                .HasAnnotation("ProductVersion", "8.0.8")
                .HasAnnotation("Relational:MaxIdentifierLength", 63);

            NpgsqlModelBuilderExtensions.UseIdentityByDefaultColumns(modelBuilder);

            modelBuilder.Entity("SpeedSolverDatabase.Models.InProjectMessage", b =>
                {
                    b.Property<int>("MessageId")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("integer");

                    NpgsqlPropertyBuilderExtensions.UseIdentityByDefaultColumn(b.Property<int>("MessageId"));

                    b.Property<string>("Content")
                        .IsRequired()
                        .HasColumnType("text");

                    b.Property<int>("ProjectId")
                        .HasColumnType("integer");

                    b.Property<DateTime>("SendedAt")
                        .HasColumnType("timestamp with time zone");

                    b.Property<int>("UserId")
                        .HasColumnType("integer");

                    b.HasKey("MessageId");

                    b.HasIndex("ProjectId");

                    b.HasIndex("UserId");

                    b.ToTable("messages", (string)null);
                });

            modelBuilder.Entity("SpeedSolverDatabase.Models.Invitation", b =>
                {
                    b.Property<int>("InviteId")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("integer");

                    NpgsqlPropertyBuilderExtensions.UseIdentityByDefaultColumn(b.Property<int>("InviteId"));

                    b.Property<int>("InvitedByLeaderId")
                        .HasColumnType("integer");

                    b.Property<int>("ToTeamId")
                        .HasColumnType("integer");

                    b.Property<int>("UserId")
                        .HasColumnType("integer");

                    b.HasKey("InviteId");

                    b.HasIndex("InvitedByLeaderId");

                    b.HasIndex("ToTeamId");

                    b.HasIndex("UserId");

                    b.ToTable("invitations", (string)null);
                });

            modelBuilder.Entity("SpeedSolverDatabase.Models.Objective", b =>
                {
                    b.Property<int>("ObjectiveId")
                        .HasColumnType("integer");

                    b.Property<string>("ObjectiveDescription")
                        .IsRequired()
                        .HasColumnType("text");

                    b.Property<string>("ObjectiveTitle")
                        .IsRequired()
                        .HasMaxLength(20)
                        .HasColumnType("character varying(20)");

                    b.Property<int>("ProjectId")
                        .HasColumnType("integer");

                    b.HasKey("ObjectiveId");

                    b.HasIndex("ProjectId");

                    b.ToTable("objectives", (string)null);
                });

            modelBuilder.Entity("SpeedSolverDatabase.Models.Project", b =>
                {
                    b.Property<int>("ProjectId")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("integer");

                    NpgsqlPropertyBuilderExtensions.UseIdentityByDefaultColumn(b.Property<int>("ProjectId"));

                    b.Property<string>("ProjectDescription")
                        .IsRequired()
                        .HasMaxLength(300)
                        .HasColumnType("character varying(300)");

                    b.Property<string>("ProjectTitle")
                        .IsRequired()
                        .HasMaxLength(50)
                        .HasColumnType("character varying(50)");

                    b.HasKey("ProjectId");

                    b.ToTable("projects", (string)null);
                });

            modelBuilder.Entity("SpeedSolverDatabase.Models.ProjectModerator", b =>
                {
                    b.Property<int>("ProjectModId")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("integer");

                    NpgsqlPropertyBuilderExtensions.UseIdentityByDefaultColumn(b.Property<int>("ProjectModId"));

                    b.Property<int>("ProjectId")
                        .HasColumnType("integer");

                    b.Property<int>("SettedByUserId")
                        .HasColumnType("integer");

                    b.Property<int>("UserId")
                        .HasColumnType("integer");

                    b.HasKey("ProjectModId");

                    b.HasIndex("ProjectId");

                    b.HasIndex("SettedByUserId");

                    b.HasIndex("UserId");

                    b.ToTable("projectmoderators", (string)null);
                });

            modelBuilder.Entity("SpeedSolverDatabase.Models.Team", b =>
                {
                    b.Property<int>("TeamId")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("integer");

                    NpgsqlPropertyBuilderExtensions.UseIdentityByDefaultColumn(b.Property<int>("TeamId"));

                    b.Property<DateTime>("CreatedAt")
                        .HasColumnType("timestamp with time zone");

                    b.Property<int>("CreatorId")
                        .HasColumnType("integer");

                    b.Property<string>("TeamDescription")
                        .IsRequired()
                        .HasMaxLength(100)
                        .HasColumnType("character varying(100)");

                    b.Property<string>("TeamName")
                        .IsRequired()
                        .HasMaxLength(30)
                        .HasColumnType("character varying(30)");

                    b.HasKey("TeamId");

                    b.HasIndex("CreatorId");

                    b.ToTable("teams", (string)null);
                });

            modelBuilder.Entity("SpeedSolverDatabase.Models.TeamObjective", b =>
                {
                    b.Property<int>("TeamObjectiveId")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("integer");

                    NpgsqlPropertyBuilderExtensions.UseIdentityByDefaultColumn(b.Property<int>("TeamObjectiveId"));

                    b.Property<int>("ObjectiveId")
                        .HasColumnType("integer");

                    b.Property<int>("TeamId")
                        .HasColumnType("integer");

                    b.HasKey("TeamObjectiveId");

                    b.HasIndex("TeamId");

                    b.ToTable("teamobjectives", (string)null);
                });

            modelBuilder.Entity("SpeedSolverDatabase.Models.UnderObjective", b =>
                {
                    b.Property<int>("UnderObjectiveId")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("integer");

                    NpgsqlPropertyBuilderExtensions.UseIdentityByDefaultColumn(b.Property<int>("UnderObjectiveId"));

                    b.Property<int>("GeneralObjectiveId")
                        .HasColumnType("integer");

                    b.Property<string>("UnderObjectiveTitle")
                        .IsRequired()
                        .HasMaxLength(20)
                        .HasColumnType("character varying(20)");

                    b.HasKey("UnderObjectiveId");

                    b.HasIndex("GeneralObjectiveId");

                    b.ToTable("underobjectives", (string)null);
                });

            modelBuilder.Entity("SpeedSolverDatabase.Models.User", b =>
                {
                    b.Property<int>("UserId")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("integer");

                    NpgsqlPropertyBuilderExtensions.UseIdentityByDefaultColumn(b.Property<int>("UserId"));

                    b.Property<string>("Login")
                        .IsRequired()
                        .HasColumnType("text");

                    b.Property<string>("Name")
                        .HasColumnType("text");

                    b.Property<string>("Password")
                        .IsRequired()
                        .HasColumnType("text");

                    b.Property<string>("Patronymic")
                        .HasColumnType("text");

                    b.Property<string>("PhoneNumber")
                        .HasMaxLength(12)
                        .HasColumnType("character varying(12)");

                    b.Property<string>("Surname")
                        .HasColumnType("text");

                    b.HasKey("UserId");

                    b.ToTable("users", (string)null);
                });

            modelBuilder.Entity("SpeedSolverDatabase.Models.InProjectMessage", b =>
                {
                    b.HasOne("SpeedSolverDatabase.Models.Project", "Project")
                        .WithMany("ChatHistory")
                        .HasForeignKey("ProjectId")
                        .OnDelete(DeleteBehavior.Cascade)
                        .IsRequired();

                    b.HasOne("SpeedSolverDatabase.Models.User", "User")
                        .WithMany()
                        .HasForeignKey("UserId")
                        .OnDelete(DeleteBehavior.Cascade)
                        .IsRequired();

                    b.Navigation("Project");

                    b.Navigation("User");
                });

            modelBuilder.Entity("SpeedSolverDatabase.Models.Invitation", b =>
                {
                    b.HasOne("SpeedSolverDatabase.Models.User", "InvitedByLeader")
                        .WithMany()
                        .HasForeignKey("InvitedByLeaderId")
                        .OnDelete(DeleteBehavior.Cascade)
                        .IsRequired();

                    b.HasOne("SpeedSolverDatabase.Models.Team", "ToTeam")
                        .WithMany()
                        .HasForeignKey("ToTeamId")
                        .OnDelete(DeleteBehavior.Cascade)
                        .IsRequired();

                    b.HasOne("SpeedSolverDatabase.Models.User", "User")
                        .WithMany("Invites")
                        .HasForeignKey("UserId")
                        .OnDelete(DeleteBehavior.Cascade)
                        .IsRequired();

                    b.Navigation("InvitedByLeader");

                    b.Navigation("ToTeam");

                    b.Navigation("User");
                });

            modelBuilder.Entity("SpeedSolverDatabase.Models.Objective", b =>
                {
                    b.HasOne("SpeedSolverDatabase.Models.TeamObjective", null)
                        .WithMany("Objectives")
                        .HasForeignKey("ObjectiveId")
                        .OnDelete(DeleteBehavior.Cascade)
                        .IsRequired();

                    b.HasOne("SpeedSolverDatabase.Models.Project", "Project")
                        .WithMany("Objectives")
                        .HasForeignKey("ProjectId")
                        .OnDelete(DeleteBehavior.SetNull)
                        .IsRequired();

                    b.Navigation("Project");
                });

            modelBuilder.Entity("SpeedSolverDatabase.Models.ProjectModerator", b =>
                {
                    b.HasOne("SpeedSolverDatabase.Models.Project", "Project")
                        .WithMany("Moderators")
                        .HasForeignKey("ProjectId")
                        .OnDelete(DeleteBehavior.Cascade)
                        .IsRequired();

                    b.HasOne("SpeedSolverDatabase.Models.User", "SettedByUser")
                        .WithMany()
                        .HasForeignKey("SettedByUserId")
                        .OnDelete(DeleteBehavior.Cascade)
                        .IsRequired();

                    b.HasOne("SpeedSolverDatabase.Models.User", "User")
                        .WithMany("ProjectModerated")
                        .HasForeignKey("UserId")
                        .OnDelete(DeleteBehavior.Cascade)
                        .IsRequired();

                    b.Navigation("Project");

                    b.Navigation("SettedByUser");

                    b.Navigation("User");
                });

            modelBuilder.Entity("SpeedSolverDatabase.Models.Team", b =>
                {
                    b.HasOne("SpeedSolverDatabase.Models.User", "Creator")
                        .WithMany("Teams")
                        .HasForeignKey("CreatorId")
                        .OnDelete(DeleteBehavior.Cascade)
                        .IsRequired();

                    b.Navigation("Creator");
                });

            modelBuilder.Entity("SpeedSolverDatabase.Models.TeamObjective", b =>
                {
                    b.HasOne("SpeedSolverDatabase.Models.Team", "Team")
                        .WithMany("Objectives")
                        .HasForeignKey("TeamId")
                        .OnDelete(DeleteBehavior.Cascade)
                        .IsRequired();

                    b.Navigation("Team");
                });

            modelBuilder.Entity("SpeedSolverDatabase.Models.UnderObjective", b =>
                {
                    b.HasOne("SpeedSolverDatabase.Models.Objective", "GeneralObjective")
                        .WithMany("UnderObjectives")
                        .HasForeignKey("GeneralObjectiveId")
                        .OnDelete(DeleteBehavior.Cascade)
                        .IsRequired();

                    b.Navigation("GeneralObjective");
                });

            modelBuilder.Entity("SpeedSolverDatabase.Models.Objective", b =>
                {
                    b.Navigation("UnderObjectives");
                });

            modelBuilder.Entity("SpeedSolverDatabase.Models.Project", b =>
                {
                    b.Navigation("ChatHistory");

                    b.Navigation("Moderators");

                    b.Navigation("Objectives");
                });

            modelBuilder.Entity("SpeedSolverDatabase.Models.Team", b =>
                {
                    b.Navigation("Objectives");
                });

            modelBuilder.Entity("SpeedSolverDatabase.Models.TeamObjective", b =>
                {
                    b.Navigation("Objectives");
                });

            modelBuilder.Entity("SpeedSolverDatabase.Models.User", b =>
                {
                    b.Navigation("Invites");

                    b.Navigation("ProjectModerated");

                    b.Navigation("Teams");
                });
#pragma warning restore 612, 618
        }
    }
}
