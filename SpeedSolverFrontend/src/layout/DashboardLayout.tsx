import { Outlet, NavLink } from 'react-router-dom';

const DashboardLayout = () => {
  return (
    <>
      <nav className='bg-neutral-800/70 p-2 flex flex-row gap-x-1'>
        <NavLink
          to='/companies'
          className={({ isActive }) =>
            isActive ? 'dashboard-active-button' : 'dashboard-button'}
        >
          Организации
        </NavLink>
        <NavLink
          to='/teams'
          className={({ isActive }) =>
            isActive ? 'dashboard-active-button' : 'dashboard-button'}
        >
          Команды
        </NavLink>
        <NavLink
          to='/projects'
          className={({ isActive }) =>
            isActive ? 'dashboard-active-button' : 'dashboard-button'}
        >
          Проекты
        </NavLink>
      </nav>
      <Outlet />
    </>
  );
};

export default DashboardLayout;
