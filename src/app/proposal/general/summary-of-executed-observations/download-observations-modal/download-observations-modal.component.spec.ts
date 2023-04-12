import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DownloadObservationsModalComponent } from './download-observations-modal.component';

describe('DownloadObservationsModalComponent', () => {
  let component: DownloadObservationsModalComponent;
  let fixture: ComponentFixture<DownloadObservationsModalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DownloadObservationsModalComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DownloadObservationsModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
