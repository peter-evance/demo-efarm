import { Component } from '@angular/core';
import { Milk } from 'src/app/dairy/interfaces/interfaces';
import { MilkService } from 'src/app/dairy/services/milk.services';

@Component({
  selector: 'dairy-milk-list',
  templateUrl: './dairy-milk-list.component.html',
  styleUrls: ['./dairy-milk-list.component.css']
})
export class DairyMilkListComponent {

  milks: Milk[] = [];

  constructor(private milkService: MilkService) {}

  ngOnInit(): void {
    this.milkService.getMilk().subscribe((milks) => {
      this.milks = milks;
    });

};
}
