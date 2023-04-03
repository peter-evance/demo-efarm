import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';

@Component({
  selector: 'dairy-home',
  templateUrl: './dairy-home.component.html',
  styleUrls: ['./dairy-home.component.css']
})
export class DairyHomeComponent {
  gifUrl: string = 'https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOGI3NTBhZTQzNzA3MTRhNmZkNDc2OGNkOThlYzg5YmM2ZjBhNTUwOSZjdD1n/XncE2zmvthjyg/giphy.gif';

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
  }
}
