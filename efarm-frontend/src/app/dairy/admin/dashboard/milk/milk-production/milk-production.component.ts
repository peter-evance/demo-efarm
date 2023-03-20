import { Component } from '@angular/core';
import { MilkService } from 'src/services/dairy/milk.services';

@Component({
  selector: 'total-daily-milk-production',
  templateUrl: './milk-production.component.html',
  styleUrls: ['./milk-production.component.css']
})
export class MilkProductionComponent {
  totalMilkToday!: number;
  totalMilkYesterday!: number;
  percentageDiff!: number;
  

  constructor(private milkService: MilkService) { }

  ngOnInit() {
    this.milkService.getTotalMilkToday().subscribe(response => {
      this.totalMilkToday = response.total_milk_today;
      this.totalMilkYesterday = response.total_milk_yesterday;
      this.percentageDiff = response.percentage_difference;
    });
  }

}
