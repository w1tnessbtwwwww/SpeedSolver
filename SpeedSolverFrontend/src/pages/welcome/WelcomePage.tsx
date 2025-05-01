import 'react-toastify/dist/ReactToastify.css';
import { ToastContainer } from "react-toastify";
import { Link } from "react-router-dom";
import AnimatedText from '@/components/swappingText/SwappingText';

const WelcomePage = () => {
  const flexText: string[] = [
    'создавайте организации.',
    'создавайте команды.',
    'распределяйте задачи.',
    'планируйте сроки.'
  ];

  return (
    <div className='centered flex-col gap-20'>
      <div className="flex flex-col justify-center gap-2.5">
        <h1 className="text-white text-5xl">SpeedSolver</h1>
        <AnimatedText strings={flexText} />
      </div>

      <div className='flex justify-center gap-x-16 gap-y-4 flex-col md:flex-row'>
        <Link to="/login">
          <button className='glass-button w-[200px]'>Войти</button>
        </Link>
        <Link to="/register">
          <button className='glass-button w-[200px]'>Зарегистрироваться</button>
        </Link>
      </div>

      <Link
        to='/about'
        className='text-white hover:underline'
      >
        Узнайте о нас
      </Link>

      <ToastContainer />
    </div>
  );
}

export default WelcomePage;
