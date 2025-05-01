import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { get_team_by_id } from '@/app/axios_api';
import { Button } from '@/components/ui/button';
import { Undo2 } from 'lucide-react';
import Card from '@/components/card/Card';

interface TeamMemberProfile {
  surname: string;
  name: string;
  birthdate: string;
  userId: string;
  avatar_path: string | null;
  patronymic: string;
  id: string;
  about: string;
}

interface TeamMemberUser {
  password: string;
  is_mail_verified: boolean;
  id: string;
  email: string;
  registered: string;
  profile: TeamMemberProfile;
}

interface TeamMember {
  id: string;
  invited_by_request_id: string | null;
  userId: string;
  teamId: string;
  user: TeamMemberUser;
}

interface TeamProject {
  id: string;
  creator_id: string;
  title: string;
  description: string;
  created_at: string;
}

interface TeamProjectLink {
  teamId: string;
  projectId: string;
  id: string;
  project: TeamProject;
}

interface Team {
  title: string;
  description: string;
  organizationId: string | null;
  id: string;
  leaderId: string;
  created_at: string;
  projects: TeamProjectLink[];
  members: TeamMember[];
}

const TeamPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [team, setTeam] = useState<Team | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

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
          <h2 className="text-white text-lg font-semibold ">Описание</h2>
          <p className="text-white">{team.description}</p>
        </Card>
        
        <Card className="mb-4">
          <h2 className="text-white text-lg font-semibold">Участники</h2>
          <div className="space-y-2">
            {team.members.map(member => (
              <div key={member.id} className="text-white">
                {member.user.profile.name}{' '}
                {member.user.profile.surname}
                <br/>
                <span className='text-neutral-600'>
                    {member.user.email}    
                </span>
              </div>
            ))}
          </div>
        </Card>

        <Card className="mb-4">
          <h2 className="text-white text-lg font-semibold">Проекты команды</h2>
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
        <p className="text-neutral-600 text-sm">Дата создания: {new Date(team.created_at).toLocaleDateString()}</p>
      </div>
    </div>
  );
};

export default TeamPage;