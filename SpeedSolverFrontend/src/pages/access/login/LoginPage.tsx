import { useState } from "react"
import { authorize } from "@/app/axios_api"
import { toast, ToastContainer } from "react-toastify"
import PasswordInput from "@/components/passwordInput/PasswordInput"
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
       <div className='auth-form centered baseBackground'>
            <div className="multipart-form">
                <h1 className="mediaHeader text-center text-3xl">Войти</h1>
                <div className="form-inputs">
                    <input
                        type="text"
                        className="defaultInput"
                        placeholder="Логин"
                        onChange={
                        (e) => {
                            setAuthForm({...authForm, username: e.target.value})}
                    }/>
                    <PasswordInput />
                    <button className="primary-button" onClick={handleAuthorize}>
                        Авторизоваться
                    </button> 
                </div>
            </div>
            <ToastContainer />
       </div> 
    )
}