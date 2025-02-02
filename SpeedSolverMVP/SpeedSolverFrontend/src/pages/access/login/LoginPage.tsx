import "./LoginPage.css"
import "../../../anystyles/centeredContainer.css"
import "../../../anystyles/speedsolveruikit.css"
import { PrimaryButton } from "../../../components/primaryButton/PrimaryButton"
export const LoginPage = () => {
    return (
       <div className='login-form-container centered baseBackground'>
            <div className="multipart-form">
                <h1 className="mediaHeader" style={{textAlign: "center", fontSize: 40}}>Войти</h1>
                <div className="login-inputs">
                    <input type="text" className="defaultInput" placeholder="Логин"/>
                    <input type="password" className="defaultInput" placeholder="Пароль"/>
                </div>
                <PrimaryButton text="Авторизоваться" />
            </div>
       </div> 
    )
}