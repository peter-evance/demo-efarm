import { Component } from '@angular/core';
import { CowService } from 'src/app/dairy/services/cow.service';

@Component({
  selector: 'total-pregnant-cows',
  templateUrl: './total-pregnant-cows.component.html',
  styleUrls: ['./total-pregnant-cows.component.css']
})
export class TotalPregnantCowsComponent {

  totalPregnantCows!: number;

  constructor(private cowService: CowService) {}

  ngOnInit() {
    this.cowService.getPregnantCows().subscribe(response => {
      this.totalPregnantCows = response.pregnancies_count;
    });
  }

}
