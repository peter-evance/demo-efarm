import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Milk } from 'src/app/dairy/interfaces/interfaces';
import { MilkService } from 'src/app/dairy/services/milk.services';

@Component({
  selector: 'dairy-milk-detail',
  templateUrl: './dairy-milk-detail.component.html',
  styleUrls: ['./dairy-milk-detail.component.css']
})
export class DairyMilkDetailComponent {

  milk!: Milk;

  constructor(private route: ActivatedRoute, private milkService: MilkService, private router: Router) { }

  ngOnInit() {
    const id = this.route.snapshot.paramMap?.get('id');
    if (id) {
      this.milkService.getMilk(Number(id)).subscribe(milk => this.milk = milk);
    }
  }

  onDelete(): void {
    if (confirm('Are you sure you want to delete this milk record?')) {
      this.milkService.deleteMilk(this.milk.id).subscribe(() => {
        this.router.navigate(['/dairy/milk']);
      });
    }
  }

}
