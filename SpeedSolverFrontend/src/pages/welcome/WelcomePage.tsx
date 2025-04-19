import 'react-toastify/dist/ReactToastify.css';
import styles from "./WelcomePage.module.css"
import "../../anystyles/speedsolveruikit.css"
import { PrimaryButton } from "../../components/primaryButton/PrimaryButton";
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
                    <PrimaryButton text="Войти" />
                </Link>
                
                <Link to="/register">
                    <PrimaryButton text="Зарегистрироваться"/>
                </Link>
                
            </div>
            <ToastContainer />
        </div>
    )
}

export default WelcomePage