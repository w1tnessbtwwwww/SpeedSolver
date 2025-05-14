import { Button } from '@/components/ui/button';
import { Plus } from 'lucide-react';

interface ProjectCreator {
  id: string;
  email: string;
  is_mail_verified: boolean;
  profile: {
    name: string;
    surname: string;
    patronymic: string;
    about: string;
    birthdate: string;
    avatar_path: string | null;
  } | null;
}

interface Project {
  id: string;
  title: string;
  description: string;
  created_at: string;
  creator: ProjectCreator;
  has_subtasks?: boolean;
}

interface ProjectLink {
  id: string;
  project: Project;
}

interface ProjectCardProps {
  projectLink: ProjectLink;
  setSelectedProject: (project: Project) => void;
  fetchProjectTasks: (projectId: string) => void;
  setSelectedProjectId: (projectId: string) => void;
  setIsSubtaskDialogOpen: (isOpen: boolean) => void;
}

const ProjectCard = ({ projectLink, setSelectedProject, fetchProjectTasks, setSelectedProjectId, setIsSubtaskDialogOpen }: ProjectCardProps) => {
  const handleCardClick = () => {
    setSelectedProject(projectLink.project);
    fetchProjectTasks(projectLink.project.id);
  };

  return (
    <div 
      className="p-4 bg-neutral-700 rounded-lg hover:bg-neutral-600 transition-colors cursor-pointer"
      onClick={handleCardClick}
    >
      <div className="flex justify-between items-start">
        <div>
          <h3 className="font-medium text-white">{projectLink.project.title}</h3>
          <p className="text-sm text-gray-300 mt-1">{projectLink.project.description}</p>
          <p className="text-xs text-gray-400 mt-2">
            Создатель: {projectLink.project.creator.profile?.name || projectLink.project.creator.email}
          </p>
        </div>
        <div className="flex gap-2">
          <Button
            onClick={(e) => {
              e.stopPropagation(); // Предотвращаем всплытие события клика
              setSelectedProjectId(projectLink.project.id);
              setIsSubtaskDialogOpen(true);
            }}
            className="bg-green-600 hover:bg-green-700"
            size="sm"
          >
            <Plus className="w-4 h-4 mr-1" />
            Задача
          </Button>
        </div>
      </div>
    </div>
  );
};

export default ProjectCard;
