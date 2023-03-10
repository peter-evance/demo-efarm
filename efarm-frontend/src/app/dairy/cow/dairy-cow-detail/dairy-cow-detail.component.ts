import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Cow } from 'src/models/dairy/models';
import { CowService } from 'src/services/dairy/cow.service';

@Component({
  selector: 'dairy-cow-detail',
  templateUrl: './dairy-cow-detail.component.html',
  styleUrls: ['./dairy-cow-detail.component.css']
})
export class DairyCowDetailComponent implements OnInit {

  cow!: Cow;

  constructor(private route: ActivatedRoute, private cowService: CowService, private router: Router) { }

  ngOnInit() {
    const id = this.route.snapshot.paramMap?.get('id');
    if (id) {
      this.cowService.getCows(Number(id)).subscribe(cow => this.cow = cow);
    }
  }

  onDelete(): void {
    if (confirm('Are you sure you want to delete this cow?')) {
      this.cowService.deleteCow(this.cow.id).subscribe(() => {
        this.router.navigate(['/dairy/cows']);
      });
    }
  }
}
