import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BlockSelectionComponent } from './block-selection.component';

describe('BlockViewNavigationComponent', () => {
  const defaultBlocks = [
    { id: 1, name: 'A' },
    { id: 2, name: 'B' },
    { id: 546, name: 'C' },
  ];

  let component: BlockSelectionComponent;
  let fixture: ComponentFixture<BlockSelectionComponent>;

  const previousButton = () =>
    fixture.nativeElement.querySelectorAll('button')[0];

  const nextButton = () => fixture.nativeElement.querySelectorAll('button')[1];

  const select = () => fixture.nativeElement.querySelector('select');

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [BlockSelectionComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(BlockSelectionComponent);
    component = fixture.componentInstance;
    component.blocks = defaultBlocks;
    component.selectedBlock = defaultBlocks[0];
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should disable the previous button', () => {
    component.blocks = defaultBlocks;
    component.selectedBlock = defaultBlocks[0];
    fixture.detectChanges();
    expect(previousButton().disabled).toBeTrue();
  });

  it('should enable the previous button', () => {
    component.blocks = defaultBlocks;
    component.selectedBlock = defaultBlocks[1];
    fixture.detectChanges();
    expect(previousButton().disabled).toBeFalse();
  });

  it('should disable the next button', () => {
    component.blocks = defaultBlocks;
    component.selectedBlock = defaultBlocks[2];
    fixture.detectChanges();
    expect(nextButton().disabled).toBeTrue();
  });

  it('should enable the next button', () => {
    component.blocks = defaultBlocks;
    component.selectedBlock = defaultBlocks[1];
    fixture.detectChanges();
    expect(nextButton().disabled).toBeFalse();
  });

  it('should select the previous block when the previous button is clicked', () => {
    component.blocks = defaultBlocks;
    component.selectedBlock = defaultBlocks[1];
    fixture.detectChanges();
    const emitSpy = spyOn(component.select, 'emit');
    previousButton().click();
    expect(emitSpy).toHaveBeenCalledWith(defaultBlocks[0]);
  });

  it('should select the next block', () => {
    component.blocks = defaultBlocks;
    component.selectedBlock = defaultBlocks[1];
    fixture.detectChanges();
    const emitSpy = spyOn(component.select, 'emit');
    nextButton().click();
    expect(emitSpy).toHaveBeenCalledWith(defaultBlocks[2]);
  });

  it('should initially select the correct option', () => {
    component.blocks = defaultBlocks;
    component.selectedBlock = defaultBlocks[2];
    fixture.detectChanges();
    expect(select().options[2].selected).toBeTrue();
  });

  it('should select the block for the selected option', () => {
    component.blocks = defaultBlocks;
    component.selectedBlock = defaultBlocks[0];
    fixture.detectChanges();
    const emitSpy = spyOn(component.select, 'emit');
    select().value = select().options[1].value;
    select().dispatchEvent(new Event('change'));
    expect(emitSpy).toHaveBeenCalledWith(defaultBlocks[1]);
  });
});
