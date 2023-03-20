import { Component } from '@angular/core';
import { LactationService } from 'src/services/dairy/lactation.service';

@Component({
  selector: 'total-lactating-cows',
  templateUrl: './total-lactating-cows.component.html',
  styleUrls: ['./total-lactating-cows.component.css']
})
export class TotalLactatingCowsComponent {
  totalLactatingCows!: number;

  constructor(private lactationService: LactationService ) {}

  ngOnInit() {
    this.lactationService.getLactatingCows().subscribe(response => {
      this.totalLactatingCows = response.lactating_cows_count;
    });
  }

}
