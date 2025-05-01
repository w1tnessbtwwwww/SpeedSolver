import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { get_all_teams } from '@/app/axios_api';
import { Checkbox } from '@/components/ui/checkbox';
import { Button } from '@/components/ui/button';
import AddTeamForm from '@/components/addTeamForm/addTeamForm';

interface Leader {
  password: string;
  is_mail_verified: boolean;
  id: string;
  email: string;
  registered: string;
}

interface Team {
  title: string;
  description: string;
  organizationId: string | null;
  id: string;
  created_at: string;
  organization: null;
  leader: Leader;
}

const Teams = () => {
  const [teams, setTeams] = useState<Team[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [userEmail, setUserEmail] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [showOnlyAdmin, setShowOnlyAdmin] = useState(false);
  const [showAddForm, setShowAddForm] = useState(false);
  const navigate = useNavigate();

  const fetchTeams = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const email = localStorage.getItem('user_email');
      setUserEmail(email);

      if (!token) {
        navigate('/login');
        return;
      }

      const data = await get_all_teams();
      setTeams(Array.isArray(data) ? data : []);
    } catch (err: any) {
      console.error('Error fetching teams:', err);

      if (err.message === 'Authentication failed') {
        localStorage.removeItem('access_token');
        navigate('/login');
      } else {
        setError('Ошибка загрузки команд');
      }
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchTeams();
  }, [navigate]);

  const handleAddTeamSuccess = () => {
    setShowAddForm(false);
    fetchTeams();
  };

  const filteredTeams = teams.filter(team => {
    const matchesSearch = team.title.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesAdminFilter = !showOnlyAdmin || (userEmail && team.leader.email === userEmail);
    return matchesSearch && matchesAdminFilter;
  });

  if (isLoading) return <div>Загрузка...</div>;
  if (error) return <div>{error}</div>;

  const content = filteredTeams.length === 0 ? (
    <p>Нет команд 😭</p>
  ) : (
    console.log(filteredTeams),
    filteredTeams.map((team) => (
      
      <div
        key={team.id}
        className="p-4 border-1 border-[#161616] rounded-[10px] mb-6 bg-[#0a0a0a] cursor-pointer hover:border-[#262626]"
        onClick={() => navigate(`/team/${team.id}`)}
      >
        <div className="flex gap-6 items-center">
          <h2>{team.title}</h2>
          {userEmail && team.leader.email === userEmail && (
            <div className='bg-black rounded-[10px]'>
              <span className="text-admin-gradient text-white px-2 py-1 rounded text-sm">
                Admin
              </span>
            </div>
          )}
        </div>
      </div>
    ))
  );

  return (
    <div className='p-6'>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-white text-xl font-bold">Команды</h1>
        <Button 
          onClick={() => setShowAddForm(!showAddForm)}
          className="bg-[#8F297A] hover:bg-[#6F1960] fixed md:static z-10 right-8 bottom-8"
        >
          {showAddForm ? 'Отменить' : 'Создать команду'}
        </Button>
      </div>

      {showAddForm && <AddTeamForm onClose={() => setShowAddForm(false)} onSuccess={handleAddTeamSuccess} />}

      <div className="flex gap-4 items-center mb-6">
        <input
          type="text"
          placeholder="Поиск команд..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="bg-[#0a0a0a] text-white px-4 py-2 rounded-[10px] border-1 border-[#161616] w-64"
        />
        <div className="flex items-center gap-2 text-white">
          <Checkbox
            id="admin-filter"
            checked={showOnlyAdmin}
            onCheckedChange={(checked) => setShowOnlyAdmin(checked as boolean)}
          />
          <label
            htmlFor="admin-filter"
            className="text-sm font-medium leading-none cursor-pointer"
          >
            Только мои команды
          </label>
        </div>
      </div>

      <div className="text-white">
        {content}
      </div>
    </div>
  );
};

export default Teams;
