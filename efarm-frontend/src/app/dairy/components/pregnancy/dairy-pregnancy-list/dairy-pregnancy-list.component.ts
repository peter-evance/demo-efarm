import { Component } from '@angular/core';
import { Pregnancy } from 'src/app/dairy/interfaces/interfaces';
import { PregnancyService } from 'src/app/dairy/services/pregnancy.service';

@Component({
  selector: 'dairy-pregnancy-list',
  templateUrl: './dairy-pregnancy-list.component.html',
  styleUrls: ['./dairy-pregnancy-list.component.css']
})
export class DairyPregnancyListComponent {
  pregnancies: Pregnancy[] = [];
  loading = false;

  constructor(private pregnancyService: PregnancyService) {}

  ngOnInit(): void {
    this.loading = true;
    this.pregnancyService.getPregnancies().subscribe((pregnancies) => {
      this.pregnancies = pregnancies;
      this.loading = false;
    });

};
}

