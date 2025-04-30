import NavButton from '@/components/navItem/NavButton';
import { useBreakpoint } from '@/hooks/use-breackpoint';
import { Sidebar } from "@/components/sidebar"
import { useState, useEffect } from 'react';
import { SquareChevronRight } from 'lucide-react';
import { Link, NavLink, useNavigate } from 'react-router-dom';

const Header = () => {
  const isMobile = useBreakpoint(1000);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [userEmail, setUserEmail] = useState<string | null>(null);
  const navigate = useNavigate();
  const toggleSidebar = () => setIsSidebarOpen(!isSidebarOpen);

  useEffect(() => {
    const email = localStorage.getItem('user_email');
    setUserEmail(email);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user_email');
    navigate('/login');
  };

  const navLinks = [
    { title: "Организации", to: "/companies", type: "left" },
    { title: "Команды", to: "/teams", type: "left" },
    { title: "Проекты", to: "/projects", type: "left" },
    { title: "О нас", to: "/about", type: "left" },
  ];

  const authLinks = !userEmail ? [
    { title: "Войти", to: "/login", type: "right" },
    { title: "Создать аккаунт", to: "/register", type: "right" },
  ] : [];

  return (
    <header className='flex flex-row bg-neutral-800/70 px-6 gap-6 items-center sticky top-0 z-5'>
      {isMobile ? (
        <div className="flex items-center">
          <button onClick={toggleSidebar} className="text-white mr-4">
            <SquareChevronRight />
          </button>
          <Link
          to='/'
          className='text-white font-bold mr-6 my-2'>
            SpeedSolver
          </Link>
          <Sidebar isOpen={isSidebarOpen} setIsOpen={setIsSidebarOpen}>
            <h1 className='font-bold text-xl text-white mt-6 mb-3 hover:text-[#8F297A] transition-[0.15s]'>
              SpeedSolver
            </h1>
            <nav className="flex flex-col gap-4">
              {navLinks.map((link, index) => (
                <NavLink 
                  key={index} 
                  to={link.to}
                  className={({ isActive }) => 
                    `block rounded hover:underline ${isActive ? 'text-gradient' : 'text-[#818181]'}`
                  }
                  onClick={toggleSidebar}
                >
                  {link.title}
                </NavLink>
              ))}
              {!userEmail ? (
                authLinks.map((link, index) => (
                  <NavLink
                    key={`auth-${index}`}
                    to={link.to}
                    className={({ isActive }) => 
                      `block rounded hover:underline ${isActive ? 'text-gradient' : 'text-[#818181]'}`
                    }
                    onClick={toggleSidebar}
                  >
                    {link.title}
                  </NavLink>
                ))
              ) : (
                <div className="flex flex-col gap-2 mt-2">
                  <Link to="/profile" className="text-white hover:text-[#8F297A] transition-colors">
                    {userEmail}
                  </Link>
                  <button 
                    onClick={() => {
                      handleLogout();
                      toggleSidebar();
                    }}
                    className="text-[#818181] hover:text-white transition-colors text-left"
                  >
                    Выйти
                  </button>
                </div>
              )}
            </nav>
          </Sidebar>
        </div>
      ) : (
        <>
          <Link to='/' className='text-white font-bold mr-6 my-2'>
            SpeedSolver
          </Link>
          <div className='flex flex-1 items-center'>
            <div className='flex gap-x-1'>
              {navLinks.filter(link => link.type === 'left').map((link, index) => (
                <NavButton key={index} to={link.to}>
                  {link.title}
                </NavButton>
              ))}
            </div>
            <div className='ml-auto flex gap-x-1 items-center'>
              {!userEmail ? (
                authLinks.map((link, index) => (
                  <NavButton key={index} to={link.to}>
                    {link.title}
                  </NavButton>
                ))
              ) : (
                <div className="flex items-center gap-4">
                  <Link to="/profile" className="text-white hover:text-[#8F297A] transition-colors">
                    {userEmail}
                  </Link>
                  <button 
                    onClick={handleLogout}
                    className="text-[#818181] hover:text-white transition-colors"
                  >
                    Выйти
                  </button>
                </div>
              )}
            </div>
          </div>
        </>
      )}
    </header>
  );
};

export default Header;