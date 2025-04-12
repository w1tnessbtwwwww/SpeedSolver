import { Route, Routes } from "react-router-dom"
import WelcomePage from "./pages/welcome/WelcomePage"
import { LoginPage } from "./pages/access/login/LoginPage"
import { RegisterPage } from "./pages/access/register/RegisterPage"
import { Dashboard } from "./pages/dashboard/Dashboard"
import { TeamsPage } from "./pages/teams/TeamsPage"
function App() {
  return (
    <Routes>
      <Route path="/" element={<WelcomePage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/teams" element={<TeamsPage />} />
    </Routes>  
  )
}

export default App
