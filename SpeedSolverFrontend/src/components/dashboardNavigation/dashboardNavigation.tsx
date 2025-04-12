import { PrimaryButton } from "../primaryButton/PrimaryButton"
import "./dashboardNavigation.css"

export const DashboardNavigation = () => {
    return (
        <div className="headerNavigation">
            <div className="headerNavigation__buttons">
                <PrimaryButton text="Мои организации"/>
                <PrimaryButton text="Мои команды" onClick={() => {
                    window.location.href = "/teams"
                }}/>
                <PrimaryButton text="Мои проекты"/>
            </div>
        </div>
    )
}