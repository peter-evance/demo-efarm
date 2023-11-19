import { HttpClient } from '@angular/common/http';
import { Injectable, inject, signal } from '@angular/core';
import { firstValueFrom } from 'rxjs';
import { LoginData, LoginResponse, RegistrationResponse, UserProfile, UserRegistrationData } from '../users/users.interfaces';
import { Router } from '@angular/router';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private baseUrl = 'http://localhost:8000/auth/users/';
  private loginUrl = 'http://localhost:8000/auth/login/';
  private logOutUrl = 'http://localhost:8000/auth/logout/';
  private userMeUrl = 'http://127.0.0.1:8000/auth/users/me/';

  private http = inject(HttpClient);
  private router = inject(Router)

  // Signals to represent user roles
  isFarmOwner = signal(false);
  isFarmManager = signal(false);
  isAsstFarmManager = signal(false);
  isFarmWorker = signal(false);

  /**
   * Registers a new user.
   * @param userData - User registration data.
   * @returns A welcome message.
   * @throws Error if registration fails.
   */
  async registerUser(userData: UserRegistrationData): Promise<string> {
    try {
      const response = await firstValueFrom(this.http.post<RegistrationResponse>(this.baseUrl, userData));
      const welcomeMessage = `Welcome, ${response.username}! to Peter's FARMS`;
      return welcomeMessage;
    } catch (error) {
      throw error;
    }
  }

  /**
   * Logs in a user and stores the authentication token.
   * @param userLoginData - User login data.
   * @returns Authentication token.
   * @throws Error if login fails.
   */
  async login(userLoginData: LoginData): Promise<string> {
    try {
      const response = await firstValueFrom(this.http.post<LoginResponse>(this.loginUrl, userLoginData));
      localStorage.setItem('Token', response.auth_token);
      return response.auth_token;
    } catch (error) {
      throw 'An error occurred during login. Please try again.';
    }
  }

  /**
   * Logs out the current user, removes the authentication token, and resets user role signals.
   * @throws Error if logout fails.
   */
  async logout(): Promise<void> {
    try {
      await firstValueFrom(this.http.post(this.logOutUrl, {}));
      localStorage.removeItem('Token');
      this.resetSignals();
      this.router.navigate(['/login']);
    } catch (error) {
      throw 'An error occurred during logout. Please try again.';
    }
  }

  /**
   * Verifies the authentication token and sets user role signals based on the user profile.
   * @returns True if the token is valid, and the user is authenticated; otherwise, false.
   */
  async verifyToken(): Promise<boolean> {
    try {
      const response = await firstValueFrom(this.http.get<UserProfile>(this.userMeUrl));
      if (response instanceof Object) {
        // Assuming there's a property like 'id' that indicates a valid user
        if (response.id) {
          this.setSignals(response); // Set signals based on user roles
          return true; // Token is valid, and user is authenticated
        } else {
          localStorage.removeItem('Token');
          this.resetSignals();
          return false; // Token is valid, but the user is not authenticated
        }
      } else {
        localStorage.removeItem('Token');
        this.resetSignals();
        return false; // Token is invalid or unauthorized
      }
    } catch (error) {
      this.resetSignals();
      return false; // Token is invalid or unauthorized
    }
  }

  /**
   * Sets user role signals based on the user profile.
   * @param userProfile - User profile containing role information.
   */
  private setSignals(userProfile: UserProfile): void {
    this.isFarmOwner.set(userProfile.is_farm_owner);
    this.isFarmManager.set(userProfile.is_farm_manager);
    this.isAsstFarmManager.set(userProfile.is_assistant_farm_manager);
    this.isFarmWorker.set(userProfile.is_farm_worker);
  }

  /**
   * Resets user role signals to false.
   */
  private resetSignals(): void {
    this.isFarmOwner.set(false);
    this.isFarmManager.set(false);
    this.isAsstFarmManager.set(false);
    this.isFarmWorker.set(false);
  }
}
