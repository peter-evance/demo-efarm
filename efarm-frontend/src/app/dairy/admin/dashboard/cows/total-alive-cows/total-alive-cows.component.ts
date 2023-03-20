import { Component } from '@angular/core';
import { CowService } from 'src/services/dairy/cow.service';

@Component({
  selector: 'total-alive-cows',
  templateUrl: './total-alive-cows.component.html',
  styleUrls: ['./total-alive-cows.component.css']
})
export class TotalAliveCowsComponent {
  totalAliveCows!: number;

  constructor(private cowService: CowService) {}

  ngOnInit() {
    this.cowService.getAliveCows().subscribe(response => {
      this.totalAliveCows = response.total_alive_cows;
    });
  }
};
