import "./dashboardNavigation.css"

export const DashboardNavigation = () => {
    return (
        <div className="headerNavigation">
            <div className="headerNavigation__buttons">
                <button className="primary-button">
                Мои организации
                </button>
                <button
                    className="primary-button"
                    onClick={() => {
                    window.location.href = "/teams"
                }}>
                    Мои команды
                </button>
                <button className="primary-button">
                    Мои проекты
                </button>
            </div>
        </div>
    )
}