import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LiaisonAstronomerModalComponent } from './liaison-astronomer-modal.component';

describe('LiaisonAstronomerModalComponent', () => {
  let component: LiaisonAstronomerModalComponent;
  let fixture: ComponentFixture<LiaisonAstronomerModalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ LiaisonAstronomerModalComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(LiaisonAstronomerModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
