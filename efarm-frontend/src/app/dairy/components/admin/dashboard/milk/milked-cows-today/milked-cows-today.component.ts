import { Component } from '@angular/core';
import { MilkService } from 'src/app/dairy/services/milk.services';

@Component({
  selector: 'milked-cows-today',
  templateUrl: './milked-cows-today.component.html',
  styleUrls: ['./milked-cows-today.component.css']
})
export class MilkedCowsTodayComponent {
  totalCows!: number;

  constructor(private milkService: MilkService) { }

  ngOnInit() {
    this.milkService.getMilkedCowsToday().subscribe(response => {
      this.totalCows = response.cows_milked_today;
    });
  }


}
