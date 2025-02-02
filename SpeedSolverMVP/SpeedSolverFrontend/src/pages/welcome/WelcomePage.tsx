import 'react-toastify/dist/ReactToastify.css';
import styles from "./WelcomePage.module.css"
import "../../anystyles/speedsolveruikit.css"
import { PrimaryButton } from "../../components/primaryButton/PrimaryButton";
import { ToastContainer } from "react-toastify";
import { Link } from "react-router-dom";

const WelcomePage = () => {

    return (
        <div className={styles.container}>

            <h1 className="mediaHeader">SpeedSolver</h1>
            
            <div className={styles.button_container}>
                <Link to="/login">
                    <PrimaryButton text="Войти" />
                </Link>
                

                <PrimaryButton text="Зарегистрироваться" onClick={() => {
                   
                }}/>
            </div>
            <ToastContainer />
        </div>
    )
}

export default WelcomePage