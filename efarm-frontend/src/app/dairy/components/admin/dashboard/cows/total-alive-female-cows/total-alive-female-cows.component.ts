import { Component } from '@angular/core';
import { CowService } from 'src/app/dairy/services/cow.service';

@Component({
  selector: 'total-alive-female-cows',
  templateUrl: './total-alive-female-cows.component.html',
  styleUrls: ['./total-alive-female-cows.component.css']
})
export class TotalAliveFemaleCowsComponent {
  totalAliveFemaleCows!: number;

  constructor(private cowService: CowService) {}

  ngOnInit() {
    this.cowService.getAliveFemaleCows().subscribe(response => {
      this.totalAliveFemaleCows = response.total_alive_female_cows;
    });
  }

}
