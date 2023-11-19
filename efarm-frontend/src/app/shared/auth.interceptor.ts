import { Injectable } from '@angular/core';
import { HttpRequest, HttpHandler, HttpEvent, HttpInterceptor } from '@angular/common/http';
import { Observable } from 'rxjs';

/**
 * Interceptor to add the authorization token to outgoing HTTP requests.
 */
@Injectable({ providedIn: 'root' })
export class AuthInterceptor implements HttpInterceptor {

  /**
   * Intercept the HTTP request and add the authorization token if available in local storage.
   * @param request - The original HTTP request.
   * @param next - The next HTTP handler in the chain.
   * @returns An observable of the HTTP event.
   */
  intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    const token = localStorage.getItem('Token');

    if (token) {
      // Clone the request and add the Authorization header with the token
      request = request.clone({
        setHeaders: {
          Authorization: 'Token ' + token
        }
      });
    }
    
    return next.handle(request);
  }
}
