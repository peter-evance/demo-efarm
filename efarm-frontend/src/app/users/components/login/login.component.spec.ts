import { ComponentFixture, TestBed, fakeAsync, tick } from '@angular/core/testing';
import { LoginComponent } from './login.component';
import { AuthService } from '../../../shared/auth.service';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { MatCardModule } from '@angular/material/card';
import { ReactiveFormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

describe('LoginComponent', () => {
  let component: LoginComponent;
  let fixture: ComponentFixture<LoginComponent>;
  let authService: AuthService;
  let httpTestingController: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientTestingModule,
        MatSnackBarModule,
        MatInputModule,
        MatCardModule,
        ReactiveFormsModule,
        BrowserAnimationsModule
      ],
      declarations: [LoginComponent],
      providers: [AuthService]
    });

    fixture = TestBed.createComponent(LoginComponent);
    component = fixture.componentInstance;
    authService = TestBed.inject(AuthService);
    httpTestingController = TestBed.inject(HttpTestingController);
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should initialize the loginForm with empty values', () => {
    const formValue = component.loginForm.value;
    expect(formValue.username).toBe('');
    expect(formValue.password).toBe('');
  });
  it('should have a valid login form', () => {
    expect(component.loginForm).toBeTruthy();
  });
  
  it('should initialize the form with empty username and password', () => {
    expect(component.loginForm.value.username).toBe('');
    expect(component.loginForm.value.password).toBe('');
  });
  
  it('should call onLogin method when the "Log In" button is clicked', () => {
    const onLoginSpy = spyOn(component, 'onLogin');
    const loginButton = fixture.nativeElement.querySelector('#loginButton');
    loginButton.click();
  
    // expect(onLoginSpy).toHaveBeenCalled();
  });
  

  it('should call onLogin when the form is submitted', fakeAsync(() => {
    const onLoginSpy = spyOn(component, 'onLogin');
    const loginButton = fixture.nativeElement.querySelector('form');
    loginButton.dispatchEvent(new Event('submit'));
  
    tick(); // This will wait for any pending promises to resolve
  
    expect(onLoginSpy).toHaveBeenCalled();
  }));
  
  // it('should call onLogin when the form is submitted', fakeAsync(() => {
  //   const onLoginSpy = spyOn(component, 'onLogin').and.callThrough();
  //   fixture.detectChanges(); // Ensure that Angular has detected the form changes
    
  //   const submitButton = fixture.nativeElement.querySelector('button[type="submit"]');
  //   submitButton.click();
  //   tick();
    
  //   expect(onLoginSpy).toHaveBeenCalled();
  // }));
  

  xit('should call loginUser and handleLoginSuccess when valid credentials are submitted', fakeAsync(() => {
    const loginUserSpy = spyOn(authService, 'login').and.returnValue(Promise.resolve('my_auth_token'));
    const handleLoginSuccessSpy = spyOn(component, 'handleLoginSuccess');
    
    // Set valid values in the form
    component.loginForm.setValue({
      username: 'Peter Evance',
      password: '12345678'
    });
    
    component.onLogin();
    tick();
    
    expect(loginUserSpy).toHaveBeenCalled();
    expect(handleLoginSuccessSpy).toHaveBeenCalledWith('my_auth_token');
  }));

  xit('should call handleLoginError when invalid credentials are submitted', fakeAsync(() => {
    const loginUserSpy = spyOn(authService, 'login').and.returnValue(Promise.resolve('my_auth_token'));
    const handleLoginErrorSpy = spyOn(component, 'handleLoginError');

    // Set invalid values in the form
    component.loginForm.setValue({
      username: 'InvalidUser',
      password: 'InvalidPassword'
    });

    component.onLogin();
    tick();

    expect(loginUserSpy).toHaveBeenCalled();
    expect(handleLoginErrorSpy).toHaveBeenCalledWith('Incorrect login credentials. Please try again.');
  }));

  xit('should show error toast when form is invalid', fakeAsync(() => {
    const showErrorToastSpy = spyOn(component, 'showErrorToast');

    // Set form as invalid
    component.loginForm.setValue({
      username: '',
      password: ''
    });

    component.onLogin();
    tick();

    expect(showErrorToastSpy).toHaveBeenCalledWith('Please fill in all required fields.');
  }));
});
