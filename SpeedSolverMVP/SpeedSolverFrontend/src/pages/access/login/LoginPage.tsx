import "./LoginPage.css"
import "../../../anystyles/centeredContainer.css"
import "../../../anystyles/speedsolveruikit.css"
import { PrimaryButton } from "../../../components/primaryButton/PrimaryButton"
import { useState } from "react"
import { authorize } from "../../../app/axios_api"
import { toast, ToastContainer } from "react-toastify"
export const LoginPage = () => {

    const [authForm, setAuthForm] = useState(
    {
        username: "", 
        password: ""
    })


    const handleAuthorize = () => {
        authorize(authForm.username, authForm.password)
        .then(() => window.location.href = "/dashboard")
        .catch(error => toast.error(error))
    }

    return (
       <div className='login-form-container centered baseBackground'>
            <div className="multipart-form">
                <h1 className="mediaHeader" style={{textAlign: "center", fontSize: 30}}>Войти</h1>
                <div className="login-inputs">
                    <input type="text" className="defaultInput" placeholder="Логин" onChange={
                        (e) => {
                            setAuthForm({...authForm, username: e.target.value})}
                    }/>
                    <input type="password" className="defaultInput" placeholder="Пароль" onChange={
                        (e) => {
                            setAuthForm({...authForm, password: e.target.value})
                        }
                    }/>
                    <PrimaryButton text="Авторизоваться" className="button-auth" onClick={handleAuthorize}/> 
                </div>
            </div>
            <ToastContainer />
       </div> 
    )
}