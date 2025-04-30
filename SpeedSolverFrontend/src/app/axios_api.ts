import axios from "axios";
import { getCookie } from "../utils/cookieUtils";


const client = axios.create({
    baseURL: import.meta.env.VITE_SPEEDSOLVER_DEPLOY_API_URL,
    withCredentials: true
})

export const get_all_teams = () => {
    const token = localStorage.getItem("access_token") || getCookie("access_token")  ;
    return client.get("https://api.speedsolver.ru/v1/account/teams/get_all", {
        headers: {
            Authorization: `Bearer ${token}`
        }
    })
    .then(response => response.data)
    .catch(async (error) => {
        if (error.response?.status === 401) {
            try {
                await refreshToken();
                const newToken = localStorage.getItem("access_token") || getCookie("access_token");
                const retryResponse = await client.get("https://api.speedsolver.ru/v1/account/teams/get_all", {
                    headers: {
                        Authorization: `Bearer ${newToken}`
                    }
                });
                return retryResponse.data;
            } catch (refreshError) {
                localStorage.removeItem("access_token");
                throw new Error('Authentication failed');
            }
        }
        throw error;
    });
}

export const refreshToken = () => {
    return client.get("/access/refresh")
    .then(response => {
        if (response.data.access_token) {
            localStorage.setItem("access_token", response.data.access_token);
        }
    })
    .catch(error => {
        localStorage.removeItem("access_token");
        return Promise.reject(error);
    });
}

export const authorize = async (formData: URLSearchParams) => {
    try {
        const response = await axios.post(
            'https://api.speedsolver.ru/v1/access/authorize',
            formData,
            {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                withCredentials: true
            }
        );
        if (response.data.access_token) {
            localStorage.setItem("access_token", response.data.access_token);
            localStorage.setItem("refresh_token", response.data.refresh_token);
            localStorage.setItem("user_email", formData.get("username") || "");
        }
        return response.data;
    } catch (error) {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        localStorage.removeItem("user_email");
        if (axios.isAxiosError(error)) {
            throw error.response?.data?.message || 'Authorization failed';
        }
        throw 'Authorization failed';
    }
};

export const register = (email: string, password: string) => {
    return client.post("https://api.speedsolver.ru/v1/access/register", {
        email: email,
        password: password
    }, {
        withCredentials: true,
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .catch(error => {
        if (error.response) {
            console.error('Server error:', error.response.data);
            return Promise.reject(error.response.data.detail || "Неизвестная ошибка");
        }
        console.error('Client error:', error);
        return Promise.reject("Ошибка на стороне клиента.");
    });
}

export const confirmVerification = (code: string, email: string) => {
    return client.post("https://api.speedsolver.ru/v1/verification/confirm", {
        code: code,
        email: email
    })
    .then(response => {
        console.log('Verification response:', response.data);
        return response.data;
    })
    .catch(error => {
        if (error.response) {
            console.error('Verification error:', error.response.data);
            return Promise.reject(error.response.data.detail || "Verification failed");
        }
        console.error('Client error:', error);
        return Promise.reject("Client-side error occurred");
    });
}


interface CreateTeamData {
    title: string;
    description: string;
    organizationId?: string;
}

export const create_team = (teamData: CreateTeamData) => {
    const token = localStorage.getItem("access_token") || getCookie("access_token");
    return client.post("https://api.speedsolver.ru/v1/teams/create", teamData, {
        headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.data)
    .catch(async (error) => {
        if (error.response?.status === 401) {
            try {
                await refreshToken();
                const newToken = localStorage.getItem("access_token") || getCookie("access_token");
                const retryResponse = await client.post("https://api.speedsolver.ru/v1/teams/create", teamData, {
                    headers: {
                        Authorization: `Bearer ${newToken}`,
                        'Content-Type': 'application/json'
                    }
                });
                return retryResponse.data;
            } catch (refreshError) {
                localStorage.removeItem("access_token");
                throw new Error('Authentication failed');
            }
        }
        throw error;
    });
};


interface TeamMemberProfile {
  surname: string;
  name: string;
  birthdate: string;
  userId: string;
  avatar_path: string | null;
  patronymic: string;
  id: string;
  about: string;
}

interface TeamMemberUser {
  password: string;
  is_mail_verified: boolean;
  id: string;
  email: string;
  registered: string;
  profile: TeamMemberProfile;
}

interface TeamMember {
  id: string;
  invited_by_request_id: string | null;
  userId: string;
  teamId: string;
  user: TeamMemberUser;
}

interface TeamProject {
  id: string;
  creator_id: string;
  title: string;
  description: string;
  created_at: string;
}

interface TeamProjectLink {
  teamId: string;
  projectId: string;
  id: string;
  project: TeamProject;
}

interface TeamDetails {
  title: string;
  description: string;
  organizationId: string | null;
  id: string;
  leaderId: string;
  created_at: string;
  projects: TeamProjectLink[];
  members: TeamMember[];
}

export const get_team_by_id = (teamId: string) => {
    const token = localStorage.getItem("access_token") || getCookie("access_token");
    return client.get(`https://api.speedsolver.ru/v1/teams/about/${teamId}`, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    })
    .then(response => response.data[0]) // Получаем первый элемент массива, так как API возвращает массив
    .catch(async (error) => {
        if (error.response?.status === 401) {
            try {
                await refreshToken();
                const newToken = localStorage.getItem("access_token") || getCookie("access_token");
                const retryResponse = await client.get(`https://api.speedsolver.ru/v1/teams/about/${teamId}`, {
                    headers: {
                        Authorization: `Bearer ${newToken}`
                    }
                });
                return retryResponse.data[0];
            } catch (refreshError) {
                localStorage.removeItem("access_token");
                throw new Error('Authentication failed');
            }
        }
        throw error;
    });
};