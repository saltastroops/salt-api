import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { User } from '../types/user';
import { AuthenticationService } from '../service/authentication.service';

@Component({
  selector: 'wm-navigation-bar',
  templateUrl: './navigation-bar.component.html',
  styleUrls: ['./navigation-bar.component.scss'],
})
export class NavigationBarComponent implements OnInit {
  user$!: Observable<User | null>;

  constructor(private authService: AuthenticationService) {}

  ngOnInit(): void {
    this.user$ = this.authService.user();
  }

  logout() {
    this.authService.logout();
  }
}
