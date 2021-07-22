import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UsedInTableComponent } from './used-in-table.component';

describe('UseInTableComponent', () => {
  let component: UsedInTableComponent;
  let fixture: ComponentFixture<UsedInTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ UsedInTableComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(UsedInTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
