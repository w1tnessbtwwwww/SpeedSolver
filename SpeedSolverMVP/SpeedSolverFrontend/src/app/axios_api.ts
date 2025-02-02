import axios from "axios";


const client = axios.create({
    baseURL: import.meta.env.VITE_SPEEDSOLVER_LOCAL_API_URL
})

export const authorize = (username: string, password: string) => {
    return client.post("/access/authorize", `username=${username}&password=${password}`, {
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        }
    }).then(response => response.data)
    .catch(error => {
        if (error.response) {
            return Promise.reject(error.response.data.detail) || "Неизвестная ошибка"
        }
        return Promise.reject("Ошибка на стороне клиента.")
    })
}