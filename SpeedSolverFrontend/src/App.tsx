import { Route, Routes } from "react-router-dom"

import Layout from '@/layout/MainLayout'

import WelcomePage from "./pages/welcome/WelcomePage"
import { LoginPage } from "./pages/auth/login/LoginPage"
import { RegisterPage } from "./pages/auth/register/RegisterPage"
import Teams from "./pages/users/teams/Teams"
import Companies from "./pages/users/companies/Companies"
import Projects from "./pages/users/projects/Projects"
import AboutPage from "./pages/aboutUs/aboutPage"
import TestPage from "./pages/test/TestPage"

function App() {
  return (
    <Routes>
      
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />

      <Route element={<Layout/>}>
        <Route path="/" element={<WelcomePage />} />
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
