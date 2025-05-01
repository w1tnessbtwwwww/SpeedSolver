import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import Card from '@/components/card/Card';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"

interface Profile {
  surname: string;
  name: string;
  birthdate: string;
  userId: string;
  avatar_path: string | null;
  patronymic: string;
  id: string;
  about: string;
}

const formSchema = z.object({
  surname: z.string().min(2, { message: "Фамилия должна содержать минимум 2 символа" }),
  name: z.string().min(2, { message: "Имя должно содержать минимум 2 символа" }),
  patronymic: z.string().optional(),
  about: z.string().optional(),
  birthdate: z.string().regex(/^\d{4}-\d{2}-\d{2}$/, { message: "Неверный формат даты" }),
});

const ProfilePage = () => {
  const navigate = useNavigate();
  const [profile, setProfile] = useState<Profile | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isEditing, setIsEditing] = useState(false);

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      surname: "",
      name: "",
      patronymic: "",
      about: "",
      birthdate: "",
    },
  });

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await fetch('https://api.speedsolver.ru/v1/account/profile/get', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          }
        });

        if (!response.ok) {
          if (response.status === 401) {
            setError('Ошибка авторизации. Пожалуйста, войдите снова.');
            navigate('/login');
            return;
          }
          if (response.status === 404) {
            setError('Профиль не найден. Пожалуйста, создайте профиль.');
            return;
          }
          const errorText = await response.text();
          throw new Error(`Ошибка сервера: ${response.status}. ${errorText}`);
        }

        const contentType = response.headers.get("content-type");
        if (!contentType || !contentType.includes("application/json")) {
          throw new Error("Получен неверный формат данных от сервера");
        }

        const data = await response.json();
        setProfile(data);
        form.reset({
          surname: data.surname,
          name: data.name,
          patronymic: data.patronymic || "",
          about: data.about || "",
          birthdate: data.birthdate,
        });
      } catch (err) {
        console.error('Ошибка при загрузке профиля:', err);
        setError(`Не удалось загрузить профиль: ${err instanceof Error ? err.message : 'Неизвестная ошибка'}`);
      } finally {
        setIsLoading(false);
      }
    };

    fetchProfile();
  }, []);

  const onSubmit = async (values: z.infer<typeof formSchema>) => {
    try {
      const response = await fetch('https://api.speedsolver.ru/v1/account/profile/update', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify(values)
      });
      
      if (!response.ok) {
        if (response.status === 401) {
          setError('Ошибка авторизации. Пожалуйста, войдите снова.');
          navigate('/login');
          return;
        }
        const errorText = await response.text();
        throw new Error(`Ошибка сервера: ${response.status}. ${errorText}`);
      }

      const contentType = response.headers.get("content-type");
      if (!contentType || !contentType.includes("application/json")) {
        throw new Error("Получен неверный формат данных от сервера");
      }

      const updatedData = await response.json();
      setProfile({ ...profile!, ...updatedData });
      setIsEditing(false);
      setError(null);
    } catch (err) {
      console.error('Ошибка при обновлении профиля:', err);
      if (err instanceof TypeError && err.message === 'Failed to fetch') {
        setError('Не удалось подключиться к серверу. Пожалуйста, проверьте ваше интернет-соединение и попробуйте снова.');
      } else {
        setError(`Не удалось обновить профиль: ${err instanceof Error ? err.message : 'Неизвестная ошибка'}`);
      }
    }
  };

  if (isLoading) return <div className="text-white p-6">Загрузка...</div>;
  if (error) return (
    <div className="p-6">
      <div className="bg-red-500/10 border border-red-500 rounded-md p-4 mb-4">
        <p className="text-red-500">{error}</p>
      </div>
      {error.includes('авторизации') && (
        <Button onClick={() => navigate('/login')} className="bg-[#8F297A] hover:bg-[#6F1960]">
          Войти
        </Button>
      )}
    </div>
  );
  if (!profile) return (
    <div className="p-6">
      <div className="bg-yellow-500/10 border border-yellow-500 rounded-md p-4">
        <p className="text-yellow-500">Профиль не найден</p>
      </div>
    </div>
  );

  return (
    <div className='p-6'>
      <h1 className="text-white text-xl font-bold mb-6">Мой профиль</h1>
      
      <Card className="p-6 bg-[#0a0a0a] border-[#161616]">
        {!isEditing ? (
          <>
            <div className="mb-4">
              <h2 className="text-white text-lg mb-2">Личные данные</h2>
              <p className="text-white ">Имя: {profile.name}</p>
              <p className="text-white">Фамилия: {profile.surname}</p>
              <p className="text-white">Отчество: {profile.patronymic || "Не указано"}</p>
              <p className="text-white">Дата рождения: {new Date(profile.birthdate).toLocaleDateString()}</p>
              <p className="text-white">О себе: {profile.about || "Не указано"}</p>
            </div>
            <Button onClick={() => setIsEditing(true)}>
              Редактировать
            </Button>
          </>
        ) : (
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
              <FormField
                control={form.control}
                name="name"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel className="text-white">Имя</FormLabel>
                    <FormControl>
                      <Input className="text-white bg-transparent" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="surname"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel className="text-white">Фамилия</FormLabel>
                    <FormControl>
                      <Input className="text-white bg-transparent" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="patronymic"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel className="text-white">Отчество</FormLabel>
                    <FormControl>
                      <Input className="text-white bg-transparent" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="birthdate"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel className="text-white">Дата рождения</FormLabel>
                    <FormControl>
                      <Input type="date" className="text-white bg-transparent" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="about"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel className="text-white">О себе</FormLabel>
                    <FormControl>
                      <textarea 
                        className="w-full min-h-[100px] rounded-md border bg-transparent px-3 py-2 text-white border-input"
                        {...field} 
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <div className="flex gap-4">
                <Button type="submit">Сохранить</Button>
                <Button type="button" variant="outline" onClick={() => setIsEditing(false)}>
                  Отмена
                </Button>
              </div>
            </form>
          </Form>
        )}
      </Card>
    </div>
  );
};

export default ProfilePage;