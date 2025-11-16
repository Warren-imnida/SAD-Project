import { Component } from '@angular/core';
import { Router} from "@angular/router";

@Component({
  selector: 'app-first-page',
  standalone: true,
  imports: [],
  templateUrl: './first-page.html',
  styleUrl: './first-page.css',
})
export class FirstPage {
  constructor(private router: Router) {}

  goToDashboard() {
    this.router.navigate(['/dashboard']);
  }
}
