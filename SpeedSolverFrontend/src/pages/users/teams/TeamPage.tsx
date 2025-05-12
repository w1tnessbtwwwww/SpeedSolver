import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { get_team_by_id } from '@/app/axios_api';
import { Button } from '@/components/ui/button';
import { Undo2, Plus } from 'lucide-react';
import Card from '@/components/card/Card';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";

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
      } catch (err: any) {
        console.error('Error fetching team:', err);
        if (err.message === 'Authentication failed') {
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

  const handleCreateProject = async () => {
    try {
      const response = await fetch(`https://api.speedsolver.ru/v1/projects/create/${id}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
        body: JSON.stringify({
          title: newProject.title,
          description: newProject.description,
          auto_invite: [] // Можно добавить логику выбора пользователей позже
        }),
      });

      if (!response.ok) {
        throw new Error('Ошибка при создании проекта');
      }

      // Перезагружаем данные команды
      const data = await get_team_by_id(id!);
      setTeam(data);
      setIsDialogOpen(false);
      setNewProject({ title: '', description: '' });
    } catch (err) {
      console.error('Ошибка при создании проекта:', err);
      setError('Ошибка при создании проекта');
    }
  };

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
        <h1 className="text-white text-xl font-bold">{team.title}</h1>
      </div>

      <div>
        <Card className="mb-4">
          <h2 className="text-white text-lg font-semibold">Описание</h2>
          <p className="text-white">{team.description}</p>
        </Card>
        
        <Card className="mb-4">
          <h2 className="text-white text-lg font-semibold">Участники</h2>
          <div className="space-y-2">
            {team.members.map(member => (
              <div key={member.id} className="text-white">
                {member.user.profile ? (
                  <>
                    {member.user.profile.name}{' '}
                    {member.user.profile.surname}
                  </>
                ) : (
                  'Профиль не заполнен'
                )}
                <br/>
                <span className='text-neutral-600'>
                  {member.user.email}    
                </span>
              </div>
            ))}
          </div>
        </Card>

        <Card className="mb-4">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-white text-lg font-semibold">Проекты команды</h2>
            <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
              <DialogTrigger asChild>
                <Button className="bg-blue-600 hover:bg-blue-700">
                  <Plus className="w-4 h-4 mr-2" />
                  Создать проект
                </Button>
              </DialogTrigger>
              <DialogContent className="bg-neutral-800 text-white">
                <DialogHeader>
                  <DialogTitle>Создать новый проект</DialogTitle>
                </DialogHeader>
                <div className="space-y-4 mt-4">
                  <div>
                    <label className="block mb-2">Название проекта</label>
                    <Input
                      value={newProject.title}
                      onChange={(e) => setNewProject({ ...newProject, title: e.target.value })}
                      className="bg-neutral-700 border-neutral-600"
                    />
                  </div>
                  <div>
                    <label className="block mb-2">Описание</label>
                    <Textarea
                      value={newProject.description}
                      onChange={(e) => setNewProject({ ...newProject, description: e.target.value })}
                      className="bg-neutral-700 border-neutral-600"
                    />
                  </div>
                  <Button 
                    onClick={handleCreateProject}
                    className="w-full bg-blue-600 hover:bg-blue-700"
                  >
                    Создать
                  </Button>
                </div>
              </DialogContent>
            </Dialog>
          </div>
          <div className="space-y-2">
            {team.projects.length > 0 ? (
              team.projects.map(projectLink => (
                <div key={projectLink.id} className="text-white">
                  <h3 className="font-medium">{projectLink.project.title}</h3>
                  <p className="text-sm text-gray-400">{projectLink.project.description}</p>
                </div>
              ))
            ) : (
              <p className="text-white">Нет проектов</p>
            )}
          </div>
        </Card>
      </div>
      <div className='text-right'>
        <p className="text-neutral-600 text-sm">
          Дата создания: {new Date(team.created_at).toLocaleDateString()}
        </p>
      </div>
    </div>
  );
};

export default TeamPage;