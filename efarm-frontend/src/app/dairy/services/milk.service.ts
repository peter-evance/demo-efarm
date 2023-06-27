import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class MilkService {

  private apiUrl1 = 'http://127.0.0.1:8000/dairy/milk/';
  private apiUrl2 = 'http://127.0.0.1:8000/dairy/';

  constructor(private http: HttpClient) { }

  // Get milk by ID, or all milk record if no ID is provided
  getMilk(id?: number): Observable<any> {
  const url = id ? `${this.apiUrl1}${id}/` : this.apiUrl1;
  return this.http.get(url);
}

  // Add new milk record
  createMilk(data: any): Observable<any> {
    return this.http.post(this.apiUrl1, data);
  }

  // Update an existing milk record
  updateMilk(id: any, data: any): Observable<any> {
    const url = `${this.apiUrl1}${id}/`;
    return this.http.put(url, data);
  }

  // Delete an existing milk record
  deleteMilk(id: any): Observable<any> {
    const url = `${this.apiUrl1}${id}/`;
    return this.http.delete(url);
  }

  // Retrieve the total milk production per day
  getTotalMilkToday(): Observable<{ total_milk_today: number, total_milk_yesterday:number, 
    percentage_difference:number }> {
    const url = `${this.apiUrl2}admin/dashboard/daily-milk-production`;
    return this.http.get<{ total_milk_today: number,  total_milk_yesterday:number, 
      percentage_difference:number }>(url);
  }

  // Retrieve the total number of milked cows per day
  getMilkedCowsToday(): Observable<{ cows_milked_today: number }> {
    const url = `${this.apiUrl2}admin/dashboard/milked-cows`;
    return this.http.get<{ cows_milked_today: number }>(url);
  }

  getWeeklyMilkChartData(): Observable<any> {
    const url = `${this.apiUrl2}admin/dashboard/weekly-milk-chart-data`;
    return this.http.get<any>(url);
  }
}
