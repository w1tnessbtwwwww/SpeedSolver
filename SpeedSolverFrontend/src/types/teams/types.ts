// types.ts
export interface Profile {
    patronymic: string;
    id: string;
    about: string;
    name: string;
    surname: string;
    birthdate: string;
  }
  
export interface Leader {
    id: string;
    email: string;
    registered: string;
    password: string;
    is_mail_verified: boolean;
    profile: Profile;
}
  
export interface Team {
    id: string;
    leaderId: string;
    title: string;
    description: string;
    organizationId: string | null;
    leader: Leader;
}
  