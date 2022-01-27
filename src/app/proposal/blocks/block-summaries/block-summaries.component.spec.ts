import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BlockSummariesComponent } from './block-summaries.component';
import { BlockSummary } from '../../../types/block';

describe('BlockSummaryComponent', () => {
  const blocks: BlockSummary[] = [
    {
      id: 123,
      semester: '2020-2',
      name: 'A',
      status: {
        value: 'Completed',
        reason: null,
      },
      observationTime: 1380,
      priority: 1,
      requestedObservations: 5,
      acceptedObservations: 5,
      isObservableTonight: false,
      remainingNights: 0,
      observingConditions: {
        minimumSeeing: 1,
        maximumSeeing: 5,
        transparency: 'Clear',
        maximumLunarPhase: 100,
        minimumLunarDistance: 10,
      },
      instruments: [
        {
          name: 'RSS',
          modes: ['Spectroscopy'],
          gratings: ['pg0900'],
          filters: ['pc03850'],
        },
      ],
    },
    {
      id: 100,
      semester: '2009-2',
      name: 'A',
      status: {
        value: 'On hold',
        reason:
          'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Atque dolores laborum veritatis.',
      },
      observationTime: 1380,
      priority: 1,
      requestedObservations: 5,
      acceptedObservations: 1,
      isObservableTonight: false,
      remainingNights: 0,
      observingConditions: {
        minimumSeeing: 1,
        maximumSeeing: 5,
        transparency: 'Clear',
        maximumLunarPhase: 100,
        minimumLunarDistance: 10,
      },
      instruments: [
        {
          name: 'RSS',
          modes: ['Spectropolarimetry'],
          gratings: ['pg2300'],
          filters: ['pc03850'],
        },
      ],
    },
  ];

  let component: BlockSummariesComponent;
  let fixture: ComponentFixture<BlockSummariesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [BlockSummariesComponent],
    }).compileComponents();
    fixture = TestBed.createComponent(BlockSummariesComponent);
    component = fixture.componentInstance;
    component.blocks = blocks;
    fixture.detectChanges();
  });

  it('should create', async () => {
    expect(component).toBeTruthy();
  });
});
