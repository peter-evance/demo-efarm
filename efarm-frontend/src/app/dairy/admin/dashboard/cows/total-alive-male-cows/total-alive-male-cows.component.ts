import { Component } from '@angular/core';
import { CowService } from 'src/services/dairy/cow.service';

@Component({
  selector: 'total-alive-male-cows',
  templateUrl: './total-alive-male-cows.component.html',
  styleUrls: ['./total-alive-male-cows.component.css']
})
export class TotalAliveMaleCowsComponent {

  totalAliveMaleCows!: number;

  constructor(private cowService: CowService) {}

  ngOnInit() {
    this.cowService.getAliveMaleCows().subscribe(response => {
      this.totalAliveMaleCows = response.total_alive_male_cows;
    });
  }


}
