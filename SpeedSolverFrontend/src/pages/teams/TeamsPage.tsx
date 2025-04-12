import { useEffect, useState } from "react"
import "../../anystyles/centeredContainer.css"
import { Team } from "../../types/teams/types"
import { get_all_teams } from "../../app/axios_api"
import { TeamsList } from "../../components/teamslist/TeamsList"
import "./TeamsPage.css"

// interface TeamProps {
//     teams: Team[]
// }

export const TeamsPage = () => {

    const [teams, setTeams] = useState<Team[]>([])

    useEffect(() => {
        get_all_teams().then(res => setTeams(res))
        console.log(teams)
    }, [])


    return (
        <div className="centered baseBackground">
            <div className="content">
                <TeamsList teams={teams} />
            </div>
        </div>
    )
}