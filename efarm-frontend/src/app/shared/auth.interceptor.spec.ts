import { TestBed } from '@angular/core/testing';
import { HTTP_INTERCEPTORS, HttpClient, HttpHeaders, HttpClientModule } from '@angular/common/http';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { AuthInterceptor } from './auth.interceptor';

describe('AuthInterceptor', () => {
  let interceptor: AuthInterceptor;
  let httpTestingController: HttpTestingController;
  let httpClient: HttpClient;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [
        AuthInterceptor,
        {
          provide: HTTP_INTERCEPTORS,
          useClass: AuthInterceptor,
          multi: true,
        },
      ],
    });

    interceptor = TestBed.inject(AuthInterceptor);
    httpTestingController = TestBed.inject(HttpTestingController);
    httpClient = TestBed.inject(HttpClient);
  });
  

  it('should be created', () => {
    expect(interceptor).toBeTruthy();
  });

  it('should set the Authorization header with the auth token', () => {
    // Set the auth token in localStorage
    localStorage.setItem('authToken', 'my_auth_token');

    // Make a test HTTP request
    httpClient.get('http://127.0.0.1:8000/auth/users/').subscribe();

    // Expect the request to have the Authorization header
    const req = httpTestingController.expectOne('http://127.0.0.1:8000/auth/users/');
    expect(req.request.headers.has('Authorization')).toBeTrue();
    expect(req.request.headers.get('Authorization')).toBe('Token my_auth_token');

    httpTestingController.verify();
  });

  it('should not set the Authorization header when no auth token', () => {
    // Clear any existing auth token
    localStorage.removeItem('authToken');

    // Make a test HTTP request
    httpClient.get('http://127.0.0.1:8000/auth/users/').subscribe();

    // Expect the request not to have the Authorization header
    const req = httpTestingController.expectOne('http://127.0.0.1:8000/auth/users/');
    expect(req.request.headers.has('Authorization')).toBeFalse();

    httpTestingController.verify();
  });
});
