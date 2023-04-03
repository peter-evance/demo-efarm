import { Component, OnInit } from '@angular/core';
import { CowService } from 'src/app/dairy/services/cow.service';

@Component({
  selector: 'dairy-cow-list',
  templateUrl: './dairy-cow-list.component.html',
  styleUrls: ['./dairy-cow-list.component.css']
})
export class DairyCowListComponent implements OnInit {
  cows: any[] = [];

  constructor(private cowService: CowService) { }

  ngOnInit(): void {
    this.cowService.getCows()
      .subscribe((data: any[]) => {
        this.cows = data;
      });
  }
}








