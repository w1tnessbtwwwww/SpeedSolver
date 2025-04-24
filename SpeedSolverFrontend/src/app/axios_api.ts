import axios from "axios";
import { getCookie } from "../utils/cookieUtils";


const client = axios.create({
    baseURL: import.meta.env.VITE_SPEEDSOLVER_DEPLOY_API_URL,
    withCredentials: true
})

export const get_all_teams = () => {
    console.log(getCookie("access_token"))
    return client.get("/account/teams/get_all", {
        headers: {
            Authorization: `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiIwNTVjNjdiNS1lNTc5LTQ1MzEtOTIzOC0xYjVlOGUzNDRlNWEiLCJleHAiOjE3NDQ0NTU2NTF9.Neoa88txlnadWifRplHS9_gFixTC9Tqb4fEUHOfRDH4`
        }
    })
    .then(response => {
        console.log(response.data)
        return response.data
    })
    .catch(error => console.log(error))
}

export const refreshToken = () => {
    return client.get("/access/refresh")
    .then()
    .catch(error => Promise.reject(error))
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
        return response.data;
    } catch (error) {
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
    })
    .then(response => {
        console.log('Server response:', response.data);
        return response.data;
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