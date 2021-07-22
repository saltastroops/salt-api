import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ArcBibleTableComponent } from './arc-bible-table.component';

describe('ArcBibleTableComponent', () => {
  let component: ArcBibleTableComponent;
  let fixture: ComponentFixture<ArcBibleTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ArcBibleTableComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ArcBibleTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
