import NavButton from '@/components/navItem/NavButton';

const Header = () => {
  return (
    <header>
        <nav className='bg-neutral-800/70 pt-1 px-4 flex flex-row gap-x-1'>
            <NavButton to='/companies'>Организации</NavButton>
            <NavButton to='/teams'>Команды</NavButton>
            <NavButton to='/projects'>Проекты</NavButton>
            <NavButton to='/about'>О нас</NavButton>
        </nav>
    </header>
  )
}

export default Header