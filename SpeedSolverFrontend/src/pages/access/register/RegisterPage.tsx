import { useRef } from "react"
import { ToastContainer } from "react-toastify"
import PasswordInput from "@/components/passwordInput/PasswordInput"

export const RegisterPage: React.FC = () => {
    const loginInput = useRef<HTMLInputElement>(null);

    const handleRegister = (e: React.MouseEvent<HTMLButtonElement>) => {
        e.preventDefault();
        const loginValue = loginInput.current?.value;
        console.log("Введённый логин:", loginValue);
    };

    return ( 
        <div className="register-page centered baseBackground">
            <form className="multipart-form">
                <h1 className="mediaHeader text-center text-3xl">Регистрация</h1>
                <div className="form-inputs">
                    <input
                        id="login"
                        ref={loginInput}
                        type="text"
                        placeholder="Логин"
                    />
                    <PasswordInput />
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
