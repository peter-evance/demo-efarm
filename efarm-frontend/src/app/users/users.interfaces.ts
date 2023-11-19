export interface UserRegistrationData {
    username: string;
    password: string;
    firstName: string;
    lastName: string;
    phoneNumber: string;
    sex: string;
  }

export interface RegistrationResponse {
    username: string;
  }


export interface LoginData {
    username: string;
    password: string;
  }
export interface LoginResponse{
  auth_token: string;
}

export interface UserProfile {
  first_name: string;
  last_name: string;
  phone_number: string;
  sex: string;
  is_farm_owner: boolean;
  is_farm_manager: boolean;
  is_assistant_farm_manager: boolean;
  is_farm_worker: boolean;
  is_team_leader: boolean;
  id: number;
  username: string;
}
