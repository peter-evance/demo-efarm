import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { DatePipe } from '@angular/common';
import { PregnancyService } from 'src/services/dairy/pregnancy.service';
import { CowService } from 'src/services/dairy/cow.service';
import { Pregnancy, Cow } from 'src/models/dairy/models';

@Component({
  selector: 'dairy-pregnancy-update',
  templateUrl: './dairy-pregnancy-update.component.html',
  styleUrls: ['./dairy-pregnancy-update.component.css']
})
export class DairyPregnancyUpdateComponent implements OnInit {

  pregnancy: Pregnancy = new Pregnancy();
  cows: Cow[] = [];
  pregnancyStatuses: string[] = [
    'Unconfirmed',
    'Confirmed',
    'Failed',
  ];

  pregnancyOutcomes: string[] = [
    'Live',
    'Stillborn',
    'Miscarriage',
  ];
  constructor(private route: ActivatedRoute,
    // private datePipe: DatePipe, 
    private pregnancyService: PregnancyService,
    private cowService: CowService, 
    private router: Router) { }

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.pregnancyService.getPregnancies(Number(id)).subscribe(pregnancy => {
        this.pregnancy = pregnancy;
      });
      this.cowService.getCows().subscribe((cows) => {
        this.cows = cows;
      })
    }
  }

  onSubmit(): void {

    this.pregnancyService.updatePregnancy(this.pregnancy.id, this.pregnancy).subscribe(() => {
      this.router.navigate(['/dairy/pregnancies']);
    });
  }

  onCancel(): void {
    this.router.navigate(['/dairy/pregnancies']);
  }

}

