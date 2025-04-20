import { useRef } from "react";
import { authorize } from "@/app/axios_api";
import { toast, ToastContainer } from "react-toastify";
import PasswordInput, { PasswordInputRef } from "@/components/passwordInput/PasswordInput";

export const LoginPage = () => {
    const loginInput = useRef<HTMLInputElement>(null);
    const passwordInput = useRef<PasswordInputRef>(null);

    const handleAuthorize = (e: React.MouseEvent<HTMLButtonElement>) => {
        e.preventDefault();
        const username = loginInput.current?.value || "";
        const password = passwordInput.current?.value || "";

        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);

        authorize(formData)
            .then(() => window.location.href = "/about")
            .catch(error => toast.error(error));
    };

    return (
        <div className='auth-form centered baseBackground'>
            <form className="multipart-form">
                <h1 className="media-header">Войти</h1>
                <div className="form-inputs">
                    <input
                        ref={loginInput}
                        type="text"
                        placeholder="Логин"
                    />
                    <PasswordInput ref={passwordInput} />
                    <button 
                        className="primary-button" 
                        onClick={handleAuthorize}
                    >
                        Авторизоваться
                    </button> 
                </div>
            </form>
            <ToastContainer />
        </div> 
    );
};