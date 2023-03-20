import { Component } from '@angular/core';
import { PregnancyService } from 'src/services/dairy/pregnancy.service';
import { CowService } from 'src/services/dairy/cow.service';
import { Cow, Pregnancy } from 'src/models/dairy/models';
import { Router } from '@angular/router';

@Component({
  selector: 'dairy-pregnancy-create',
  templateUrl: './dairy-pregnancy-create.component.html',
  styleUrls: ['./dairy-pregnancy-create.component.css']
})
export class DairyPregnancyCreateComponent {
  pregnancy: Pregnancy = new Pregnancy();
  cows: Cow[] = [];

  constructor(
    private pregnancyService: PregnancyService, 
    private cowService: CowService,
    private router: Router) {}

  ngOnInit(): void {
    // Fetch list of cows from the server using the CowService
    this.cowService.getCows().subscribe((cows: Cow[]) => {
      this.cows = cows;
    });
  }

  createPregnancy(): void {
    if (!this.pregnancy.cow) {
      alert('Please select a cow');
      return;}
    
    this.pregnancyService.createPregnancy(this.pregnancy).subscribe(() => {
      alert('Pregnancy created successfully!');
      this.router.navigate(['/dairy/pregnancies']);
    });
  }
  
}
