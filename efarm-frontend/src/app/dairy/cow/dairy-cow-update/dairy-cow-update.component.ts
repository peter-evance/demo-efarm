import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Cow } from 'src/models/dairy/models';
import { CowService } from 'src/services/dairy/cow.service';

@Component({
  selector: 'dairy-cow-update',
  templateUrl: './dairy-cow-update.component.html',
  styleUrls: ['./dairy-cow-update.component.css']
})

export class DairyCowUpdateComponent implements OnInit {
  cowId!: number;
  cow: Cow = new Cow();
  breeds: string[] = [
    'Friesian',
    'Jersey',
    'Guernsey',
    'Ayrshire',
  ];

  constructor(private route: ActivatedRoute, private cowService: CowService,private router: Router) {
    const cowIdParam = this.route.snapshot.paramMap.get('id');
    if (cowIdParam !== null) {
      this.cowId = parseInt(cowIdParam, 10);
    }
  }
  

  ngOnInit() {
    this.cowService.getCows(this.cowId).subscribe((cow) => {
      this.cow = cow;
    });
  }

  onSubmit(): void {
    if (this.cow) {
      this.cowService.updateCow(this.cow.id, this.cow).subscribe(() => {
        this.router.navigate(['/dairy/cows']);
      });
    }
  }
}
