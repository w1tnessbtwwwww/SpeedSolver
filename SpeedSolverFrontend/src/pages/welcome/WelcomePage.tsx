import 'react-toastify/dist/ReactToastify.css';
import styles from "./WelcomePage.module.css"

import { ToastContainer } from "react-toastify";
import { Link } from "react-router-dom";
import AnimatedText from '../../components/swappingText/SwappingText';

const WelcomePage = () => {

    return (
        <div className={styles.container}>
            
            <div className="welcome-text">
                <h1 className="mediaHeader">SpeedSolver</h1>
                <AnimatedText />
            </div>
            
            <div className={styles.button_container}>
                <Link to="/login">
                    <button className='primary-button'>Войти</button>
                </Link>
                
                <Link to="/register">
                    <button className='primary-button'>Зарегистрироваться</button>
                </Link>
                
            </div>
            <ToastContainer />
        </div>
    )
}

export default WelcomePage