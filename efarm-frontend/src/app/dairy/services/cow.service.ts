import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CowService {

  private apiUrl = 'http://127.0.0.1:8000/dairy/cows/';
  private apiUrl2 = 'http://127.0.0.1:8000/dairy/';

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
  updateCow(id: any, data: any): Observable<any> {
    const url = `${this.apiUrl}${id}/`;
    return this.http.put(url, data);
  }

  // Delete an existing cow
  deleteCow(id: any): Observable<any> {
    const url = `${this.apiUrl}${id}/`;
    return this.http.delete(url);
  }

  // Retrieve the total number of alive cows in the farm
  getAliveCows(): Observable<{ total_alive_cows: number }> {
    const url = `${this.apiUrl2}admin/dashboard/total-alive-cows`;
    return this.http.get<{ total_alive_cows: number }>(url);
  }

  // Retrieve the total number of alive female cows in the farm
  getAliveFemaleCows(): Observable<{ total_alive_female_cows: number }> {
    const url = `${this.apiUrl2}admin/dashboard/total-alive-female-cows`;
    return this.http.get<{ total_alive_female_cows: number }>(url);
  }

  // Retrieve the total number of alive male cows in the farm
  getAliveMaleCows(): Observable<{ total_alive_male_cows: number }> {
    const url = `${this.apiUrl2}admin/dashboard/total-alive-male-cows`;
    return this.http.get<{ total_alive_male_cows: number }>(url);
  }

  // Retrieve the total number of pregnant cows in the farm
  getPregnantCows(): Observable<{ pregnancies_count: number }> {
    const url = `${this.apiUrl2}admin/dashboard/pregnant-cows`;
    return this.http.get<{ pregnancies_count: number }>(url);
  }




}
