import { TestBed, fakeAsync, tick } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';

import { AuthService } from './auth.service';
import { LoginData } from '../users/users.interfaces';

describe('AuthService', () => {
  let service: AuthService;
  let httpTestingController: HttpTestingController;

  beforeEach(() => {
    localStorage.removeItem('authToken');
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [AuthService]
    });
    service = TestBed.inject(AuthService);
    httpTestingController = TestBed.inject(HttpTestingController);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should login successfully with valid credentials', fakeAsync(() => {
    const loginData: LoginData = {
      username: 'Peter Evance',
      password: '12345678',
    };
  
    let authToken: string | undefined;
    
    service.login(loginData).then((token) => {
      authToken = token;
      expect(authToken).toBe('my_auth_token');
    });
  
    const req = httpTestingController.expectOne('http://localhost:8000/auth/login/');
    expect(req.request.method).toBe('POST');
    req.flush({ auth_token: 'my_auth_token' });
  
    tick();
  
    // Outside the callback, authToken is still accessible for further assertions
    expect(authToken).toBe('my_auth_token');
    expect(localStorage.getItem('authToken')).toBeDefined();
  }));
  

  it('should handle login failure with invalid credentials', fakeAsync(() => {
    const loginData: LoginData = {
      // Provide invalid login data here
      username: 'InvalidUser',
      password: 'InvalidPassword',
    };
  
    let errorResponse: string | undefined;
  
    service.login(loginData).catch((error) => {
      errorResponse = error;
    });
  
    const req = httpTestingController.expectOne('http://localhost:8000/auth/login/');
    expect(req.request.method).toBe('POST');
  
    // Simulate an error response with a 400 status and your specific error message
    req.flush({ non_field_errors: ['Unable to log in with provided credentials'] }, { status: 400, statusText: 'Bad Request' }
 );
  
    tick();
  
    expect(errorResponse).toBe('An error occurred during login. Please try again.');
  }));

  it('should logout successfully and remove the token from local storage', fakeAsync(() => {
    // Simulate that a user is logged in by setting the token in local storage
    localStorage.setItem('authToken', 'my_auth_token');

    let logoutSuccess: boolean = false;

    service.logout().then(() => {
      logoutSuccess = true;
    });

    const req = httpTestingController.expectOne('http://localhost:8000/auth/logout/');
    expect(req.request.method).toBe('POST');
    req.flush({ status: 204, statusText: 'No Content' });

    tick();

    expect(logoutSuccess).toBeTrue();
    expect(localStorage.getItem('authToken')).toBeNull(); // Ensure token is removed from local storage
  }));

  it('should handle logout failure', fakeAsync(() => {
    // Simulate that a user is logged in by setting the token in local storage
    localStorage.setItem('authToken', 'my_auth_token');

    let errorResponse: string | undefined;

    service.logout().catch((error) => {
      errorResponse = error;
    });

    const req = httpTestingController.expectOne('http://localhost:8000/auth/logout/');
    expect(req.request.method).toBe('POST');

    // Simulate an error response with a 401 status and your specific error message
    req.flush({ error: 'Unauthorized' }, { status: 401, statusText: 'Unauthorized'});

    tick();

    expect(errorResponse).toBe('An error occurred during logout. Please try again.');
    expect(localStorage.getItem('authToken')).toBe('my_auth_token'); // Ensure token is not removed from local storage
  }));

  it('should verify a valid token', fakeAsync(() => {
    // Simulate that a user is logged in by setting the token in local storage
    localStorage.setItem('authToken', 'my_auth_token');

    let verificationResult: boolean | undefined;

    service.verifyToken().then((result) => {
      verificationResult = result;
    });

    const req = httpTestingController.expectOne('http://127.0.0.1:8000/auth/users/me/');
    expect(req.request.method).toBe('GET');

    // Simulate a successful token verification response
    req.flush({}, { status: 200, statusText: 'OK' });

    tick();

    expect(verificationResult).toBeTrue();
  }));
  it('should handle token verification failure', fakeAsync(() => {
    // Simulate that a user is logged in by setting the token in local storage
    localStorage.setItem('authToken', 'my_auth_token');

    let verificationResult: boolean | undefined;

    service.verifyToken().then((result) => {
      verificationResult = result;
    });

    const req = httpTestingController.expectOne('http://127.0.0.1:8000/auth/users/me/');
    expect(req.request.method).toBe('GET');

    // Simulate a token verification failure response (e.g., unauthorized)
    req.flush({ detail: 'Invalid Token' }, { status: 401, statusText: 'Unauthorized' });

    tick();

    expect(verificationResult).toBeFalse();
  }));
  it('should handle token verification when no token exists', fakeAsync(() => {
    let verificationResult: boolean | undefined;

    service.verifyToken().then((result) => {
      verificationResult = result;
    });

    tick();

    expect(verificationResult).toBeFalse();
  }));
  
  
  
  afterEach(() => {
    httpTestingController.verify();
  });
});
