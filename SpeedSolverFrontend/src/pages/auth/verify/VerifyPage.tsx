import { VerificationInput } from "@/components/verificationInput/VerificationInput";
import { toast, ToastContainer } from "react-toastify";
import { useLocation, useNavigate } from "react-router-dom";
import { confirmVerification } from "@/app/axios_api";

export const VerificationPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const email = location.state?.email;

  const handleVerification = async (e: React.FormEvent) => {
    e.preventDefault();
    const code = (e.target as HTMLFormElement).querySelector('input')?.value;

    if (!code || !email) {
      toast.error("Verification code is required");
      return;
    }

    try {
      await confirmVerification(code, email);
      toast.success("Email verified successfully!");
      navigate("/login");
    } catch (error) {
      toast.error(typeof error === 'string' ? error : "Verification failed");
    }
  };

  return (
        <div className="centered">
            <form className="multipart-form" onSubmit={handleVerification}>
                <h1 className="media-header">Введите код из письма</h1>
                <VerificationInput />
                <button type="submit" className="primary-button">
                    Подтвердить
                </button>
                <ToastContainer/>
            </form>
        </div>
  );
};