import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InlineLoginComponent } from './inline-login.component';

describe('InlineLoginComponent', () => {
  let component: InlineLoginComponent;
  let fixture: ComponentFixture<InlineLoginComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [InlineLoginComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(InlineLoginComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
