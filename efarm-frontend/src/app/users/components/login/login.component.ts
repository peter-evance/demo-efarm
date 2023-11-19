import { Component, OnInit, inject } from '@angular/core';
import { AuthService } from '../../../shared/auth.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';

/**
 * Component responsible for user login.
 */
@Component({
  selector: 'login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  loginForm: FormGroup;

  public fb = inject(FormBuilder);
  public authService = inject(AuthService);
  public snackBar = inject(MatSnackBar);
  public router = inject(Router);

  constructor() {
    this.loginForm = this.fb.group({
      username: ['', [Validators.required]],
      password: ['', [Validators.required]]
    });
  }

  /**
   * Performs initialization logic when the component is created.
   * Checks if the user is already logged in and redirects accordingly.
   */
  async ngOnInit() {
    const isUserAuthenticated = await this.authService.verifyToken();

    if (isUserAuthenticated) {
      this.router.navigate(['/logout']);
      this.showSuccessToast('Already Logged In.');
    } else {
      this.router.navigate(['/login']);
    }
  }

  /**
   * Handles the login process when the login form is submitted.
   * If successful, navigates to the logout page; otherwise, displays an error message.
   */
  async onLogin() {
    if (this.loginForm.valid) {
      const userLoginData = this.loginForm.value;
      try {
        const token = await this.authService.login(userLoginData);
        if (token) {
          this.router.navigate(['/logout']);
          this.showSuccessToast('Logged in successfully');
        } else {
          this.handleLoginError('Incorrect login credentials. Please try again.');
        }
      } catch (error) {
        this.handleLoginError('Login failed. Please try again.');
      }
    } else {
      this.showErrorToast('Please fill in all required fields.');
    }
  }

  /**
   * Displays a success toast message.
   * @param message - The success message to be displayed.
   */
  showSuccessToast(message: string) {
    this.snackBar.open(message, 'Close', {
      duration: 3000,
    });
  }

  /**
   * Displays an error toast message.
   * @param message - The error message to be displayed.
   */
  showErrorToast(message: string) {
    this.snackBar.open(message, 'Close', {
      duration: 3000
    });
  }

  /**
   * Handles the actions to be taken on successful login.
   * @param Token - The authentication token received upon successful login.
   */
  handleLoginSuccess(token: string) {
    localStorage.setItem('Token', token);
    this.router.navigate(['/logout']);
    this.showSuccessToast('Logged in successfully');
  }

  /**
   * Handles the actions to be taken on login failure.
   * @param message - The error message to be displayed.
   */
  handleLoginError(message: string) {
    this.showErrorToast(message);
  }
}
