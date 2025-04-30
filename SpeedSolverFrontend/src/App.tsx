import { Route, Routes } from "react-router-dom"

import Layout from '@/layout/MainLayout'
import BlobLayout from "./layout/BlobLayout"

import WelcomePage from "./pages/welcome/WelcomePage"
import { LoginPage } from "./pages/auth/login/LoginPage"
import { RegisterPage } from "./pages/auth/register/RegisterPage"
import { VerificationPage } from "./pages/auth/verify/VerifyPage"
import Teams from "./pages/users/teams/Teams"
import TeamPage from "./pages/users/teams/TeamPage" // TODO: fix this import, it's not working right now, it's just a tem
import Companies from "./pages/users/companies/Companies"
import Projects from "./pages/users/projects/Projects"
import AboutPage from "./pages/aboutUs/aboutPage"
import TestPage from "./pages/test/TestPage"

function App() {
  return (
    <Routes>
      <Route element={<BlobLayout />} >
        <Route path="/" element={<WelcomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/verify" element={<VerificationPage />} />
      </Route>

      <Route element={<Layout/>}>
        <Route path="/teams" element={<Teams />} />
        <Route path="/team/:id" element={<TeamPage />} />
        <Route path="/companies" element={<Companies />} />
        <Route path="/projects" element={<Projects />} />
        <Route path="/about" element={<AboutPage/>}/>
      </Route>
      <Route path="/test" element={<TestPage />} />
    </Routes>  
  )
}

export default App
