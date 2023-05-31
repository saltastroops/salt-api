import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SaFormComponent } from './sa-form.component';

describe('SaFormComponent', () => {
  let component: SaFormComponent;
  let fixture: ComponentFixture<SaFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SaFormComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SaFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
