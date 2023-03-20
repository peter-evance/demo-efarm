import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class LactationService {

  private apiUrl1 = 'http://127.0.0.1:8000/dairy/lactations/';
  private apiUrl2 = 'http://127.0.0.1:8000/dairy/';

  constructor(private http: HttpClient) { }

  // // Get all lactations for a given cow
  // getLactationsForCow(cowId: number): Observable<any> {
  //   const url = `${this.apiUrl1}?cow=${cowId}`;
  //   return this.http.get(url);
  // }

  // Get  lactations count
  getLactatingCows(): Observable<{lactating_cows_count:number}> {
    const url = `${this.apiUrl2}admin/dashboard/lactating-cows`;
    return this.http.get<{lactating_cows_count: number}>(url);
  }
}

