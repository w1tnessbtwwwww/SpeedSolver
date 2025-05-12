import { useRef } from "react";
import { authorize } from "@/app/axios_api";
import { toast, ToastContainer } from "react-toastify";
import PasswordInput, { PasswordInputRef } from "@/components/passwordInput/PasswordInput";
import { useNavigate } from "react-router-dom";
import { Blob } from "@/components/blob/Blob";
import { Link } from "react-router-dom";

export const LoginPage = () => {
    const navigate = useNavigate();
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
            .then(() => navigate("/about"))
            .catch(error => toast.error(error));
    };

    return (
        <div className='auth-form centered'>
            <Blob size={5000} />
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
                <Link
                    className="text-white text-center hover:underline"
                    to='/register'>
                        Нет аккаунта? Создать аккаунт
                </Link>
            </form>
            <ToastContainer />
        </div> 
    );
};