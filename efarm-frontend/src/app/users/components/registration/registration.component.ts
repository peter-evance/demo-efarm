import { Component, OnInit, inject } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { AuthService } from '../../../shared/auth.service';

/**
 * Component responsible for user registration.
 */
@Component({
  selector: 'registration',
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.css'],
})
export class RegistrationComponent implements OnInit {
  registrationForm: FormGroup;

  public authService = inject(AuthService);
  public fb = inject(FormBuilder);
  public snackBar = inject(MatSnackBar);
  public router = inject(Router);

  constructor() {
    this.registrationForm = this.fb.group({
      username: ['', [Validators.required]],
      password: ['', [Validators.required]],
      first_name: ['', [Validators.required]],
      last_name: ['', [Validators.required]],
      phone_number: ['', [Validators.required]],
      sex: ['', [Validators.required]],
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
      this.router.navigate(['/register']);
    }
  }

  /**
   * Handles the form submission for user registration.
   * If successful, navigates to the login page.
   */
  async onSubmit() {
    if (this.registrationForm.valid) {
      try {
        const formData = this.registrationForm.value;
        const welcomeMessage = await this.authService.registerUser(formData);
        this.handleRegistrationSuccess(welcomeMessage);
        this.router.navigate(['/login']);
      } catch (error) {
        this.handleRegistrationError(error);
      }
    }
  }

  private handleRegistrationSuccess(welcomeMessage: string) {
    this.openSnackBar(welcomeMessage, 'Registration Successful', 4000);
    this.router.navigate(['/login']);
  }

  private handleRegistrationError(error: any) {
    if (error.status === 400 && error.error) {
      if (error.error && typeof error.error === 'object') {
        const errorKeys = Object.keys(error.error);
        const errorMessages = errorKeys.map((key) => error.error[key].join(', '));
        this.openSnackBar(errorMessages.join('\n'), 'Error', 3000);
      } else {
        this.openSnackBar(
          'Registration failed. Please check your input.',
          'Error',
          3000
        );
      }
    } else {
      this.openSnackBar(
        'An error occurred. Please try again.',
        'Error',
        3000
      );
    }
  }

  /**
   * Displays a success toast message using MatSnackBar.
   * @param message - The message to be displayed.
   */
  showSuccessToast(message: string) {
    this.snackBar.open(message, 'Close', {
      duration: 3000
    });
  }

  /**
   * Displays a snack bar with a specified message and action.
   * @param message - The message to be displayed.
   * @param action - The action button text.
   * @param duration - The duration for which the snack bar is displayed.
   */
  private openSnackBar(message: string, action: string, duration: number) {
    this.snackBar.open(message, action, {
      duration,
      verticalPosition: 'top',
    });
  }
}
