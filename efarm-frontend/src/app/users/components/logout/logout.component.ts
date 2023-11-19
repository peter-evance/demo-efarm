import { Component, inject } from '@angular/core';
import { AuthService } from '../../../shared/auth.service';
import { MatSnackBar } from '@angular/material/snack-bar';

/**
 * Component responsible for handling user logout.
 */
@Component({
  selector: 'logout',
  templateUrl: './logout.component.html',
  styleUrls: ['./logout.component.css']
})
export class LogoutComponent {

  private authService = inject(AuthService);
  private snackBar = inject(MatSnackBar);

  /**
   * Initiates the logout process and displays a success or error message.
   */
  async onLogout() {
    try {
      this.authService.logout();
      this.showSuccessToast('You have been logged out successfully');
    } catch (error) {
      this.showErrorToast('Logout failed. Please try again.');
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
   * Displays an error toast message using MatSnackBar.
   * @param message - The error message to be displayed.
   */
  showErrorToast(message: string) {
    this.snackBar.open(message, 'Close', {
      duration: 3000
    });
  }
}
