import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BvitComponent } from './bvit.component';

describe('BvitTablesComponent', () => {
  let component: BvitComponent;
  let fixture: ComponentFixture<BvitComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ BvitComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(BvitComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
