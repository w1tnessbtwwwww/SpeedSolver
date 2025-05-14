import Card from '@/components/card/Card';

interface UserProfile {
  surname: string;
  name: string;
  patronymic: string;
  about: string;
  birthdate: string;
  avatar_path: string | null;
}

interface User {
  id: string;
  email: string;
  is_mail_verified: boolean;
  profile: UserProfile | null;
}

interface TeamMember {
  id: string;
  user: User;
}

interface MemberCardProps {
  members: TeamMember[];
}

const MemberCard = ({ members }: MemberCardProps) => {
  return (
    <Card className="h-full">
      <h2 className="text-white text-lg font-semibold mb-4">Участники</h2>
      <div className="space-y-3">
        {members.map(member => (
          <div
            key={member.id}
            className="p-3 bg-neutral-700 rounded-lg hover:bg-neutral-600 transition-colors"
          >
            <div className="text-white font-medium">
              {member.user.profile ? (
                `${member.user.profile.name} ${member.user.profile.surname}`
              ) : (
                'Профиль не заполнен'
              )}
            </div>
            <div className='text-neutral-400 text-sm'>
              {member.user.email}
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
};

export default MemberCard;
