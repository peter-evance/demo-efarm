import { Component, OnInit } from '@angular/core';
import { Cow } from 'src/models/dairy/models';
import { CowService } from 'src/services/dairy/cow.service';
import { Router } from '@angular/router';

@Component({
  selector: 'dairy-cow-create',
  templateUrl: './dairy-cow-create.component.html',
  styleUrls: ['./dairy-cow-create.component.css']
})
export class DairyCowCreateComponent implements OnInit {
  newCow: Cow = new Cow();
  cows: Cow[] = [];
  breeds: string[] = [
    'Friesian',
    'Jersey',
    'Guernsey',
    'Ayrshire',
  ];


  nameTouched = false
  maleSelected: boolean = false;
  showTooltip = false
  constructor(private cowService: CowService,private router: Router,) {}

  ngOnInit() {

  }
  
  onSubmit() {
    // Make an HTTP POST request to your server with the data from the form
    this.cowService.createCow(this.newCow)
      .subscribe((createdCow) => {
        // Add the new cow to the list of cows displayed in the component
        this.cows.push(createdCow);
        this.router.navigate(['/dairy/cows']);
  
        // Reset the newCow object to clear the form
        // this.newCow = new Cow();
      });
  }
}
