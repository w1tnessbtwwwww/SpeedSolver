import { useRef } from "react";
import { ToastContainer } from "react-toastify";
import PasswordInput, { PasswordInputRef } from "@/components/passwordInput/PasswordInput";

export const RegisterPage: React.FC = () => {
    const loginInput = useRef<HTMLInputElement>(null);
    const passwordInput = useRef<PasswordInputRef>(null);

    const handleRegister = (e: React.MouseEvent<HTMLButtonElement>) => {
        e.preventDefault();
        const loginValue = loginInput.current?.value;
        const passwordValue = passwordInput.current?.value;
        
        console.log("Введённые данные:", {
          login: loginValue,
          password: passwordValue
        });
    };

    return ( 
        <div className="register-page centered baseBackground">
            <form className="multipart-form">
                <h1 className="media-header">Регистрация</h1>
                <div className="form-inputs">
                    <input
                        id="login"
                        ref={loginInput}
                        type="text"
                        placeholder="Логин"
                    />
                    <PasswordInput ref={passwordInput} />
                </div>
                <button
                    className="primary-button"
                    onClick={handleRegister}
                >
                    Зарегистрироваться
                </button>
            </form>
            <ToastContainer/>
        </div>
    );
};