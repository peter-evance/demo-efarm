import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router  } from '@angular/router';
import { Cow, Milk } from 'src/models/dairy/models';
import { MilkService } from 'src/services/dairy/milk.services';
import { CowService } from 'src/services/dairy/cow.service';

@Component({
  selector: 'dairy-milk-update',
  templateUrl: './dairy-milk-update.component.html',
  styleUrls: ['./dairy-milk-update.component.css']
})
export class DairyMilkUpdateComponent implements OnInit {
  milk: Milk = new Milk();
  cows: Cow[] = [];

  constructor(
    private milkService: MilkService,
    private cowService: CowService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    this.getMilk(Number(id));
    this.cowService.getCows().subscribe((cows) => {
      this.cows = cows;
    });
  }

  getMilk(id: number): void {
    this.milkService.getMilk(id).subscribe((milk) => {
      this.milk = milk;
    });
  }

  updateMilk(): void {
    this.milkService.updateMilk(this.milk.id, this.milk).subscribe(() => {
      alert('Milk updated successfully');
      this.router.navigate(['/dairy/milk']);
    });
  }

  onSubmit(): void {
    this.updateMilk();
  }
}
