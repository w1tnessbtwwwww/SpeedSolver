import "../../swalfire.css"
import 'react-toastify/dist/ReactToastify.css';
import styles from "./WelcomePage.module.css"
import { PrimaryButton } from "../../components/primaryButton/PrimaryButton";
import { ToastContainer,  } from "react-toastify";

const WelcomePage = () => {

    return (
        <div className={styles.container}>

            <h1 className={styles.title_text}>SpeedSolver</h1>
            
            <div className={styles.button_container}>
                <PrimaryButton text="Войти" onClick={() => {
                    console.log("sign in")
                }}/>

                <PrimaryButton text="Зарегистрироваться" onClick={() => {
                    
                }}/>
            </div>
            <ToastContainer />
        </div>
    )
}

export default WelcomePage