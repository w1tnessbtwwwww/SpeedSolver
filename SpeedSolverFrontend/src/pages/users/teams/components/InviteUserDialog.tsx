import { useState, useEffect } from 'react';
import axios from 'axios';
import { Button } from '@/components/ui/button';
import { X, UserPlus } from 'lucide-react';

interface User {
  id: string;
  email: string;
  is_mail_verified: boolean;
  profile: {
    surname: string;
    name: string;
    patronymic: string;
  } | null;
}

interface InviteUserDialogProps {
  setIsInviteDialogOpen: (open: boolean) => void;
  teamId: string;
}

const InviteUserDialog = ({ setIsInviteDialogOpen, teamId }: InviteUserDialogProps) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [users, setUsers] = useState<User[]>([]);
  const [error, setError] = useState<string | null>(null);

  const searchUsers = async (query: string) => {
    if (!query) {
      setUsers([]);
      return;
    }
    
    try {
      const token = localStorage.getItem('access_token');
      const response = await axios.get(`https://api.speedsolver.ru/v1/search/user/find/${query}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      setUsers(response.data || []);
      setError(null);
    } catch (err) {
      setUsers([]);
      setError('Ошибка при поиске пользователей');
      console.error(err);
    }
  };

  const handleInviteUser = async (userId: string) => {
    try {
      const token = localStorage.getItem('access_token');
      
      const response = await axios.post(
        'https://api.speedsolver.ru/v1/teams/invites/invite',
        null, // без тела
        {
          params: { team_id: teamId, user_id: userId },
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      );
      
      
      console.log('Invite response:', response.data);
      
      setUsers(users.filter(user => user.id !== userId));
      setError(null);
    } catch (err) {
      if (axios.isAxiosError(err)) {
        console.log('Invite error response:', err.response?.data);
      }
      
      if (axios.isAxiosError(err)) {
        const errorData = err.response?.data;
        if (Array.isArray(errorData)) {
          // Handle validation error array
          const errorMessage = errorData.map(error => error.msg).join(', ');
          setError(errorMessage || 'Ошибка при приглашении пользователя');
        } else if (typeof errorData === 'object' && errorData !== null) {
          // Handle single error object
          const errorMessage = typeof errorData.detail === 'string' ? 
            errorData.detail : 
            'Ошибка при приглашении пользователя';
          setError(errorMessage);
        } else {
          setError('Ошибка при приглашении пользователя');
        }
      } else {
        setError('Ошибка при приглашении пользователя');
      }
      console.error(err);
    }
  };

  useEffect(() => {
    const debounceTimeout = setTimeout(() => {
      if (searchQuery) {
        searchUsers(searchQuery);
      }
    }, 500);

    return () => clearTimeout(debounceTimeout);
  }, [searchQuery]);

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-neutral-800 rounded-lg p-6 w-96">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-white text-lg font-semibold">Пригласить пользователей</h2>
          <Button
            onClick={() => setIsInviteDialogOpen(false)}
            className="bg-transparent hover:bg-neutral-700"
          >
            <X className="w-4 h-4" />
          </Button>
        </div>

        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Поиск пользователей..."
          className="w-full p-2 mb-4 bg-neutral-700 text-white rounded"
        />

        {error && (
          <div className="bg-red-900/20 border border-red-900/50 rounded p-2 mb-4">
            <p className="text-red-500 text-sm">{error}</p>
          </div>
        )}

        <div className="space-y-2 max-h-96 overflow-y-auto">
          {users.map(user => (
            <div key={user.id} className="flex justify-between items-center bg-neutral-700 p-3 rounded">
              <div>
                <p className="text-white">{user.email}</p>
                {user.profile && (
                  <p className="text-sm text-gray-400">
                    {`${user.profile.surname} ${user.profile.name} ${user.profile.patronymic}`}
                  </p>
                )}
              </div>
              <Button
                onClick={() => handleInviteUser(user.id)}
                className="bg-[#8f297a] hover:bg-[#6d1d5d]"
              >
                <UserPlus className="w-4 h-4" />
              </Button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default InviteUserDialog;