import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { get_team_by_id } from '@/app/axios_api';
import axios from 'axios';
import { Button } from '@/components/ui/button';
import { Undo2, Plus } from 'lucide-react';
import ProjectCard from './components/ProjectCard';
import MemberCard from './components/MemberCard';
import TaskList from './components/TaskList';
import CreateProjectDialog from './components/CreateProjectDialog';
import CreateSubtaskDialog from './components/CreateSubtaskDialog';
import Card from '@/components/card/Card';

interface UserProfile {
  surname: string;
  name: string;
  patronymic: string;
  about: string;
  birthdate: string;
  avatar_path: string | null;
}

interface User {
  id: string;
  email: string;
  is_mail_verified: boolean;
  profile: UserProfile | null;
}

interface TeamMember {
  id: string;
  user: User;
}

interface ProjectCreator {
  id: string;
  email: string;
  is_mail_verified: boolean;
  profile: UserProfile | null;
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

interface Team {
  id: string;
  title: string;
  description: string;
  created_at: string;
  projects: ProjectLink[];
  members: TeamMember[];
}

interface TaskAuthor {
  id: string;
  profile: {
    fullname: string;
  };
}

interface Task {
  id: string;
  title: string;
  description: string;
  created_at: string;
  deadline_date: string;
  author: TaskAuthor;
  child_objectives: Task[];
  parent_objectiveId: string | null;
}

const TeamPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [team, setTeam] = useState<Team | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [newProject, setNewProject] = useState({
    title: '',
    description: '',
  });
  const [newSubtask, setNewSubtask] = useState({
    title: '',
    description: '',
    deadline_date: '',
  });
  const [_, setSelectedProjectId] = useState<string | null>(null);
  const [projectTasks, setProjectTasks] = useState<Task[]>([]);
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);
  const [isSubtaskDialogOpen, setIsSubtaskDialogOpen] = useState(false);
  const [selectedTaskId, setSelectedTaskId] = useState<string | null>(null);

  const fetchProjectTasks = async (projectId: string) => {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        navigate('/login');
        return;
      }

      const response = await axios.get(`https://api.speedsolver.ru/v1/projects/tasks/all/${projectId}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      setProjectTasks(response.data);
    } catch (err) {
      console.error('Ошибка при получении задач:', err);
      if (axios.isAxiosError(err) && err.response?.status === 401) {
        localStorage.removeItem('access_token');
        navigate('/login');
      }
      setError('Ошибка при получении задач');
    }
  };

  const handleCreateSubtask = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const refreshToken = localStorage.getItem('refresh_token');

      if (!token || !refreshToken) {
        navigate('/login');
        return;
      }

      if (!selectedProject) {
        throw new Error('Не выбран проект');
      }

      if (!newSubtask.deadline_date) {
        throw new Error('Не указан срок выполнения');
      }

      const requestData = {
        title: newSubtask.title,
        description: newSubtask.description,
        parent_objectiveId: selectedTaskId || null,
        deadline_date: newSubtask.deadline_date,
      };

      const response = await axios.post(
        `https://api.speedsolver.ru/v1/projects/tasks/create/${selectedProject.id}`,
        requestData,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      );

      if (!response.data) {
        throw new Error('Ошибка при создании задачи');
      }

      setIsSubtaskDialogOpen(false);
      setNewSubtask({ title: '', description: '', deadline_date: '' });
      setSelectedTaskId(null);

      await fetchProjectTasks(selectedProject.id);

    } catch (err) {
      console.error('Ошибка при создании задачи:', err);
      if (axios.isAxiosError(err) && err.response?.status === 401) {
        localStorage.removeItem('access_token');
        navigate('/login');
      } else if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('Ошибка при создании задачи');
      }
    }
  };

  const handleCreateProject = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const refreshToken = localStorage.getItem('refresh_token');

      if (!token || !refreshToken) {
        navigate('/login');
        return;
      }

      const response = await axios.post(`https://api.speedsolver.ru/v1/projects/create/${id}`, {
        title: newProject.title,
        description: newProject.description,
        auto_invite: []
      }, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.data) {
        throw new Error('Ошибка при создании проекта');
      }

      const data = await get_team_by_id(id!);
      setTeam(data);
      setIsDialogOpen(false);
      setNewProject({ title: '', description: '' });
    } catch (err) {
      console.error('Ошибка при создании проекта:', err);
      if (axios.isAxiosError(err) && err.response?.status === 401) {
        localStorage.removeItem('access_token');
        navigate('/login');
      }
      setError('Ошибка при создании проекта');
    }
  };

  useEffect(() => {
    const fetchTeam = async () => {
      try {
        const token = localStorage.getItem('access_token');
        if (!token) {
          navigate('/login');
          return;
        }

        const data = await get_team_by_id(id!);
        setTeam(data);
      } catch (err) {
        console.error('Error fetching team:', err);
        if (axios.isAxiosError(err) && err.response?.status === 401) {
          localStorage.removeItem('access_token');
          navigate('/login');
        } else {
          setError('Ошибка загрузки команды');
        }
      } finally {
        setIsLoading(false);
      }
    };

    fetchTeam();
  }, [id, navigate]);

  if (isLoading) return <div>Загрузка...</div>;
  if (error) return <div>{error}</div>;
  if (!team) return <div>Команда не найдена</div>;

  return (
    <div className='p-6'>
      <div className="flex items-center mb-6 gap-6">
        <Button
          onClick={() => navigate('/teams')}
          className="bg-transparent hover:bg-neutral-600 rounded"
          title='Назад'
        >
          <Undo2 className='text-white'/>
        </Button>
        <div className="relative group">
          <h1 className="text-white text-xl font-bold cursor-help">{team.title}</h1>
          <div className="absolute left-0 top-full mt-2 p-4 bg-neutral-800 rounded-lg shadow-lg opacity-0 group-hover:opacity-100 transition-opacity duration-200 z-10 w-64">
            <h2 className="text-white text-lg font-semibold mb-2">Описание</h2>
            <p className="text-white text-sm">{team.description}</p>
          </div>
        </div>
      </div>

      <div className="flex gap-6">
        <div className="flex-1">
          <Card className="h-full">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-white text-lg font-semibold">Проекты команды</h2>
              <div>
                <Button
                  onClick={() => setIsDialogOpen(true)}
                  className="bg-tra hover:bg-[#8f297a]"
                >
                  <Plus className="w-4 h-4 mr-2" />
                  Создать
                </Button>
              </div>
            </div>
            <div className="space-y-4">
              {team.projects.length > 0 ? (
                team.projects.map(projectLink => (
                  <ProjectCard
                    key={projectLink.id}
                    projectLink={projectLink}
                    setSelectedProject={setSelectedProject}
                    fetchProjectTasks={fetchProjectTasks}
                    setSelectedProjectId={setSelectedProjectId}
                    setIsSubtaskDialogOpen={setIsSubtaskDialogOpen}
                  />
                ))
              ) : (
                <p className="text-white text-center p-4">Нет проектов</p>
              )}
            </div>
          </Card>
        </div>

        <div className="w-80">
          <MemberCard members={team.members} />
        </div>
      </div>

      <div className='text-right mt-4'>
        <p className="text-neutral-600 text-sm">
          Дата создания: {new Date(team.created_at).toLocaleDateString()}
        </p>
      </div>

      {isDialogOpen && (
        <CreateProjectDialog
          newProject={newProject}
          setNewProject={setNewProject}
          setIsDialogOpen={setIsDialogOpen}
          handleCreateProject={handleCreateProject}
        />
      )}

      {selectedProject && (
        <TaskList
          selectedProject={selectedProject}
          projectTasks={projectTasks}
          setSelectedProject={setSelectedProject}
          setSelectedTaskId={setSelectedTaskId}
          setIsSubtaskDialogOpen={setIsSubtaskDialogOpen}
        />
      )}

      {isSubtaskDialogOpen && (
        <CreateSubtaskDialog
          newSubtask={newSubtask}
          setNewSubtask={setNewSubtask}
          setIsSubtaskDialogOpen={setIsSubtaskDialogOpen}
          handleCreateSubtask={handleCreateSubtask}
          selectedTaskId={selectedTaskId}
        />
      )}
    </div>
  );
};

export default TeamPage;
