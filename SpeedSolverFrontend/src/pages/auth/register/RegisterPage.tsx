import { useRef } from "react";
import { toast, ToastContainer } from "react-toastify";
import { useNavigate } from "react-router-dom";
import { register } from "@/app/axios_api";
import PasswordInput, { PasswordInputRef } from "@/components/passwordInput/PasswordInput";

export const RegisterPage: React.FC = () => {
    const navigate = useNavigate();
    const emailInput = useRef<HTMLInputElement>(null);
    const passwordInput = useRef<PasswordInputRef>(null);

    const handleRegister = async (e: React.MouseEvent<HTMLButtonElement>) => {
        e.preventDefault();
        const email = emailInput.current?.value || "";
        const password = passwordInput.current?.value || "";

        if (!email || !password) {
            toast.error("Please fill in all fields");
            return;
        }

        try {
            await register(email, password);
            toast.success("Registration successful! Please check your email for verification code.");
            navigate("/verify", { state: { email } });
        } catch (error) {
            toast.error(typeof error === 'string' ? error : "Registration failed");
        }
    };

    return ( 
        <div className="register-page centered flex-col gap-6">
            <form className="multipart-form">
                <h1 className="media-header">Регистрация</h1>
                <div className="form-inputs">
                    <input
                        id="email"
                        ref={emailInput}
                        type="email"
                        placeholder="Email"
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