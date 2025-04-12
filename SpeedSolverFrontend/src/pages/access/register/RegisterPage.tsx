
import "../../../anystyles/centeredContainer.css"
import "../../../anystyles/speedsolveruikit.css"
import { PrimaryButton } from "../../../components/primaryButton/PrimaryButton"
import { useState } from "react"
import { register } from "../../../app/axios_api"
import { toast, ToastContainer } from "react-toastify"



export const RegisterPage: React.FC = () => {

    const [registerForm, setRegisterForm] = useState({
        username: "",
        password: ""
    })

    return ( 
        <div className="register-page centered baseBackground">
            <div className="multipart-form">
                <h1 className="mediaHeader" style={{textAlign: "center", fontSize: 30}}>Регистрация</h1>
                <div className="login-inputs">
                    <input type="text" className="defaultInput" placeholder="Логин" onChange={(e) => {
                        setRegisterForm({...registerForm, username: e.target.value})
                    }}>
                    </input>
                    <input type="password" placeholder="Пароль" className="defaultInput" onChange={(e) => {
                        setRegisterForm({...registerForm, password: e.target.value})
                    }}>
                    </input>
                    
                    <PrimaryButton text="Зарегистрироваться" className="button-auth" onClick={() => {
                        
                    }}/>
                </div>
            </div>
            <ToastContainer/>
        </div>
    )
}