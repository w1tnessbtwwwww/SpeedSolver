import axios from "axios";
import { getCookie } from "../utils/cookieUtils";


const client = axios.create({
    baseURL: import.meta.env.VITE_SPEEDSOLVER_DEPLOY_API_URL
})

// client.interceptors.response.use (
//     response => {
//         return response
//     },
//     error => {
//         if (error.response && error.response.status === 401) {
//             return refreshToken()
//         }
//     }
// )


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
                }
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

export const register = (username: string, password: string) => {
    return client.post("/access/register", {
        username: username,
        password: password
    }).then(response => response.data)
    .catch(error => {
        if (error.response) {
            return Promise.reject(error.response.data.detail) || "Неизвестная ошибка"
        }
        return Promise.reject("Ошибка на стороне клиента.")
    })
}