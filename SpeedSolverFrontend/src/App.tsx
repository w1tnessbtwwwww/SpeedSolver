import { Route, Routes } from "react-router-dom"
import WelcomePage from "./pages/welcome/WelcomePage"
import { LoginPage } from "./pages/access/login/LoginPage"
import { RegisterPage } from "./pages/access/register/RegisterPage"
import { Dashboard } from "./pages/dashboard/Dashboard"
import Teams from "./pages/dashboard/Teams"
import Companies from "./pages/dashboard/Companies"
import Projects from "./pages/dashboard/Projects"
import TestPage from "./pages/test/TestPage"
import DashboardLayout from '@/layout/DashboardLayout'
import AboutPage from "./pages/aboutUs/aboutPage"

function App() {
  return (
    <Routes>
      <Route path="/" element={<WelcomePage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/dashboard" element={<Dashboard />} />

      <Route element={<DashboardLayout/>}>
        <Route path="/teams" element={<Teams />} />
        <Route path="/companies" element={<Companies />} />
        <Route path="/projects" element={<Projects />} />
        <Route path="/about" element={<AboutPage/>}/>
      </Route>
      <Route path="/test" element={<TestPage />} />
    </Routes>  
  )
}

export default App
