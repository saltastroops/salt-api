import {
  findByText,
  fireEvent,
  getByText,
  render,
  waitFor,
} from '@testing-library/angular';
import { BlockViewComponent } from './block-view.component';
import { BlockSelectionComponent } from './block-selection/block-selection.component';
import { Block, BlockIdentifier } from '../../types';
import { BlockService } from '../../service/block.service';
import { Observable, of, throwError } from 'rxjs';
import {
  discardPeriodicTasks,
  fakeAsync,
  flush,
  TestBed,
  tick,
} from '@angular/core/testing';
import { TestScheduler } from 'rxjs/testing';
import { delay, map, switchMap } from 'rxjs/operators';

const MockBlockService = {
  /**
   * Return an object of the form {id: id, name: `Block ${id}`.
   *
   * The id is taken as the time it takes the request to finish (or fail), in
   * milliseconds.
   */
  getBlock(id: number): Observable<Block> {
    if (id === 42 || id == 43) {
      return of(block(id)).pipe(
        delay(id),
        switchMap(() => throwError(`Error for id ${id}.`))
      );
    }

    return of(block(id)).pipe(delay(id));
  },
};

function blockIdentifier(id: number): BlockIdentifier {
  return { id, name: `Block ${id}` };
}

function block(id: number): Block {
  return { id, name: `Loaded Block ${id}` };
}

