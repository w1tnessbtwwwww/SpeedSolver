import "../../anystyles/centeredContainer.css"
import "../../anystyles/speedsolveruikit.css"
import "./Dashboard.css"
import { useEffect } from "react"
import { DashboardNavigation } from "../../components/dashboardNavigation/dashboardNavigation"


export const Dashboard: React.FC = () => {

    useEffect(() => {

    })

    return (
        <div className="centered baseBackground">
            <DashboardNavigation />
        </div>
    )
}

