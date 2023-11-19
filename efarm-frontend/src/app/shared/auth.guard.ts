import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from './auth.service';
import { inject } from '@angular/core';

/**
 * Guard to prevent access to the registration page for authenticated users.
 * Redirects to the logout page if the user is authenticated.
 */
export const registrationGuard: CanActivateFn = async () => {
  const authService = inject(AuthService);
  const router = inject(Router);

  const isUserAuthenticated = await authService.verifyToken();

  if (isUserAuthenticated) {
    router.navigate(['/logout']);
    return false;
  } else {
    return true;
  }
};

/**
 * Guard to prevent access to the login page for authenticated users.
 * Redirects to the logout page if the user is authenticated.
 */
export const loginGuard: CanActivateFn = async () => {
  const authService = inject(AuthService);
  const router = inject(Router);

  const isUserAuthenticated = await authService.verifyToken();

  if (isUserAuthenticated) {
    router.navigate(['/logout']);
    return false;
  } else {
    return true;
  }
};

/**
 * Guard to ensure access to the logout page only for authenticated users.
 * Redirects to the login page if the user is not authenticated.
 */
export const logOutGuard: CanActivateFn = async () => {
  const authService = inject(AuthService);
  const router = inject(Router);

  const isUserAuthenticated = await authService.verifyToken();

  if (isUserAuthenticated) {
    return true;
  } else {
    router.navigate(['/login']);
    return false;
  }
};

/**
 * Guard to ensure access to pages only for farm owners.
 * Redirects to the logout page if the user is not a farm owner.
 */
export const farmOwnerGuard: CanActivateFn = async () => {
  const authService = inject(AuthService);
  const router = inject(Router);

  const isUserAuthenticated = await authService.verifyToken();

  if (isUserAuthenticated && authService.isFarmOwner()) {
    return true;
  } else {
    router.navigate(['/logout']);
    return false;
  }
};

/**
 * Guard to ensure access to pages only for farm managers.
 * Redirects to the logout page if the user is not a farm manager.
 */
export const farmManagerGuard: CanActivateFn = async () => {
  const authService = inject(AuthService);
  const router = inject(Router);

  const isUserAuthenticated = await authService.verifyToken();

  if (isUserAuthenticated && authService.isFarmManager()) {
    return true;
  } else {
    router.navigate(['/logout']);
    return false;
  }
};

/**
 * Guard to ensure access to pages only for assistant farm managers.
 * Redirects to the logout page if the user is not an assistant farm manager.
 */
export const assistantFarmManagerGuard: CanActivateFn = async () => {
  const authService = inject(AuthService);
  const router = inject(Router);

  const isUserAuthenticated = await authService.verifyToken();

  if (isUserAuthenticated && authService.isAsstFarmManager()) {
    return true;
  } else {
    router.navigate(['/logout']);
    return false;
  }
};

/**
 * Guard to ensure access to pages only for farm workers.
 * Redirects to the logout page if the user is not a farm worker.
 */
export const farmWorkerGuard: CanActivateFn = async () => {
  const authService = inject(AuthService);
  const router = inject(Router);

  const isUserAuthenticated = await authService.verifyToken();

  if (isUserAuthenticated && authService.isFarmWorker()) {
    return true;
  } else {
    router.navigate(['/logout']);
    return false;
  }
};
