import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';

interface Project {
  id: string;
  title: string;
  description: string;
  created_at: string;
  team_id: string;
  leader: {
    id: string;
    email: string;
  };
}

const Projects = () => {
const [projects] = useState<Project[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error] = useState<string | null>(null);
  const [userEmail, setUserEmail] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [showOnlyAdmin, setShowOnlyAdmin] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const email = localStorage.getItem('user_email');
    setUserEmail(email);
    setIsLoading(false);
  }, []);

  const filteredProjects = projects.filter(project => {
    const matchesSearch = project.title.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesAdminFilter = !showOnlyAdmin || (userEmail && project.leader.email === userEmail);
    return matchesSearch && matchesAdminFilter;
  });

  if (isLoading) return <div>Загрузка...</div>;
  if (error) return <div>{error}</div>;

  const content = filteredProjects.length === 0 ? (
    <p>Нет проектов 😭</p>
  ) : (
    filteredProjects.map((project) => (
      <div
        key={project.id}
        className="p-4 border-1 border-[#161616] rounded-[10px] mb-6 bg-[#0a0a0a] cursor-pointer hover:border-[#262626]"
        onClick={() => navigate(`/project/${project.id}`)}
      >
        <div className="flex gap-6 items-center">
          <h2>{project.title}</h2>
          {userEmail && project.leader.email === userEmail && (
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
        <h1 className="text-white text-xl font-bold">Проекты</h1>
        <Button 
          onClick={() => navigate('/create-project')}
          className="bg-[#8F297A] hover:bg-[#6F1960] fixed md:static z-10 right-8 bottom-8"
        >
          Создать проект
        </Button>
      </div>

      <div className="flex gap-4 items-center mb-6">
        <input
          type="text"
          placeholder="Поиск проектов..."
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
            Только мои проекты
          </label>
        </div>
      </div>

      <div className="text-white">
        {content}
      </div>
    </div>
  );
};

export default Projects;