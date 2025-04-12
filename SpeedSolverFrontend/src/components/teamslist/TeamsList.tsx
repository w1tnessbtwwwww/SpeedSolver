import { Team } from "../../types/teams/types"
import "./TeamsList.css"

interface TeamListProps {
    teams: Team[]
}

export const TeamsList: React.FC<TeamListProps> = ({ teams }) => {
    return (
        <div className="teamsList"> 
            {teams.map((team) => (
                <div key={team.id} className="team-item">
                    <h3>{team.title}</h3>
                    <p>{team.description}</p>
                </div>
            ))}
        </div>
    )
}
