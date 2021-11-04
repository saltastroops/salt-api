import { Component } from '@angular/core';
import { AuthenticationService } from './service/authentication.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'wm-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent {
  title = 'Web Manager';

  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthenticationService
  ) {}

  ngOnInit() {
    // Make sure that invalid tokens are removed
    if (!this.authService.isAuthenticated()) {
      this.authService.logout();
    }

    // Load the user details
    this.authService.updateUser();
  }
}
