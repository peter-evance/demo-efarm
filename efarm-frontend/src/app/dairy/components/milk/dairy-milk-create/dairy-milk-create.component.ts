import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { Milk, Cow } from 'src/app/dairy/interfaces/interfaces';
import { CowService } from 'src/app/dairy/services/cow.service';
import { MilkService } from 'src/app/dairy/services/milk.services';

@Component({
  selector: 'app-dairy-milk-create',
  templateUrl: './dairy-milk-create.component.html',
  styleUrls: ['./dairy-milk-create.component.css']
})
export class DairyMilkCreateComponent {
  newMilk: Milk = new Milk();
  cows: Cow[] = [];

  constructor(
    private milkService: MilkService, 
    private cowService: CowService,
    private router: Router) {
    }


  ngOnInit(): void {
      this.cowService.getCows().subscribe((cows: Cow[]) => {
        this.cows = cows;
      });
    }
  
  onSubmit() {
    if (!this.newMilk.cow) {
      alert('Please select a cow');
      return;
    }
      this.milkService.createMilk(this.newMilk)
        .subscribe(() => {
          this.router.navigate(['/dairy/milk']);
    
        });
    };
  }