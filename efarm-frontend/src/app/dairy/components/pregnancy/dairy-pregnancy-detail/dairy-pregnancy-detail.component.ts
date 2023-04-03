import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { PregnancyService } from 'src/app/dairy/services/pregnancy.service';
import { Pregnancy } from 'src/app/dairy/interfaces/interfaces';

@Component({
  selector: 'dairy-pregnancy-detail',
  templateUrl: './dairy-pregnancy-detail.component.html',
  styleUrls: ['./dairy-pregnancy-detail.component.css']
})
export class DairyPregnancyDetailComponent implements OnInit {
  pregnancy!: Pregnancy;

  constructor(private route: ActivatedRoute, private PregnancyService: PregnancyService, private router: Router) { }

  ngOnInit() {
    const id = this.route.snapshot.paramMap?.get('id');
    if (id) {
      this.PregnancyService.getPregnancies(Number(id)).subscribe(pregnancy => this.pregnancy = pregnancy);
      console.log(this.pregnancy);
    }
  }

  onDelete(): void {
    if (confirm('Are you sure you want to delete this pregnancy record?')) {
      this.PregnancyService.deletePregnancy(this.pregnancy.id).subscribe(() => {
        this.router.navigate(['/dairy/pregancies']);
      });
    }
  }
}