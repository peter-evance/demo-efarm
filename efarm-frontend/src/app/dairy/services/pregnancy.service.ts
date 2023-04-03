import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PregnancyService {
  
  private apiUrl = 'http://127.0.0.1:8000/dairy/pregnancies/';

  constructor(private http: HttpClient) { }

  // Get pregnancy by ID, or all pregnancies if no ID is provided
  getPregnancies(id?: number): Observable<any> {
    const url = id ? `${this.apiUrl}${id}/` : this.apiUrl;
    return this.http.get(url);
  }

  // Create a new pregnancy
  createPregnancy(data: any): Observable<any> {
    return this.http.post(this.apiUrl, data);
  }

  // Update an existing pregnancy
  updatePregnancy(id: any, data: any): Observable<any> {
    const url = `${this.apiUrl}${id}/`;
    return this.http.put(url, data);
  }

  // Delete an existing pregnancy
  deletePregnancy(id: any): Observable<any> {
    const url = `${this.apiUrl}${id}/`;
    return this.http.delete(url);
  }

  // Get pregnancies by cow ID
  getPregnanciesByCowId(cowId: number): Observable<any> {
    const url = `${this.apiUrl}?cow=${cowId}`;
    return this.http.get(url);
  }

  // Get pregnancies by due date range
  getPregnanciesByDueDateRange(startDate: string, endDate: string): Observable<any> {
    const url = `${this.apiUrl}?due_date__gte=${startDate}&due_date__lte=${endDate}`;
    return this.http.get(url);
  }
}
