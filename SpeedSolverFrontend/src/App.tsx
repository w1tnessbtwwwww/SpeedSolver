import { Route, Routes } from "react-router-dom"
import WelcomePage from "./pages/welcome/WelcomePage"
import { LoginPage } from "./pages/access/login/LoginPage"
import { RegisterPage } from "./pages/access/register/RegisterPage"
function App() {
  return (
    <Routes>
      <Route path="/" element={<WelcomePage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
    </Routes>  
  )
}

export default App
