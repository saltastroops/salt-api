import { Component, OnInit } from '@angular/core';
import { AuthenticationService } from '../service/authentication.service';
import { Observable } from 'rxjs';
import { User } from '../types/user';

@Component({
  selector: 'wm-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
export class HomeComponent implements OnInit {
  user$!: Observable<User | null>;
  constructor(private authService: AuthenticationService) {}

  ngOnInit() {
    console.log(Object.keys(this.authService));
    this.user$ = this.authService.user();
  }
}