describe('BlockViewComponent', () => {
  const loadingTestId = 'block-view-loading';

  const defaultBlocks: BlockIdentifier[] = [
    { id: 10, name: 'Block A' },
    { id: 11, name: 'Block B' },
    { id: 12, name: 'Block C' },
  ];

  const defaultComponent = async (
    blocks: BlockIdentifier[] = defaultBlocks
  ) => {
    return render(BlockViewComponent, {
      declarations: [BlockSelectionComponent],
      componentProperties: {
        blocks,
      },
      componentProviders: [
        { provide: BlockService, useValue: MockBlockService },
      ],
      providers: [{ provide: BlockService, useValue: MockBlockService }],
    });
  };

  it('should render the block view', async () => {
    const component = await render(BlockViewComponent, {
      componentProperties: {
        blocks: [blockIdentifier(0), blockIdentifier(1), blockIdentifier(2)],
      },
      providers: [{ provide: BlockService, useValue: MockBlockService }],
      componentProviders: [
        { provide: BlockService, useValue: MockBlockService },
      ],
    });
    expect(component).toBeTruthy();
  });

  it('should update all navigation elements when the user selects a block', async () => {
    const component = await defaultComponent();

    // Select the third block in the first select element
    const selectElements = component.getAllByDisplayValue('Block A');
    const value = (selectElements[0] as HTMLSelectElement).options[2].value;
    fireEvent.change(selectElements[0], { target: { value } });

    // The third block is selected in the second select element as well
    await waitFor(() => {
      expect(component.getAllByDisplayValue('Block C')).toHaveSize(2);
    });
  });

  it('should change selected block when the user clicks on a navigation button', async () => {
    const component = await defaultComponent();

    // The first block is shown
    let selectElements = component.getAllByDisplayValue('Block A');
    const selectElement = selectElements[0] as HTMLSelectElement;
    expect(selectElement.selectedIndex).toBe(0);

    // Get a previous and a next button
    const previousButton = component.getAllByText(/Prev/)[0];
    const nextButton = component.getAllByText(/Next/)[0];

    // Clicking on the next button selects the next block
    nextButton.click();
    await waitFor(() => {
      expect(component.getAllByDisplayValue('Block B')).toHaveSize(2);
    });

    // Clicking on the previous button selects the previous block
    previousButton.click();
    await waitFor(() => {
      expect(component.getAllByDisplayValue('Block A')).toHaveSize(2);
    });
  });

  it('should select the first block and load it immediately', fakeAsync(async () => {
    const component = await defaultComponent([
      blockIdentifier(10),
      blockIdentifier(20),
    ]);

    // The first block is selected...
    const selectElements = component.getAllByDisplayValue('Block 10');
    expect(selectElements).toHaveSize(2);

    // ... and loaded
    expect(component.queryByTestId(loadingTestId)).not.toBeNull();
    expect(component.queryByText(/Loaded Block 10/)).toBeNull();
    tick(120);
    component.fixture.detectChanges();
    expect(component.queryByTestId(loadingTestId)).toBeNull();
    expect(component.queryByText(/Loaded Block 10/)).not.toBeNull();

    flush();
    discardPeriodicTasks();
  }));

  it('should update content when blocks are selected', fakeAsync(async () => {
    // The following scenario is tested:
    // Request 1 (made after two debounced selections) is successful.
    // Request 2 fails.
    // Request 3 is overtaken by request 4.
    // Request 4 is successful.
    // Request 5 is overtaken by request 6.
    // Request 6 fails.
    const blocks = [
      blockIdentifier(10),
      blockIdentifier(42),
      blockIdentifier(300),
      blockIdentifier(40),
      blockIdentifier(30),
      blockIdentifier(43),
    ];
    const component = await defaultComponent(blocks);
    const fixture = component.fixture;

    const selectElements = component.getAllByDisplayValue('Block 10');
    const selectElement = selectElements[0] as HTMLSelectElement;
    const selectBlock = (selectedIndex: number) => {
      const value = selectElement.options[selectedIndex].value;
      fireEvent.change(selectElement, { target: { value } });
    };

    // Wait for the first block to load
    tick(400);

    // Rapidly select a few blocks
    selectBlock(1);
    fixture.detectChanges();
    expect(component.queryByTestId(loadingTestId)).not.toBeNull();
    tick(30);
    selectBlock(0);
    fixture.detectChanges();
    expect(component.queryByTestId(loadingTestId)).not.toBeNull();
    tick(30);
    selectBlock(3);
    fixture.detectChanges();
    expect(component.queryByTestId(loadingTestId)).not.toBeNull();

    tick(120); // Due to debouncing the second request has not been made, so no new
    // content has been loaded yet.
    fixture.detectChanges();
    expect(component.queryByTestId(loadingTestId)).not.toBeNull();
    expect(component.queryByText(/Loaded Block 10/)).not.toBeNull();

    // But after the while the last selected block is loaded
    tick(3000);
    fixture.detectChanges();
    expect(component.queryByTestId(loadingTestId)).toBeNull();
    expect(component.queryByText(/Loaded Block 10/)).toBeNull();
    expect(component.queryByText(/Loaded Block 40/)).not.toBeNull();

    // Make a failing request
    selectBlock(2);
    tick(150);
    selectBlock(5);
    fixture.detectChanges();
    expect(component.queryByTestId(loadingTestId)).not.toBeNull();
    tick(3000);
    fixture.detectChanges();
    expect(component.queryByTestId(loadingTestId)).toBeNull();
    expect(component.queryByText(/Loaded Block 40/)).toBeNull();
    expect(component.queryByText(/Loaded Block 42/)).toBeNull();
    expect(component.queryByText(/Error for id 43/)).not.toBeNull();

    // Make a slow request followed by a fast one
    selectBlock(2);
    expect(component.queryByTestId(loadingTestId)).not.toBeNull();
    expect(component.queryByText(/Error for id 43/)).toBeNull();

    tick(150);
    selectBlock(4);
    tick(400);
    fixture.detectChanges();
    expect(component.queryByText(/Loaded Block 40/)).toBeNull();
    expect(component.queryByText(/Loaded Block 300/)).toBeNull();
    expect(component.queryByText(/Loaded Block 30/)).not.toBeNull();

    // Make a slow request followed by a failing one
    selectBlock(2);
    tick(150);
    selectBlock(1);
    fixture.detectChanges();
    expect(component.queryByTestId(loadingTestId)).not.toBeNull();
    tick(400);
    fixture.detectChanges();
    expect(component.queryByTestId(loadingTestId)).toBeNull();
    expect(component.queryByText(/Loaded Block 300/)).toBeNull();
    expect(component.queryByText(/Loaded Block 30/)).toBeNull();
    expect(component.queryByText(/Error for id 42/)).not.toBeNull();

    flush();
    discardPeriodicTasks();
  }));
});
