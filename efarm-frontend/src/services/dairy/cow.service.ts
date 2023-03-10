import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CowService {

  private apiUrl = 'http://127.0.0.1:8000/dairy/cows/';

  constructor(private http: HttpClient) { }

  // Get cow by ID, or all cows if no ID is provided
  getCows(id?: number): Observable<any> {
  const url = id ? `${this.apiUrl}${id}/` : this.apiUrl;
  return this.http.get(url);
}

  // Create a new cow
  createCow(data: any): Observable<any> {
    return this.http.post(this.apiUrl, data);
  }

  // Update an existing cow
  updateCow(id: number, data: any): Observable<any> {
    const url = `${this.apiUrl}${id}/`;
    return this.http.put(url, data);
  }

  // Delete an existing cow
  deleteCow(id: any): Observable<any> {
    const url = `${this.apiUrl}${id}/`;
    return this.http.delete(url);
  }

}
